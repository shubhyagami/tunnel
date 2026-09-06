# tunnel

A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single TCP port.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![GitHub CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR** – Forward any local TCP service to a publicly reachable URL with a single command.

---

## 👋 Quick start

```bash
# Clone the repo
git clone https://github.com/shubhyagami/tunnel.git && cd tunnel

# Install dependencies and build
npm ci
npm run build

# Start the server (listens on 8080 by default)
npm start

# In another terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

You’ll see a public URL in the client output, e.g. `http://my-app.localhost:8080`.  
The real‑time dashboard lives at `http://localhost:4040`.

---

## 🧩 What it does

- **Single‑port multiplexing** – many tunnels share one listening port, identified by a unique sub‑domain.
- **Zero configuration** – works with any HTTP or TCP‑based service (SSH, Redis, custom protocol, …).
- **WebSocket support** – tunnel traffic over a secure WebSocket (`wss://`) if your server uses TLS.
- **Heartbeat** – optional keep‑alive pings keep idle connections alive.
- **Basic auth** – protect all tunnels with a single `user:pass`.
- **Real‑time dashboard** – monitor traffic, latency and connection health.

---

## 📦 Prerequisites

- Node.js ≥18
- A publicly reachable TCP port (default `8080`)

---

## 🚀 Installation

```bash
npm ci          # Install dependencies
npm run build   # Compile TypeScript → dist/
```

All code needed for production lives in `dist/`.

---

## 🎛️ Server

Start the server with:

```bash
npm start
```

Optional flags can be passed after `--`:

| Flag      | Description                                          | Default   |
|-----------|-------------------------------------------------------|-----------|
| `--port`  | TCP port to listen on                                 | `8080`    |
| `--tls`   | Generate a self‑signed TLS cert and use HTTPS        | `false`   |
| `--host`  | Bind to a specific IP or hostname                     | `0.0.0.0` |
| `--auth`  | Basic Auth credentials (`user:pass`) for all tunnels | none      |

Example:

```bash
npm start -- --port 9090 --tls
```

The server logs the public URL for each tunnel as it is established.

---

## 🖥️ Client

Expose a local TCP port to the server:

```bash
node dist/client.js \
  --port 3000 \
  --subdomain my-app \
  [--host tunnel.example.com] \
  [--keepalive] \
  [--auth user:pass]
```

| Flag        | Description                                                  | Required |
|-------------|--------------------------------------------------------------|----------|
| `--host`    | Tunnel server hostname or IP                                | no       |
| `--port`    | Local port to expose                                         | **yes**  |
| `--subdomain` | Desired sub‑domain for the tunnel                         | **yes**  |
| `--keepalive` | Send periodic ping frames to keep the connection alive   | no       |
| `--auth`    | Basic Auth credentials (`user:pass`)                         | no       |

The client prints the public URL once the tunnel is ready.

---

## 📊 Dashboard

Navigate to `http://localhost:4040` while the server is running.  
It displays:

- Traffic counters
- Latency charts
- Connection health indicators

Updates are pushed in real time via Server‑Sent Events.

---

## ☁️ Deployment

`tunnel` can run on any host that accepts inbound TCP connections.

### Render.com

1. Create a new Render service that pulls from this repo.  
2. Paste a `render.yaml` (see repository) – Render automatically builds and deploys.  
3. Note the public hostname, e.g. `wss://tunnel.example.com`.  
4. Run the client:

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

The same steps apply to other providers (Heroku, DigitalOcean, Fly.io, etc.) with minimal adjustments.

---

## ❓ FAQ

| Question | Answer |
|----------|--------|
| *How do I avoid sub‑domain collisions?* | Use environment‑specific names: `dev-myapp`, `staging-myapp`, `prod-myapp`. |
| *Do I need TLS?* | TLS is optional. Use `--tls` on the server and `wss://` on the client. |
| *Can I tunnel non‑HTTP services?* | Yes. Any TCP service will work; the tunnel simply forwards traffic. |
| *Why does the connection drop?* | Network instability may cause brief drops. Enable `--keepalive` to mitigate. |
| *How many concurrent tunnels are allowed?* | Unlimited, limited only by system resources and the number of sub‑domains. |

---

## 🤝 Contributing

Pull requests are welcome! Please follow these steps:

1. Fork the repository and create a feature branch (`feat/...` or `fix/...`).  
2. Add tests if applicable and run `npm test`.  
3. Submit a PR that references the related issue.  
4. Keep commits focused, descriptive and small.

---

## 📗 Changelog (excerpt)

**2026‑08‑26**

- Added millisecond timestamps to disruption logs.  
- Introduced latency graphs on the dashboard.  
- Fixed race condition causing premature connection reports.  
- Updated docs with new usage tips.

---

## 📜 License

[MIT](LICENSE) © tunnel team
