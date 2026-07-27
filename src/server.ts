import * as http from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import { v4 as uuidv4 } from 'uuid';
import { URL } from 'url';

const PORT = process.env.PORT || 8080;

interface ClientSession {
    subdomain: string;
    controlWs: WebSocket;
}

const activeClients = new Map<string, ClientSession>();
const pendingRequests = new Map<string, { req: http.IncomingMessage, res: http.ServerResponse }>();

const server = http.createServer((req, res) => {
    const hostHeader = req.headers.host || '';
    const subdomain = hostHeader.split('.')[0];

    const session = activeClients.get(subdomain);
    if (!session) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Tunnel not found for subdomain: ' + subdomain);
        return;
    }

    const connectionId = uuidv4();
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

const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
    req.socket.setNoDelay(true);

    const url = new URL(req.url!, `http://${req.headers.host || 'localhost'}`);
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

    } else if (type === 'data') {
        const connectionId = url.searchParams.get('id');
        if (!connectionId || !pendingRequests.has(connectionId)) {
            ws.close(1008, 'Invalid connection ID');
            return;
        }

        const { req: proxiedReq, res: proxiedRes } = pendingRequests.get(connectionId)!;
        pendingRequests.delete(connectionId);

        let responseMetadataReceived = false;

        if (proxiedReq.complete) {
            ws.send(JSON.stringify({ type: 'request_end' }));
        } else {
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
                } catch (e) {
                    console.error('Invalid response meta');
                }
            } else if (isBinary && responseMetadataReceived) {
                proxiedRes.write(data);
            }
        });

        ws.on('close', () => proxiedRes.end());
        ws.on('error', () => proxiedRes.end());
        proxiedRes.on('close', () => ws.close());
    }
});

server.listen(PORT, () => console.log(`Proxy listening on port ${PORT}`));
