# TunnelX

[![Node.js Version](https://img.shields.io/badge/node-%3E%3D16-brightgreen)](https://nodejs.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/shubhyagami/tunnel/pulls)
[![Build Status](https://img.shields.io/badge/build-passing-success)]()

```
   _____ _   _ _   _ _____ _   _ _   _  ___
  |_   _| | | | \ | | ____| \ | | \ | |/ _ \
    | | | | | |  \| |  _| |  \| |  \| | | | |
    | | | |_| | |\  | |___| |\  | |\  | |_| |
    |_|  \___/|_| \_|_____|_| \_|_| \_|\___/
```

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

---

## 🎯 Pro Tips

- **Use a memorable subdomain** – Pick something short and descriptive (e.g., `staging`, `api-demo`). This avoids URL confusion during demos.
- **Monitor traffic in real time** – The Dashboard at `localhost:4040` shows live requests. Perfect for debugging webhook integrations.
- **Pair with local HTTPS** – If your local server uses self‑signed certificates, TunnelX handles the WebSocket handshake transparently. No extra config needed.
- **Keep the client running** – Auto‑reconnect with exponential backoff means you can restart your local server without losing the tunnel. The client will automatically re‑attach.
- **Limit exposure** – Use `--basic-auth` even for internal demos. It prevents accidental public access while you iterate.

---

## 📅 Changelog – 2026-07-29

- **Dashboard UI refresh** – Added request timeline visualization and per‑subdomain traffic breakdown.
- **Improved reconnection logic** – Reduced unnecessary reconnects during brief network blips.
- **New `--max-connections` flag** – Control how many concurrent tunnels a single client can open (default 10).
- **Fixed** – Client now properly cleans up stale WebSocket connections on server restart.

---

> *“The best way to predict the future is to build it.” – Alan Kay*

Happy tunneling! 🚇