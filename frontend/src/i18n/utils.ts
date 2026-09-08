import pt from "./pt.json";
import en from "./en.json";

export const languages = { pt, en } as const;
export type Lang = keyof typeof languages;

export function getLangFromUrl(url: URL): Lang {
  const [, first] = url.pathname.split("/");
  return first === "en" ? "en" : "pt";
}

function get(dict: Record<string, unknown>, path: string): string {
  let current: unknown = dict;
  for (const part of path.split(".")) {
    if (typeof current !== "object" || current === null || Array.isArray(current)) {
      return path;
    }
    current = (current as Record<string, unknown>)[part];
  }
  return typeof current === "string" ? current : path;
}

export function useTranslations(lang: Lang) {
  const dict = languages[lang] as unknown as Record<string, unknown>;
  return (key: string): string => get(dict, key);
}
