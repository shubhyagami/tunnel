# tunnel

A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single TCP port.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)

---

## 📦 Getting Started

```bash
# Clone & install
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel
npm ci

# Build the TypeScript sources
npm run build

# Start the server (defaults to port 8080)
npm start

# In a new terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

You’ll receive a public URL, e.g.:

```
http://my-app.localhost:8080
```

Open that address in a browser or use it in your code. The real‑time dashboard is available at `http://localhost:4040`.

---

## 🧩 Overview

`tunnel` forwards traffic from a globally reachable TCP port to one or more local services, optionally over WebSocket.  
* Works with any HTTP server or TCP‑based service (SSH, Redis, custom protocols, etc.).  
* The server accepts multiple tunnels on a single listening port, each identified by a unique sub‑domain.

---

## ✨ Features

* **Single‑port multiplexing** – many tunnels share one listening port.  
* **Low latency** – Nagle’s algorithm disabled; configurable keep‑alive.  
* **Real‑time metrics** – dashboard at `localhost:4040` with traffic counters, latency charts, and connection health.  
* **Basic authentication** – optional `user:pass` protection for all tunnels.  
* **Automatic reconnection** – exponential back‑off with detailed logs.  
* **HTTPS / WSS support** – self‑signed certificates via `--tls`.

---

## ⚙️ Prerequisites

* **Node.js ≥18**  
* A publicly reachable TCP port (default `8080`)

---

## 📥 Installation

```bash
npm ci      # Install dependencies
npm run build
```

The `dist/` folder contains the compiled JavaScript ready for production.

---

## ▶️ Server

Start the server with:

```bash
npm start
```

**Optional flags** (pass after `--`):

| Flag      | Description                                            | Default    |
|-----------|--------------------------------------------------------|------------|
| `--port`  | TCP port to listen on                                  | `8080`     |
| `--tls`   | Generate a self‑signed TLS cert and use HTTPS          | `false`    |
| `--host`  | Bind to a specific hostname or IP                     | `0.0.0.0`  |
| `--auth`  | Basic Auth credentials (`user:pass`) for all tunnels | none       |

*Example*

```bash
npm start -- --port 9090 --tls
```

The server logs the public URL for each tunnel as it is established.

---

## 🧑‍💻 Client

Expose a local TCP port to the tunnel server:

```bash
node dist/client.js \
  --port 3000 \
  --subdomain my-app \
  [--host tunnel.example.com] \
  [--keepalive] \
  [--auth user:pass]
```

| Flag        | Description                                          | Required |
|-------------|------------------------------------------------------|-----------|
| `--host`    | Tunnel server hostname or IP                        | defaults to `localhost` |
| `--port`    | Local port to expose                               | **yes**   |
| `--subdomain` | Desired sub‑domain for the tunnel                | **yes**   |
| `--keepalive` | Send periodic ping frames to keep the connection alive | no  |
| `--auth`    | Basic Auth credentials (`user:pass`)                | no        |

The client prints the public URL once the tunnel is ready.

---

## 📊 Dashboard

When the server is running, open:

```
http://localhost:4040
```

The dashboard shows:

* Traffic counters
* Latency charts
* Connection health indicators

Updates are pushed automatically in real time.

---

## 🛠️ Deployment

`tunnel` can run on any host that accepts inbound TCP connections.

### Render.com

1. Create a new Render service that pulls from this repo.  
2. Render will detect `render.yaml`, build, and deploy automatically.  
3. Note the public host, e.g. `wss://tunnel.example.com`.  
4. Run the client:

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

The same steps apply to other providers (Heroku, DigitalOcean, etc.).

---

## ❓ FAQ

| Question | Answer |
|----------|--------|
| How do I avoid sub‑domain collisions? | Use environment‑specific names, e.g. `dev-myapp`, `staging-myapp`. |
| Do I need TLS? | TLS is optional. Use `--tls` on the server and `wss://` on the client. |
| Can I tunnel non‑HTTP services? | Yes. Any TCP service will work; the tunnel simply forwards traffic. |
| Why does the connection drop? | Network instability may cause brief drops. Enable `--keepalive` to mitigate. |
| How many concurrent tunnels are allowed? | Unlimited (subject to system limits). Each uses its own sub‑domain. |

---

## 🤝 Contributing

Pull requests are welcome! Please follow these steps:

1. Fork the repository and create a feature branch (`feat/...` or `fix/...`).  
2. Add tests if applicable and run `npm test`.  
3. Submit a PR that references the related issue.  
4. Keep commits small, focused, and descriptive.

---

## 📗 Changelog (excerpt)

**2026‑08‑26**

* Added millisecond timestamps to disruption logs.  
* Introduced latency graphs on the dashboard.  
* Fixed race condition causing premature connection reports.  
* Updated documentation with new usage tips.

---

## 📄 License

[MIT](LICENSE) © tunnel team

---
