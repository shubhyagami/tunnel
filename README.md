# Tunnel

A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single port.

## Badges

[![Node.js ≥ 18](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/shubhyagami/0d2e5b6a9cd3d5cd1f7b8b18b6e3a9f6/raw/continuous-node.json&style=flat-square)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![CI Build](https://img.shields.io/github/actions/workflow/status/shubhyagami/tunnel/.github/workflows/ci.yml?branch=main&label=Build&style=flat-square)](https://github.com/shubhyagami/tunnel/actions)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/shubhyagami/tunnel/pulls)

> **TL;DR** – Run `npm install && npm run build && npm start` to host a server, then in another terminal expose a local service with `node src/client.js --port <local-port> --subdomain <name>`.

---

## Features

* **Single‑port multiplexing** – many tunnels share the same TCP port.
* **WebSocket + HTTP support** – works for both protocols.
* **Low‑latency** – Nagle’s algorithm disabled, configurable keep‑alive.
* **Real‑time dashboard** – traffic, latency, and connection status at `localhost:4040`.
* **Basic authentication** – optional `user:pass` for added security.
* **Automatic reconnection** – exponential back‑off with detailed logs.

---

## Getting Started

```bash
# 1. Clone
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# 2. Install + build
npm ci
npm run build

# 3. Start the server (port 8080 by default)
npm start

# 4. In a separate terminal, expose a local HTTP server
python -m http.server 3000
node src/client.js --port 3000 --subdomain my-app
```

The tunnel will output a URL like:

```
http://my-app.localhost:8080
```

Open that in a browser or call it from your code. The dashboard is available at `http://localhost:4040`.

---

## Installation

```bash
npm install
npm run build
```

* `npm install` – Installs all dependencies.
* `npm run build` – Transpiles TypeScript and bundles the application.

---

## Running the Server

```bash
npm start
```

The server listens on `8080` by default. Change the port with the `--port` flag:

```bash
npm start -- --port 9090
```

### TLS / HTTPS

To serve over TLS, drop the `--tls` flag and point the client at `wss://<host>`.

---

## Exposing a Local Service

1. **Start your local backend**

   ```bash
   python -m http.server 3000   # or any other local server
   ```

2. **Run the client**

   ```bash
   node src/client.js --port 3000 --subdomain my-app
   ```

3. **Navigate to the URL** printed by the client, e.g. `http://my-app.localhost:8080`.

> **Tip** – Choose a unique subdomain per environment (`dev`, `staging`, `prod`) to avoid collisions.

---

## Dashboard

While the server is running, visit `http://localhost:4040`. It shows:

* Live traffic counters
* Latency charts
* Connection health

---

## Deployment

The server can be deployed to any host that allows inbound TCP connections. Render.com provides a ready‑to‑use `render.yaml`.

### Render.com

1. Create a Render.com Blueprint linked to this repo.
2. Add a `tunnel` service; Render will read `render.yaml`, build and deploy.
3. Note the public URL, e.g., `wss://tunnel.example.com`.
4. Run the client pointing to that host:

   ```bash
   node src/client.js --host tunnel.example.com --port 3000 --subdomain my-app
   ```

Deployments to other providers follow the same pattern: copy the built artifacts and run `npm start`.

---

## Configuration

The client supports the following command‑line options:

| Flag          | Description                                 | Default |
|---------------|---------------------------------------------|---------|
| `--host`      | Tunnel server hostname (e.g. `localhost` or a public URL) | `localhost` |
| `--port`      | Local server port to expose                 | **required** |
| `--subdomain` | Unique subdomain for the tunnel              | **required** |
| `--keepalive` | Send periodic ping frames to keep the connection alive | `false` |
| `--auth`      | Basic Auth credentials (`user:pass`)        | none |

**Example with keep‑alive**

```bash
node src/client.js --port 3000 --subdomain my-app --keepalive
```

---

## FAQ & Tips

* **Subdomain conflicts** – Use environment‑specific names (`dev-myapp`, `staging-myapp`).  
* **Securing sensitive services** – Provide credentials with `--auth user:password`.  
* **Stability over flaky networks** – Enable `--keepalive`.  
* **Monitoring** – Keep the dashboard open to catch latency spikes or errors early.

---

## Contributing

Pull requests are welcome! Please follow these steps:

1. Open an issue to discuss your idea or bug.
2. Fork the repository and create a feature branch (`feat/...`) or bug‑fix branch (`fix/...`).
3. Add tests if applicable; run `npm test` to ensure all tests pass.
4. Submit a PR, referencing the issue number in the title or body.
5. Await review, respond to feedback, and merge.

Focus on small, well‑scoped changes and keep commit history clean.

---

## Changelog

### 2026‑08‑26

* Millisecond‑precision timestamps in disruption logs.
* Real‑time latency graphs added to the dashboard.
* Fixed race condition causing premature connection reports under load.
* Updated documentation with additional usage tips.

*You can find older releases in the `Releases` tab.*

---

## License

MIT © tunnel team

---
