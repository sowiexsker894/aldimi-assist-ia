import { HttpErrorResponse } from '@angular/common/http';

/** Extrae un mensaje legible de un error HTTP de FastAPI. */
export function extractHttpError(err: unknown, fallback: string): string {
  if (!(err instanceof HttpErrorResponse)) return fallback;
  const errBody = err.error as Record<string, unknown> | null | undefined;
  if (!errBody || typeof errBody !== 'object') return err.message || fallback;

  const detail = errBody['detail'];

  // 422 gatekeeper: { status: "rejected", rejection: { code, message } }
  if (detail && typeof detail === 'object' && 'rejection' in detail) {
    const r = (detail as { rejection?: { message?: string } }).rejection;
    return r?.message ?? fallback;
  }
  if (typeof detail === 'string') return detail;
  if (detail !== undefined) return JSON.stringify(detail);
  return err.message || fallback;
}
