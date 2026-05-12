import { environment } from '../../../environments/environment';

/** Ruta al servicio de visión; con proxy dev: `/vision/v1/...` → service-vision (p. ej. puerto 8002). */
export function visionApiUrl(pathWithinApi: string): string {
  const normalized = pathWithinApi.replace(/^\/+/, '');
  const base = environment.visionApiBaseUrl.replace(/\/+$/, '');
  if (base) {
    return `${base}/${normalized}`;
  }
  return `/vision/${normalized}`;
}
