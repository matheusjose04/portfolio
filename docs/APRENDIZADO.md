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

## Etapa 2 — Navbar

**O que foi feito:**
Criamos a navbar (logo em estilo terminal, links âncora para as seções
futuras, toggle de tema e seletor PT/EN) e montamos toda a base de i18n
necessária pra ela funcionar: rotas `/` (PT) e `/en/` (EN) via i18n
nativo do Astro, arquivos `pt.json`/`en.json` e um helper `t()`
type-safe. O menu mobile vira tela cheia com um botão hambúrguer.

**Arquivos criados/alterados:**
- `frontend/astro.config.mjs` — adiciona `i18n` (locale padrão `pt` sem
  prefixo, `en` com prefixo `/en/`)
- `frontend/src/i18n/pt.json`, `en.json` — chaves de tradução (schema de
  `docs/dados/i18n-chaves.md`); só `nav.*` e `hero.cta.*` preenchidos por
  enquanto, o resto será preenchido pelas próximas etapas
- `frontend/src/i18n/utils.ts` — `getLangFromUrl()` e `useTranslations()`
  (lookup de chave tipo `"nav.about"` sem usar `any`)
- `frontend/src/components/ThemeToggle.astro` — botão sol/lua que troca
  `data-theme` e persiste no `localStorage`
- `frontend/src/components/Navbar.astro` — logo, links, seletor de
  idioma, `<ThemeToggle />` e botão hambúrguer com menu fullscreen mobile
- `frontend/src/layouts/Base.astro` — script anti-flash agora também
  respeita `prefers-color-scheme` quando não há tema salvo
- `frontend/src/styles/global.css` — `color-scheme` sincronizado com o
  tema e `scroll-behavior: smooth` (com fallback `auto` em
  `prefers-reduced-motion`)
- `frontend/src/pages/index.astro` — agora renderiza `<Navbar lang="pt" />`
- `frontend/src/pages/en/index.astro` — versão EN da home (mesma
  estrutura, `lang="en"`)

**Conceitos explicados:**
- **i18n com rotas por prefixo**: o Astro pode gerar `/` para o idioma
  padrão e `/en/` para os outros automaticamente, a partir de uma pasta
  `src/pages/en/`. É como ter duas "cópias" do site, uma por idioma —
  mas nós reaproveitamos os MESMOS componentes (`Navbar`, `Base`),
  só trocando qual idioma (`lang`) é passado como propriedade.
- **Helper de tradução `t("nav.about")`**: em vez de escrever o texto
  direto no componente (`<a>Sobre</a>`), escrevemos `t("nav.about")`.
  A função `t` vai no JSON do idioma atual, desce pelas chaves separadas
  por ponto (`nav` → `about`) e devolve o texto. Isso permite trocar
  idioma sem duplicar componentes.
- **Menu hambúrguer sem framework**: usamos classes Tailwind
  (`hidden md:flex` no menu, `md:hidden` no botão) pra esconder/mostrar
  conforme o tamanho de tela, e um `<script>` pequeno que só troca
  classes (`hidden`/`flex`) e o atributo `aria-expanded` — sem precisar
  de nenhuma biblioteca de UI.
- **`aria-expanded` e `aria-controls`**: são atributos de acessibilidade.
  `aria-expanded="true/false"` avisa leitores de tela se o menu está
  aberto; `aria-controls="primary-nav"` diz qual elemento aquele botão
  controla. Fechar o menu com a tecla `Esc` também é uma prática comum de
  acessibilidade pra modais/menus.

**Código-chave comentado (`src/i18n/utils.ts`, lookup de chave):**
```ts
function get(dict: Record<string, unknown>, path: string): string {
  let current: unknown = dict;
  for (const part of path.split(".")) {
    // se não for mais um objeto (ex: já virou string, ou não existe),
    // devolve a própria chave como fallback — fácil de notar no site
    // que uma tradução está faltando.
    if (typeof current !== "object" || current === null || Array.isArray(current)) {
      return path;
    }
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "string" ? current : path;
}
```

**Como testar:**
1. `cd frontend && npx astro dev --background`
2. Em `http://localhost:4321/`: navbar em PT, clicar no toggle de tema
   alterna claro/escuro instantaneamente
3. Clicar em "en" na navbar → vai para `/en/` com os links traduzidos
   (home/about/skills/projects/contact) e o tema permanece o mesmo
4. Recarregar a página com `theme=light` no localStorage → sem flash
5. Reduzir a largura da janela abaixo de 768px (DevTools → toggle
   device toolbar) → os links somem, aparece o ícone de hambúrguer;
   clicar nele abre um menu em tela cheia
6. `npx astro check` → 0 erros
7. `npx astro dev stop`

**Desafio opcional:**
Adicione uma chave nova em `pt.json`/`en.json` (ex: `"nav.blog": "blog"`
e a versão EN) e use `t("nav.blog")` num link temporário na navbar. Isso
mostra como qualquer texto novo do site sempre passa pelo mesmo caminho:
JSON → `t()` → componente.

**Decisões tomadas:**
- `docs/componentes/Navbar.md` também está ausente do pacote (só existe
  `docs/etapas/02-navbar.md`, que aponta pra ele). Usamos
  `docs/estilo/responsividade.md` (regra "hambúrguer/fullscreen no
  mobile, links inline no desktop") e os testes de aceite da própria
  etapa como especificação.
- `docs/componentes/ThemeToggle.md` exige que, sem tema salvo no
  `localStorage`, o site abra no tema do sistema operacional. Isso é
  mais específico que a frase geral do `MASTER_PROMPT.md` ("dark é o
  padrão") — interpretamos que dark continua sendo o padrão quando o SO
  não indica claramente "light" (ou seja, SO escuro ou sem preferência
  → dark; SO claro → light).
- Optamos por implementar a troca de idioma como duas páginas raiz
  (`/` e `/en/`) usando o roteamento i18n nativo do Astro, em vez de um
  JS que reescreve textos no cliente — mantém tudo estático/SSG e
  `<html lang>` sempre correto por página (exigência da Etapa 9).

## Etapa 3 — Hero com Terminal Animado

**O que foi feito:**
Construímos a seção principal (`TerminalHero`): um "terminal" com header
de 3 bolinhas que digita os comandos `whoami` e `ls ./skills` caractere a
caractere e mostra a resposta, em loop; ao lado, a foto (placeholder SVG,
já que o usuário ainda não colocou o arquivo real) com borda neon e os
3 botões (baixar CV, LinkedIn, GitHub) com os links reais do
`CONTENT.md`.

**Arquivos criados/alterados:**
- `frontend/src/components/TerminalHero.astro` — componente completo:
  markup do terminal + foto + CTAs, e o `<script>` que faz a digitação
- `frontend/src/i18n/pt.json`, `en.json` — `hero.terminal.lines`
  preenchido com dados reais (skills do `CONTENT.md`: python,
  typescript, javascript, fastapi, sqlite, docker, git, linux)
- `frontend/src/styles/global.css` — token `--color-warning` (bolinha
  amarela do terminal, não previsto em `tokens.md`) e a animação
  `@keyframes blink` do cursor
- `frontend/src/pages/index.astro` / `en/index.astro` — trocam o
  placeholder "hello world" pelo `<TerminalHero />`

**Conceitos explicados:**
- **`setTimeout` recursivo em vez de `setInterval`**: a cada caractere
  digitado, a função agenda A SI MESMA de novo com `setTimeout`. Isso é
  mais fácil de controlar que `setInterval` — dá pra mudar o tempo de
  espera dependendo da fase (digitando vs. pausado no resultado) e não
  corre o risco de dois "ticks" se sobreporem.
- **`data-*` attributes pra passar dados do servidor pro cliente**: o
  Astro roda no servidor (build time) e não tem acesso direto às
  variáveis do frontmatter dentro do `<script>` do cliente. A solução é
  serializar os dados como JSON num atributo `data-lines` do HTML, e o
  `<script>` (que roda no navegador) lê esse atributo e faz
  `JSON.parse`.
- **`prefers-reduced-motion` tratado em dois lugares**: a REGRA GLOBAL
  no CSS (`* { animation: none }`) já cuida do cursor piscando (que é
  uma animação CSS pura). Mas o efeito de "digitar" é feito em
  JavaScript, não CSS — por isso o script também verifica
  `matchMedia("(prefers-reduced-motion: reduce)")` e, se verdadeiro,
  já escreve o texto inteiro de uma vez, sem loop.
- **Fallback de imagem com SVG inline**: em vez de um `<img>` que
  tentaria carregar um arquivo que não existe (gerando um ícone de
  imagem quebrada), desenhamos um ícone de pessoa direto em SVG. Fica
  sempre bonito, nunca "quebra".

**Como testar:**
1. `cd frontend && npx astro dev --background`
2. Abrir `http://localhost:4321/` — ver o terminal digitando em loop,
   foto com anel neon, 3 botões
3. DevTools → Rendering → emular `prefers-reduced-motion: reduce` →
   recarregar → texto aparece todo de uma vez, sem digitação nem cursor
   piscando
4. Reduzir a janela pra <768px → layout vira 1 coluna (terminal → foto
   → botões)
5. Clicar em LinkedIn/GitHub → abrem em nova aba nos links reais do
   `CONTENT.md`
6. `npx astro check` e `npm run build` sem erros

**Desafio opcional:**
Troque a ordem das duas linhas do terminal em `pt.json` (primeiro
`ls ./skills`, depois `whoami`) e veja o loop mudar sem tocar em nenhum
código — só no JSON. Isso mostra a separação entre dado (JSON) e
comportamento (script).

**Decisões tomadas:**
- Não existe ainda `frontend/public/images/foto-perfil.jpg` nem
  `frontend/public/cv-matheus.pdf` (o `CONTENT.md` deixou os campos como
  "coloque o arquivo aqui"). Seguimos exatamente o que
  `docs/componentes/TerminalHero.md` já previa pra esse caso: fallback
  de avatar em SVG inline. O botão "baixar CV" já aponta pro caminho
  certo (`/cv-matheus.pdf`); quando o usuário colocar o PDF ali, o botão
  passa a funcionar sem nenhuma mudança de código. **Pendência pro
  usuário:** adicionar `frontend/public/images/foto-perfil.jpg` e
  `frontend/public/cv-matheus.pdf`.
- `docs/estilo/tokens.md` não define uma cor pra bolinha amarela do
  terminal (só bg/surface/border/primary/accent/success/danger/text).
  Criamos `--color-warning` com o mesmo valor (âmbar) nos dois temas,
  já que é um elemento decorativo fixo (imita macOS), não uma cor
  semântica que precise mudar entre dark/light.
