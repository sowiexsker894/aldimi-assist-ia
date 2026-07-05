import { HttpErrorResponse } from '@angular/common/http';
import {
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { MarkdownComponent } from 'ngx-markdown';

import { UiButton, UiInput } from '../../shared/ui';
import { NlpChatHistoryItem, NlpChatService } from '../../core/services/nlp-chat.service';

type TranscriptLine = { role: 'user' | 'assistant'; text: string };

@Component({
  selector: 'app-guest-chat',
  imports: [UiButton, UiInput, MarkdownComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './guest-chat.component.html',
  styleUrl: './guest-chat.component.scss',
})
export class GuestChatComponent {
  protected readonly draft = signal('');
  protected readonly transcript = signal<TranscriptLine[]>([]);
  protected readonly loading = signal(false);
  protected readonly error = signal<string | null>(null);

  private readonly chatScroll = viewChild<ElementRef<HTMLDivElement>>('chatScroll');
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
    this.scheduleScrollToBottom();

    this.nlp.chat({ message: t, history }).subscribe({
      next: (res) => {
        this.loading.set(false);
        this.transcript.update((x) => [...x, { role: 'assistant', text: res.reply }]);
        this.scheduleScrollToBottom();
      },
      error: (err: HttpErrorResponse) => {
        this.loading.set(false);
        const detail =
          err.error && typeof err.error === 'object' && err.error !== null && 'detail' in err.error
            ? (err.error as { detail: unknown }).detail
            : undefined;
        const msg =
          typeof detail === 'string'
            ? detail
            : detail !== undefined
              ? JSON.stringify(detail)
              : err.message ||
                'No se pudo obtener respuesta. ¿Está el servicio NLP en marcha (puerto 8001)?';
        this.error.set(msg);
        this.transcript.update((x) => x.slice(0, -1));
        this.draft.set(t);
        this.scheduleScrollToBottom();
      },
    });
  }

  private scheduleScrollToBottom(): void {
    setTimeout(() => {
      const el = this.chatScroll()?.nativeElement;
      if (el) {
        el.scrollTop = el.scrollHeight;
      }
    });
  }
}
