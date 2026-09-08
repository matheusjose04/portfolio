# Etapa 11 — Deploy na VPS

## Especificação completa: ver `docs/deploy/`
## ANTES: fazer as 5 perguntas do DEPLOY_VPS.md ao usuário
## Testes
- [ ] `docker compose up -d` sobe tudo na VPS
- [ ] HTTPS ativo (Caddy) no domínio informado
- [ ] `deploy.sh` atualiza o site com 1 comando (git pull + rebuild)
- [ ] Projetos antigos da VPS intactos (docker ps antes/depois igual)
- [ ] Painel admin funciona em produção

## Commit sugerido
`deploy: docker-compose, caddy e script de deploy`
