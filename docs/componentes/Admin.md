# Painel Admin — Especificação

## Rotas (frontend Astro, hidratadas)
- `/admin/login` — form usuário/senha
- `/admin` — layout com sidebar (Projetos | + Novo | Sair)
- `/admin/new`, `/admin/edit/[id]` — formulário de projeto

## Auth flow
1. POST `/api/auth/login` {username, password} → `{access_token}`
2. Token em `localStorage` (`admin_token`), enviado em `Authorization: Bearer`
3. 401/403 em qualquer chamada → limpa token, redireciona pro login

## Formulário de projeto (todos os campos do modelo)
Título, slug (auto-do-título), categoria (select), descrição PT, descrição EN,
porquê PT, porquê EN, skills (multi-select das skills cadastradas), GitHub URL,
Demo URL, imagem (upload → POST /api/upload → retorna image_url), featured (toggle)

## Lista de projetos
- Tabela: imagem thumb, título, categoria, ações (editar/excluir)
- Excluir: modal de confirmação `~# rm projeto? [y/n]`

## Estética
Mesmo tema hacker, MAS mais sóbria/funcional (é ferramenta, não vitrine).
