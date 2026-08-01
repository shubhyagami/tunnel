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
   git checkout -b fix/your-timeline-patch
   ```
2. **Make your changes** – ensure you run `npm test` to verify the timeline remains stable.
3. **Write a clear commit message** that explains the nexus event you’re fixing.
4. **Open a pull request** – one of our Minutemen will review it. Expect a response within 42 time units (days, unless you’re in the Void).
5. **Celebrate** – once merged, your contribution will be immortalized in the Sacred Chronicle (CHANGELOG.md).

### ⏳ Need Help?
If you find yourself in a branching paradox or encounter a temporal paradox, open an issue with the label `timeline-disruption`. One of our analysts (who definitely aren’t variants) will assist.

### 📚 Resources
- [TVA Handbook for New Recruits](https://github.com/shubhyagami/tunnel/wiki)
- [Node.js API Reference](https://nodejs.org/en/docs/) (the Ancient Texts)
- [Render.com Docs](https://render.com/docs) (the TemPad manual)

**Remember:** All glory to the TVA. And to TunnelX.