# Etapa 6 — Backend FastAPI

## Especificação completa: ver `docs/backend/` (models, endpoints, auth, seed)
## Testes
- [ ] `uvicorn app.main:app --reload` sobe; `/docs` (Swagger) abre
- [ ] GET /api/projects lista seed; filtros ?category= funcionam
- [ ] POST /api/projects sem token → 401
- [ ] POST com token JWT válido → 201, projeto aparece no GET
- [ ] `pytest` passa (testes de auth + CRUD mínimos)

## Commit sugerido
`feat(api): FastAPI com CRUD de projetos, auth JWT e seed`
