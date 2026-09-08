# docker-compose.yml — Especificação

## Serviços
### frontend
- Build: `Dockerfile` (node:20-alpine → npm ci → astro build → serve com
  `npx serve dist` OU nginx:alpine servindo `dist/`)
- Porta INTERNA 3000; exposta só pro proxy (não publicar 3000:3000)

### backend
- Build: `Dockerfile` (python:3.12-slim → pip install -r requirements.txt
  → uvicorn)
- Volume `db_data:/app/data` (SQLite) + `uploads:/app/uploads`
- Env via `.env` (SECRET_KEY, ADMIN_USER, ADMIN_PASSWORD, ORIGINS)
- Healthcheck: `curl -f http://localhost:8000/api/health`
- `restart: unless-stopped`

## Rede
Rede interna `portfolio_net`; proxy (existente na VPS) aponta pro
container do frontend/backend por nome de serviço.
