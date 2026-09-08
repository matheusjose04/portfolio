# Seed — Especificação

`python seed.py` deve:
1. Criar tabelas (se não existirem)
2. Criar admin com dados do CONTENT.md (default admin/admin123)
3. Inserir projetos do CONTENT.md (2 complete, 2 small)
4. Ser idempotente: rodar 2x não duplica (upsert por slug)

## Placeholders de exemplo (se CONTENT.md vazio)
- complete: "Sistema de Gestão X", "API de Autenticação Y"
- small: "CLI de Automação Z", "Bot de Discord W"
Imagens: SVG placeholders gerados em `frontend/public/images/projects/`.
