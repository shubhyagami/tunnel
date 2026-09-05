# tunnel
A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single TCP port.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)

---

## Table of Contents
- [Quick Start](#quick-start)
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Server](#server)
- [Client](#client)
- [Dashboard](#dashboard)
- [Deployment](#deployment)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install and build
npm ci
npm run build

# Start the server
npm start

# In another terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

You’ll receive a public URL, e.g.:

```
http://my-app.localhost:8080
```

Open that address in a browser or use it in your client code. The real‑time dashboard is available at `http://localhost:4040`.

---

## Overview

`tunnel` forwards traffic from a globally reachable TCP port to one or more local services, optionally over WebSocket. It works with:

- Any HTTP server
- Any TCP‑based service (SSH, Redis, custom protocols, etc.)

The server accepts multiple tunnels on a single listening port, each identified by a unique sub‑domain.

---

## Features

- **Single‑port multiplexing** – many tunnels share one listening port
- **Low latency** – Nagle’s algorithm disabled, configurable keep‑alive
- **Real‑time metrics** – dashboard on `localhost:4040`
- **Basic authentication** – optional `user:pass` protection
- **Automatic reconnection** – exponential back‑off, detailed logs
- **HTTPS / WSS support** – self‑signed certificates via `--tls`

---

## Prerequisites

- **Node.js ≥ 18**
- A publicly reachable TCP port (default `8080`)

---

## Installation

```bash
npm ci
npm run build
```

The `dist/` folder contains compiled JavaScript ready for production.

---

## Server

Run the server with:

```bash
npm start
```

Optional flags (append after `--`):

| Flag      | Description                                    | Default |
|-----------|------------------------------------------------|---------|
| `--port`  | Port to listen on                             | `8080`  |
| `--tls`   | Generate a self‑signed TLS cert and use HTTPS | `false` |
| `--host`  | Bind to a specific hostname or IP             | `0.0.0.0` |
| `--auth`  | Basic Auth credentials (`user:pass`) for all tunnels | none |

**Example**

```bash
npm start -- --port 9090 --tls
```

The server logs the public URL for each tunnel as it is established.

---

## Client

The client forwards a local TCP port to the tunnel server.

```bash
node dist/client.js \
  --port 3000 \
  --subdomain my-app \
  [--host tunnel.example.com] \
  [--keepalive] \
  [--auth user:pass]
```

| Flag        | Description                                             | Required |
|-------------|---------------------------------------------------------|----------|
| `--host`    | Tunnel server hostname or IP                            | defaults to `localhost` |
| `--port`    | Local port to expose                                   | **yes**  |
| `--subdomain` | Desired sub‑domain for the tunnel                    | **yes**  |
| `--keepalive` | Send periodic ping frames to keep the connection alive | no |
| `--auth`    | Basic Auth credentials (`user:pass`)                 | no |

The client prints the public URL once the tunnel is ready.

---

## Dashboard

When the server is running, visit:

```
http://localhost:4040
```

The dashboard displays:

- Traffic counters
- Latency charts
- Connection health indicators

Updates are pushed automatically in real time.

---

## Deployment

`tunnel` can run on any host that accepts inbound TCP connections.  
Below is a minimal Render example; the same steps apply to Heroku, DigitalOcean, etc.

### Render.com

1. Create a new Render service that pulls from this repo.  
2. Render will detect `render.yaml`, build, and deploy automatically.  
3. Note the public host, e.g. `wss://tunnel.example.com`.  
4. Run the client:

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

---

## FAQ

| Question | Answer |
|----------|--------|
| How do I avoid sub‑domain collisions? | Use environment‑specific names, e.g. `dev-myapp`, `staging-myapp`. |
| Do I need TLS? | TLS is optional. Use `--tls` on the server and `wss://` on the client. |
| Can I tunnel non‑HTTP services? | Yes. Any TCP service will work; the tunnel simply forwards traffic. |
| Why does the connection drop? | Network instability may cause brief drops. Enable `--keepalive` to mitigate. |
| How many concurrent tunnels are allowed? | Unlimited (subject to system limits). Each uses its own sub‑domain. |

---

## Contributing

Pull requests are welcome! Please follow these steps:

1. Fork the repository and create a feature branch (`feat/...` or `fix/...`).  
2. Add tests if applicable and run `npm test`.  
3. Submit a PR that references any related issue.  
4. Keep commits small, focused, and descriptive.

---

## Changelog (excerpt)

**2026‑08‑26**

- Added millisecond timestamps to disruption logs.  
- Introduced latency graphs on the dashboard.  
- Fixed race condition causing premature connection reports.  
- Updated documentation with new usage tips.

---

## License

[MIT](LICENSE) © tunnel team

---
