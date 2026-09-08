# Upload de Imagens — Especificação

- POST /api/upload (só admin): aceita png/jpg/webp, máx 2MB
- Salva em `backend/uploads/` com nome `{slug}-{timestamp}.{ext}`
- Servida estaticamente em `/uploads/` (StaticFiles mount)
- Frontend envia com `multipart/form-data` e usa a `image_url` retornada
- Rejeitar: exe, pdf, svg com script (validar MIME real, não só extensão)
