# Auth JWT — Especificação

## Env
```
SECRET_KEY=          # gerar: openssl rand -hex 32
ACCESS_TOKEN_EXPIRE_MINUTES=720
```

## Fluxo
1. POST /api/auth/login → verifica bcrypt → cria JWT
   `sub=username, exp=agora+12h` (HS256)
2. Dependência `get_current_admin`: decoda Bearer token; inválido/expirado → 401
3. Hash de senha NUNCA retornado em nenhum schema

## Teste obrigatório
- Senha errada → 401
- Token inválido no POST /api/projects → 401
- Token válido → 201
