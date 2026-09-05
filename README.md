# tunnel

A lightweight, high‑performance HTTP/WebSocket tunnel that exposes local services to the public Internet over a single TCP port.

---

## 📦 Quick Start

```bash
# Clone the repository
git clone https://github.com/shubhyagami/tunnel.git
cd tunnel

# Install dependencies and build
npm ci
npm run build

# Start the server (default on port 8080)
npm start

# In another terminal, expose a local service
node dist/client.js --port 3000 --subdomain my-app
```

You’ll receive a public URL, e.g.:

```
http://my-app.localhost:8080
```

Open that address in a browser or use it in your client code. The real‑time dashboard is available at `http://localhost:4040`.



## 🌍 Overview

`tunnel` forwards traffic from one globally reachable TCP port to one or more local services, optionally over WebSocket. It works with:

- Any HTTP server
- Any TCP‑based service (SSH, Redis, custom protocols, etc.)

**Key features**

- **Single‑port multiplexing** – many tunnels share one listening port.
- **Low latency** – Nagle’s algorithm disabled; keep‑alive configurable.
- **Real‑time metrics** – dashboard on `localhost:4040`.
- **Basic authentication** – secure tunnels with `user:pass`.
- **Automatic reconnection** – exponential back‑off and detailed logs.

---

## ⚙️ Prerequisites

- **Node.js ≥ 18**
- A publicly reachable TCP port (default `8080`)



## 🚀 Server

Run the server with `npm start`.  
Optional flags (append after `--`):

| Flag      | Description                                     | Default |
|----------|--------------------------------------------------|--------|
| `--port` | TCP port the server listens on                    | `8080` |
| `--tls`  | Generate a self‑signed TLS cert and use HTTPS  | `false`|
| `--host` | Bind to a specific hostname or IP               | `0.0.0.0`|
| `--auth` | Basic Auth credentials (`user:pass`) for all tunnels | none |

**Example**

```bash
npm start -- --port 9090 --tls
```

The server logs the public URL for each tunnel as it is established.



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

| Flag        | Description                                      | Required |
|------------|--------------------------------------------------|----------|
| `--host`   | Tunnel server hostname or IP                    | defaults to `localhost` |
| `--port`   | Local port to expose                            | **yes** |
| `--subdomain` | Desired subdomain for the tunnel              | **yes** |
| `--keepalive` | Send periodic ping frames to keep the connection alive | no |
| `--auth`   | Basic Auth credentials (`user:pass`)          | no |

The client prints the public URL once the tunnel is ready.



## 📊 Dashboard

While the server is running, visit:

```
http://localhost:4040
```

You’ll see:

- Traffic counters
- Latency charts
- Connection health indicators

The dashboard updates automatically in real time.



## 🌐 Deployment

`tunnel` can run on any host that accepts inbound TCP connections.  
Below is a quick example for Render, but the same steps apply to other providers (Heroku, DigitalOcean, etc.).

### Render.com

1. Create a new Render service that pulls from this repo.  
2. Render will detect `render.yaml`, build, and deploy automatically.  
3. Note the public host, e.g. `wss://tunnel.example.com`.  
4. Run the client:

```bash
node dist/client.js --host tunnel.example.com --port 3000 --subdomain my-app
```



## ❓ FAQ

| Question | Answer |
|----------|--------|
| How do I avoid sub‑domain collisions? | Use environment‑specific names, e.g. `dev-myapp`, `staging-myapp`. |
| Do I need TLS? | TLS is optional. Use `--tls` on the server and `wss://` on the client. |
| Can I tunnel non‑HTTP services? | Yes. Any TCP service will work; the tunnel simply forwards traffic. |
| Why does the connection drop? | Network instability may cause brief drops. Enable `--keepalive` to mitigate. |
| How many concurrent tunnels are allowed? | Unlimited (subject to system limits). Each uses its own sub‑domain. |



## 🤝 Contributing

Pull requests are welcome! Please follow these steps:

1. Fork the repo and create a feature branch (e.g. `feat/...` or `fix/...`).  
2. Add tests if applicable and run `npm test`.  
3. Submit a PR that references any related issue.  
4. Keep commits small, focused, and descriptive.



## 📅 Changelog (excerpt)

**2026‑08‑26**

- Added millisecond timestamps to disruption logs.  
- Introduced latency graphs on the dashboard.  
- Fixed race condition causing premature connection reports.  
- Updated documentation with new usage tips.



## 📜 License

[MIT](LICENSE) © tunnel team



--- 

![License](https://img.shields.io/badge/License-MIT-blue.svg)
