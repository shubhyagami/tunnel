#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import asyncio
import json
import base64
import queue
import logging
import sys
import webbrowser
from urllib.parse import urlencode

import aiohttp


class QueueHandler(logging.Handler):
    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(self.format(record))


class TunnelGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Port Tunnel Client")
        self.root.geometry("700x500")
        self.root.minsize(500, 350)

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

        # --- Connection frame ---
        conn = ttk.LabelFrame(main, text="Connection", padding=10)
        conn.pack(fill=tk.X, pady=(0, 8))

        ttk.Label(conn, text="Server:").grid(row=0, column=0, sticky=tk.W, padx=(0, 6))
        self.server_var = tk.StringVar(value="https://port-tunnel.onrender.com")
        ttk.Entry(conn, textvariable=self.server_var).grid(row=0, column=1, sticky=tk.EW, padx=(0, 12))

        ttk.Label(conn, text="Client ID:").grid(row=1, column=0, sticky=tk.W, padx=(0, 6), pady=(4, 0))
        self.cid_var = tk.StringVar(value="mytunnel")
        ttk.Entry(conn, textvariable=self.cid_var).grid(row=1, column=1, sticky=tk.EW, padx=(0, 12), pady=(4, 0))

        ttk.Label(conn, text="Local Port:").grid(row=2, column=0, sticky=tk.W, padx=(0, 6), pady=(4, 0))
        self.port_var = tk.IntVar(value=3000)
        port_spin = ttk.Spinbox(conn, from_=1, to=65535, textvariable=self.port_var, width=8)
        port_spin.grid(row=2, column=1, sticky=tk.W, padx=(0, 12), pady=(4, 0))

        conn.columnconfigure(1, weight=1)

        # --- Controls ---
        ctrl = ttk.Frame(main)
        ctrl.pack(fill=tk.X, pady=(0, 8))

        self.start_btn = ttk.Button(ctrl, text="Start Tunnel", command=self.start_tunnel)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.stop_btn = ttk.Button(ctrl, text="Stop", command=self.stop_tunnel, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.tunnel_url_var = tk.StringVar()
        self.url_entry = ttk.Entry(ctrl, textvariable=self.tunnel_url_var, state="readonly")
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        # --- Log ---
        log_frame = ttk.LabelFrame(main, text="Log", padding=6)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_area = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED, wrap=tk.WORD,
                                                   font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4",
                                                   insertbackground="white")
        self.log_area.pack(fill=tk.BOTH, expand=True)

        # --- Status bar ---
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=(6, 2))
        status_bar.pack(fill=tk.X)

    def _setup_logging(self):
        handler = QueueHandler(self.log_queue)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
        logging.getLogger("tunnel-client").addHandler(handler)
        logging.getLogger("tunnel-client").setLevel(logging.INFO)

    def _log(self, msg: str):
        self.log_queue.put(msg)

    def poll_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get_nowait()
            self.log_area.configure(state=tk.NORMAL)
            self.log_area.insert(tk.END, msg + "\n")
            self.log_area.see(tk.END)
            self.log_area.configure(state=tk.DISABLED)
        self.root.after(100, self.poll_log_queue)

    def start_tunnel(self):
        server = self.server_var.get().strip()
        cid = self.cid_var.get().strip()
        port = self.port_var.get()

        if not server or not cid:
            self._log("ERROR: Server URL and Client ID are required")
            return

        self.running = True
        self.start_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.status_var.set("Connecting...")
        self.tunnel_url_var.set(f"{server.rstrip('/')}/{cid}/")
        self.stop_event.clear()

        self.tunnel_thread = threading.Thread(target=self._run_async_client,
                                              args=(server, cid, port), daemon=True)
        self.tunnel_thread.start()

    def stop_tunnel(self):
        self.stop_event.set()
        self.status_var.set("Stopping...")

    def _run_async_client(self, server: str, cid: str, port: int):
        try:
            asyncio.run(self._tunnel_client(server, cid, port))
        except Exception as e:
            self._log(f"FATAL: {e}")
        finally:
            self.root.after(0, self._on_tunnel_stopped)

    def _on_tunnel_stopped(self):
        self.running = False
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.status_var.set("Disconnected")

    async def _tunnel_client(self, server: str, cid: str, port: int):
        logger = logging.getLogger("tunnel-client")
        server = server.rstrip("/")
        ws_url = server.replace("http://", "ws://").replace("https://", "wss://")
        ws_url += f"/ws?{urlencode({'client_id': cid, 'port': port})}"

        logger.info(f"Connecting to {ws_url}")
        logger.info(f"Tunnel URL: {server}/{cid}/")

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
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                if data.get("type") == "request":
                                    await self._handle_request(session, ws, data, port, logger)
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                logger.error(f"WebSocket error: {ws.exception()}")
                                break
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    if self.stop_event.is_set():
                        break
                    logger.error(f"Connection error: {e}")
                    logger.info(f"Reconnecting in 3s...")
                    self.root.after(0, lambda: self.status_var.set("Reconnecting..."))
                    await asyncio.sleep(3)

    async def _handle_request(self, session: aiohttp.ClientSession, ws, data: dict, local_port: int, logger: logging.Logger):
        rid = data["request_id"]
        method = data["method"]
        path = data["path"]
        headers = {k: v for k, v in data.get("headers", {}).items()
                   if k.lower() not in ("host", "transfer-encoding", "content-encoding", "content-length")}
        body_b64 = data.get("body", "")
        body = base64.b64decode(body_b64) if body_b64 else b""

        target_url = f"http://localhost:{local_port}{path}"
        query = data.get("query", {})
        if query:
            target_url += "?" + urlencode(query)

        logger.info(f"  {method} {target_url}")

        try:
            async with session.request(method, target_url, headers=headers, data=body,
                                        timeout=aiohttp.ClientTimeout(total=30),
                                        allow_redirects=False) as resp:
                resp_body = await resp.read()
                resp_headers = {k: v for k, v in resp.headers.items()
                                if k.lower() not in ("transfer-encoding", "content-encoding", "content-length")}

                await ws.send_json({
                    "type": "response",
                    "request_id": rid,
                    "status_code": resp.status,
                    "headers": resp_headers,
                    "body": base64.b64encode(resp_body).decode() if resp_body else "",
                })
                logger.info(f"    -> {resp.status}")
        except Exception as e:
            logger.error(f"  Error: {e}")
            await ws.send_json({
                "type": "response",
                "request_id": rid,
                "status_code": 502,
                "headers": {"Content-Type": "text/plain"},
                "body": base64.b64encode(str(e).encode()).decode(),
            })

    def _on_close(self):
        self.stop_event.set()
        self.root.destroy()


def main():
    app = TunnelGUI()
    app.root.mainloop()


if __name__ == "__main__":
    main()
