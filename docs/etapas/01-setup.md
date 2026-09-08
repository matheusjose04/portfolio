# Etapa 1 — Setup do Projeto

## Objetivo de aceite
`npm run dev` sobe sem erros; trocar `data-theme` no DevTools muda todas as
cores instantaneamente; reload não pisca tema errado.

## Passos exatos
1. `npm create astro@latest frontend -- --template minimal --typescript strict`
2. `cd frontend && npx astro add tailwind` (aceitar integração @tailwindcss/vite)
3. Criar `src/styles/global.css` MANTENDO `@import "tailwindcss";` na linha 1
   e colando os tokens do UI_SPECS.md abaixo
4. Criar `src/layouts/Base.astro` com script anti-flash inline no `<head>`
5. Criar `src/pages/index.astro` de placeholder ("hello, world" mono)
6. `git init` na RAIZ (portfolio/), com .gitignore:
   `node_modules/`, `venv/`, `__pycache__/`, `*.db`, `.env`, `dist/`

## Testes que DEVEM passar antes de commitar
- [ ] `npm run build` sem erros de TS
- [ ] DevTools > Application > localStorage: setar `theme=light`, reload →
      página abre clara sem piscar escuro
- [ ] `document.documentElement.dataset.theme` muda ao clicar no toggle

## Erros comuns nesta etapa (registrar no APRENDIZADO.md se ocorrerem)
- npm install falhando por rede → `npm install --fetch-timeout=600000`
- Tailwind v4 sem `@tailwindcss/vite` no astro.config → cores do shadcn
  aparecem, as do projeto não
