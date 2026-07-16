import os
import json
import struct
import uuid
import asyncio
import logging
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Query
from fastapi.responses import Response, JSONResponse
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tunnel-server")

START_TIME = time.time()
app = FastAPI(title="Port Tunnel", version="2.0.0")

clients: dict[str, WebSocket] = {}
target_ports: dict[str, int] = {}
pending: dict[str, asyncio.Future] = {}


# Binary protocol:
# [4B: total_len][1B: type(0=req,1=resp)][12B: rid][4B: json_len][JSON...][body...]
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
    meta = json.loads(frame[21:21+jlen])
    body = frame[21+jlen:]
    return msg_type, rid, meta, body


@app.get("/")
async def root():
    tunnels = [{"client_id": c, "local_port": target_ports.get(c), "url": f"/{c}/"}
               for c in clients]
    return {"name": "Port Tunnel", "version": "2.0.0", "uptime": int(time.time() - START_TIME),
            "active_tunnels": tunnels}


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
        while True:
            raw = await websocket.receive_bytes()
            msg_type, rid, meta, body = decode_frame(raw)
            if msg_type == TYPE_RESPONSE and rid in pending:
                pending[rid].set_result((meta, body))
    except WebSocketDisconnect:
        logger.info(f"Client '{client_id}' disconnected")
    except Exception as e:
        logger.error(f"Client '{client_id}' error: {e}")
    finally:
        clients.pop(client_id, None)
        target_ports.pop(client_id, None)
        for rid in list(pending.keys()):
            if not pending[rid].done():
                pending[rid].set_exception(ConnectionError("Tunnel disconnected"))


@app.api_route("/{client_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def proxy(client_id: str, path: str, request: Request):
    if client_id not in clients:
        return JSONResponse({"error": f"Tunnel '{client_id}' not found"}, status_code=404)

    ws = clients[client_id]
    rid = uuid.uuid4().hex[:12]
    body = await request.body()

    meta = {"method": request.method, "path": f"/{path}",
            "query": dict(request.query_params), "headers": dict(request.headers)}
    future = asyncio.get_event_loop().create_future()
    pending[rid] = future

    try:
        await ws.send_bytes(encode_frame(TYPE_REQUEST, rid, meta, body))
        resp_meta, resp_body = await asyncio.wait_for(future, timeout=60)
        resp_headers = {k: v for k, v in resp_meta.get("headers", {}).items()
                        if k.lower() not in ("transfer-encoding", "content-encoding", "content-length", "host")}
        return Response(content=resp_body, status_code=resp_meta.get("status", 200), headers=resp_headers)
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
