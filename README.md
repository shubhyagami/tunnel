# Tunnel

A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single port.

## Badges

[![Node.js ≥ 18](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/shubhyagami/0d2e5b6a9cd3d5cd1f7b8b18b6e3a9f6/raw/continuous-node.json&style=flat-square)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![CI Build](https://img.shields.io/github/actions/workflow/status/shubhyagami/tunnel/.github/workflows/ci.yml?branch=main&label=Build&style=flat-square)](https://github.com/shubhyagami/tunnel/actions)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/shubhyagami/tunnel/pulls)

> **TL;DR** – After building the project, run `npm start` to launch the server, then expose a local service with `node src/client.js --port <local‑port> --subdomain <name>`.

---

## Features

- **Single‑port multiplexing** – multiple tunnels share one TCP port.
- **HTTP and WebSocket support** – works with any web server.
- **Low latency** – Nagle’s algorithm disabled; configurable keep‑alive.
- **Real‑time dashboard** – traffic, latency, and connection status live at `localhost:4040`.
- **Optional Basic Auth** – secure your tunnels with `user:pass`.
- **Automatic reconnection** – exponential back‑off with detailed logs.

---

## Getting Started

1. `git clone https://github.com/shubhyagami/tunnel.git`
2. `cd tunnel`
3. `npm ci`
4. `npm run build`
5. `npm start` – the server starts on port **8080** by default.

Now expose a local HTTP server (or any TCP service):

1. Start a local server, e.g. `python -m http.server 3000`.
2. In a new terminal, run  
   `node src/client.js --port 3000 --subdomain my-app`.

The client prints a public URL such as

```
http://my-app.localhost:8080
```

Open that URL in a browser or use it from client code. The dashboard is available at `http://localhost:4040`.

---

## Server

Run the server with `npm start`.  
Available options:

| Flag | Description | Default |
|------|-------------|---------|
| `--port` | TCP port the server listens on | `8080` |
| `--tls` | Generate a self‑signed TLS cert and run as HTTPS | `false` |
| `--host` | Custom hostname or IP to bind to | `0.0.0.0` |

Example with a custom port:

```
npm start -- --port 9090
```

---

## Client

The client forwards a local port to the tunnel server.

| Flag | Description | Required |
|------|-------------|----------|
| `--host` | Tunnel server hostname or IP | defaults to `localhost` |
| `--port` | Local port to expose | **yes** |
| `--subdomain` | Unique subdomain for the tunnel | **yes** |
| `--keepalive` | Periodic ping frames to keep the connection alive | no |
| `--auth` | Basic Auth credentials in `user:pass` format | no |

Example with keep‑alive:

```
node src/client.js --port 3000 --subdomain my-app --keepalive
```

---

## Dashboard

While the server is running, visit `http://localhost:4040` to view:

- Live traffic counters
- Latency charts
- Connection health indicators

---

## Deployment

You can deploy the server to any host that accepts inbound TCP connections. Render.com supplies a ready‑to‑use `render.yaml`.

### Render.com

1. Create a new Render service linked to this repo.
2. Render will read `render.yaml`, build, and deploy automatically.
3. Note the public host, e.g. `wss://tunnel.example.com`.
4. Run the client pointing at that host:

```
node src/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

The same workflow applies to other providers: copy the built artifacts and run `npm start`.

---

## FAQ

| Question | Answer |
|----------|--------|
| **How do I avoid subdomain collisions?** | Use environment‑specific names, e.g. `dev-myapp`, `staging-myapp`. |
| **Do I need TLS?** | Optional. Use the `--tls` flag on the server and `wss://` on the client. |
| **Can I use the tunnel for non‑HTTP services?** | Yes. Any TCP service will work; the tunnel simply forwards traffic. |
| **Why does the connection drop?** | Network instability may cause brief drops. Enable `--keepalive` to mitigate. |

---

## Contributing

Pull requests are welcome! Please follow these steps:

1. Open an issue to discuss the change.
2. Fork the repository and create a feature branch (e.g. `feat/...` or `fix/...`).
3. Add tests if appropriate and run `npm test`.
4. Submit a PR referencing the issue number.

Keep commits small and focused.

---

## Changelog

### 2026‑08‑26

- Added millisecond timestamps to disruption logs.
- Introduced latency graphs on the dashboard.
- Fixed race condition causing premature connection reports.
- Updated documentation with new usage tips.

Older releases are available in the **Releases** tab.

---

## License

MIT © tunnel team

---
