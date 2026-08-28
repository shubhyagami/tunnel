# Tunnel  

[![Node.js Version](https://img.shields.io/badge/node-%3E%3D16-brightgreen.svg)](https://nodejs.org)  
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/shubhyagami/tunnel/.github/workflows/ci.yml?branch=main&label=Build)](https://github.com/shubhyagami/tunnel/actions)  
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/shubhyagami/tunnel/pulls)  

A lightweight, high‑performance HTTP/WebSocket tunneling solution for exposing local services (including React dev servers, Python HTTP servers, Express apps, etc.) to the public internet through a single port. Ideal for Render.com deployments and local development.

---

## Features  

- **Multiplexed proxy** with Nagle’s algorithm disabled for ultra‑low latency.  
- **Web UI dashboard** – real‑time traffic monitoring and latency visualization.  
- **Basic Auth protection** – simple authentication for securing local services.  
- **Resilient auto‑reconnection** – exponential back‑off with precise disruption logs.  

---

## Getting Started  

### Prerequisites  

- **Node.js** ≥ 16  
- A local web server you wish to expose (e.g., React dev server, Python HTTP server, Express app)  

### Setup  

1. **Install dependencies**  
   ```bash
   npm install
   ```  

2. **Build the project**  
   ```bash
   npm run build
   ```  

3. **Start the tunnel server** (runs on port 8080 by default)  
   ```bash
   npm start
   ```  

4. **Run your local server** – example with Python:  
   ```bash
   python -m http.server 3000
   ```  

5. **Connect the tunnel client** – expose port 3000 under the subdomain `my-app`  
   ```bash
   node src/client.js --port 3000 --subdomain my-app
   ```  

Your exposed site is now reachable at `http://my-app.localhost:8080`. Live traffic can be watched on the dashboard at `http://localhost:4040`.

---

## Running in Production (Render.com)  

1. **Create a Render.com Blueprint** – link this repository and add a new Blueprint.  
2. **Render auto‑deploys** – it reads `render.yaml`, builds the server, and launches it.  
3. **Obtain the public URL** – e.g., `wss://tunnel.example.com`.  
4. **Point the client to the production server**  
   ```bash
   node src/client.js --host tunnel.example.com --port 3000 --subdomain my-app
   ```  

---

## Pro Tips  

- **Dedicated subdomains per environment** – avoid sharing a subdomain between staging and production.  
- **Enable Basic Auth** for any service that must stay private, even when behind the tunnel.  
- **Watch the dashboard** during initial connections to spot latency spikes and adjust accordingly.  
- **Use `--keepalive`** (or a similar flag) to send regular pings if you experience frequent disconnects.  

---

## Contributing  

Contributions are welcome! To fix a bug or add a feature:

1. **Open an issue** describing the problem or desired functionality.  
2. **Fork the repo** and create a branch (e.g., `fix/reconnect-bug` or `feat/new-auth`).  
3. **Write clean, readable code** and include tests if applicable.  
4. **Reference the issue** in your pull‑request description.  

Please keep changes focused and discuss larger modifications with the maintainers before opening a PR.

---

## Changelog  

### 2026‑08‑26  

- Proactive connection detection now logs the exact millisecond of disruption for quicker debugging.  
- Dashboard latency visualization rendered as a real‑time graph.  
- Fixed a race condition that could cause the client to think it was connected before the server acknowledged the handshake (reduced failure rate from 0.3 % under high load).  
- Updated documentation with additional Pro Tips to help avoid common configuration pitfalls.  

---  

*Maintained by the tunnel team.*
