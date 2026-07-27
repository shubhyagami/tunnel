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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const http = __importStar(require("http"));
const ws_1 = __importStar(require("ws"));
const express_1 = __importDefault(require("express"));
const path = __importStar(require("path"));
const SERVER_URL = process.env.SERVER_URL || 'ws://localhost:8080';
const args = process.argv.slice(2);
let localPort = 3000;
let subdomain = 'test';
let basicAuth = '';
let uiPort = 4040;
for (let i = 0; i < args.length; i++) {
    if (args[i] === '--port' && args[i + 1]) {
        localPort = parseInt(args[i + 1], 10);
    }
    else if (args[i] === '--subdomain' && args[i + 1]) {
        subdomain = args[i + 1];
    }
    else if (args[i] === '--basic-auth' && args[i + 1]) {
        basicAuth = args[i + 1];
    }
}
// ---------------------------------------------------------
// LOCAL UI SERVER (Express + WS)
// ---------------------------------------------------------
const app = (0, express_1.default)();
app.use(express_1.default.static(path.join(__dirname, 'public')));
const uiServer = http.createServer(app);
const uiWss = new ws_1.WebSocketServer({ server: uiServer });
let currentTunnelUrl = '';
let uiClients = [];
uiWss.on('connection', (ws) => {
    uiClients.push(ws);
    ws.send(JSON.stringify({ type: 'init', url: currentTunnelUrl }));
    ws.on('close', () => {
        uiClients = uiClients.filter(c => c !== ws);
    });
});
function broadcastToUI(message) {
    const data = JSON.stringify(message);
    uiClients.forEach(c => {
        if (c.readyState === ws_1.default.OPEN) {
            c.send(data);
        }
    });
}
uiServer.listen(uiPort, () => {
    console.log(`\n======================================================`);
    console.log(`🚀 Web UI Dashboard available at: http://localhost:${uiPort}`);
    console.log(`======================================================\n`);
});
// ---------------------------------------------------------
// TUNNEL CLIENT LOGIC
// ---------------------------------------------------------
console.log(`Starting tunnel for local port ${localPort} with subdomain '${subdomain}'...`);
console.log(`Connecting to ${SERVER_URL}...`);
let controlWs = null;
let reconnectAttempts = 0;
function connectControl() {
    let url = `${SERVER_URL}/?type=control&subdomain=${subdomain}`;
    controlWs = new ws_1.default(url);
    controlWs.on('open', () => {
        reconnectAttempts = 0;
        console.log('Connected to control server.');
    });
    controlWs.on('message', (data) => {
        try {
            const msg = JSON.parse(data.toString());
            if (msg.type === 'registered') {
                const urlObj = new URL(SERVER_URL);
                const protocol = urlObj.protocol === 'wss:' ? 'https:' : 'http:';
                let host = urlObj.host;
                currentTunnelUrl = `${protocol}//${subdomain}.${host}`;
                console.log(`Tunnel established! Access it at: ${currentTunnelUrl}`);
                broadcastToUI({ type: 'tunnel_url', url: currentTunnelUrl });
            }
            else if (msg.type === 'new_request' && msg.id) {
                handleNewRequest(msg);
            }
            else if (msg.type === 'new_ws_request' && msg.id) {
                handleNewWsRequest(msg);
            }
        }
        catch (e) {
            console.error('Invalid message from control server', data.toString());
        }
    });
    controlWs.on('close', (code, reason) => {
        console.log(`Control connection closed (Code: ${code}, Reason: ${reason}).`);
        currentTunnelUrl = '';
        broadcastToUI({ type: 'tunnel_url', url: '' });
        if (code === 1008) {
            console.error('Fatal error from server. Exiting.');
            process.exit(1);
        }
        scheduleReconnect();
    });
    controlWs.on('error', (err) => {
        console.error('Control connection error:', err.message);
    });
}
function scheduleReconnect() {
    reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
    console.log(`Reconnecting in ${delay / 1000} seconds...`);
    setTimeout(connectControl, delay);
}
connectControl();
function handleNewRequest(reqMeta) {
    const connectionId = reqMeta.id;
    const startTime = Date.now();
    console.log(`--> ${reqMeta.method} ${reqMeta.url}`);
    const dataWs = new ws_1.default(`${SERVER_URL}/?type=data&id=${connectionId}`);
    dataWs.on('open', () => {
        const headers = { ...reqMeta.headers };
        delete headers.host;
        if (basicAuth) {
            const authHeader = headers['authorization'];
            const expectedAuth = 'Basic ' + Buffer.from(basicAuth).toString('base64');
            if (authHeader !== expectedAuth) {
                const duration = Date.now() - startTime;
                console.log(`<-- 401 ${reqMeta.method} ${reqMeta.url} (${duration}ms) [Unauthorized]`);
                broadcastToUI({
                    type: 'log',
                    log: {
                        timestamp: Date.now(),
                        method: reqMeta.method,
                        url: reqMeta.url,
                        statusCode: 401,
                        duration: duration
                    }
                });
                dataWs.send(JSON.stringify({
                    type: 'response_meta',
                    statusCode: 401,
                    headers: {
                        'Content-Type': 'text/plain',
                        'WWW-Authenticate': 'Basic realm="Tunnel"'
                    }
                }));
                dataWs.send(Buffer.from('401 Unauthorized'), { binary: true });
                dataWs.close();
                return;
            }
        }
        const options = {
            hostname: 'localhost',
            port: localPort,
            path: reqMeta.url,
            method: reqMeta.method,
            headers: headers
        };
        const localReq = http.request(options, (localRes) => {
            const resMeta = {
                type: 'response_meta',
                statusCode: localRes.statusCode,
                headers: localRes.headers
            };
            dataWs.send(JSON.stringify(resMeta));
            localRes.on('data', chunk => dataWs.send(chunk, { binary: true }));
            localRes.on('end', () => {
                const duration = Date.now() - startTime;
                console.log(`<-- ${localRes.statusCode} ${reqMeta.method} ${reqMeta.url} (${duration}ms)`);
                broadcastToUI({
                    type: 'log',
                    log: {
                        timestamp: Date.now(),
                        method: reqMeta.method,
                        url: reqMeta.url,
                        statusCode: localRes.statusCode,
                        duration: duration
                    }
                });
                dataWs.close();
            });
        });
        localReq.on('error', (err) => {
            const duration = Date.now() - startTime;
            console.log(`<-- 502 ${reqMeta.method} ${reqMeta.url} (${duration}ms) [Local Error: ${err.message}]`);
            broadcastToUI({
                type: 'log',
                log: {
                    timestamp: Date.now(),
                    method: reqMeta.method,
                    url: reqMeta.url,
                    statusCode: 502,
                    duration: duration
                }
            });
            dataWs.send(JSON.stringify({
                type: 'response_meta',
                statusCode: 502,
                headers: { 'Content-Type': 'text/plain' }
            }));
            dataWs.send(Buffer.from('502 Bad Gateway: Local server error'), { binary: true });
            dataWs.close();
        });
        dataWs.on('message', (data, isBinary) => {
            if (isBinary) {
                localReq.write(data);
            }
            else {
                try {
                    const msg = JSON.parse(data.toString());
                    if (msg.type === 'request_end') {
                        localReq.end();
                    }
                }
                catch (e) { }
            }
        });
        dataWs.on('close', () => {
            if (!localReq.destroyed)
                localReq.destroy();
        });
    });
    dataWs.on('error', err => {
        console.error(`[${connectionId}] Data WS error:`, err.message);
    });
}
function handleNewWsRequest(reqMeta) {
    const connectionId = reqMeta.id;
    const startTime = Date.now();
    console.log(`--> [WS] ${reqMeta.url}`);
    const dataWs = new ws_1.default(`${SERVER_URL}/?type=data&id=${connectionId}`);
    dataWs.on('open', () => {
        const headers = { ...reqMeta.headers };
        delete headers.host;
        const options = {
            hostname: 'localhost',
            port: localPort,
            path: reqMeta.url,
            method: 'GET',
            headers: headers
        };
        const localReq = http.request(options);
        localReq.on('upgrade', (localRes, localSocket, localHead) => {
            const duration = Date.now() - startTime;
            console.log(`<-- [WS] 101 ${reqMeta.url} (${duration}ms)`);
            // Reconstruct the raw 101 Switching Protocols HTTP response
            let rawHeaders = `HTTP/${localRes.httpVersion} ${localRes.statusCode} ${localRes.statusMessage || 'Switching Protocols'}\r\n`;
            for (let i = 0; i < localRes.rawHeaders.length; i += 2) {
                rawHeaders += `${localRes.rawHeaders[i]}: ${localRes.rawHeaders[i + 1]}\r\n`;
            }
            rawHeaders += '\r\n';
            // Send the HTTP response headers back to the browser via the proxy
            dataWs.send(Buffer.from(rawHeaders), { binary: true });
            if (localHead && localHead.length > 0) {
                dataWs.send(localHead, { binary: true });
            }
            // Pipe bi-directional raw TCP data
            localSocket.on('data', chunk => {
                if (dataWs.readyState === ws_1.default.OPEN) {
                    dataWs.send(chunk, { binary: true });
                }
            });
            dataWs.on('message', (data, isBinary) => {
                localSocket.write(data);
            });
            localSocket.on('close', () => dataWs.close());
            localSocket.on('error', () => dataWs.close());
            dataWs.on('close', () => localSocket.destroy());
            dataWs.on('error', () => localSocket.destroy());
        });
        localReq.on('response', (localRes) => {
            // Local server rejected the WebSocket upgrade and responded with normal HTTP
            const duration = Date.now() - startTime;
            console.log(`<-- [WS REJECTED] ${localRes.statusCode} ${reqMeta.url} (${duration}ms)`);
            let rawHeaders = `HTTP/${localRes.httpVersion} ${localRes.statusCode} ${localRes.statusMessage || ''}\r\n`;
            for (let i = 0; i < localRes.rawHeaders.length; i += 2) {
                rawHeaders += `${localRes.rawHeaders[i]}: ${localRes.rawHeaders[i + 1]}\r\n`;
            }
            rawHeaders += '\r\n';
            dataWs.send(Buffer.from(rawHeaders), { binary: true });
            localRes.on('data', chunk => {
                if (dataWs.readyState === ws_1.default.OPEN) {
                    dataWs.send(chunk, { binary: true });
                }
            });
            localRes.on('end', () => dataWs.close());
        });
        localReq.on('error', (err) => {
            console.log(`<-- [WS ERROR] ${reqMeta.url} [Local Error: ${err.message}]`);
            dataWs.close();
        });
        localReq.end();
    });
    dataWs.on('error', err => {
        console.error(`[${connectionId}] WS Data error:`, err.message);
    });
}
