# Animações — Especificação

| Animação | Técnica | Fallback |
|---|---|---|
| Digitação do terminal | setTimeout recursivo 50ms/char | texto fixo (reduced-motion) |
| Cursor terminal | `steps(2)` blink infinito | estático |
| Reveal on scroll | CSS `animation-timeline: view()` | classe `.visible` via IntersectionObserver |
| Hover cards | translateY(-4px) + glow, 200ms ease | — |
| Barra de nível skill | width 0→N% 600ms ease | aparece cheia |
| Transição de tema | `transition: background .3s, color .3s` | — |

Global: `@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important } }`
