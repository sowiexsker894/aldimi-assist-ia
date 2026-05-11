export interface AppEnvironment {
  production: boolean;
  /** Origen del API (vacío = rutas relativas al host del portal; p. ej. `ng serve` + proxy). */
  apiBaseUrl: string;
}
