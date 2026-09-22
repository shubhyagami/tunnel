# tunnel

A lightweight, high‑performance TCP tunnel that exposes local services behind a single public port.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR** – Expose any local TCP service to a public URL with a single command.

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Getting started](#getting-started)
  - [Quick start (local)](#quick-start)
  - [Deploying the server](#deploying-the-server)
  - [Exposing a local service](#exposing-a-local-service)
- [Installation](#installation)
- [Server](#server)
- [Client](#client)
- [Dashboard](#dashboard)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Overview

`tunnel` multiplexes many TCP tunnels over a single listening port. Each tunnel is addressed by a unique sub‑domain, allowing you to expose numerous services without opening additional ports. Traffic can be forwarded over plain TCP or WebSocket (`wss://`) when TLS is enabled. A single pair of credentials protects all tunnels via Basic Authentication.

---

## Features

- **One‑port multiplexing** – expose many services behind a single TCP socket.
- **Sub‑domain routing** – each tunnel is reachable at `subdomain.<server-host>:<port>`.
- **Zero‑agent client** – no server‑side installation on the host you want to expose.
- **WebSocket and TLS** – secure traffic with `wss://` when `--tls` is enabled.
- **Basic Auth** – lock down the entire server with one username/password.
- **Real‑time dashboard** – metrics, latency, and connection health at `http://localhost:4040`.
- **Keep‑alive** – periodic ping frames keep TCP/WS connections alive on flaky networks.

---

## Getting started

Below is a minimal workflow for a local development environment. If you already have a publicly reachable server, skip to **Deploying the server**.

### Quick start (local)

```bash
# Clone the repository
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build
npm ci
npm run build

# Start the server (HTTP on 8080, no TLS)
npm start

# In a separate terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

The client will print a public URL such as `http://my-app.localhost.tunnel:8080`.  
While the server is running, the dashboard is accessible at `http://localhost:4040`.

### Deploying the server

Deploy `tunnel` on any host that can accept inbound TCP connections (e.g., a VPS, Render, Fly.io, or your own server).

```bash
# On the server
npm ci && npm run build
npm start -- --port 8080 --tls
```

The `--tls` flag generates a self‑signed certificate and serves HTTPS. If you prefer plain TCP, omit the flag.

### Exposing a local service

Once the server is reachable, expose a service from any machine that can connect to it:

```bash
node dist/client.js \
  --host tunnel.example.com \
  --port 3000 \
  --subdomain dev-myapp \
  [--keepalive] \
  [--auth user:pass]
```

Replace `tunnel.example.com` with your server’s hostname.  
The tunnel will be available at `http://dev-myapp.tunnel.example.com:8080`.

---

## Installation

```bash
npm ci            # Install dependencies
npm run build     # Compile TypeScript → ./dist/
```

Production code lives in the `dist/` directory.

---

## Server

Start the server with:

```bash
npm start
```

### Flags

| Flag      | Meaning                                            | Default |
|-----------|----------------------------------------------------|---------|
| `--port`  | TCP port to listen on                             | `8080`  |
| `--tls`   | Generate a self‑signed cert and serve HTTPS       | `false` |
| `--host`  | Bind to a specific IP or hostname                 | `0.0.0.0` |
| `--auth`  | Basic auth (`user:pass`) for all tunnels          | none    |

Flags after `--` are passed directly to Node. Example:

```bash
npm start -- --port 9090 --tls
```

The server writes the public URL of each new tunnel to `stdout`.

---

## Client

Expose a local TCP port to the server:

```bash
node dist/client.js \
  --host tunnel.example.com \  # optional (defaults to localhost)
  --port 3000 \                  # local port to expose
  --subdomain my-app \           # desired sub‑domain
  [--keepalive] \                # send periodic ping frames
  [--auth user:pass]             # optional Basic Auth
```

The client prints the public URL once the tunnel is ready.

---

## Dashboard

While the server is running, visit `http://localhost:4040`.  
The dashboard shows:

- Traffic per tunnel
- Latency charts
- Connection health indicators

Updates are streamed live via Server‑Sent Events.

---

## FAQ

| Question | Answer |
|----------|--------|
| **How do I avoid sub‑domain collisions?** | Prefix your subdomains with environment or project names (`dev‑myapp`, `staging‑myapp`). |
| **Is TLS required?** | No. Use `--tls` on the server and `wss://` on the client if you want encryption. |
| **Can I tunnel non‑HTTP services?** | Yes – the tunnel forwards raw TCP traffic. |
| **Why do connections drop?** | Network instability can cause brief disconnects. Enabling `--keepalive` mitigates this. |
| **How many tunnels can I run?** | Unlimited, limited only by system resources and the number of sub‑domains you can register. |

---

## Contributing

Pull requests are welcome. Please follow these steps:

1. Fork the repository and create a feature branch (`feat/...` or `fix/...`).
2. Add tests if the change affects functionality.
3. Run `npm test` to ensure the suite passes.
4. Submit a PR that references the related issue.
5. Keep commits focused and descriptive.

---

## Changelog

**2026‑09‑22**

- Updated README formatting and syntax.
- Minor bug fixes in client keep‑alive logic.
- Improved dashboard latency charts.

**2026‑08‑26**

- Added millisecond timestamps to disruption logs.
- Introduced latency graphs on the dashboard.
- Fixed race condition that caused premature connection reports.
- Updated docs with new usage tips.

---

## License

[MIT](./LICENSE) © tunnel team
