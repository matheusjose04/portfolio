import type { Lang } from "../i18n/utils";

export interface ApiProject {
  id: number;
  title: string;
  slug: string;
  description: string;
  why: string;
  category: "complete" | "small";
  skills: string[];
  github_url: string | null;
  demo_url: string | null;
  image_url: string | null;
  featured: boolean;
  created_at: string;
}

interface FallbackProject {
  id: number;
  title: string;
  slug: string;
  description: { pt: string; en: string };
  why: { pt: string; en: string };
  category: "complete" | "small";
  skills: string[];
  image_url: string;
}

// Espelha os placeholders de backend/seed.py — usados só quando a API
// está offline (docs/componentes/ProjectsGrid.md: "fallback p/ dados locais").
const DESCRIPTION = {
  pt: "Projeto de exemplo (placeholder) — substitua pelos seus projetos reais no CONTENT.md ou pelo painel /admin.",
  en: "Example (placeholder) project — replace it with your real projects via CONTENT.md or the /admin panel.",
};
const WHY = {
  pt: "Placeholder — adicione a motivação real deste projeto.",
  en: "Placeholder — add the real motivation behind this project.",
};

const FALLBACK_PROJECTS: FallbackProject[] = [
  {
    id: 1,
    title: "Sistema de Gestão X",
    slug: "sistema-de-gestao-x",
    description: DESCRIPTION,
    why: WHY,
    category: "complete",
    skills: ["python", "fastapi", "sqlite"],
    image_url: "/images/projects/placeholder-complete-1.svg",
  },
  {
    id: 2,
    title: "API de Autenticação Y",
    slug: "api-de-autenticacao-y",
    description: DESCRIPTION,
    why: WHY,
    category: "complete",
    skills: ["python", "fastapi", "sqlite", "git"],
    image_url: "/images/projects/placeholder-complete-2.svg",
  },
  {
    id: 3,
    title: "CLI de Automação Z",
    slug: "cli-de-automacao-z",
    description: DESCRIPTION,
    why: WHY,
    category: "small",
    skills: ["python", "git"],
    image_url: "/images/projects/placeholder-small-1.svg",
  },
  {
    id: 4,
    title: "Bot de Discord W",
    slug: "bot-de-discord-w",
    description: DESCRIPTION,
    why: WHY,
    category: "small",
    skills: ["python", "docker"],
    image_url: "/images/projects/placeholder-small-2.svg",
  },
];

export function resolveFallback(lang: Lang): ApiProject[] {
  return FALLBACK_PROJECTS.map((p) => ({
    id: p.id,
    title: p.title,
    slug: p.slug,
    description: p.description[lang],
    why: p.why[lang],
    category: p.category,
    skills: p.skills,
    github_url: null,
    demo_url: null,
    image_url: p.image_url,
    featured: false,
    created_at: "1970-01-01T00:00:00Z",
  }));
}
