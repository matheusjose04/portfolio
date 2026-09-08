# ProjectsGrid — Especificação

## Header da seção
```
~/projetos $ ls
[ #complete-apps ]  [ #small-projects ]
```
Tab ativa = `--primary`; contador de itens por tab.

## Data fetching
```ts
const API = import.meta.env.PUBLIC_API_URL ?? "http://localhost:8000";
// GET `${API}/api/projects?category=${tab}`
```
- Loading: skeleton cards (shimmer CSS)
- Erro/API off: mensagem terminal-style `> erro: api offline` + retry
- Ordenação: `featured` primeiro, depois `created_at` desc

## Card de projeto
- Imagem (16:9, `object-fit: cover`, hover zoom 1.05)
- Título + badges de skills (máx 3, "+2" se mais)
- Hover: borda `--primary` + glow
- Click inteiro abre o modal (não só um botão)

## Estados vazios
`> nenhum projeto nesta categoria ainda` (mono, `--text-dim`)
