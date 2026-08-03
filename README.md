Here is the complete updated README, including the original content (exactly as provided) and the new "Contributing" section with TVA-themed language.

---

```markdown
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

## 🌌 Contributing – TVA Edition

Welcome, Time-Keeper Candidate! You’ve been selected to help us maintain the **Sacred Timeline** of TunnelX.  
Every pull request is a nexus event that can either strengthen or prune the codebase. Please follow these temporal protocols:

### ⏳ Before You Start
- **File a Variant Report** – Open an issue describing the bug or feature you want to tackle. This prevents paradoxes.
- **Check the Timeline** – Look at existing PRs and issues so you don’t accidentally create a branching reality.

### 🕰️ How to Submit a Pull Request
1. **Fork the Repository** – Create your own timeline branch (a fork of the Sacred Timeline).
2. **Create a Feature Branch** – Use a descriptive name like `fix/connection-reset` or `feat/quantum-dashboard`.
3. **Make Your Changes** – Follow the existing code style (use the Temporal Codex – linting rules).
4. **Write Temporal Tests** – Every new feature must have a unit test that passes across all parallel universes.
5. **Commit with Purpose** – Use clear commit messages. Example:  
   `feat: add auto-reconnect decay factor to prevent timeline fragmentation`
6. **Open a Pull Request** – Label it with the appropriate TVA tag:
   - `⚡ Nexus Event` – Major feature
   - `🔧 Prune Request` – Bug fix
   - `📜 Sacred Scroll` – Documentation update
7. **Wait for the Time-Keepers** – Our core maintainers (He Who Remains) will review your PR. We may ask for adjustments to keep the timeline stable.

### 🚫 What Gets Pruned
- Spam or duplicate PRs
- Changes that break the multiversal API contract
- Code that introduces latency anomalies (we track these with the TVA’s TemPad monitors)

### 🌟 Recognition
Every accepted contribution earns you a place in the **Hall of Variants** (our CONTRIBUTORS.md file). Top contributors may be granted a **Time Stone** (read: a sticker pack and eternal gratitude).

*Remember: For all time. Always.*  
– The TVA Temporal Engineering Department
```