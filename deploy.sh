#!/usr/bin/env bash
# Deploy do backend do portfólio na VPS (Dokploy/Traefik).
# Uso: ./deploy.sh          -> pull + rebuild + restart
#      ./deploy.sh logs     -> tail dos logs do container
#      ./deploy.sh backup   -> backup do SQLite antes de atualizar
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER=portfolio-backend
IMAGE=portfolio-backend:latest
NETWORK=dokploy-network
DOMAIN="${PORTFOLIO_API_DOMAIN:-portfolio-api.2-25-98-165.sslip.io}"

cd "$REPO_DIR"

if [ "${1:-}" = "logs" ]; then
  docker logs -f "$CONTAINER"
  exit 0
fi

if [ "${1:-}" = "backup" ]; then
  ts=$(date +%Y%m%d-%H%M%S)
  mkdir -p backups
  docker run --rm -v portfolio_data:/data -v "$REPO_DIR/backups:/backup" alpine \
    sh -c "cp /data/portfolio.db /backup/portfolio-$ts.db"
  echo "Backup salvo em backups/portfolio-$ts.db"
  exit 0
fi

echo "==> git pull"
git pull origin master

echo "==> docker build"
docker build -t "$IMAGE" -f backend/Dockerfile backend

echo "==> parar container antigo (se existir)"
docker rm -f "$CONTAINER" 2>/dev/null || true

echo "==> subir novo container"
docker run -d \
  --name "$CONTAINER" \
  --network "$NETWORK" \
  --env-file backend/.env \
  -v portfolio_data:/app/data \
  -v portfolio_uploads:/app/uploads \
  --restart unless-stopped \
  --label traefik.enable=true \
  --label "traefik.http.routers.portfolio-api.rule=Host(\`$DOMAIN\`)" \
  --label traefik.http.routers.portfolio-api.entrypoints=websecure \
  --label traefik.http.routers.portfolio-api.tls.certresolver=letsencrypt \
  --label traefik.http.services.portfolio-api.loadbalancer.server.port=8000 \
  "$IMAGE"

echo "==> healthcheck"
ok=false
for i in $(seq 1 30); do
  if docker exec "$CONTAINER" python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" 2>/dev/null; then
    ok=true
    break
  fi
  sleep 2
done

if [ "$ok" = true ]; then
  echo "==> OK: backend no ar em https://$DOMAIN"
else
  echo "==> FALHOU healthcheck, veja os logs: docker logs $CONTAINER"
  exit 1
fi
