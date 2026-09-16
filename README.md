# tunnel

A lightweight, high‑performance HTTP / WebSocket tunnel that exposes local services on a single public TCP port.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR** – Expose any local TCP service to a public URL with one command.

---

## Table of contents

- [Overview](#overview)
- [Quick start](#quick-start)
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

## Overview

`tunnel` multiplexes many TCP tunnels over a single listening port.  
Each tunnel is identified by a unique sub‑domain, so you can expose multiple services without opening additional ports. The tunnel forwards traffic either over plain TCP or WebSocket (`wss://`) when TLS is enabled. Basic authentication protects all tunnels with a single credential.

---

## Quick start

```bash
# Clone and build
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel
npm ci
npm run build

# Run the server (port 8080, no TLS)
npm start

# In another shell, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

The client prints a public URL such as `http://my-app.localhost:8080`.  
While the server is running, visit `http://localhost:4040` to view the real‑time dashboard.

---

## Prerequisites

- **Node.js 18 or newer** (no compilation needed for the server, but the client uses the bundled JavaScript).
- A publicly reachable TCP port (default `8080`).  
  In cloud deployments, map the server port to the host’s HTTP port or use the provided cloud‑specific configuration files.

---

## Installation

```bash
npm ci          # Install dependencies
npm run build   # Compile TypeScript to ./dist/
```

All production code lives in the `dist/` directory.

---

## Server

Start the server with:

```bash
npm start       # Runs ./dist/server.js
```

### Flags

| Flag      | Description                                          | Default     |
|-----------|------------------------------------------------------|-------------|
| `--port`  | TCP port to listen on                                | `8080`      |
| `--tls`   | Generate a self‑signed cert and serve HTTPS         | `false`     |
| `--host`  | Bind to a specific IP or hostname                   | `0.0.0.0`   |
| `--auth`  | Basic auth credentials (`user:pass`) for all tunnels | none        |

> **Note:** Flags after `--` are passed to the underlying `node` process.  
> Example: `npm start -- --port 9090 --tls`.

The server writes the public URL for each new tunnel to stdout.

---

## Client

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
|---------------|-----------------------------------------------------------|----------|
| `--host`      | Tunnel server hostname or IP                               | no       |
| `--port`      | Local port to expose                                      | **yes** |
| `--subdomain` | Desired sub‑domain for the tunnel                         | **yes** |
| `--keepalive` | Send periodic ping frames to keep the connection alive    | no       |
| `--auth`      | Basic Auth credentials (`user:pass`)                      | no       |

The client prints the public URL once the tunnel is ready.

---

## Dashboard

While the server is running, navigate to `http://localhost:4040`.  
The dashboard shows:

- Total traffic per tunnel
- Latency charts
- Connection health indicators

Updates are streamed live via Server‑Sent Events.

---

## Deployment

`tunnel` runs on any host that accepts inbound TCP connections. The following are minimal examples; adapt the host‑specific instructions as needed.

### Render.com

1. Create a new Render service pulling from this repo.  
2. Add the provided `render.yaml` (see repo).  
3. Deploy – Render will assign a public hostname (e.g., `tunnel.example.com`).  
4. Run the client:

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

### Fly.io

```bash
fly launch --private-network
fly apps create tunnel
fly launch  # map port 8080 to host
fly secrets set AUTH_USER=alice AUTH_PASS=secret
fly deploy
fly launch  # expose port 8080
```

### Other Providers

Most other PaaS platforms (Heroku, DigitalOcean App Platform, etc.) follow the same pattern: expose port 8080 and run the server; then point the client at the assigned hostname.

---

## FAQ

| Question | Answer |
|----------|--------|
| **How do I avoid sub‑domain collisions?** | Use environment‑specific prefixes, e.g. `dev-myapp`, `staging-myapp`, `prod-myapp`. |
| **Is TLS required?** | No. Use `--tls` on the server and `wss://` on the client if you need encrypted traffic. |
| **Can I tunnel non‑HTTP services?** | Yes. The tunnel forwards raw TCP data, so any service that listens on a TCP port will work. |
| **Why do connections drop?** | Network instability can cause brief disconnects. Enabling `--keepalive` sends periodic pings to keep the TCP/WS connection alive. |
| **How many tunnels can I run concurrently?** | Unlimited, limited only by system resources and the number of sub‑domains you can register. |

---

## Contributing

Pull requests are welcome. Please follow these guidelines:

1. Fork the repository and create a feature branch (`feat/...` or `fix/...`).  
2. Add tests if the change affects functionality.  
3. Run `npm test` to ensure the suite passes.  
4. Submit a PR that references the related issue.  
5. Keep commits focused and descriptive.

---

## Changelog

**2026‑08‑26**

- Added millisecond timestamps to disruption logs.  
- Introduced latency graphs on the dashboard.  
- Fixed a race condition that caused premature connection reports.  
- Updated docs with new usage tips.

---

## License

[MIT](./LICENSE) © tunnel team

---
