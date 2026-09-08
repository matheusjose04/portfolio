# ProjectModal — Especificação

## Conteúdo (tudo via API, do modelo Project)
1. Imagem grande (se houver)
2. Título + categoria (`#complete-app`)
3. **Descrição** (`description_pt` conforme idioma ativo)
4. **Por que fiz** (campo `why_pt/why_en` — destaque em bloco com borda esquerda `--primary`)
5. **Skills usadas** — badges clicáveis → rolam até #skills e destacam a skill
6. **Links**: [GitHub] (se `github_url`) e [Demo ↗] (se `demo_url`, `target=_blank`)
   - Se demo não existe: botão desabilitado com tooltip "sem demo pública"

## Comportamento
- Mesma infra de modal do SkillModal (ESC, overlay, foco, scroll lock)
- URL opcional: `#projeto/<slug>` pra link direto (nice-to-have)
