# TunnelX

A high-performance, single-port HTTP/WebSocket tunneling solution designed for Render.com and local development. It allows you to expose your local web servers to the public internet securely and fast.

## Features
- 🚀 **Ultra-fast multiplexed proxy** (disables Nagle's algorithm for minimum latency)
- 🎨 **Web UI Dashboard** for real-time traffic monitoring
- 🔒 **Basic Auth protection** for local services
- ⚡ **Auto-reconnecting resilience** with exponential backoff

---

## 1. How to run it LOCALLY (for testing)

First, start the Tunnel Server:
```bash
npm install
npm run build
npm start
```
*(The server will run on port 8080 by default)*

Next, start your local web server (the one you want to expose). For example, a simple Python server:
```bash
python -m http.server 3000
```

Finally, start the Tunnel Client to connect them:
```bash
# Connects your local port 3000 to the server, requesting the subdomain "my-app"
node src/client.js --port 3000 --subdomain my-app
```

Now you can:
- View your exposed site at: `http://my-app.localhost:8080`
- View your Live Traffic Dashboard at: `http://localhost:4040`

---

## 2. How to run it in PRODUCTION (Render.com)

1. Connect this GitHub repository to Render.com and create a new **Blueprint**.
2. Render will automatically read the `render.yaml` file, build the server, and deploy it.
3. Render will give you a public URL (e.g., `wss://tunnel-app-xyz.onrender.com`).

To connect your local computer to your new production server, run the client with the `SERVER_URL` environment variable:

```bash
# Windows PowerShell
$env:SERVER_URL="wss://tunnel-app-xyz.onrender.com"; node src/client.js --port 3000 --subdomain my-app
```

*(For Mac/Linux):*
```bash
SERVER_URL=wss://tunnel-app-xyz.onrender.com node src/client.js --port 3000 --subdomain my-app
```

---

## Advanced Flags

You can secure your exposed site using Basic Auth:
```bash
node src/client.js --port 3000 --subdomain my-app --basic-auth admin:password123
```
Anyone visiting your public URL will be required to log in with `admin` and `password123`.
