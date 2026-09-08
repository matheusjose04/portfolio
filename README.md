# 📦 Portfólio Matheus — Pacote para Claude Code (modo ensino)

## O que tem aqui
| Arquivo | O que é |
|---|---|
| `docs/ARCHITECTURE.md` | Stack, estrutura de pastas, decisões e ordem de implementação |
| `docs/UI_SPECS.md` | Design system: cores dark/light, tipografia, layout, animações |
| `docs/FEATURES.md` | Funcionalidades: hero, skills, projetos, painel admin, i18n |
| `MASTER_PROMPT.md` | Prompt para colar no Claude Code |
| `README.md` | Este arquivo |

## Como usar
1. Extraia este ZIP numa pasta nova e abra no terminal
2. Rode `claude`
3. Cole o conteúdo de `MASTER_PROMPT.md` como primeira mensagem
4. O Claude Code vai planejar com `/ecc:plan`, construir etapa por etapa e
   PARAR para você confirmar antes de prosseguir

## 🎓 Modo ensino
A cada etapa ele cria/atualiza `docs/APRENDIZADO.md` explicando tudo
que fez, com código comentado e um desafio opcional. Ao final do projeto,
você terá um material de estudo completo do seu próprio portfólio.

## Se travar
> "Continue de onde parou, seguindo a ordem do ARCHITECTURE.md"
