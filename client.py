#!/usr/bin/env python3
import asyncio
import json
import base64
import argparse
import logging
import sys
from urllib.parse import urlparse, urlencode

import aiohttp

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("tunnel-client")


async def main():
    parser = argparse.ArgumentParser(description="Port Tunnel Client - expose localhost to the internet")
    parser.add_argument("--server", required=True, help="Tunnel server URL (e.g. https://tunnel-2sgh.onrender.com)")
    parser.add_argument("--client-id", required=True, help="Unique name for this tunnel")
    parser.add_argument("--port", type=int, default=80, help="Local port to forward to (default: 80)")
    args = parser.parse_args()

    server = args.server.rstrip("/")
    ws_url = server.replace("http://", "ws://").replace("https://", "wss://")
    ws_url += f"/ws?{urlencode({'client_id': args.client_id, 'port': args.port})}"

    logger.info(f"Connecting to {ws_url}")
    logger.info(f"Forwarding localhost:{args.port} -> {server}/{args.client_id}/")

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as ws:
            logger.info("Connected to tunnel server")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data.get("type") == "request":
                        await handle_request(session, ws, data, args.port)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
                    break


async def handle_request(session: aiohttp.ClientSession, ws, data: dict, local_port: int):
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
    except Exception as e:
        logger.error(f"  Error: {e}")
        await ws.send_json({
            "type": "response",
            "request_id": rid,
            "status_code": 502,
            "headers": {"Content-Type": "text/plain"},
            "body": base64.b64encode(str(e).encode()).decode(),
        })


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down")
        sys.exit(0)
