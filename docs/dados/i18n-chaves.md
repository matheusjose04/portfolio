# i18n — Estrutura de Chaves

## Arquivos: `frontend/src/i18n/pt.json`, `en.json` (mesmas chaves, SEMPRE)

```json
{
  "nav": { "home": "", "about": "", "skills": "", "projects": "", "contact": "" },
  "hero": {
    "terminal": { "lines": [ { "cmd": "", "output": "" } ] },
    "cta": { "cv": "", "linkedin": "", "github": "" }
  },
  "about": { "heading": "", "text": "" },
  "skills": {
    "heading": "", "categories": { "languages": "", "databases": "",
    "frameworks": "", "tools": "" },
    "modal": { "level": "", "projectsLink": "" }
  },
  "projects": {
    "heading": "", "tabs": { "complete": "", "small": "" },
    "empty": "", "modal": { "why": "", "skillsUsed": "", "demo": "", "github": "" }
  },
  "contact": { "heading": "", "text": "", "email": "" },
  "footer": { "rights": "", "exit": "" },
  "admin": { "login": "", "logout": "", "newProject": "", "save": "", "delete": "" }
}
```

## Regras
- NENHUMA string visível fora desses JSONs (procurar por textos soltos no
  código deve retornar zero)
- Idioma ativo: `localStorage.lang` + rota (`/en/` força EN)
- Componentes leem via helper `t("skills.heading")`
