# tunnel

A lightweight, high-performance TCP tunnel that exposes local services behind a single public port.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR:** Expose any local TCP service at a public URL with a single command.

---

## Overview

`tunnel` carries multiple TCP tunnels over a single listening port. Each tunnel gets its own subdomain, so you can expose many local services at once without opening extra firewall ports.

Traffic is forwarded as raw TCP, or over secure WebSockets (`wss://`) when TLS is enabled. A single server-level username/password pair can protect all tunnels via Basic Authentication.

```
local service ──▶ client ──▶ server (:8080) ──▶ subdomain.your-server.com
```

## Features

- **One-port multiplexing** — host multiple services behind a single TCP socket.
- **Subdomain routing** — reach services at `subdomain.your-server.com:port`.
- **Lightweight client** — no extra agents or daemons; just Node.js and one command.
- **TLS support** — secure traffic with `wss://` using the `--tls` flag.
- **Basic Auth** — optional server-wide protection via username/password.
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

## Deployment & Usage

### Server

Deploy on any VPS or host with public TCP access:

```bash
npm start -- --port 8080 --tls --auth admin:password123
```

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--port` | TCP port to listen on | `8080` |
| `--host` | IP or hostname to bind to | `0.0.0.0` |
| `--tls` | Enable TLS (generates a self-signed certificate) | `false` |
| `--auth` | Basic auth credentials, `user:pass` | none |

### Client

Connect a local service to the remote server:

```bash
node dist/client.js \
  --host tunnel.example.com \
  --port 3000 \
  --subdomain dev-myapp \
  --keepalive \
  --auth admin:password123
```

|
