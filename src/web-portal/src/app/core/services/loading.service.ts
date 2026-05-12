import { computed, Injectable, signal } from '@angular/core';

/**
 * Indicador de carga global apilable: varias operaciones concurrentes
 * incrementan el contador; el overlay permanece hasta el último `hide()`.
 */
@Injectable({ providedIn: 'root' })
export class LoadingService {
  private readonly _depth = signal(0);

  /** Mensaje opcional bajo el indicador. */
  readonly message = signal<string | null>(null);

  readonly visible = computed(() => this._depth() > 0);

  show(text?: string | null): void {
    if (text !== undefined) {
      this.message.set(text);
    }
    this._depth.update((d) => d + 1);
  }

  hide(): void {
    this._depth.update((d) => Math.max(0, d - 1));
    if (this._depth() === 0) {
      this.message.set(null);
    }
  }
}
