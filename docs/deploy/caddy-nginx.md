# Reverse Proxy na VPS — Especificação

## Opção A: VPS já usa Caddy
Adicionar AO Caddyfile existente (nunca substituir):
```
portfolio.seudominio.com {
    reverse_proxy portfolio-frontend:3000
}
api.portfolio.seudominio.com {
    reverse_proxy portfolio-backend:8000
}
```
HTTPS automático. Conectar container Caddy à `portfolio_net`
(`docker network connect portfolio_net <container_caddy>`).

## Opção B: VPS usa Nginx
Server block novo em `sites-available/portfolio` (symlink em sites-enabled),
proxy_pass para `http://127.0.0.1:PORTA_HOST` (mapear portas nos compose
só pra localhost: `127.0.0.1:3001:3000`). Certbot: `certbot --nginx -d ...`.

## Regra de segurança
ANTES de alterar qualquer proxy existente: `cp Caddyfile Caddyfile.bak`
(ou backup do nginx.conf) e testar config (`caddy validate` /
`nginx -t`). Se falhar, restaurar backup.
