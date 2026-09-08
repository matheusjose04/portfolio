const STORAGE_KEY = "admin_token";

export const API_BASE = import.meta.env.PUBLIC_API_URL ?? "http://localhost:8000";

export function getToken(): string | null {
  return localStorage.getItem(STORAGE_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(STORAGE_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(STORAGE_KEY);
}

// Anexa o Bearer token em toda chamada; se a API responder 401/403
// (token ausente/expirado/inválido), limpa e manda pro login —
// docs/componentes/Admin.md: "401/403 em qualquer chamada → limpa
// token, redireciona pro login".
export async function adminFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers = new Headers(init.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers });

  if (res.status === 401 || res.status === 403) {
    clearToken();
    window.location.href = "/admin/login";
  }

  return res;
}
