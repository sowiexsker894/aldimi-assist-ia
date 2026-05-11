import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

import { NlpChatHistoryItem, NlpChatService } from '../../core/services/nlp-chat.service';

type TranscriptLine = { role: 'user' | 'assistant'; text: string };

@Component({
  selector: 'app-guest-chat',
  imports: [UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="mx-auto flex h-full min-h-[calc(100dvh-4.5rem)] max-w-3xl flex-col gap-4 p-4 md:p-6">
      <app-ui-card title="Chat invitado" [padding]="'md'">
        <p class="mb-4 text-sm text-muted-foreground">
          Preguntas frecuentes: las respuestas las genera el asistente configurado en el
          backend (Azure o modo desarrollo stub).
        </p>
        <div
          class="max-h-96 space-y-2 overflow-y-auto rounded-lg border border-border bg-surface-elevated p-3 text-sm"
          aria-live="polite"
        >
          @for (line of transcript(); track $index) {
            <p class="text-foreground">
              <span class="font-medium text-muted-foreground"
                >{{ line.role === 'user' ? 'Tú' : 'Asistente' }}:</span
              >
              {{ line.text }}
            </p>
          } @empty {
            <p class="text-muted-foreground">Escribe un mensaje para comenzar.</p>
          }
        </div>
        @if (error()) {
          <p class="mt-2 rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive">
            {{ error() }}
          </p>
        }
        <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-end">
          <app-ui-input
            class="min-w-0 flex-1"
            label="Mensaje"
            inputId="guest-chat-input"
            placeholder="Escribe aquí…"
            [disabled]="loading()"
            [(value)]="draft"
          />
          <app-ui-button
            variant="primary"
            [disabled]="loading()"
            (clicked)="send()"
            >{{ loading() ? 'Enviando…' : 'Enviar' }}</app-ui-button
          >
        </div>
      </app-ui-card>
    </div>
  `,
})
export class GuestChatComponent {
  protected readonly draft = signal('');
  protected readonly transcript = signal<TranscriptLine[]>([]);
  protected readonly loading = signal(false);
  protected readonly error = signal<string | null>(null);

  private readonly nlp = inject(NlpChatService);

  protected send(): void {
    const t = this.draft().trim();
    if (!t || this.loading()) {
      return;
    }
    this.error.set(null);

    const prior = this.transcript();
    const history: NlpChatHistoryItem[] = prior.map((line) => ({
      role: line.role,
      content: line.text,
    }));

    this.draft.set('');
    this.loading.set(true);
    this.transcript.update((x) => [...x, { role: 'user', text: t }]);

    this.nlp.chat({ message: t, history }).subscribe({
      next: (res) => {
        this.loading.set(false);
        this.transcript.update((x) => [...x, { role: 'assistant', text: res.reply }]);
      },
      error: (err: HttpErrorResponse) => {
        this.loading.set(false);
        const detail = err.error && typeof err.error === 'object' && err.error !== null && 'detail' in err.error
          ? (err.error as { detail: unknown }).detail
          : undefined;
        const msg =
          typeof detail === 'string'
            ? detail
            : detail !== undefined
              ? JSON.stringify(detail)
              : err.message || 'No se pudo obtener respuesta. ¿Está el servicio NLP en marcha (puerto 8001)?';
        this.error.set(msg);
        this.transcript.update((x) => x.slice(0, -1));
        this.draft.set(t);
      },
    });
  }
}
