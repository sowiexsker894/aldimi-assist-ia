import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

@Component({
  selector: 'app-guest-chat',
  imports: [UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="mx-auto flex h-full min-h-[calc(100dvh-4.5rem)] max-w-3xl flex-col gap-4 p-4 md:p-6">
      <app-ui-card title="Chat invitado" [padding]="'md'">
        <p class="mb-4 text-sm text-muted-foreground">
          Vista previa: solo texto. El flujo completo del asistente se integrará más
          adelante.
        </p>
        <div
          class="max-h-64 space-y-2 overflow-y-auto rounded-lg border border-border bg-surface-elevated p-3 text-sm"
          aria-live="polite"
        >
          @for (line of messages(); track $index) {
            <p class="text-foreground">{{ line }}</p>
          } @empty {
            <p class="text-muted-foreground">Escribe un mensaje para comenzar.</p>
          }
        </div>
        <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-end">
          <app-ui-input
            class="min-w-0 flex-1"
            label="Mensaje"
            inputId="guest-chat-input"
            placeholder="Escribe aquí…"
            [(value)]="draft"
          />
          <app-ui-button variant="primary" (clicked)="send()">Enviar</app-ui-button>
        </div>
      </app-ui-card>
    </div>
  `,
})
export class GuestChatComponent {
  protected readonly draft = signal('');
  protected readonly messages = signal<string[]>([]);

  protected send(): void {
    const t = this.draft().trim();
    if (!t) {
      return;
    }
    this.messages.update((m) => [...m, t]);
    this.draft.set('');
  }
}
