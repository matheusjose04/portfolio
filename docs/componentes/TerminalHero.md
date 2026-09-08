# TerminalHero — Especificação

## Estrutura
```
┌─────────────────────────────┐
│ matheus@fullstack:~$ whoami │  <- digita caractere a caractere
│ > Desenvolvedor Fullstack   │  <- resposta aparece após "Enter"
│   & Cybersecurity           │
│ matheus@fullstack:~$ ls ./skills
│ > python typescript astro fastapi docker ...
└─────────────────────────────┘
        [foto]  [CV] [LinkedIn] [GitHub]
```

## Dados (i18n: `hero.terminal.lines` — array de {cmd, output})
```json
"lines": [
  { "cmd": "whoami", "output": "Desenvolvedor Fullstack & Cybersecurity" },
  { "cmd": "ls ./skills", "output": "python typescript astro fastapi react sql docker git" }
]
```

## Comportamento
- Digitação: intervalo ~50ms/char (use `setTimeout` recursivo, NÃO `setInterval`)
- Cursor: `▋` piscando via CSS `steps()` (`animation: blink 1s steps(2) infinite`)
- Loop: reinicia após 8s parado no fim
- Reduced-motion: mostra tudo de uma vez, sem animação
- Container: card `--surface`, borda `--border`, glow sutil, header com 3
  bolinhas (vermelho/amarelo/verde imitando janela de terminal)

## Foto
- `public/images/foto-perfil.jpg` (fallback: avatar placeholder SVG inline)
- Círculo 180px, `border: 3px solid var(--primary)`, hover: `box-shadow: var(--glow)`

## Botões (i18n: `hero.cta.*`)
- CV: `<a href="/cv-matheus.pdf" download>` — botão primário (glow)
- LinkedIn/GitHub: botão outline, `target="_blank" rel="noopener"`
