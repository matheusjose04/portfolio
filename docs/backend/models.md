# Modelos de Dados (SQLAlchemy)

## Project
| Campo | Tipo | Notas |
|---|---|---|
| id | Integer PK | |
| title | String(120) | obrigatório |
| slug | String(140) unique, index | gerado do título |
| description_pt / description_en | Text | obrigatório |
| why_pt / why_en | Text | "por que fiz" |
| category | String(20) | check in {"complete", "small"} |
| skills | JSON (list[str]) | ids das skills |
| github_url | String(255) nullable | validar URL |
| demo_url | String(255) nullable | validar URL |
| image_url | String(255) nullable | caminho do upload |
| featured | Boolean | default False |
| created_at | DateTime | default utcnow |

## Skill (opcional nesta fase; skills vivem no frontend em TS)
Se persistir: id, key (unique), name, category, level (1-5), summary_pt/en,
experience_pt/en, icon.

## AdminUser
id, username unique, password_hash (bcrypt), created_at.
Criado pelo seed com dados do CONTENT.md.
