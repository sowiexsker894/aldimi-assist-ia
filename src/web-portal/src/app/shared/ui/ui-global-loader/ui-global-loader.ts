import { ChangeDetectionStrategy, Component, inject } from '@angular/core';

import { LoadingService } from '../../../core/services/loading.service';

@Component({
  selector: 'app-ui-global-loader',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @if (loading.visible()) {
      <div
        class="fixed inset-0 z-[200] flex items-center justify-center bg-surface-dark/45 backdrop-blur-[2px]"
        role="alert"
        aria-live="polite"
        aria-busy="true"
      >
        <div
          class="flex max-w-sm flex-col items-center gap-4 rounded-xl border border-border bg-surface-elevated px-8 py-7 shadow-xl"
        >
          <div
            class="h-11 w-11 shrink-0 animate-spin rounded-full border-[3px] border-primary border-t-transparent"
            aria-hidden="true"
          ></div>
          <p class="text-center text-sm text-muted-foreground">
            {{ loading.message() || 'Por favor espere…' }}
          </p>
        </div>
      </div>
    }
  `,
})
export class UiGlobalLoader {
  protected readonly loading = inject(LoadingService);
}
