// Si portal y API comparten host (reverse proxy en /api), mantén apiBaseUrl en ''.
// Si el API está en otro origen, define la URL base sin barra final (p. ej. https://api.ejemplo.com).
import type { AppEnvironment } from './environment.model';

export const environment: AppEnvironment = {
  production: true,
  apiBaseUrl: '',
  nlpApiBaseUrl: '',
};
