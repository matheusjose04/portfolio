# ThemeToggle — Especificação

## Lógica (estado único de verdade: `document.documentElement.dataset.theme`)
1. Base.astro roda ANTES do paint: lê localStorage → aplica tema (anti-flash)
2. Toggle: inverte valor, grava localStorage, troca ícone
3. `color-scheme` sincronizado via CSS (`:root { color-scheme: dark }`)

## Código-chave (referência)
```ts
const next = root.dataset.theme === "dark" ? "light" : "dark";
root.dataset.theme = next;
localStorage.setItem("theme", next);
```

## Teste de aceite
Mudar tema do OS + apagar localStorage → site abre com tema do OS.
