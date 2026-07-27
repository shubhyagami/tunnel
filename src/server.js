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
const ws_1 = __importStar(require("ws"));
const uuid_1 = require("uuid");
const activeClients = new Map();
const pendingRequests = new Map();
const server = http.createServer((req, res) => {
    try {
        const host = req.headers.host || '';
        const subdomain = host.split('.')[0];
        const targetClient = activeClients.get(subdomain);
        if (!targetClient) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Tunnel not found or disconnected.');
            return;
        }
        const connectionId = (0, uuid_1.v4)();
        pendingRequests.set(connectionId, { req, res });
        targetClient.send(JSON.stringify({
            type: 'new_request',
            id: connectionId,
            method: req.method,
            url: req.url,
            headers: req.headers
        }));
    }
    catch (err) {
        res.writeHead(500);
        res.end('Internal Server Error');
    }
});
const wss = new ws_1.WebSocketServer({ noServer: true });
server.on('upgrade', (req, socket, head) => {
    const url = new URL(req.url || '', `http://${req.headers.host}`);
    const type = url.searchParams.get('type');
    // Internal Tunnel WebSocket Upgrades
    if (type === 'control' || type === 'data') {
        wss.handleUpgrade(req, socket, head, (ws) => {
            wss.emit('connection', ws, req);
        });
        return;
    }
    // External Public WebSocket Upgrades (e.g. Guacamole, Socket.io)
    const host = req.headers.host || '';
    const subdomain = host.split('.')[0];
    const targetClient = activeClients.get(subdomain);
    if (!targetClient) {
        socket.destroy();
        return;
    }
    const connectionId = (0, uuid_1.v4)();
    pendingRequests.set(connectionId, { req, res: null, socket, head, isUpgrade: true });
    targetClient.send(JSON.stringify({
        type: 'new_ws_request',
        id: connectionId,
        url: req.url,
        headers: req.headers
    }));
});
wss.on('connection', (ws, req) => {
    const url = new URL(req.url || '', `http://${req.headers.host}`);
    const type = url.searchParams.get('type');
    if (type === 'control') {
        const subdomain = url.searchParams.get('subdomain');
        if (!subdomain) {
            ws.close(1008, 'Missing subdomain');
            return;
        }
        activeClients.set(subdomain, ws);
        console.log(`[Control] Client registered: ${subdomain}`);
        ws.send(JSON.stringify({ type: 'registered' }));
        ws.on('close', () => {
            activeClients.delete(subdomain);
            console.log(`[Control] Client disconnected: ${subdomain}`);
        });
    }
    else if (type === 'data') {
        const id = url.searchParams.get('id');
        const pending = pendingRequests.get(id);
        if (!pending) {
            ws.close();
            return;
        }
        pendingRequests.delete(id);
        if (pending.isUpgrade) {
            // Raw TCP Tunneling for WebSockets
            const browserSocket = pending.socket;
            if (pending.head && pending.head.length > 0) {
                ws.send(pending.head, { binary: true });
            }
            browserSocket.on('data', (data) => {
                if (ws.readyState === ws_1.default.OPEN) {
                    ws.send(data, { binary: true });
                }
            });
            ws.on('message', (data, isBinary) => {
                // Pipe proxy data directly back to the browser socket
                browserSocket.write(data);
            });
            browserSocket.on('error', () => ws.close());
            ws.on('error', () => browserSocket.destroy());
            browserSocket.on('close', () => ws.close());
            ws.on('close', () => browserSocket.destroy());
        }
        else {
            // Standard HTTP Tunneling
            const res = pending.res;
            ws.on('message', (data, isBinary) => {
                if (isBinary) {
                    res.write(data);
                }
                else {
                    try {
                        const msg = JSON.parse(data.toString());
                        if (msg.type === 'response_meta') {
                            res.writeHead(msg.statusCode, msg.headers);
                        }
                        else if (msg.type === 'request_end') {
                            res.end();
                        }
                    }
                    catch (e) { }
                }
            });
            pending.req.on('data', chunk => {
                ws.send(chunk, { binary: true });
            });
            pending.req.on('end', () => {
                ws.send(JSON.stringify({ type: 'request_end' }));
            });
            pending.req.on('close', () => ws.close());
            ws.on('close', () => res.end());
        }
    }
});
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`Proxy listening on port ${PORT}`);
});
