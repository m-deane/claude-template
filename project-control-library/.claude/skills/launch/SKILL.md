---
name: launch
description: Start backend and frontend services on unused ports without disrupting other projects. Maintains a port registry, scans for occupied ports, and provides a status dashboard of all running services across all managed projects.
---

# Launch — Safe Service Startup Manager

## Overview

Launch backend and frontend services, documentation sites, dashboards, and artifacts on unused ports. Never kills processes from other projects on pre-existing ports. Maintains a central port registry and provides a unified status dashboard.

---

# Process

## Phase 1: Port Discovery

### 1.1 Scan Current Port Usage

Before launching anything, identify all occupied ports:

```bash
# Find all listening TCP ports and their processes
ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null

# Alternative: check specific port range
for port in $(seq 3000 4000); do
  (echo >/dev/tcp/localhost/$port) 2>/dev/null && echo "Port $port: IN USE"
done
```

### 1.2 Read Port Registry

Load the central port registry from `project-control-library/config.json`:

```json
{
  "port_registry": {
    "3000": { "project": "digital-filofax", "service": "dev-server", "pid": 12345, "started": "2026-03-03T10:00:00Z" },
    "3001": { "project": "api-gateway", "service": "dev-server", "pid": 12346, "started": "2026-03-03T10:05:00Z" },
    "6006": { "project": "ml-dashboard", "service": "storybook", "pid": 12347, "started": "2026-03-03T09:30:00Z" }
  }
}
```

### 1.3 Find Available Port

Select the next available port using this priority:

1. **Project's preferred port** — if defined in project CLAUDE.md and currently free
2. **Sequential from 3000** — first available in 3000-3999 range for dev servers
3. **Sequential from 4000** — first available in 4000-4999 range for doc sites
4. **Sequential from 5000** — first available in 5000-5999 range for dashboards
5. **Sequential from 8000** — first available in 8000-8999 range for API backends

**Port range conventions:**
| Range | Purpose |
|-------|---------|
| 3000-3999 | Development servers (Next.js, React, etc.) |
| 4000-4999 | Documentation sites (Docusaurus, Storybook) |
| 5000-5999 | Dashboards and monitoring UIs |
| 8000-8999 | Backend API servers |
| 9000-9999 | Database tools (Prisma Studio, pgAdmin) |

---

## Phase 2: Service Launch

### 2.1 Identify What to Launch

Read the target project's CLAUDE.md and package.json to determine available services:

```bash
# Check available npm scripts
cat ~/projects/{target}/package.json | python3 -c "
import json, sys
pkg = json.load(sys.stdin)
scripts = pkg.get('scripts', {})
for name, cmd in scripts.items():
    print(f'  {name}: {cmd}')
"
```

### 2.2 Launch Service on Safe Port

For each service to launch:

```bash
# Set the port via environment variable
# NEVER use kill/pkill on a port you don't own
PORT={available_port} npm run dev --prefix ~/projects/{target}
```

### 2.3 Service Types and Launch Commands

| Service Type | Typical Command | Port Env Var |
|-------------|-----------------|--------------|
| Next.js dev | `npm run dev` | `PORT` |
| React dev | `npm start` | `PORT` |
| Docusaurus | `npm run start` | `PORT` |
| Storybook | `npm run storybook` | `STORYBOOK_PORT` |
| Prisma Studio | `npx prisma studio` | `BROWSER_PORT` |
| Python Flask | `python app.py` | `FLASK_PORT` |
| Python FastAPI | `uvicorn main:app` | `--port` flag |
| Custom Express | `node server.js` | `PORT` |
| Documentation | `npx serve docs/` | `--listen` flag |

### 2.4 Register in Port Registry

After successful launch, update `config.json`:

```json
{
  "port_registry": {
    "{port}": {
      "project": "{project-name}",
      "service": "{service-type}",
      "pid": "{process-id}",
      "started": "{ISO-timestamp}",
      "command": "{launch-command}",
      "url": "http://localhost:{port}"
    }
  }
}
```

---

## Phase 3: Verification

### 3.1 Health Check

After launching, verify the service is responding:

```bash
# Wait for service to be ready (max 30 seconds)
for i in $(seq 1 30); do
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:{port} | grep -q "200\|304"; then
    echo "Service ready on port {port}"
    break
  fi
  sleep 1
done
```

### 3.2 Report Launch Status

```markdown
## Launch Report

### Service: {project-name} — {service-type}
- **URL**: http://localhost:{port}
- **PID**: {pid}
- **Status**: Running
- **Port**: {port} (was available, now registered)

### All Running Services
| Project | Service | Port | URL | PID | Uptime |
|---------|---------|------|-----|-----|--------|
| digital-filofax | dev-server | 3000 | http://localhost:3000 | 12345 | 2h 15m |
| api-gateway | dev-server | 3001 | http://localhost:3001 | 12346 | 2h 10m |
| {new-project} | {service} | {port} | http://localhost:{port} | {pid} | just started |
```

---

## Safety Rules (MANDATORY)

1. **NEVER run `kill`, `pkill`, or `killall` on PIDs you didn't create** in this session
2. **NEVER use `lsof -ti :{port} | xargs kill`** on ports owned by other projects
3. **ALWAYS check port registry** before assuming a port is available
4. **ALWAYS scan with `ss` or `netstat`** before launching — registry may be stale
5. **ALWAYS register** newly launched services in the port registry
6. **ALWAYS verify** the service is responding after launch
7. **If a project's preferred port is taken**, use the next available port — NEVER kill the occupant
8. **If launching fails**, report the error — don't retry on a different port without user confirmation

---

## Cleanup

### Stopping Your Own Services

To stop a service you launched in this session:

```bash
# Only kill a PID you registered in this session
kill {pid}

# Remove from port registry
# Update config.json to remove the entry
```

### Stale Registry Cleanup

To clean up stale entries (process no longer running):

```bash
# Check if registered PIDs are still alive
for entry in port_registry:
  if not kill -0 {pid} 2>/dev/null:
    remove entry from registry
```
