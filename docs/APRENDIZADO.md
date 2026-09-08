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

## Etapa 4 — Seção Sobre

**O que foi feito:**
Criamos a seção "Sobre" com o texto EXATO que o usuário escreveu no
`CONTENT.md` (nada inventado), heading em estilo terminal (`~# sobre` /
`~# about`), e um bloco de código decorativo (`// quem sou eu`) ao lado,
mostrando foco e formação — também só com dados que já estavam no
`CONTENT.md`.

**Arquivos criados/alterados:**
- `frontend/src/components/About.astro` — seção com `id="sobre"`
  (âncora da navbar), texto em 2 parágrafos + bloco de código decorativo
- `frontend/src/i18n/pt.json`, `en.json` — chave `about.text` com o
  texto do usuário (PT) e uma tradução fiel pro inglês (o `CONTENT.md`
  deixou o campo EN vazio e autorizou explicitamente: "deixe vazio que
  ele traduz"); `about.decoration.*` com foco/formação
- `frontend/src/pages/index.astro` / `en/index.astro` — adicionam
  `<About lang={...} />` depois do hero

**Conceitos explicados:**
- **`split("\n\n")` pra parágrafos**: guardamos o texto inteiro numa
  única string no JSON (mais fácil de manter que um array), com `\n\n`
  marcando onde um parágrafo termina e outro começa. No componente,
  `.split("\n\n")` transforma essa string em uma lista, e
  `.map()` gera um `<p>` pra cada parágrafo.
- **Por que a âncora `id="sobre"` não muda de idioma**: o link da navbar
  aponta sempre pra `#sobre` (fixo), mesmo na versão `/en/`. Isso é uma
  escolha proposital: a ROTA da página muda (`/` vs `/en/`), mas a
  ESTRUTURA da página (os ids das seções) fica igual — assim o mesmo
  componente `Navbar` funciona sem precisar de um mapa de tradução de
  âncoras.

**Como testar:**
1. `cd frontend && npx astro dev --background`
2. `http://localhost:4321/#sobre` → heading `~# sobre`, texto em 2
   parágrafos à esquerda, bloco de código à direita (desktop) — testado
   visualmente, confere
3. `http://localhost:4321/en/#sobre` → mesmo conteúdo em inglês,
   heading `~# about` — testado, confere
4. Redimensionar <768px → 1 coluna (texto acima do bloco decorativo) —
   testado, confere
5. `npx astro check` e `npm run build` sem erros

**Desafio opcional:**
Compare `about.text` no `pt.json` com o texto original no `CONTENT.md`,
frase por frase — é assim que você confirma (e qualquer revisor externo
também consegue confirmar) que o "modo ensino" não inventou nada sobre
você.

**Decisões tomadas:**
- Nenhuma pendência nova nesta etapa — tudo que aparece na seção Sobre
  veio direto do `CONTENT.md`.

## Etapa 5 — Skills com Modais

**O que foi feito:**
Criamos a grade de skills com 4 abas de categoria (LANGUAGES, DATABASES,
FRAMEWORKS, OTHER TOOLS) e um modal (janela de detalhes) que abre ao
clicar num card, mostrando ícone, nível (com barrinha animada),
descrição da tecnologia e como o usuário já usou ela — tudo com
acessibilidade (teclado, foco preso, ESC fecha).

**Arquivos criados/alterados:**
- `frontend/src/data/skills.ts` — os dados das 8 skills marcadas no
  `CONTENT.md` (Python, TypeScript, JavaScript, SQLite, FastAPI, Docker,
  Git/GitHub, Linux), no formato de `docs/dados/skills-data.md`
- `frontend/src/components/Skills.astro` — grid + abas + modal único
  reutilizado (em vez de um modal por skill)
- `frontend/src/i18n/pt.json`, `en.json` — `skills.heading`,
  `skills.categories.*`, `skills.modal.*`
- `frontend/src/styles/global.css` — import do `devicon/devicon.min.css`
  (ícones das tecnologias)
- `package.json` — nova dependência `devicon`

**Conceitos explicados:**
- **Um modal só, reaproveitado**: em vez de criar 8 `<dialog>` (um por
  skill) e ter que garantir que só um abre por vez, criamos UM elemento
  de modal fixo no HTML e, ao clicar num card, preenchemos ele com os
  dados daquela skill via JavaScript (`textContent`, `className`). Isso
  já garante sozinho a regra "só um modal aberto por vez" — não existe
  um segundo modal pra abrir.
- **Focus trap (prender o foco)**: com o modal aberto, apertar Tab não
  pode "escapar" pro resto da página (ruim pra quem navega só com
  teclado). O código escuta `Tab`/`Shift+Tab` e, quando o foco chegaria
  no último elemento focável do modal (ou no primeiro, indo pra trás),
  ele "pula" de volta pro começo (ou fim) — o foco fica preso dentro do
  modal.
- **Devolver o foco de onde veio**: guardamos em `lastFocused` qual
  botão/card foi clicado pra abrir o modal. Ao fechar (ESC, X, ou
  clique fora), o foco volta pra esse elemento — importante pra quem
  usa teclado não "perder o lugar" na página.
- **Filtro de categoria só com CSS `display`**: clicar numa aba não
  recria o grid — só percorre os cards existentes e esconde
  (`display: none`) os que não são da categoria escolhida. Mais simples
  e rápido que re-renderizar.

**Como testar:**
1. `cd frontend && npx astro dev --background`
2. `http://localhost:4321/#skills` → só os cards de LANGUAGES aparecem
   de cara (a aba já vem marcada como ativa no HTML)
3. Clicar em "OTHER TOOLS" → troca pra Docker/Git-GitHub/Linux
4. Clicar num card → modal abre com nível, resumo e experiência
5. `Esc` fecha o modal e o foco volta pro card
6. Clicar fora do card (no fundo escurecido) também fecha
7. `npx astro check` e `npm run build` sem erros

**Desafio opcional:**
Aperte Tab repetidamente com o modal aberto e veja o foco "circular"
entre o X de fechar e o link "Ver projetos" sem nunca escapar pro resto
da página — depois tente proposital­mente remover o `focus trap` do
código e repita o teste pra sentir a diferença de acessibilidade.

**Decisões tomadas:**
- O `CONTENT.md` só dá 3 níveis (`basico`/`intermediario`/`avancado`),
  mas `docs/dados/skills-data.md` usa uma escala de 1 a 5. Mapeamos
  `basico → 2` e `intermediario → 3` (nenhuma skill do usuário está
  marcada como avançado, então `4` e `5` não são usados por enquanto).
  Registrado no código-fonte também (comentário em `skills.ts`).
- **Bug encontrado e corrigido durante o teste manual**: o filtro de
  categoria só rodava quando uma aba era CLICADA — no carregamento
  inicial da página, a aba "LANGUAGES" aparecia marcada como ativa
  visualmente, mas todos os 8 cards ficavam visíveis (o filtro nunca
  tinha rodado). Corrigido chamando a mesma função de filtro uma vez,
  já no carregamento, pra aba que vem ativa por padrão.
- Durante o teste, uma ferramenta de automação do navegador (não o
  código do site) abriu o modal sozinha numa das capturas de tela —
  confirmamos com um teste limpo, direto no Chrome real, que isso era
  um artefato da ferramenta de teste, não um bug do site.

## Etapa 6 — Backend FastAPI

**O que foi feito:**
Criamos a API em Python/FastAPI: modelos de banco (Project, AdminUser),
schemas de validação (Pydantic v2), autenticação JWT, CRUD completo de
projetos (público pra leitura, protegido por token pra escrever), upload
de imagem, e o script de seed com admin + 4 projetos placeholder
(explicado abaixo).

**Arquivos criados/alterados:**
- `backend/app/config.py` — lê `.env` (SECRET_KEY, admin, CORS, etc.)
- `backend/app/database.py` — engine SQLAlchemy, `SessionLocal`, `get_db`
- `backend/app/models.py` — `Project` e `AdminUser` (SQLAlchemy 2.x)
- `backend/app/schemas.py` — `ProjectCreate/Update/Out`, `LoginRequest`,
  validação de URL (`http(s)://`) e de skills válidas
- `backend/app/auth.py` — hash de senha (bcrypt), criação/verificação de
  JWT, dependência `get_current_admin`
- `backend/app/crud.py` — geração de slug único (com transliteração de
  acento) a partir do título
- `backend/app/routers/{auth,projects,upload}.py` — os endpoints
- `backend/app/main.py` — monta tudo, CORS, `/uploads` estático, `/api/health`
- `backend/seed.py` — cria admin + 4 projetos placeholder (idempotente)
- `backend/tests/` — 6 testes pytest (health, login certo/errado, criar
  sem token, criar com token + aparece na listagem, skill inválida)
- `backend/.env.example` / `backend/.env` — variáveis de ambiente
  (o `.env` real tem uma SECRET_KEY gerada e não é commitado)
- `backend/requirements.txt` — dependências (fixadas por versão)
- `frontend/public/images/projects/*.svg` — 4 imagens placeholder locais
- `.gitignore` (raiz) — adiciona `backend/uploads/` e `.pytest_cache/`

**Conceitos explicados:**
- **Por que `description` no banco é `description_pt`/`description_en`
  mas a API devolve só `description`**: o banco guarda os dois idiomas
  pra sempre ter a informação completa; a API "resolve" qual mostrar
  baseado no header `Accept-Language` do navegador (ou `?lang=`),
  devolvendo só UM campo já no idioma certo. O frontend nem precisa
  saber que existem dois campos no banco.
- **JWT (JSON Web Token)**: depois do login certo, a API gera um "crachá"
  assinado digitalmente (o token) contendo o nome do admin e uma data de
  expiração. Esse crachá vai no header `Authorization: Bearer <token>`
  em cada requisição protegida. A API confere a assinatura (com a
  `SECRET_KEY`) pra saber se o crachá é válido e não foi forjado — sem
  precisar guardar sessão em lugar nenhum.
- **Dependency Injection do FastAPI (`Depends`)**: `Depends(get_current_admin)`
  num endpoint significa "antes de rodar essa função, rode
  `get_current_admin` primeiro". Se o token for inválido, ela já
  interrompe com 401 antes mesmo do código do endpoint rodar. Isso evita
  repetir a checagem de auth em todo endpoint manualmente.
- **Idempotência do seed**: rodar `python seed.py` duas vezes não deveria
  duplicar nada. A solução foi checar, ANTES de inserir, se já existe um
  projeto com aquele slug esperado — se existir, pula.

**Como testar:**
1. `cd backend && python -m venv venv` (já feito) e
   `venv\Scripts\pip install -r requirements.txt`
2. Copiar `.env.example` pra `.env` e gerar uma `SECRET_KEY` real com
   `python -c "import secrets; print(secrets.token_hex(32))"`
3. `venv\Scripts\python -m pytest -q` → 6 testes passam
4. `venv\Scripts\python seed.py` → cria admin + 4 projetos (rodar de novo
   não duplica)
5. `venv\Scripts\python -m uvicorn app.main:app --reload` → `/docs` abre
   (testei manualmente: GET lista projetos, POST sem token → 401, POST
   com token → 201, PUT/DELETE funcionam, filtro `?featured=true`
   funciona, `Accept-Language: en` troca o idioma da resposta)

**Desafio opcional:**
Abra `http://localhost:8000/docs` (Swagger, gerado automaticamente pelo
FastAPI a partir dos schemas) e tente criar um projeto por lá, sem
token — veja o erro 401. Depois faça login em `/api/auth/login`, copie o
`access_token`, clique em "Authorize" no topo da página e tente de novo.

**Decisões tomadas:**
- **Bug encontrado e corrigido**: a versão mais nova do pacote `bcrypt`
  (5.x) quebra a integração com `passlib` (biblioteca de hash de senha) —
  erro `password cannot be longer than 72 bytes` no autoteste interno do
  passlib. Fixamos a versão do `bcrypt` em `4.0.1` no
  `requirements.txt`, que é compatível.
- **Bug encontrado e corrigido**: a geração de slug (`slugify`) não
  removia acentos corretamente — "Sistema de Gestão X" virava
  `sistema-de-gest-o-x` (o "ã" simplesmente sumia). Corrigido com
  `unicodedata.normalize` pra transliterar (ã→a, ç→c, etc.) antes de
  limpar o resto — agora vira `sistema-de-gestao-x`.
- **Lista de skills válidas duplicada** entre `frontend/src/data/skills.ts`
  (TypeScript) e `backend/app/schemas.py` (Python) — não há build
  compartilhado entre as duas linguagens nesta fase do projeto, então a
  validação do backend usa sua própria cópia da lista de ids. Se
  adicionar uma skill nova no frontend, adicionar também em
  `VALID_SKILL_IDS` no backend.
- **Upload real de imagem (MIME de verdade, não só extensão)**: além de
  checar o `content_type` enviado pelo navegador (que pode ser
  forjado), tentamos abrir o arquivo com Pillow (`Image.open(...).verify()`)
  — se não for uma imagem de verdade, rejeita. Isso está implementado no
  endpoint, mas só será testado de fato na Etapa 8 (painel admin), que é
  quem vai efetivamente enviar arquivos.
- Como o `CONTENT.md` não tinha projetos preenchidos, os 4 projetos do
  seed são os placeholders sugeridos em `docs/backend/seed.md`
  ("Sistema de Gestão X", "API de Autenticação Y", "CLI de Automação Z",
  "Bot de Discord W"), com `github_url`/`demo_url` deixados como `null`
  (não inventamos links). **Pendência pro usuário:** trocar esses 4
  projetos pelos reais, pelo painel `/admin` (Etapa 8) ou editando o
  `CONTENT.md` e rodando o seed de novo.

## Etapa 7 — Seção Projetos

**O que foi feito:**
Criamos a grade de projetos que consome a API real (`GET /api/projects`),
com abas por categoria, contador de itens, skeleton de carregamento,
fallback pra dados locais se a API cair (com botão "tentar de novo"), e
um modal de detalhes reaproveitando a mesma infraestrutura de
acessibilidade do modal de skills — inclusive integração entre os dois:
clicar numa skill dentro do modal de projeto pula pra seção Skills, troca
de aba se precisar, e destaca o card certo.

**Arquivos criados/alterados:**
- `frontend/src/components/ProjectsGrid.astro` — grid + abas + skeleton +
  fetch com fallback + modal de projeto
- `frontend/src/components/Skills.astro` — adiciona `data-skill-id` nos
  cards e um listener do evento `skills:focus` (troca de aba + destaque
  temporário) disparado pelo modal de projetos
- `frontend/src/data/fallback-projects.ts` — cópia local dos 4
  placeholders do `backend/seed.py`, usada só quando a API está offline
- `frontend/src/i18n/pt.json`, `en.json` — chaves `projects.*` completas
  (heading, tabs, empty, error, retry, modal.*)
- `frontend/.env.example` — documenta `PUBLIC_API_URL`
- `frontend/src/pages/index.astro` / `en/index.astro` — adicionam
  `<ProjectsGrid lang={...} />`

**Conceitos explicados:**
- **`fetch` com fallback (try/catch)**: o código tenta buscar os dados
  reais da API; se a rede falhar OU a resposta não for "ok" (`res.ok`),
  cai no bloco `catch` e usa os dados locais (`fallback-projects.ts`).
  Assim o site nunca fica com a seção de projetos vazia, mesmo se o
  backend estiver fora do ar.
- **`CustomEvent` pra comunicação entre componentes**: `Skills.astro` e
  `ProjectsGrid.astro` não se importam um do outro — eles são
  independentes. Pra um "avisar" o outro (clicar numa skill no modal de
  projeto deve fazer algo na seção Skills), usamos
  `window.dispatchEvent(new CustomEvent("skills:focus", {...}))` de um
  lado e `window.addEventListener("skills:focus", ...)` do outro. É como
  gritar um recado pra quem quiser ouvir, sem precisar se conhecer.
- **Por que construir os cards com `document.createElement` em vez de
  `innerHTML`**: os dados dos projetos vêm da API e, a partir da Etapa 8,
  vão poder ser digitados por um admin num formulário. Se a gente
  colocasse esse texto direto num `innerHTML`, um título malicioso tipo
  `<img src=x onerror=alert(1)>` viraria HTML de verdade e executaria
  script (isso se chama XSS). Usando `textContent` e
  `document.createElement`, o texto SEMPRE é tratado como texto puro,
  nunca como HTML — mesmo que venha de uma fonte não confiável.
- **Contagem por aba sem duas requisições**: em vez de seguir a
  literalidade da spec (`GET .../api/projects?category=${tab}`, uma
  chamada por aba), buscamos a lista completa (`GET .../api/projects`)
  UMA vez e filtramos no navegador. Isso já dá o contador das duas abas
  de graça e evita refazer a requisição toda vez que o usuário clica
  numa aba.

**Como testar:**
1. `cd backend && venv\Scripts\python -m uvicorn app.main:app --reload`
   (porta 8000) e `cd frontend && npx astro dev --background` (porta 4321)
2. `http://localhost:4321/#projetos` → 2 projetos em #complete-apps,
   contador certo nas duas abas — testei e confere
3. Clicar num card → modal com imagem, descrição, "Por que fiz",
   skills, botão Demo desabilitado (sem `demo_url`) — testei e confere
4. Clicar numa skill dentro do modal → fecha o modal, rola até #skills,
   troca pra aba certa e destaca o card por 1.5s — testei e confere
5. Parar o backend (`Ctrl+C` no uvicorn) e recarregar a página → aparece
   "> erro: api offline" + botão "tentar de novo", mas os cards
   continuam aparecendo (dados locais) — testei e confere
6. Religar o backend e clicar em "tentar de novo" → erro some, dados
   reais voltam — testei e confere
7. `npx astro check` e `npm run build` sem erros

**Desafio opcional:**
Com o backend rodando, crie um projeto novo direto pelo Swagger
(`http://localhost:8000/docs`, endpoint `POST /api/projects`, precisa do
token de `/api/auth/login` primeiro) e recarregue a página — o projeto
novo deve aparecer na grade, sem precisar rebuildar o frontend. Isso é o
"sem rebuild" que o critério de aceite do projeto pede.

**Decisões tomadas:**
- O link "direto pra um projeto" via URL (`#projeto/<slug>`) citado como
  "nice-to-have" em `docs/componentes/ProjectModal.md` foi deixado de
  fora por enquanto — é uma melhoria opcional, não um critério de
  aceite da etapa.
- Fetch consolidado (uma chamada, filtro local) em vez de uma chamada
  por aba — decisão registrada acima, mais simples e com o mesmo
  resultado observável pro usuário.

## Etapa 8 — Painel Admin

**O que foi feito:**
Construímos o painel `/admin`: login com JWT, lista de projetos com
editar/excluir (excluir pede confirmação), formulário de criar/editar
com todos os campos do modelo (incluindo upload de imagem de verdade), e
proteção automática — sem token válido, qualquer página admin manda pro
login.

**Arquivos criados/alterados:**
- `backend/app/schemas.py` — novo `ProjectAdminOut` (campos brutos
  `description_pt/en`, `why_pt/en`, sem resolver idioma)
- `backend/app/routers/projects.py` — novo endpoint
  `GET /api/projects/id/{id}` (só admin), usado pelo formulário de edição
- `backend/tests/test_api.py` — 2 testes novos pro endpoint acima
- `frontend/src/lib/admin-api.ts` — `adminFetch()` (anexa o token, trata
  401/403), `getToken/setToken/clearToken`
- `frontend/src/lib/image-url.ts` — `resolveImageUrl()` (ver decisão/bug
  abaixo)
- `frontend/src/layouts/AdminLayout.astro` — sidebar (projetos/+novo/sair)
  + guarda de autenticação
- `frontend/src/pages/admin/login.astro` — form de login
- `frontend/src/pages/admin/index.astro` — lista + modal de confirmação
  de exclusão
- `frontend/src/pages/admin/new.astro`, `edit.astro` — usam o
  `ProjectForm` compartilhado
- `frontend/src/components/admin/ProjectForm.astro` — formulário
  completo (create E edit no mesmo componente)

**Conceitos explicados:**
- **Guarda de rota no cliente (sem servidor de sessão)**: como o site é
  estático (sem backend Node/Python renderizando páginas), não existe
  "sessão" no servidor. A proteção é: todo layout de página admin roda um
  script que verifica `localStorage.admin_token` ao carregar; se não
  tiver, redireciona pro login ANTES do conteúdo ser útil. Não é 100%
  seguro sozinho — por isso a API TAMBÉM exige o token em cada chamada
  protegida (a "segurança de verdade" é sempre no backend).
- **Formulário único pra criar E editar**: em vez de dois componentes
  quase idênticos, um só `ProjectForm.astro` lê `?id=` da URL — se tiver,
  busca os dados e preenche os campos (modo edição); se não tiver, começa
  vazio (modo criação). No envio, a única diferença é `POST` (criar) vs
  `PUT` (editar).
- **Por que precisou de um endpoint novo (`/api/projects/id/{id}`)**: o
  endpoint público (`GET /api/projects/{slug}`) devolve `description` já
  resolvida num idioma só — ótimo pro site, mas o formulário de edição
  precisa dos DOIS campos (`description_pt` E `description_en`) pra
  deixar o admin editar cada um. Criamos um endpoint separado, protegido
  por token, que devolve os campos "crus" do banco.

**Como testar:**
1. Backend (`uvicorn`) e frontend (`astro dev`) rodando
2. `http://localhost:4321/admin` sem estar logado → redireciona pro
   `/admin/login` — testei e confere
3. Login errado → mensagem de erro; login certo (`admin`/`admin123`) →
   entra e lista os 4 projetos do seed — testei e confere
4. `+ novo` → preencher formulário, subir uma imagem de verdade (testei
   com um PNG gerado na hora) → salvar → projeto aparece na lista E no
   site público, com a imagem certa
5. `editar` → campos vêm preenchidos (inclusive os dois idiomas) →
   mudar o título → salvar → slug muda sozinho
6. `excluir` → modal `~# rm <título>? [y/n]` → "n" cancela, "y" exclui
   de verdade (testei os dois caminhos)
7. Token inválido/expirado + tentar uma ação protegida (ex: excluir) →
   limpa o token e manda pro login automaticamente — testei forçando um
   token inválido no `localStorage`
8. `sair` → limpa token, volta pro login
9. `cd backend && venv\Scripts\python -m pytest -q` → 8 testes passam

**Desafio opcional:**
Abra o DevTools → Application → Local Storage enquanto navega pelo
`/admin`, e observe o `admin_token` sendo criado no login e apagado no
"sair" (ou automaticamente, se você forçar um token inválido e tentar
excluir algo). Isso mostra na prática onde mora esse "crachá" de sessão.

**Decisões tomadas:**
- **Bug real encontrado e corrigido durante o teste manual**: a API de
  upload devolve uma URL relativa (`/uploads/arquivo.png`), pensada pra
  ser servida PELA PRÓPRIA API. Só que a `docs/deploy/caddy-nginx.md`
  já deixa claro que produção usa domínios SEPARADOS pro frontend
  (`portfolio.dominio`) e a API (`api.portfolio.dominio`) — igual ao dev
  (`:4321` vs `:8000`). Um `<img src="/uploads/x.png">` carregado dentro
  do FRONTEND tentaria buscar a imagem no domínio ERRADO (o do próprio
  site, não o da API). Corrigido com `resolveImageUrl()`: qualquer
  caminho que comece com `/uploads/` ganha o domínio da API antes de
  virar `src` de imagem — usado no preview do formulário, na lista do
  admin e nos cards/modal públicos de projeto. O valor GRAVADO no banco
  continua sendo o caminho relativo (mais correto — não trava a URL da
  API dentro dos dados).
- **Rota `/admin/edit/[id]` virou `/admin/edit?id=`**: `docs/componentes/
  Admin.md` sugere uma rota dinâmica `/admin/edit/[id]`, mas o site usa
  `output: "static"` (sem servidor) — rotas dinâmicas do Astro nesse modo
  precisam saber TODOS os ids possíveis no momento do build, o que é
  impossível pra projetos criados depois, sem rebuild, pelo próprio
  admin. Uma única página estática lendo `?id=` da URL no navegador
  resolve o mesmo problema sem essa limitação.
- Mantivemos o painel admin só em português (sem `/en/admin`) — é uma
  ferramenta interna de uso pessoal, não uma página pro público; o
  `MASTER_PROMPT.md` não exige i18n pro admin.

## Etapa 9 — Internacionalização PT/EN

**O que foi feito:**
As seções principais (navbar, hero, sobre, skills, projetos) já vinham
recebendo a prop `lang` e lendo textos via `t()` desde as etapas
anteriores — então a maior parte da Etapa 9 já estava pronta. Faltavam
dois pontos exigidos pelo checklist de `docs/etapas/09-i18n.md`: (1) um
punhado de textos de acessibilidade (`aria-label`) que ficaram
hardcoded em português mesmo dentro de componentes usados na versão
`/en/`, e (2) o idioma escolhido não "grudava" — ao voltar pra raiz
(`/`) depois de ter navegado pra `/en/`, o site sempre reabria em
português. Resolvemos os dois.

**Arquivos criados/alterados:**
- `frontend/src/i18n/pt.json`, `en.json` — novo grupo de chaves `a11y`
  (`primaryNav`, `openMenu`, `close`, `themeToggle`, `skillsCategories`,
  `projectsCategories`) pros textos de acessibilidade que faltavam
- `frontend/src/components/Navbar.astro` — troca os `aria-label`
  hardcoded por `t("a11y...")`; os links `pt`/`en` ganharam `id` e um
  listener que grava a escolha em `localStorage.lang`; passa `lang` pro
  `ThemeToggle`
- `frontend/src/components/ThemeToggle.astro` — antes não recebia
  `lang` nenhum (por isso o botão de tema sempre falava português,
  mesmo em `/en/`); agora aceita a prop e traduz o `aria-label`
- `frontend/src/components/ProjectsGrid.astro`,
  `frontend/src/components/Skills.astro` — `aria-label` dos
  tablists de categoria e dos botões "fechar" dos modais, traduzidos
- `frontend/src/layouts/Base.astro` — novo `<script>` inline no
  `<head>` que redireciona `/` → `/en/` quando `localStorage.lang`
  guarda `"en"`

**Conceitos explicados:**
- **`aria-label` também é texto do produto**: é fácil esquecer, porque
  não aparece na tela — só leitores de tela o anunciam. Mas pra quem
  usa um leitor de tela em inglês navegando `/en/`, ouvir "Fechar" ou
  "Abrir menu" em português é tão errado quanto um botão visível com
  texto errado. Por isso o checklist da etapa pede "nenhuma string
  visível hardcoded" — "visível" aqui inclui o que é visível pra
  tecnologias assistivas, não só pro olho.
- **Persistência de idioma num site 100% estático**: como o site é
  gerado como arquivos HTML estáticos (`output: "static"`, sem servidor
  Node por trás), não existe um jeito de o SERVIDOR lembrar "esse
  visitante prefere inglês" — cada página é um arquivo fixo. A solução
  é client-side: ao clicar em `en`, gravamos `localStorage.lang = "en"`
  ANTES de navegar; depois, um script bem no início do `<head>` de toda
  página checa esse valor e, se a página atual for a raiz em português
  E o valor salvo for `"en"`, troca a URL pra `/en/` com
  `location.replace()` (que não deixa a página em português no
  histórico do navegador, então o botão "voltar" não fica preso num
  loop de redirecionamento).
- **Por que o redirect só mexe em `location.pathname === "/"`**: o
  layout `Base.astro` é reaproveitado também pelo painel `/admin/*`
  (sempre em português, por decisão da Etapa 8). Se o redirect checasse
  só a prop `lang === "pt"`, ele dispararia TAMBÉM dentro do admin
  sempre que o visitante tivesse navegado o site público em inglês
  antes — te jogando pra fora do painel administrativo sem motivo.
  Restringir ao caminho exato `/` deixa o comportamento só na home
  pública, sem tocar em nada dentro de `/admin`.

**Como testar:**
1. `astro dev --background` e abrir `http://localhost:4321/`
2. No DevTools → Console, rodar `localStorage.setItem('lang','en')` e
   recarregar a raiz (`/`) → redireciona sozinho pra `/en/` — testei e
   confere
3. Com esse mesmo `localStorage.lang = "en"`, abrir
   `http://localhost:4321/admin/login` → continua em português, SEM
   redirecionar — testei e confere (é exatamente o bug que o
   `pathname === "/"` evita)
4. Limpar o `localStorage`, voltar pra `/`, clicar no link `en` da
   navbar → navega pra `/en/` E grava a preferência (dá pra conferir
   com `localStorage.getItem('lang')` no console) — testei e confere
5. `npx astro build` gera `dist/index.html` e `dist/en/index.html`;
   rodei `grep aria-label` nos dois e confirmei que cada um só tem os
   textos no idioma certo (`"Fechar"`/`"Close"`,
   `"Abrir menu"`/`"Open menu"`, etc.)
6. `npx astro check` → 0 erros

**Desafio opcional:**
Abra o DevTools → Application → Local Storage em `/`, apague a chave
`lang` e recarregue: repare que, sem preferência salva, o site sempre
abre em português (o padrão do `Base.astro`). Depois tente pensar: se
o projeto um dia ganhasse mais páginas além da home (não só `/` e
`/en/`), como você mudaria a checagem `location.pathname === "/"` pra
continuar funcionando sem também afetar o `/admin`?

**Decisões tomadas:**
- **Sem tradução das chaves `contact`, `footer` e `admin` em
  `pt.json`/`en.json`**: elas já existem como "esqueleto" (valores
  vazios) desde que a estrutura de chaves foi definida em
  `docs/dados/i18n-chaves.md`, mas os componentes que vão usá-las
  (`Footer`, com a seção de contato embutida) ainda não foram
  construídos — isso é trabalho da Etapa 10 (polimento), que é onde
  `docs/componentes/Footer.md` é referenciado. Preencher essas chaves
  agora, sem componente nenhum lendo elas, violaria a regra de não
  adicionar código/dado que não está sendo usado ainda.
