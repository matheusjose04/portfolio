# Endpoints da API

## Públicos
| Método | Rota | Descrição |
|---|---|---|
| GET | /api/projects | lista; query: `category`, `skill`, `featured` |
| GET | /api/projects/{slug} | detalhe |
| GET | /api/health | `{status: "ok"}` (pro docker healthcheck) |

## Admin (Bearer JWT)
| Método | Rota | Descrição |
|---|---|---|
| POST | /api/auth/login | {username,password} → {access_token} |
| POST | /api/projects | cria (201) |
| PUT | /api/projects/{id} | edita |
| DELETE | /api/projects/{id} | remove (204) |
| POST | /api/upload | multipart file → {url} |

## Regras
- Validação com Pydantic schemas (ProjectCreate, ProjectUpdate, ProjectOut)
- Slug único: em conflito, anexar `-2`, `-3`...
- CORS: liberar só ORIGINS do .env (localhost:4321 + domínio de produção)
- Respostas de erro no formato: `{"detail": "mensagem clara"}`
