import { environment } from '../../../environments/environment';

/** Ruta al NLP; con proxy dev: `/nlp/v1/...` → service-nlp en puerto 8001. */
export function nlpApiUrl(pathWithinApi: string): string {
  const normalized = pathWithinApi.replace(/^\/+/, '');
  const base = environment.nlpApiBaseUrl.replace(/\/+$/, '');
  if (base) {
    return `${base}/${normalized}`;
  }
  return `/nlp/${normalized}`;
}
