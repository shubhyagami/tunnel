# tunnel

*A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single TCP port.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![GitHub CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR** – Expose any local TCP service to a public URL with a single command.

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install deps and compile the TS source
npm ci
npm run build

# Start the server (defaults to port 8080)
npm start

# In another terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

You’ll see a public URL in the client output, e.g. `http://my-app.localhost:8080`.  
The real‑time dashboard is available at `http://localhost:4040`.

---

## 🔧 Features

| Feature | Description |
|---------|-------------|
| **Single‑port multiplexing** | Many tunnels share one listening port, identified by a unique sub‑domain. |
| **Zero configuration** | Works with any HTTP or TCP service (SSH, Redis, custom protocol, …). |
| **WebSocket support** | Forward traffic over a secure WebSocket (`wss://`) when TLS is enabled. |
| **Optional keep‑alive** | Periodic ping frames keep idle connections alive. |
| **Basic auth** | Protect all tunnels with a single `user:pass`. |
| **Real‑time dashboard** | View traffic counters, latency charts and connection health via Server‑Sent Events. |

---

## 📦 Prerequisites

- Node.js **≥18**
- A publicly reachable TCP port (default `8080`)

---

## 🏗️ Installation

```bash
npm ci          # Install dependencies
npm run build   # Compile TypeScript → dist/
```

All production‑ready code resides in the `dist/` directory.

---

## 🌐 Server

Start the server with:

```bash
npm start
```

**Flags**

| Flag      | Description                                          | Default     |
|-----------|------------------------------------------------------|-------------|
| `--port`  | TCP port to listen on                                | `8080`      |
| `--tls`   | Generate a self‑signed cert and serve HTTPS         | `false`     |
| `--host`  | Bind to a specific IP or hostname                   | `0.0.0.0`   |
| `--auth`  | Basic Auth credentials (`user:pass`) for all tunnels | none        |

Example:

```bash
npm start -- --port 9090 --tls
```

The server logs the public URL for each tunnel as it is established.

---

## 🔌 Client

Expose a local TCP port to the server:

```bash
node dist/client.js \
  --port 3000 \
  --subdomain my-app \
  [--host tunnel.example.com] \
  [--keepalive] \
  [--auth user:pass]
```

| Flag          | Description                                               | Required |
|---------------|-----------------------------------------------------------|---------|
| `--host`      | Tunnel server hostname or IP                               | no      |
| `--port`      | Local port to expose                                      | **yes** |
| `--subdomain` | Desired sub‑domain for the tunnel                         | **yes** |
| `--keepalive` | Send periodic ping frames to keep the connection alive    | no      |
| `--auth`      | Basic Auth credentials (`user:pass`)                      | no      |

The client prints the public URL once the tunnel is ready.

---

## 📊 Dashboard

While the server runs, visit `http://localhost:4040` to see:

- Traffic counters
- Latency charts
- Connection health indicators

Updates are pushed in real time via Server‑Sent Events.

---

## ☁️ Deployment

`tunnel` works on any host that accepts inbound TCP connections.

### Render.com

1. Create a new Render service that pulls from this repo.  
2. Add the provided `render.yaml` (exists in the repo).  
3. Deploy – a public hostname (e.g. `tunnel.example.com`) will be assigned.  
4. Run the client:  

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

Other providers (Heroku, Fly.io, DigitalOcean, etc.) follow the same pattern with minimal changes.

---

## ❓ FAQ

| Question | Answer |
|----------|--------|
| **How do I avoid sub‑domain collisions?** | Use environment‑specific names, e.g. `dev-myapp`, `staging-myapp`, `prod-myapp`. |
| **Is TLS required?** | No. Use `--tls` on the server and `wss://` on the client if you want encrypted traffic. |
| **Can I tunnel non‑HTTP services?** | Yes. Any TCP service will work; the tunnel simply forwards raw traffic. |
| **Why do connections drop?** | Network instability can cause brief drops. Enabling `--keepalive` helps keep connections alive. |
| **How many concurrent tunnels are allowed?** | Unlimited, limited only by system resources and the number of sub‑domains. |

---

## 🤝 Contributing

Pull requests are welcome! Please:

1. Fork the repository and create a feature branch (`feat/...` or `fix/...`).  
2. Add tests if applicable and run `npm test`.  
3. Submit a PR that references the related issue.  
4. Keep commits focused, descriptive, and small.

---

## 📚 Changelog

**2026‑08‑26**

- Added millisecond timestamps to disruption logs.  
- Introduced latency graphs on the dashboard.  
- Fixed race condition causing premature connection reports.  
- Updated docs with new usage tips.

---

## 📜 License

[MIT](LICENSE) © tunnel team
