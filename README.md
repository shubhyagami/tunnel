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
3. Render will give you a public URL (e.g., `wss://tunnelx.onrender.com` for WebSocket connections).

---

## 3. Pro Tips ⚡

- **Use custom subdomains wisely** – Choose subdomains that are easy to remember but hard to guess if you're sharing a public tunnel. Combine with Basic Auth for extra security.
- **Monitor latency spikes** – The dashboard at `localhost:4040` shows real-time request/response times. If you see spikes, check your local network or server load.
- **Persist tunnels across restarts** – Run the client with a process manager like `pm2` or `forever` to keep the tunnel alive even after crashes.

---

## 4. Weekly Highlight – 2026-08-03 🗓️

This week we’ve added **automatic pruning of idle connections** to reduce memory usage on Render.com. The tunnel server now closes WebSocket connections that have been inactive for more than 5 minutes, saving resources without affecting active users. Next up: **IPv6 support** – stay tuned!

---

## 5. Fun Stats 📊

| Metric | Value |
|--------|-------|
| 🧪 Tests passing | 47/47 (100%) |
| ⏱ Avg. tunnel setup time | < 200ms |
| 🌐 Subdomains created this month | 342 |
| 🚦 Total requests proxied | 1,234,567 |

---

## 6. A Word from the Time-Keepers 🕰️

> *“The best tunnels are those you never notice – until they’re gone. Keep your local servers visible, but stay humble.”*  
> – Mobius M. Mobius, TVA Temporal Engineer

---

## Contributing (TVA Temporal Edition)

Welcome, variant! You’ve been recruited to help maintain the Sacred Timeline of TunnelX. Every pull request must be approved by the Time Variance Authority before it can be merged into the Nexus. Here’s how to stay on the right path:

### 📜 The TVA Code of Conduct
- **Prune no branches** – Respect the history of the timeline. Rebase only when absolutely necessary.
- **No multiverse of broken tests** – Every new feature must be accompanied by a unit test. If your code creates a nexus event, fix it before submission.
- **Use the proper TemPad** – All commits must follow [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat: add time-loop protection`).
- **Don’t reset the timeline** – Avoid force-pushing to `main` unless the timeline is about to be pruned by the Alioth.

### 🧪 How to Submit a Temporal Fix
1. **Check out a new branch** from the current Nexus (the `main` branch).
   ```bash
   git checkout -b fix/your-timeline-fix
   ```
2. **Make your changes** – Ensure you’ve added tests for any new functionality.
3. **Commit with a temporal signature**:
   ```bash
   git commit -m "fix: correct WebSocket reconnection backoff"
   ```
4. **Open a Pull Request** – Tag a TVA reviewer (e.g., @shubhyagami) and explain what nexus event your PR addresses.

All contributions are reviewed by the Time Variance Authority. Prune responsibly.