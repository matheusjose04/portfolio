# .env e Segredos — Especificação

## backend/.env (NUNCA commitar; .env.example commitado sem valores)
```
SECRET_KEY=            # openssl rand -hex 32
ADMIN_USER=admin
ADMIN_PASSWORD=        # trocar o admin123 em produção!
DATABASE_URL=sqlite:///./data/portfolio.db
ACCESS_TOKEN_EXPIRE_MINUTES=720
ORIGINS=https://portfolio.seudominio.com,http://localhost:4321
UPLOAD_DIR=./uploads
MAX_UPLOAD_MB=2
```

## frontend/.env
```
PUBLIC_API_URL=https://api.portfolio.seudominio.com
```

## Checklist de segurança
- [ ] .gitignore contém `.env` e `data/`
- [ ] SECRET_KEY de produção ≠ a do exemplo
- [ ] Senha do admin trocada após 1º login
- [ ] CORS ORIGINS não contém `*` em produção
