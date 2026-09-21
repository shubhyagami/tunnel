# tunnel

*A lightweight, high‑performance TCP tunnel that exposes local services behind a single public port.*

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR** – Expose any local TCP service to a public URL with one command.

---

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Quick start](#quick-start)
- [Getting started](#getting-started)
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

`tunnel` multiplexes many TCP tunnels over a single listening port. Each tunnel is addressed by a unique sub‑domain, allowing you to expose numerous services without opening additional ports. Traffic can be forwarded over plain TCP or WebSocket (`wss://`) when TLS is enabled. Basic authentication protects all tunnels with a single credential.

---

## Features

- **Single‑port multiplexing** – expose many services behind one TCP socket.
- **Sub‑domain routing** – each tunnel is reachable at `subdomain.host.tunnel`.
- **Zero‑agent client** – no server‑side installation required on the host you want to expose.
- **WebSocket support** – TLS can be enabled for encrypted traffic (`wss://`).
- **Basic authentication** – lock down the entire server with one username/password.
- **Real‑time dashboard** – traffic, latency, and connection health displayed at `http://localhost:4040`.
- **Keep‑alive** – periodic ping frames keep TCP/WS connections alive across flaky networks.

---

## Quick start

```bash
# Clone the repo
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install & build
npm ci
npm run build

# Run the server (default 8080, no TLS)
npm start

# In another terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

The client prints a public URL such as `http://my-app.localhost.tunnel:8080`.  
While the server is running, the dashboard is available at `http://localhost:4040`.

---

## Getting started

> These steps assume you have a publicly reachable server that can accept inbound TCP connections. Replace `tunnel.example.com` with your own host.

1. **Deploy the server**  
   ```bash
   # On your host
   npm ci && npm run build
   npm start -- --port 8080 --tls
   ```
2. **Expose a local service** (from the machine you want to share)  
   ```bash
   node dist/client.js --host tunnel.example.com --port 3000 --subdomain dev-myapp
   ```

Now `http://dev-myapp.tunnel.example.com:8080` forwards traffic to your local port 3000.

---

## Installation

```bash
npm ci          # Install dependencies
npm run build   # Compile TypeScript → ./dist/
```

Production code is in the `dist/` directory.

---

## Server

Run the server with:

```bash
npm start
```

### Flags

| Flag      | Description                                | Default |
|-----------|--------------------------------------------|---------|
| `--port`  | TCP port to listen on                      | `8080`  |
| `--tls`   | Generate a self‑signed cert and serve HTTPS| `false` |
| `--host`  | Bind to a specific IP or hostname           | `0.0.0.0` |
| `--auth`  | Basic auth (`user:pass`) for all tunnels   | none    |

Flags after `--` are passed to `node`.  
Example:

```bash
npm start -- --port 9090 --tls
```

The server writes the public URL of each new tunnel to stdout.

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

| Flag          | Description                                         | Required |
|---------------|-----------------------------------------------------|---------|
| `--host`      | Tunnel server hostname or IP                       | no      |
| `--port`      | Local port to expose                               | **yes** |
| `--subdomain` | Desired sub‑domain for the tunnel                  | **yes** |
| `--keepalive` | Send periodic ping frames to keep the connection alive | no |
| `--auth`      | Basic Auth credentials (`user:pass`)               | no      |

The client prints the public URL once the tunnel is ready.

---

## Dashboard

Navigate to `http://localhost:4040` while the server is running. The dashboard shows:

- Traffic per tunnel
- Latency charts
- Connection health indicators

Updates are streamed live via Server‑Sent Events.

---

## Deployment

`tunnel` runs on any host that accepts inbound TCP connections. Below are minimal examples for popular platforms. Adapt the host‑specific instructions as needed.

### Render.com

1. Create a new Render service pulling from this repo.  
2. Add the provided `render.yaml` (check the repo).  
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

Most PaaS platforms (Heroku, DigitalOcean App Platform, etc.) follow the same pattern: expose port 8080 and run the server; then point the client at the assigned hostname.

---

## FAQ

| Question | Answer |
|----------|--------|
| How do I avoid sub‑domain collisions? | Use environment‑specific prefixes, e.g. `dev-myapp`, `staging-myapp`, `prod-myapp`. |
| Is TLS required? | No. Use `--tls` on the server and `wss://` on the client if you need encrypted traffic. |
| Can I tunnel non‑HTTP services? | Yes. The tunnel forwards raw TCP data, so any TCP service will work. |
| Why do connections drop? | Network instability can cause brief disconnects. Enabling `--keepalive` sends periodic pings. |
| How many tunnels can I run concurrently? | Unlimited, limited only by system resources and the number of sub‑domains you can register. |

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
