# APRENDIZADO.md — Diário de bordo do projeto (modo ensino)

## Etapa 1 — Setup do Projeto

**O que foi feito:**
Criamos o esqueleto do frontend com Astro (template `minimal`, TypeScript
em modo `strict`) e adicionamos o Tailwind CSS v4. Definimos os tokens de
cor do tema dark (padrão) e light como variáveis CSS, escolhemos as fontes
(JetBrains Mono para títulos/terminal, Inter para texto corrido) e criamos
o layout base com o script "anti-flash" que evita a página piscar no tema
errado ao recarregar. Por fim, iniciamos o repositório Git na raiz do
projeto.

**Arquivos criados/alterados:**
- `frontend/` — projeto Astro completo (gerado por `npm create astro@latest`)
- `frontend/astro.config.mjs` — registra o plugin `@tailwindcss/vite`
- `frontend/src/styles/global.css` — importa o Tailwind + fontes e define
  os tokens de cor (`--color-bg`, `--color-primary`, etc.) para dark e
  `[data-theme="light"]`
- `frontend/src/layouts/Base.astro` — layout HTML compartilhado por todas
  as páginas; contém o `<script>` anti-flash no `<head>`
- `frontend/src/pages/index.astro` — página inicial, agora um placeholder
  usando o `Base.astro`
- `.gitignore` (raiz) — ignora `node_modules/`, `venv/`, `__pycache__/`,
  `*.db`, `.env`, `dist/`
- `.git/` (raiz) — repositório Git inicializado

**Conceitos explicados:**
- **CSS custom properties (`--minha-variavel`)**: são "variáveis" dentro do
  CSS. Em vez de escrever `#38bdf8` em 20 lugares diferentes, escrevemos
  uma vez em `--color-primary` e usamos `var(--color-primary)` onde
  precisar. Trocar o tema vira só trocar o valor dessas variáveis.
- **`data-theme` no `<html>`**: é um atributo customizado
  (`<html data-theme="dark">`). O CSS lê esse atributo pra decidir quais
  valores de cor usar (`[data-theme="light"] { ... }` sobrescreve as
  variáveis do `:root`). É mais simples que ter duas folhas de estilo
  inteiras.
- **Script anti-flash**: sem ele, o navegador primeiro pinta a página com
  o tema padrão (dark) e só DEPOIS o JavaScript normal troca pro tema
  salvo (light) — isso causa um "flash" visível. A solução é colocar um
  `<script>` **inline** (sem arquivo externo) bem no início do `<head>`,
  que roda ANTES do navegador desenhar a página, lê o `localStorage` e já
  seta o `data-theme` correto antes de qualquer pixel aparecer.
- **`@layer` do Tailwind v4**: o Tailwind organiza seu CSS em "camadas"
  (`theme`, `base`, `components`, `utilities`) com prioridade controlada.
  Nossos tokens, por estarem FORA de qualquer `@layer`, sempre vencem os
  valores padrão do Tailwind — por isso não precisamos usar `!important`.
- **Astro layout + `<slot />`**: `Base.astro` é um "molde" de página. O
  `<slot />` é o buraco onde o conteúdo de cada página específica (ex:
  `index.astro`) é encaixado.

**Código-chave comentado (`Base.astro`, script anti-flash):**
```html
<script is:inline>
  // is:inline diz ao Astro "não processe, não mova este script — deixe
  // exatamente aqui", porque a ORDEM importa: precisa rodar antes do CSS.
  const stored = localStorage.getItem("theme"); // "dark" | "light" | null
  const theme = stored === "light" || stored === "dark"
    ? stored          // usuário já escolheu antes → respeita
    : "dark";         // primeira visita → padrão do site é dark
  document.documentElement.dataset.theme = theme;
  // dataset.theme = "dark" equivale a <html data-theme="dark">
</script>
```

**Como testar:**
1. `cd frontend && npx astro dev --background` (sobe em `http://localhost:4321`)
2. Abrir no navegador — deve aparecer `matheus@fullstack:~$ hello, world`
   em fonte mono, com fundo escuro
3. Abrir DevTools → Application → Local Storage → adicionar `theme=light`
   → recarregar a página → deve continuar sem piscar (mesmo que o CSS de
   light ainda não esteja aplicado a nenhum componente visível além do
   `<html>`/`<body>`, o atributo `data-theme="light"` já deve estar
   presente desde o primeiro frame — confirmar em Elements)
4. `npm run build` deve terminar sem erros de TypeScript
5. `npx astro dev stop` pra parar o servidor em background

**Desafio opcional:**
Troque manualmente `theme=light` no `localStorage` pelo DevTools, dê
reload, e inspecione o `<html>` no painel Elements. Depois tente mudar o
valor de `--color-primary` em `global.css` pra outra cor e veja o texto do
placeholder mudar — isso mostra o poder de centralizar cores em variáveis.

**Decisões tomadas:**
- Os docs-mestre citados pelo `MASTER_PROMPT.md`
  (`docs/ARCHITECTURE.md`, `docs/UI_SPECS.md`, `docs/FEATURES.md`) e o
  `docs/DEPLOY_VPS.md` **não existem** neste pacote. Como
  `docs/estilo/tokens.md` já se declara "cópia normativa do UI_SPECS.md",
  decidimos usar os specs granulares (`docs/etapas/`, `docs/componentes/`,
  `docs/backend/`, `docs/dados/`, `docs/estilo/`, `docs/deploy/`) como
  fonte de verdade para todo o projeto.
- `docs/estilo/tokens.md` só define cores para dark e light, sem
  detalhar `--accent`, `--success`, `--danger` e `--text-dim` no tema
  light. Decisão: manter tons semânticos equivalentes ao dark (verde/
  vermelho legíveis em fundo claro) e usar o próprio `--color-primary`
  como accent no light, já que a spec diz "sem glow" (menos elementos
  decorativos precisam de uma cor de destaque separada).
- Fontes: em vez de carregar do Google Fonts (requisição externa),
  usamos os pacotes `@fontsource/jetbrains-mono` e `@fontsource/inter`
  (self-hosted) — melhora performance/Lighthouse (etapa 10) e evita
  dependência de rede em produção.
- A seção "Projetos" do `CONTENT.md` está vazia. Isso só afeta a Etapa 6
  (seed do backend) — vamos usar 4 projetos placeholder marcados como
  TODO nessa etapa, não nesta.
