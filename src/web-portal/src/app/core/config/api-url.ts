import { environment } from '../../../environments/environment';

/** Ruta absoluta del API, p. ej. `/api/v1/auth/login` o con origen si `apiBaseUrl` está definido. */
export function apiUrl(path: string): string {
  const base = environment.apiBaseUrl.replace(/\/+$/, '');
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return base ? `${base}${normalized}` : normalized;
}
