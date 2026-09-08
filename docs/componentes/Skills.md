# Skills — Especificação (grid + modal)

## Grid
- Tabs de categoria: LANGUAGES | DATABASES | FRAMEWORKS | OTHER TOOLS
  (estilo terminal: tab ativa com fundo `--surface` e borda `--primary`)
- Grid: `repeat(auto-fit, minmax(160px, 1fr))`, gap 1rem
- Card: ícone (devicon), nome, mini-barra de nível, `cursor: pointer`
- Hover: `translateY(-4px)` + `box-shadow: var(--glow)` + borda `--primary`

## Modal (aberto no clique do card)
Conteúdo:
1. Ícone grande (48px) + nome
2. Barra de nível animada (0→width% em 600ms, cor `--primary`)
3. Nível em texto: "Nível: avançado" (i18n)
4. `summary` — o que é a tecnologia (i18n)
5. `experience` — onde/como uso, tempo (i18n)
6. Link "Ver projetos com esta skill →" (filtra e rola até #projetos)

## Acessibilidade
- `role="dialog" aria-modal="true"`, foco inicial no botão fechar
- ESC e click no overlay fecham; foco retorna pro card que abriu
- Scroll do body travado enquanto aberto

## Dados: ver `docs/dados/skills-data.md`
