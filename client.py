#!/usr/bin/env python3
import asyncio
import json
import struct
import argparse
import logging
import sys
from urllib.parse import urlencode

import aiohttp

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("tunnel-client")

TYPE_REQUEST = 0
TYPE_RESPONSE = 1


def encode_frame(msg_type: int, rid: str, metadata: dict, body: bytes = b"") -> bytes:
    meta = json.dumps(metadata).encode()
    payload = bytes([msg_type]) + rid.encode() + struct.pack("!I", len(meta)) + meta + body
    return struct.pack("!I", len(payload)) + payload


def decode_frame(frame: bytes):
    hdr = struct.unpack("!I", frame[:4])[0]
    msg_type = frame[4]
    rid = frame[5:17].decode()
    jlen = struct.unpack("!I", frame[17:21])[0]
    meta = json.loads(frame[21:21 + jlen])
    body = frame[21 + jlen:]
    return msg_type, rid, meta, body


async def handle_request(session: aiohttp.ClientSession, ws, frame: bytes, port: int):
    msg_type, rid, meta, body = decode_frame(frame)
    method = meta["method"]
    path = meta["path"]
    headers = {k: v for k, v in meta.get("headers", {}).items()
               if k.lower() not in ("host", "transfer-encoding", "content-encoding", "content-length")}
    query = meta.get("query", {})

    target_url = f"http://localhost:{port}{path}"
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
            await ws.send_bytes(encode_frame(TYPE_RESPONSE, rid,
                                             {"status": resp.status, "headers": resp_headers},
                                             resp_body))
            logger.info(f"    -> {resp.status} ({len(resp_body)} bytes)")
    except Exception as e:
        logger.error(f"  Error: {e}")
        await ws.send_bytes(encode_frame(TYPE_RESPONSE, rid,
                                         {"status": 502, "headers": {"Content-Type": "text/plain"}},
                                         str(e).encode()))


async def main():
    parser = argparse.ArgumentParser(description="Port Tunnel Client")
    parser.add_argument("--server", required=True, help="Server URL (e.g. https://tunnel-2sgh.onrender.com)")
    parser.add_argument("--client-id", required=True, help="Unique tunnel name")
    parser.add_argument("--port", type=int, default=80, help="Local port (default: 80)")
    args = parser.parse_args()

    server = args.server.rstrip("/")
    ws_url = server.replace("http://", "ws://").replace("https://", "wss://")
    ws_url += f"/ws?{urlencode({'client_id': args.client_id, 'port': args.port})}"

    logger.info(f"Connecting to {ws_url}")
    logger.info(f"Tunnel: http://localhost:{args.port} -> {server}/{args.client_id}/")

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            logger.info("Connected!")
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    await handle_request(session, ws, msg.data, args.port)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
                    break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down")
        sys.exit(0)
