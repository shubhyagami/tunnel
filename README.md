# tunnel

A lightweight TCP tunnel that exposes local services behind a single public port.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR:** Expose any local TCP service at a public URL with a single command.

---

## Overview

`tunnel` multiplexes multiple TCP tunnels over a single listening port. Each tunnel is addressed by its own subdomain, so you can expose many local services at once without opening additional firewall ports.

Traffic is forwarded as raw TCP, or over secure WebSockets (`wss://`) when TLS is enabled. A single server-level username/password pair can protect all tunnels via Basic Authentication.

```
local service ──▶ client ──▶ server (:8080) ──▶ subdomain.your-server.com
```

## Features

- **One-port multiplexing** — host multiple services behind a single TCP socket.
- **Subdomain routing** — reach each service at `subdomain.your-server.com:port`.
- **Lightweight client** — no agents or daemons; just Node.js and one command.
- **TLS support** — secure traffic over `wss://` with the `--tls` flag.
- **Basic Auth** — optional server-wide protection with a single username/password pair.
- **Real-time dashboard** — monitor traffic, latency, and tunnel health at `http://localhost:4040`.
- **Keep-alive** — periodic ping frames to prevent timeouts on unstable networks.

## Getting Started

Requires Node.js 18 or later.

### Install

```bash
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build
npm ci
npm run build
```

### Quick start (local)

Start the server:

```bash
npm start
```

In a second terminal, expose a local service:

```bash
node dist/client.js --port 3000 --subdomain my-app
```

Your service is now reachable at `http://my-app.localhost:8080`.

## Usage

### Server

Deploy on any VPS or host with a public IP:

```bash
npm start -- --port 8080 --tls --auth admin:changeme
```

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--port` | TCP port to listen on | `8080` |
| `--host` | IP or hostname to bind to | `0.0.0.0` |
| `--tls` | Enable TLS; a self-signed certificate is generated on first start | `false` |
| `--auth` | Basic Auth credentials as `user:pass` | none |

### Client

Connect a local service to the remote server:

```bash
node dist/client.js \
  --host tunnel.example.com \
  --port 3000 \
  --subdomain dev-myapp \
  --keepalive \
  --auth admin:changeme
```

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--host` | Remote tunnel server hostname | `localhost` |
| `--port` | Local port of the service to expose | required |
| `--subdomain` | Subdomain to register on the server | required |
| `--keepalive` | Send periodic ping frames to keep the connection open | `false` |
| `--auth` | Basic Auth credentials as `user:pass` | none |

### Dashboard

While the server is running, the dashboard is available at `http://localhost:4040` and shows live traffic, per-tunnel latency, and connection health.

## Notes

- With `--tls`, the server generates a self-signed certificate on first start. For production, prefer a certificate issued by a trusted CA.
- By default the client connects to the server over plain TCP. When the server runs with `--tls`, the transport switches to secure WebSockets (`wss://`).
- Basic Authentication is enforced at the server level, so all tunnels share one set of credentials.

## Development

```bash
# Run the test suite
npm test

# Type-check and lint
npm run lint
```

Pull requests are welcome. For larger changes, please open an issue first so we can discuss the approach.

## Changelog

- **2026-09-30** — README polish: removed stray auto-generated text, tightened wording, and clarified usage examples.
- **2026-09-29** — README cleanup: clarified flag tables, added client options, and documented TLS/auth behavior.
- **Earlier** — Initial release with one-port multiplexing, subdomain routing, TLS, Basic Auth, and the dashboard.

## License

[MIT](./LICENSE)
