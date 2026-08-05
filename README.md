# TunnelX

[![Node.js Version](https://img.shields.io/badge/node-%3E%3D16-brightgreen)](https://nodejs.org)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/shubhyagami/tunnel/pulls)
[![Build Status](https://img.shields.io/badge/build-passing-success)]()

```
   _____ _   _ _   _ _____ _   _ _   _  ___
  |_   _| | | | \ | | ____| \ | | \ | |/ _ \
    | | | | | |  \| |  _| |  \| |  \| | | | |
    | | | |_| | |\  | |___| |\  | |\  | |_| |
    |_|  \___/|_| \_|_____|_| \_|_| \_|\___/
```

A high-performance, single-port HTTP/WebSocket tunneling solution designed for Render.com and local development. It allows you to expose your local web servers to the public internet securely and fast.

## Features
- 🚀 **Ultra-fast multiplexed proxy** (disables Nagle's algorithm for minimum latency)
- 🎨 **Web UI Dashboard** for real-time traffic monitoring
- 🔒 **Basic Auth protection** for local services
- ⚡ **Auto-reconnecting resilience** with exponential backoff

---

## 1. How to run it LOCALLY (for testing)

First, start the Tunnel Server:
```bash
npm install
npm run build
npm start
```
*(The server will run on port 8080 by default)*

Next, start your local web server (the one you want to expose). For example, a simple Python server:
```bash
python -m http.server 3000
```

Finally, start the Tunnel Client to connect them:
```bash
# Connects your local port 3000 to the server, requesting the subdomain "my-app"
node src/client.js --port 3000 --subdomain my-app
```

Now you can:
- View your exposed site at: `http://my-app.localhost:8080`
- View your Live Traffic Dashboard at: `http://localhost:4040`

---

## 2. How to run it in PRODUCTION (Render.com)

1. Connect this GitHub repository to Render.com and create a new **Blueprint**.
2. Render will automatically read the `render.yaml` file, build the server, and deploy it.
3. Render will give you a public URL (e.g., `wss://tunn

---

## 🕰️ Contributing — The TVA Way

Welcome, Variant! You have been selected by the **Temporal Variance Authority** to help maintain the sacred timeline of TunnelX. Every contribution you make is a correction to a dangerous nexus event. Follow these guidelines to avoid being pruned.

### 🌌 The Sacred Timeline (Code of Conduct)

- All contributors must **respect the timeline**. No breaking changes without a warning first.
- **No Loki-style trickery**: write clean, readable code and keep your PR descriptions honest.
- **Do not create branches that shouldn't exist** — always fork from `main`.

### 🔧 Minuteman Workflow

1. **File a TVA Report** — open an issue describing the temporal anomaly (bug) or desired new feature. Use the templates provided.
2. **Request a Mission Brief** — we’ll assign you to the task if it aligns with our Time-Keepers’ plan.
3. **Spawn a Variant Branch** — create a branch from `main` with a name like `fix/nexus-event-123` or `feat/time-door`.
4. **Make your e

---

## 📜 Changelog — Temporal Record

### [2026-08-06] — Nexus Event Stabilization

- **Added** proactive time‑splice detection: auto‑reconnect now logs the exact millisecond of disruption for faster root‑cause analysis.
- **Improved** dashboard latency visualization — traffic flow now rendered as a sacred timeline graph (no more Nexus Events hidden in the noise).
- **Fixed** a temporal paradox where the client could sometimes believe it was connected before the server acknowledged the handshake. This caused a 0.3% failure rate in high‑load scenarios. Variants responsible have been pruned.
- **Updated** documentation with a new “Pro Tips” section (see below) to help agents avoid common timeline violations.

---

## 💡 Pro Tips — From the Time‑Keepers

- **Use a dedicated subdomain per environment.** Avoid sharing a single subdomain between staging and production — it creates timeline branches that are hard to reconcile.
- **Enable Basic Auth for sensitive services** even when behind the tunnel. A rogue variant could intercept traffic if they guess your subdomain.
- **Monitor the dashboard live** during initial connection. The traffic graph will show you exactly where latency spikes occur — those are often Nexus Events waiting to happen.
- **If you see repeated disconnects**, check your local firewall. Some networks aggressively prune WebSocket connections after idle periods. Use the `--keepalive` flag (coming in next release) to send a temporal ping every 30 seconds.

---

*This project is maintained by the TVA Temporal Engineering Division. All contributions are subject to timeline approval.*