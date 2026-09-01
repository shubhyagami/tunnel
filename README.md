# Tunnel

> A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public internet over a single port.

**Badges**

[![Node.js ≥ 16](https://img.shields.io/badge/node-%3E%3D16-brightgreen.svg)](https://nodejs.org)  
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![CI Build](https://img.shields.io/github/actions/workflow/status/shubhyagami/tunnel/.github/workflows/ci.yml?branch=main&label=Build)](https://github.com/shubhyagami/tunnel/actions)  
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/shubhyagami/tunnel/pulls)

---

## Table of Contents

- [Overview](#overview)
- [Quickstart](#quickstart)
- [Installation](#installation)
- [Running the server](#running-the-server)
- [Exposing a local service](#exposing-a-local-service)
- [Dashboard](#dashboard)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Tips & FAQ](#tips--faq)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

---

## Overview

Tunnel allows you to safely expose a local HTTP or WebSocket server to the public internet with only one open port. It is suited for local development, demonstration, and quick deployment on Render.com or other hosting providers.

Key characteristics:

- **Multiplexed proxy** – multiple tunnels share a single socket, with Nagle’s algorithm disabled for low latency.
- **Dashboard UI** – real‑time traffic and latency monitoring on `localhost:4040`.
- **Basic Auth** – optional HTTP authentication for added security.
- **Reconnect logic** – automatic reconnection with exponential back‑off and detailed disruption logs.

---

## Quickstart

```bash
# Clone the repo
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build
npm ci
npm run build

# Start the tunnel server (default port 8080)
npm start

# In another terminal, expose a local service
python -m http.server 3000      # or any local server
node src/client.js --port 3000 --subdomain my-app

# Access the service at
http://my-app.localhost:8080
```

The dashboard is available at `http://localhost:4040`.

---

## Installation

```bash
npm install
npm run build
```

- `npm install` – Installs all dependencies.
- `npm run build` – Transpiles TypeScript and bundles the code.

## Running the server

```bash
npm start
```

The server starts on port `8080` by default. You can change the port with the `--port` flag:

```bash
npm start -- --port 9090
```

---

## Exposing a local service

1. **Start your local server** (e.g., `python -m http.server 3000`).
2. **Run the client** specifying the local port and a unique subdomain:

   ```bash
   node src/client.js --port 3000 --subdomain my-app
   ```

3. **Visit the URL** shown in the client log, e.g.:

   ```
   http://my-app.localhost:8080
   ```

### Subdomains

Each tunnel is identified by a subdomain. Use a unique subdomain per environment (dev, staging, production) to avoid collisions.

---

## Dashboard

The dashboard runs on `localhost:4040` and shows:

- Live traffic statistics
- Latency graphs
- Connection status

Open the address in your browser while the server is running.

---

## Deployment

Render.com can deploy the server automatically using the provided `render.yaml`. For any other provider, copy the built artifacts and run the server as above.

### Render.com

1. Create a Render.com Blueprint linked to this repository.
2. Add the `tunnel` service; Render will read `render.yaml`, build, and deploy.
3. After deployment, note the public URL (e.g., `wss://tunnel.example.com`).
4. Point your client to the production host:

   ```bash
   node src/client.js --host tunnel.example.com --port 3000 --subdomain my-app
   ```

---

## Configuration

The client accepts the following flags:

| Flag | Description | Default |
|------|-------------|---------|
| `--host` | Tunnel server hostname (defaults to `localhost`) | |
| `--port` | Local server port to expose | required |
| `--subdomain` | Unique subdomain for the tunnel | required |
| `--keepalive` | Send periodic ping frames to keep the connection alive | false |
| `--auth` | Basic Auth credentials in `user:pass` format | none |

Example with keep‑alive:

```bash
node src/client.js --port 3000 --subdomain my-app --keepalive
```

---

## Tips & FAQ

- **Avoid subdomain conflicts** by using environment‑specific names (e.g., `dev-myapp`, `staging-myapp`).
- **Secure sensitive services** with Basic Auth: `--auth user:password`.
- **Stable connections**: enable `--keepalive` if you notice frequent disconnects, especially over shared networks.
- **Monitoring**: keep the Dashboard open during the initial run to spot latency spikes or errors.

---

## Contributing

We welcome pull requests! Please follow these steps:

1. **Open an issue** to discuss a bug or feature.
2. **Fork** the repository and create a feature branch (`feat/add-auth`) or bug‑fix branch (`fix/reconnect`).
3. **Write tests** where applicable and ensure all tests pass.
4. **Submit a PR**, referencing the issue in the title/description.
5. **Review** – maintainers will review, suggest changes, and merge.

Keep changes focused and refrain from large, unrelated modifications.

---

## Changelog

### 2026‑08‑26

- Added millisecond‑precision timestamps for disruption logs.
- Rendered latency as a real‑time graph in the dashboard.
- Fixed a race condition that caused premature connection reports under high load.
- Updated documentation with additional usage tips.

---

## License

MIT © tunnel team

---
