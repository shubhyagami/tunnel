#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import asyncio
import json
import struct
import queue
import logging
import sys
from urllib.parse import urlencode

import aiohttp

TYPE_REQUEST = 0
TYPE_RESPONSE = 1

def encode_frame(msg_type: int, rid: str, metadata: dict, body: bytes = b"") -> bytes:
    meta = json.dumps(metadata).encode()
    payload = bytes([msg_type]) + rid.encode() + struct.pack("!I", len(meta)) + meta + body
    return struct.pack("!I", len(payload)) + payload

def decode_frame(frame: bytes):
    msg_type = frame[4]
    rid = frame[5:17].decode()
    jlen = struct.unpack("!I", frame[17:21])[0]
    meta = json.loads(frame[21:21 + jlen])
    body = frame[21 + jlen:]
    return msg_type, rid, meta, body


class QueueHandler(logging.Handler):
    def __init__(self, q: queue.Queue):
        super().__init__()
        self.q = q
    def emit(self, record):
        self.q.put(self.format(record))


class TunnelGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Port Tunnel")
        self.root.geometry("720x520")
        self.root.minsize(520, 360)
        self.log_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.tunnel_thread: threading.Thread | None = None
        self.running = False
        self._build_ui()
        self._setup_logging()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.poll_log_queue()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        conn = ttk.LabelFrame(main, text="Connection", padding=10)
        conn.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(conn, text="Server:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        self.server_var = tk.StringVar(value="https://tunnel-2sgh.onrender.com")
        ttk.Entry(conn, textvariable=self.server_var).grid(row=0, column=1, sticky=tk.EW, padx=(0, 12))

        ttk.Label(conn, text="Client ID:").grid(row=1, column=0, sticky=tk.W, padx=(0, 6), pady=(4, 0))
        self.cid_var = tk.StringVar(value="mytunnel")
        ttk.Entry(conn, textvariable=self.cid_var).grid(row=1, column=1, sticky=tk.EW, padx=(0, 12), pady=(4, 0))

        ttk.Label(conn, text="Local Port:").grid(row=2, column=0, sticky=tk.W, padx=(0, 6), pady=(4, 0))
        self.port_var = tk.IntVar(value=3000)
        ttk.Spinbox(conn, from_=1, to=65535, textvariable=self.port_var, width=8
                    ).grid(row=2, column=1, sticky=tk.W, padx=(0, 12), pady=(4, 0))
        conn.columnconfigure(1, weight=1)

        ctrl = ttk.Frame(main)
        ctrl.pack(fill=tk.X, pady=(0, 8))

        self.start_btn = ttk.Button(ctrl, text="Start Tunnel", command=self.start_tunnel)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 6))
        self.stop_btn = ttk.Button(ctrl, text="Stop", command=self.stop_tunnel, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT)

        self.url_var = tk.StringVar()
        url_e = ttk.Entry(ctrl, textvariable=self.url_var, state="readonly")
        url_e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(12, 0))

        log_frame = ttk.LabelFrame(main, text="Log", padding=6)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED, wrap=tk.WORD,
                                              font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4",
                                              insertbackground="white")
        self.log.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="Ready")
        bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN,
                        anchor=tk.W, padding=(6, 2))
        bar.pack(fill=tk.X)

    def _setup_logging(self):
        h = QueueHandler(self.log_queue)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
        logging.getLogger("tunnel-client").addHandler(h)
        logging.getLogger("tunnel-client").setLevel(logging.INFO)

    def _log(self, msg: str):
        self.log_queue.put(msg)

    def poll_log_queue(self):
        while not self.log_queue.empty():
            self.log.configure(state=tk.NORMAL)
            self.log.insert(tk.END, self.log_queue.get_nowait() + "\n")
            self.log.see(tk.END)
            self.log.configure(state=tk.DISABLED)
        self.root.after(100, self.poll_log_queue)

    def start_tunnel(self):
        srv = self.server_var.get().strip()
        cid = self.cid_var.get().strip()
        port = self.port_var.get()
        if not srv or not cid:
            self._log("ERROR: Server URL and Client ID required")
            return
        self.running = True
        self.start_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.status_var.set("Connecting...")
        self.url_var.set(f"{srv.rstrip('/')}/{cid}/")
        self.stop_event.clear()
        self.tunnel_thread = threading.Thread(target=self._run, args=(srv, cid, port), daemon=True)
        self.tunnel_thread.start()

    def stop_tunnel(self):
        self.stop_event.set()
        self.status_var.set("Stopping...")

    def _run(self, server: str, cid: str, port: int):
        try:
            asyncio.run(self._client(server, cid, port))
        except Exception as e:
            self._log(f"FATAL: {e}")
        finally:
            self.root.after(0, self._stopped)

    def _stopped(self):
        self.running = False
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.status_var.set("Disconnected")

    async def _client(self, server: str, cid: str, port: int):
        logger = logging.getLogger("tunnel-client")
        server = server.rstrip("/")
        ws_url = server.replace("http://", "ws://").replace("https://", "wss://")
        ws_url += f"/ws?{urlencode({'client_id': cid, 'port': port})}"
        logger.info(f"Connecting to {ws_url}")
        logger.info(f"Tunnel: http://localhost:{port} -> {server}/{cid}/")

        async with aiohttp.ClientSession() as session:
            while not self.stop_event.is_set():
                try:
                    async with session.ws_connect(ws_url) as ws:
                        logger.info("Connected!")
                        self.root.after(0, lambda: self.status_var.set("Connected"))
                        async for msg in ws:
                            if self.stop_event.is_set():
                                await ws.close()
                                break
                            if msg.type == aiohttp.WSMsgType.BINARY:
                                await self._handle(session, ws, msg.data, port, logger)
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                logger.error(f"WebSocket error: {ws.exception()}")
                                break
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    if self.stop_event.is_set():
                        break
                    logger.error(f"Connection error: {e}")
                    logger.info("Reconnecting in 3s...")
                    self.root.after(0, lambda: self.status_var.set("Reconnecting..."))
                    await asyncio.sleep(3)

    async def _handle(self, session, ws, frame: bytes, port: int, logger):
        try:
            _, rid, meta, body = decode_frame(frame)
        except Exception as e:
            logger.error(f"Bad frame: {e}")
            return
        method = meta["method"]
        path = meta["path"]
        headers = {k: v for k, v in meta.get("headers", {}).items()
                   if k.lower() not in ("host", "transfer-encoding", "content-encoding", "content-length")}
        query = meta.get("query", {})
        target = f"http://localhost:{port}{path}"
        if query:
            target += "?" + urlencode(query)
        logger.info(f"  {method} {target}")

        try:
            async with session.request(method, target, headers=headers, data=body,
                                        timeout=aiohttp.ClientTimeout(total=30),
                                        allow_redirects=False) as resp:
                resp_body = await resp.read()
                rh = {k: v for k, v in resp.headers.items()
                      if k.lower() not in ("transfer-encoding", "content-encoding", "content-length")}
                await ws.send_bytes(encode_frame(TYPE_RESPONSE, rid,
                                                 {"status": resp.status, "headers": rh}, resp_body))
                logger.info(f"    -> {resp.status} ({len(resp_body)} bytes)")
        except Exception as e:
            logger.error(f"  Error: {e}")
            await ws.send_bytes(encode_frame(TYPE_RESPONSE, rid,
                                             {"status": 502, "headers": {"Content-Type": "text/plain"}},
                                             str(e).encode()))

    def _on_close(self):
        self.stop_event.set()
        self.root.destroy()


if __name__ == "__main__":
    TunnelGUI().root.mainloop()
