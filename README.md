[K[2m  [2mmodel deepseek-ai/deepseek-v4.1-flash failed, trying next...[0m[0m
[K[2m  [2mmodel openai/gpt-oss-20b failed, trying next...[0m[0m
[K[2m  [2mmodel openai/gpt-oss-120b failed, trying next...[0m[0m
# tunnel

A lightweight, high-performance TCP tunnel that exposes local services behind a single public port.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Node.js ≥18](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![CI](https://github.com/shubhyagami/tunnel/actions/workflows/ci.yml/badge.svg)](https://github.com/shubhyagami/tunnel/actions)

> **TL;DR:** Expose any local TCP service to a public URL with a single command.

---

## Overview

`tunnel` multiplexes multiple TCP tunnels over a single listening port. Each tunnel is routed via a unique subdomain, allowing you to expose numerous local services without needing to open additional firewall ports. 

Traffic can be forwarded over plain TCP or secured via WebSockets (`wss://`) when TLS is enabled. To ensure security, a single pair of credentials can be used to protect all tunnels via Basic Authentication.

## Features

- **One-Port Multiplexing:** Host multiple services behind a single TCP socket.
- **Subdomain Routing:** Reach services at `subdomain.your-server.com:port`.
- **Zero-Agent Client:** No complex installation required on the host being exposed.
- **TLS Support:** Secure traffic with `wss://` using the `--tls` flag.
- **Basic Auth:** Global server-level protection via username/password.
- **Real-time Dashboard:** Monitor traffic, latency, and health at `http://localhost:4040`.
- **Connection Keep-alive:** Periodic ping frames to prevent timeouts on unstable networks.

---

## Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build
npm ci
npm run build
```

### 2. Quick Start (Local Development)

To test `tunnel` on your local machine:

**Start the server:**
```bash
npm start
```

**Expose a local service (in a new terminal):**
```bash
node dist/client.js --port 3000 --subdomain my-app
```
The client will provide a public URL, e.g., `http://my-app.localhost:8080`.

---

## Deployment & Usage

### Running the Server
Deploy the server on any VPS or host with public TCP access.

```bash
npm start -- --port 8080 --tls --auth admin:password123
```

**Server Flags:**
| Flag | Description | Default |
| :--- | :--- | :--- |
| `--port` | TCP port to listen on | `8080` |
| `--tls` | Generate a self-signed cert and serve HTTPS | `false` |
| `--host` | Bind to a specific IP or hostname | `0.0.0.0` |
| `--auth` | Basic auth credentials (`user:pass`) | none |

### Running the Client
Connect your local service to the remote server:

```bash
node dist/client.js \
  --host tunnel.example.com \
  --port 3000 \
  --subdomain dev-myapp \
  --keepalive \
  --auth admin:password123
```

**Client Flags:**
| Flag | Description |
| :--- | :--- |
| `--host` | The hostname of your `tunnel` server |
| `--port` | The local TCP port you want to expose |
| `--subdomain` | The unique identifier for your tunnel |
| `--keepalive` | Send periodic pings to keep the connection open |
| `--auth` | Credentials required if the server has `--auth` enabled |

---

## Dashboard

Once the server is running, visit `http://localhost:4040` to access the monitoring dashboard. It provides live updates via Server-Sent Events (SSE) for:
- Active tunnels and their traffic volume.
- Real-time latency charts.
- Connection health status.

---

## FAQ

**How do I avoid subdomain collisions?**
Use a consistent naming convention, such as prefixing subdomains with your username or project name (e.g., `user1-api`, `user1-web`).

**Is TLS required?**
No. However, using `--tls` on the server is highly recommended for production to encrypt data in transit.

**Can I tunnel non-HTTP services?**
Yes. `tunnel` forwards raw TCP traffic, making it compatible with SSH, databases, or any other TCP-based protocol.

**Why are my connections dropping?**
This is often due to aggressive timeouts on cloud firewalls or routers. Use the `--keepalive` flag on the client to mitigate this.

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repo and create a feature branch (`feat/...` or `fix/...`).
2. Ensure any new functionality is covered by tests.
3. Run `npm test` to verify the build.
4. Submit a PR with a clear description of the changes.

---

## Changelog

**2026-09-25**
- Refined README structure and documentation.
- Fixed minor typos in client documentation.

**2026-09-22**
- Improved client keep-alive logic.
- Enhanced dashboard latency visualization.

**2026-08-26**
- Added millisecond precision to disruption logs.
- Fixed race condition in connection reporting.

---

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.
