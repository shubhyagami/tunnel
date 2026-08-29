# Tunnel  

[![Node.js Version](https://img.shields.io/badge/node-%3E%3D16-brightgreen.svg)](https://nodejs.org)  
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  
[![Build Status](https://img.shields.io/github/actions/workflow/status/shubhyagami/tunnel/.github/workflows/ci.yml?branch=main&label=Build)](https://github.com/shubhyagami/tunnel/actions)  
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/shubhyagami/tunnel/pulls)  

A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services (React dev servers, Python HTTP servers, Express apps, etc.) to the public internet through a single port. Ideal for development and Render.com deployments.

---  

## Features  

- Multiplexed proxy with Nagle’s algorithm disabled for ultra‑low latency.  
- Dashboard UI – real‑time traffic monitoring and latency visualization.  
- Basic Auth protection – simple authentication for securing services.  
- Resilient auto‑reconnection with exponential back‑off and precise disruption logs.  

---  

## Getting Started  

### Prerequisites  

- **Node.js** ≥ 16  
- A local server you want to expose (e.g., React dev server, Python HTTP server, Express app)  

### Installation & Build  

```bash
npm install      # Install dependencies
npm run build    # Build the project
```  

### Run the tunnel server  

```bash
npm start        # Starts the server on port 8080 by default
```  

### Expose a local service  

1. Start your local server (example with Python):  

   ```bash
   python -m http.server 3000
   ```  

2. Launch the tunnel client to expose port 3000 under a subdomain:  

   ```bash
   node src/client.js --port 3000 --subdomain my-app
   ```  

Your service is now reachable at `http://my-app.localhost:8080`.  

### Dashboard  

Live traffic and latency can be viewed at `http://localhost:4040`.

---  

## Running in Production (Render.com)  

1. Create a Render.com Blueprint and link this repository.  
2. Add a new Blueprint; Render automatically reads `render.yaml`, builds the server, and deploys it.  
3. Obtain the generated public URL (e.g., `wss://tunnel.example.com`).  
4. Point the client to the production server:  

   ```bash
   node src/client.js --host tunnel.example.com --port 3000 --subdomain my-app
   ```  

---  

## Pro Tips  

- Use a dedicated subdomain for each environment (staging vs. production) to avoid conflicts.  
- Enable Basic Auth for any service that must remain private, even when behind the tunnel.  
- Monitor the dashboard during initial connections to spot latency spikes and adjust configurations.  
- If you experience frequent disconnects, add a keep‑alive ping (e.g., `--keepalive`) to maintain the connection.  

---  

## Contributing  

Contributions are welcome. To fix a bug or add a feature:

1. Open an issue describing the problem or desired functionality.  
2. Fork the repository and create a branch (`fix/reconnect-bug`, `feat/new-auth`, etc.).  
3. Write clean, readable code and include tests when applicable.  
4. Reference the issue in your pull‑request description.  

Please keep changes focused and discuss larger modifications with the maintainers before opening a PR.

---  

## Changelog  

### 2026‑08‑26  

- Added precise millisecond timestamps for disruption logs.  
- Rendered dashboard latency as a real‑time graph.  
- Fixed a race condition that could cause premature connection reports, reducing failure rate under high load.  
- Updated documentation with additional Pro Tips.  

---  

*Maintained by the tunnel team.*
