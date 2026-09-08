// Imagens de seed/placeholder vivem em frontend/public/images/ (mesma origem
// do site). Imagens enviadas pelo admin vivem em backend/uploads/, servidas
// pela API — que roda numa origem DIFERENTE do frontend (docs/deploy/
// caddy-nginx.md usa subdomínios separados: portfolio.dominio vs
// api.portfolio.dominio). Por isso "/uploads/x.png" (relativo, do jeito que
// a API devolve) precisa ganhar o domínio da API antes de virar um <img src>.
export function resolveImageUrl(url: string | null, apiBase: string): string | null {
  if (!url) return url;
  if (url.startsWith("/uploads/")) return `${apiBase}${url}`;
  return url;
}
