export interface AppEnvironment {
  production: boolean;
  /** Origen del API (vacío = rutas relativas al host del portal; p. ej. `ng serve` + proxy). */
  apiBaseUrl: string;
  /**
   * Base del microservicio NLP (sin barra final). Vacío = rutas relativas `/nlp/...` vía proxy.
   * En producción: URL absoluta si el NLP está en otro host.
   */
  nlpApiBaseUrl: string;
}
