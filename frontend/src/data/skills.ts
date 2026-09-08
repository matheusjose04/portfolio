export type SkillCategory = "languages" | "databases" | "frameworks" | "tools";
export type SkillLevel = 1 | 2 | 3 | 4 | 5;

export interface Skill {
  id: string;
  category: SkillCategory;
  name: string;
  icon: string;
  level: SkillLevel;
  levelLabel: { pt: string; en: string };
  summary: { pt: string; en: string };
  experience: { pt: string; en: string };
}

const LEVEL_LABEL: Record<SkillLevel, { pt: string; en: string }> = {
  1: { pt: "básico", en: "basic" },
  2: { pt: "básico", en: "basic" },
  3: { pt: "intermediário", en: "intermediate" },
  4: { pt: "avançado", en: "advanced" },
  5: { pt: "especialista", en: "expert" },
};

function skill(
  data: Omit<Skill, "levelLabel">
): Skill {
  return { ...data, levelLabel: LEVEL_LABEL[data.level] };
}

// Níveis vêm do CONTENT.md ("basico"/"intermediario"/"avancado"), mapeados
// pra escala 1-5 de docs/dados/skills-data.md: basico=2, intermediario=3.
export const skills: Skill[] = [
  skill({
    id: "python",
    category: "languages",
    name: "Python",
    icon: "devicon-python-plain",
    level: 2,
    summary: {
      pt: "Linguagem de alto nível, muito usada em back-end, automação e ferramentas de cybersecurity.",
      en: "High-level language widely used for back-end development, automation and cybersecurity tooling.",
    },
    experience: {
      pt: "Uso em projetos acadêmicos e pessoais de desenvolvimento fullstack e em scripts de segurança.",
      en: "Used in academic and personal fullstack projects and in security-related scripts.",
    },
  }),
  skill({
    id: "typescript",
    category: "languages",
    name: "TypeScript",
    icon: "devicon-typescript-plain",
    level: 2,
    summary: {
      pt: "Superset do JavaScript com tipagem estática, usado no front-end e em ferramentas modernas.",
      en: "JavaScript superset with static typing, used across modern front-end tooling.",
    },
    experience: {
      pt: "Uso no desenvolvimento do front-end deste portfólio e em projetos pessoais.",
      en: "Used to build the front-end of this portfolio and in personal projects.",
    },
  }),
  skill({
    id: "javascript",
    category: "languages",
    name: "JavaScript",
    icon: "devicon-javascript-plain",
    level: 2,
    summary: {
      pt: "Linguagem principal da web, roda no navegador e também no back-end (Node.js).",
      en: "The core language of the web, running in the browser and on the back-end via Node.js.",
    },
    experience: {
      pt: "Base para os projetos front-end que desenvolvi durante a faculdade e por conta própria.",
      en: "Foundation for the front-end projects built during university and on my own.",
    },
  }),
  skill({
    id: "sqlite",
    category: "databases",
    name: "SQLite",
    icon: "devicon-sqlite-plain",
    level: 2,
    summary: {
      pt: "Banco de dados relacional leve, roda em um único arquivo — ótimo pra projetos pequenos/médios.",
      en: "Lightweight relational database that runs from a single file — great for small/medium projects.",
    },
    experience: {
      pt: "Uso como banco de dados em projetos acadêmicos e pessoais, incluindo este portfólio.",
      en: "Used as the database in academic and personal projects, including this portfolio.",
    },
  }),
  skill({
    id: "fastapi",
    category: "frameworks",
    name: "FastAPI",
    icon: "devicon-fastapi-plain",
    level: 2,
    summary: {
      pt: "Framework Python moderno pra construir APIs, rápido e com documentação automática.",
      en: "Modern Python framework for building APIs, fast and with automatic docs.",
    },
    experience: {
      pt: "Uso pra construir APIs em projetos acadêmicos e pessoais, incluindo o back-end deste portfólio.",
      en: "Used to build APIs in academic and personal projects, including this portfolio's back-end.",
    },
  }),
  skill({
    id: "docker",
    category: "tools",
    name: "Docker",
    icon: "devicon-docker-plain",
    level: 2,
    summary: {
      pt: "Ferramenta de containers que empacota uma aplicação com tudo que ela precisa pra rodar igual em qualquer lugar.",
      en: "Container tool that packages an application with everything it needs to run the same anywhere.",
    },
    experience: {
      pt: "Uso pra empacotar e rodar projetos pessoais, e para o deploy deste portfólio.",
      en: "Used to package and run personal projects, and for this portfolio's deployment.",
    },
  }),
  skill({
    id: "git",
    category: "tools",
    name: "Git/GitHub",
    icon: "devicon-git-plain",
    level: 3,
    summary: {
      pt: "Sistema de controle de versão (Git) e plataforma de hospedagem de código (GitHub).",
      en: "Version control system (Git) and code hosting platform (GitHub).",
    },
    experience: {
      pt: "Uso no dia a dia pra versionar todos os meus projetos acadêmicos e pessoais.",
      en: "Used daily to version all of my academic and personal projects.",
    },
  }),
  skill({
    id: "linux",
    category: "tools",
    name: "Linux",
    icon: "devicon-linux-plain",
    level: 2,
    summary: {
      pt: "Sistema operacional open-source, base de grande parte das ferramentas de cybersecurity (ex: Kali Linux).",
      en: "Open-source operating system, the base of most cybersecurity tooling (e.g. Kali Linux).",
    },
    experience: {
      pt: "Uso o Kali Linux pra explorar ferramentas de cybersecurity por conta própria.",
      en: "I use Kali Linux to explore cybersecurity tools on my own.",
    },
  }),
];
