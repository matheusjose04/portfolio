# Schema de Projeto — Contrato Frontend ↔ API

## ProjectOut (o que a API devolve e o frontend consome)
```json
{
  "id": 1,
  "title": "API de Autenticação",
  "slug": "api-autenticacao",
  "description": "...",          // JÁ RESOLVIDO por idioma? NÃO — ver abaixo
  "why": "...",
  "category": "complete",
  "skills": ["python", "fastapi", "postgresql"],
  "github_url": "https://github.com/...",
  "demo_url": null,
  "image_url": "/uploads/api-auth.png",
  "featured": true,
  "created_at": "2026-09-01T12:00:00Z"
}
```

## Decisão de i18n na API (IMPORTANTE)
A API guarda `description_pt` E `description_en`. A decisão:
- Frontend envia header `Accept-Language: pt|en` (ou query `?lang=`)
- API devolve `description` e `why` já no idioma pedido
- Fallback: se EN vazio, devolve PT

## Validações (Pydantic)
- URLs começam com http(s)://
- category ∈ {complete, small}
- skills ⊆ ids válidos do skills.ts
