# Dados de Skills — Estrutura e Exemplos

## Arquivo: `frontend/src/data/skills.ts`
```ts
export type SkillCategory = "languages" | "databases" | "frameworks" | "tools";
export interface Skill {
  id: string;                 // "python"
  category: SkillCategory;
  name: string;
  icon: string;               // classe devicon, ex: "devicon-python-plain"
  level: 1 | 2 | 3 | 4 | 5;
  levelLabel: { pt: string; en: string };  // derivado do level: 5=avançado
  summary: { pt: string; en: string };     // o que é a tecnologia
  experience: { pt: string; en: string };  // seu nível/onde usa
}
```

## Níveis
1 = básico (estudando) | 2 = básico+ | 3 = intermediário | 4 = avançado | 5 = especialista

## Seed sugerido (ajustar com CONTENT.md do usuário)
- languages: Python(4), TypeScript(4), JavaScript(4), SQL(3), Bash(3)
- databases: PostgreSQL(3), SQLite(4), MongoDB(2)
- frameworks: Astro(4), FastAPI(4), React(3), TailwindCSS(4), Django(2)
- tools: Docker(3), Git/GitHub(4), Linux(4), Nmap/Wireshark(2), VS Code(5)

## summary/experience: exemplo (Python, nível 4)
- summary.pt: "Linguagem de programação de alto nível, forte em automação,
  dados e back-end."
- experience.pt: "Uso diariamente no back-end (FastAPI), scripts de
  automação e ferramentas de segurança. ~2 anos de prática."
