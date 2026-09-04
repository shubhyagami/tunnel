# tunnel
A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single TCP port.

## 📦 Quick Start

```bash
# Clone the repo
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build
npm ci
npm run build

# Start the server (defaults to port 8080)
npm start

# In a new terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

You’ll see a public URL, e.g.:

```
http://my-app.localhost:8080
```

Open that address in a browser or use it in your client code.  
The dashboard is accessible at `http://localhost:4040`.

---

## 🌍 Overview
`tunnel` forwards traffic from a single, globally reachable TCP port to one or more local services, optionally over WebSocket. It works with:

- Any HTTP server  
- Any TCP‑based service (SSH, Redis, custom protocols, etc.)

Key characteristics:

- **Single‑port multiplexing** – multiple tunnels share one listening port.  
- **Low latency** – Nagle’s algorithm disabled; keep‑alive configurable.  
- **Real‑time dashboard** – live metrics on `localhost:4040`.  
- **Basic auth** – secure tunnels with `user:pass`.  
- **Automatic reconnection** – exponential back‑off and detailed logs.

---

## ⚙️ Installation & Prerequisites

- **Node.js ≥ 18**
- A publicly accessible TCP port (default 8080)

```bash
npm ci          # Install dependencies
npm run build   # Compile TypeScript
```

The compiled files live in `dist/`.

---

## 🚀 Server

Start the tunnel server with `npm start`.  
Optional flags:

| Flag | Description | Default |
|------|-------------|----------|
| `--port` | TCP port the server listens on | `8080` |
| `--tls` | Generate a self‑signed TLS cert and run against HTTPS | `false` |
| `--host` | Bind to a specific hostname or IP | `0.0.0.0` |
| `--auth` | Basic Auth credentials (`user:pass`) for all tunnels | none |

**Example**

```bash
npm start -- --port 9090 --tls
```

The server logs the public URL of each tunnel it receives.

---

## 🔌 Client

The client forwards a local TCP port to the tunnel server.

```bash
node dist/client.js \
  --port 3000 \
  --subdomain my-app \
  [--host tunnel.example.com] \
  [--keepalive] \
  [--auth user:pass]
```

| Flag | Description | Required |
|------|--------------|----------|
| `--host` | Tunnel server hostname or IP | defaults to `localhost` |
| `--port` | Local port to expose | **yes** |
| `--subdomain` | Desired subdomain for the tunnel | **yes** |
| `--keepalive` | Send periodic ping frames to keep the connection alive | no |
| `--auth` | Basic Auth for the tunnel (`user:pass`) | no |

The client prints the public URL once the tunnel is established.

---

## 📊 Dashboard

When the server is running, navigate to:

```
http://localhost:4040
```

You’ll see:

- Traffic counters
- Latency charts
- Connection health indicators

The dashboard is automatically updated in real‑time.

---

## 🌐 Deployment

`tunnel` can run on any host that accepts inbound TCP connections.

### Render.com (example)

1. Create a new Render service linked to this repo.  
2. Render will detect `render.yaml`, build, and deploy automatically.  
3. Note the public host, e.g. `wss://tunnel.example.com`.  
4. Run the client:

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```

The same steps work on other providers (Heroku, DigitalOcean, etc.).

---

## ❓ FAQ

| Question | Answer |
|----------|--------|
| **How do I avoid sub‑domain collisions?** | Use environment‑specific names, e.g., `dev-myapp`, `staging-myapp`. |
| **Do I need TLS?** | Optional. Use `--tls` on the server and `wss://` on the client. |
| **Can I tunnel non‑HTTP services?** | Yes. Any TCP service will work; the tunnel simply forwards traffic. |
| **Why does the connection drop?** | Network instability may cause brief drops. Enable `--keepalive` to mitigate. |
| **How many concurrent tunnels are allowed?** | Unlimited (subject to system limits). Each uses its own sub‑domain. |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo and create a feature branch (e.g. `feat/...` or `fix/...`).  
2. Add tests if appropriate and run `npm test`.  
3. Submit a PR referencing any related issue.  
4. Keep commits small, focused, and descriptive.

---

## 📅 Changelog

### 2026‑08‑26

- Added millisecond timestamps to disruption logs.  
- Introduced latency graphs on the dashboard.  
- Fixed race condition causing premature connection reports.  
- Updated documentation with new usage tips.

Older releases are listed in the **Releases** tab.

---

## 📜 License

MIT © tunnel team

---
