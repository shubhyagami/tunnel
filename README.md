[K[2m  [2mmodel z-ai/glm-5.3-flash failed, trying next...[0m[0m
[K[2m  [2mmodel deepseek-ai/deepseek-v4.1-flash failed, trying next...[0m[0m
# tunnel

A minimal TCP tunnel that exposes a local service through a single public port.  
Each service is reachable by its own subdomain, so you can run multiple
tunnels without opening more than one listening port on the server.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥ 18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR** – Expose any local TCP service at a public URL with one command.

---

## Overview

`tunnel` multiplexes many TCP tunnels over a single listening socket.  
Each tunnel is addressed by a unique subdomain, e.g. `app.example.com`.  
Traffic is forwarded as plain TCP, or as secure WebSockets (`wss://`) when TLS
is enabled on the server. A single server‑wide username/password pair protects
all tunnels with Basic Authentication.

```
local service ──▶ client ──▶ server (TCP :8080) ──▶ subdomain.server.com
```

---

## Features

- **One‑port multiplexing** – host many services behind a single TCP socket.  
- **Subdomain routing** – each tunnel is reachable at `subdomain.server.com`.  
- **Pure Node.js** – only one command line, no agent or daemon required.  
- **TLS** – enable secure transport with the `--tls` flag (self‑signed cert
  created on first run).  
- **Basic Auth** – optional server‑wide credentials (`user:pass`).  
- **Keep‑alive** – periodic ping frames to keep the connection alive over
  unstable networks.  
- **Dashboard** – live view of traffic, latency, and connection health at
  `http://localhost:4040`.

---

## Getting Started

> Requires Node.js 18 or newer.

### Install

```bash
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build the project
npm ci
npm run build
```

### Quick server start (local)

```bash
npm start
```

### Expose a local service

```bash
node dist/client.js --port 3000 --subdomain my-app
```

Your service is now reachable at `http://my-app.localhost:8080`.

---

## Usage

### Server

Deploy the server on any machine with a public IP:

```bash
npm start -- --port 8080 --tls --auth admin:changeme
```

| Flag            | Description                                  | Default   |
| ----------------| ---------------------------------------------|-----------|
| `--port`        | TCP port the server listens on              | `8080`    |
| `--host`        | IP or hostname to bind the socket           | `0.0.0.0` |
| `--tls`         | Enable TLS (self‑signed cert on first run) | `false`   |
| `--auth`        | Basic Auth credentials `user:pass`         | none      |

When `--tls` is set, the server automatically switches to secure WebSockets
(`wss://`). The dashboard continues to run on `http://localhost:4040` and
provides real‑time statistics.

### Client

Connect a local service to a remote server:

```bash
node dist/client.js \
  --host tunnel.example.com \
  --port 3000 \
  --subdomain dev-myapp \
  --keepalive \
  --auth admin:changeme
```

| Flag          | Description                                         | Default |
| ------------- | ---------------------------------------------------|---------|
| `--host`      | Remote tunnel server hostname                      | `localhost` |
| `--port`      | Local port of the service to expose                | _required_ |
| `--subdomain` | Subdomain to register on the server                | _required_ |
| `--keepalive` | Send periodic ping frames to keep the connection open | `false` |
| `--auth`      | Basic Auth credentials `user:pass`                 | none    |

### Dashboard

With the server running, open `http://localhost:4040` in a browser to see a
live overview of all tunnels, including throughput, latency, and health
status.

---

## Notes

- `--tls` creates a self‑signed certificate on the first run. For production,
  replace it with a certificate from a trusted CA.  
- The client connects over plain TCP by default. When the server runs with
  `--tls`, the transport switches automatically to secure WebSockets (`wss://`).  
- Basic Authentication is applied at the server level, so all tunnels share
  one credential set.

---

## Development

```bash
# Run the test suite
npm test

# Type‑check, format, and lint
npm run lint
```

Pull requests are welcome. For substantial changes, open an issue first so we can
discuss the approach.

---

## Changelog

- **2026‑10‑01** – Minor README cleanup: tightened wording and removed stray
  auto‑generated blocks.  
- **2026‑09‑30** – README polish: clarified usage examples and flag tables.  
- **2026‑09‑29** – Added client options and docs for TLS/auth behavior.  
- **Earlier** – Initial release with one‑port multiplexing, subdomain routing,
  TLS, Basic Auth, and a live dashboard.

---

## License

[MIT](./LICENSE)
