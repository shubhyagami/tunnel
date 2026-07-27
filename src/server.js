"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const http = __importStar(require("http"));
const ws_1 = require("ws");
const uuid_1 = require("uuid");
const url_1 = require("url");
const PORT = process.env.PORT || 8080;
const activeClients = new Map();
const pendingRequests = new Map();
const server = http.createServer((req, res) => {
    const hostHeader = req.headers.host || '';
    const subdomain = hostHeader.split('.')[0];
    const session = activeClients.get(subdomain);
    if (!session) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Tunnel not found for subdomain: ' + subdomain);
        return;
    }
    const connectionId = (0, uuid_1.v4)();
    pendingRequests.set(connectionId, { req, res });
    req.socket.setNoDelay(true);
    const reqMeta = {
        type: 'new_request',
        id: connectionId,
        method: req.method,
        url: req.url,
        headers: req.headers
    };
    session.controlWs.send(JSON.stringify(reqMeta));
    req.on('close', () => {
        if (!res.writableEnded) {
            pendingRequests.delete(connectionId);
        }
    });
});
const wss = new ws_1.WebSocketServer({ server });
wss.on('connection', (ws, req) => {
    req.socket.setNoDelay(true);
    const url = new url_1.URL(req.url, `http://${req.headers.host || 'localhost'}`);
    const type = url.searchParams.get('type');
    if (type === 'control') {
        const subdomain = url.searchParams.get('subdomain');
        if (!subdomain) {
            ws.close(1008, 'Missing subdomain');
            return;
        }
        if (activeClients.has(subdomain)) {
            ws.close(1008, 'Subdomain in use');
            return;
        }
        activeClients.set(subdomain, { subdomain, controlWs: ws });
        console.log(`[Control] Client registered: ${subdomain}`);
        ws.send(JSON.stringify({ type: 'registered', subdomain }));
        ws.on('close', () => {
            console.log(`[Control] Client disconnected: ${subdomain}`);
            activeClients.delete(subdomain);
        });
    }
    else if (type === 'data') {
        const connectionId = url.searchParams.get('id');
        if (!connectionId || !pendingRequests.has(connectionId)) {
            ws.close(1008, 'Invalid connection ID');
            return;
        }
        const { req: proxiedReq, res: proxiedRes } = pendingRequests.get(connectionId);
        pendingRequests.delete(connectionId);
        let responseMetadataReceived = false;
        if (proxiedReq.complete) {
            ws.send(JSON.stringify({ type: 'request_end' }));
        }
        else {
            proxiedReq.on('data', chunk => ws.send(chunk, { binary: true }));
            proxiedReq.on('end', () => ws.send(JSON.stringify({ type: 'request_end' })));
        }
        ws.on('message', (data, isBinary) => {
            if (!isBinary && !responseMetadataReceived) {
                try {
                    const meta = JSON.parse(data.toString());
                    if (meta.type === 'response_meta') {
                        responseMetadataReceived = true;
                        proxiedRes.writeHead(meta.statusCode, meta.headers);
                    }
                }
                catch (e) {
                    console.error('Invalid response meta');
                }
            }
            else if (isBinary && responseMetadataReceived) {
                proxiedRes.write(data);
            }
        });
        ws.on('close', () => proxiedRes.end());
        ws.on('error', () => proxiedRes.end());
        proxiedRes.on('close', () => ws.close());
    }
});
server.listen(PORT, () => console.log(`Proxy listening on port ${PORT}`));
