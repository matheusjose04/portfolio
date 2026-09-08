# deploy.sh — Especificação

## Uso (da sua máquina ou na VPS)
```bash
./deploy.sh          # pull + rebuild + restart
./deploy.sh logs     # tail dos logs
./deploy.sh backup   # backup do SQLite antes de atualizar
```

## Lógica
1. `git pull origin main`
2. `docker compose build` (frontend + backend)
3. `docker compose up -d`
4. `docker compose ps` + healthcheck da API (30 tentativas, 2s)
5. Se healthcheck falhar → `docker compose rollback` (imagem anterior)
   e exit 1

## Opcional: GitHub Actions
Workflow `deploy.yml` (on: push main): SSH na VPS → `./deploy.sh`.
Usa secrets: VPS_HOST, VPS_USER, VPS_SSH_KEY.
