import os
import json
import base64
import uuid
import asyncio
import logging
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Query
from fastapi.responses import Response, JSONResponse, HTMLResponse
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tunnel-server")

START_TIME = time.time()

app = FastAPI(title="Port Tunnel", version="1.0.0")

clients: dict[str, WebSocket] = {}
target_ports: dict[str, int] = {}
pending: dict[str, asyncio.Future] = {}


@app.get("/")
async def root():
    tunnels = []
    for cid, ws in list(clients.items()):
        tunnels.append({
            "client_id": cid,
            "local_port": target_ports.get(cid),
            "connected": True,
            "url": f"/{cid}/",
        })
    return {
        "name": "Port Tunnel",
        "version": "1.0.0",
        "uptime": int(time.time() - START_TIME),
        "active_tunnels": tunnels,
        "usage": {
            "server": "ws://host/ws?client_id=NAME&port=PORT",
            "client": "python client.py --server ws://host --client-id NAME --port PORT",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "uptime": int(time.time() - START_TIME)}


@app.websocket("/ws")
async def tunnel_ws(websocket: WebSocket, client_id: str = Query(...), port: int = Query(80)):
    await websocket.accept()
    clients[client_id] = websocket
    target_ports[client_id] = port
    logger.info(f"Client '{client_id}' connected (-> localhost:{port})")
    try:
        async for raw in websocket.iter_json():
            if raw.get("type") == "response":
                rid = raw.get("request_id")
                if rid and rid in pending:
                    pending[rid].set_result(raw)
    except WebSocketDisconnect:
        logger.info(f"Client '{client_id}' disconnected")
    except Exception as e:
        logger.error(f"Client '{client_id}' error: {e}")
    finally:
        clients.pop(client_id, None)
        target_ports.pop(client_id, None)
        for rid in list(pending.keys()):
            if not pending[rid].done():
                pending[rid].set_exception(ConnectionError("Tunnel client disconnected"))


@app.api_route("/{client_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy(client_id: str, path: str, request: Request):
    if client_id not in clients:
        return JSONResponse({"error": f"Tunnel '{client_id}' not found"}, status_code=404)

    ws = clients[client_id]
    rid = uuid.uuid4().hex[:12]
    body = await request.body()

    msg = {
        "type": "request",
        "request_id": rid,
        "method": request.method,
        "path": f"/{path}",
        "query": dict(request.query_params),
        "headers": dict(request.headers),
        "body": base64.b64encode(body).decode() if body else "",
    }

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    pending[rid] = future

    try:
        await ws.send_json(msg)
        resp = await asyncio.wait_for(future, timeout=60)
        resp_body = base64.b64decode(resp.get("body", "")) if resp.get("body") else b""
        resp_headers = {k: v for k, v in resp.get("headers", {}).items()
                        if k.lower() not in ("transfer-encoding", "content-encoding", "content-length", "host")}
        return Response(content=resp_body, status_code=resp.get("status_code", 200), headers=resp_headers)
    except asyncio.TimeoutError:
        pending.pop(rid, None)
        return JSONResponse({"error": "Tunnel timeout"}, status_code=504)
    except ConnectionError as e:
        return JSONResponse({"error": str(e)}, status_code=502)
    finally:
        pending.pop(rid, None)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
