import { ChangeDetectionStrategy, Component, computed, input, output } from '@angular/core';

export type UiButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';

@Component({
  selector: 'app-ui-button',
  standalone: true,
  templateUrl: './ui-button.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UiButton {
  readonly variant = input<UiButtonVariant>('primary');
  readonly disabled = input(false);
  readonly type = input<'button' | 'submit'>('button');
  readonly clicked = output<MouseEvent>();

  protected readonly hostClass = computed(() => {
    const base =
      'inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-surface disabled:pointer-events-none disabled:opacity-50';
    switch (this.variant()) {
      case 'primary':
        return `${base} bg-primary text-white hover:bg-primary/90`;
      case 'secondary':
        return `${base} border-2 border-primary bg-transparent text-primary hover:bg-primary/5`;
      case 'ghost':
        return `${base} bg-transparent text-primary hover:bg-primary/5`;
      case 'danger':
        return `${base} border-2 border-accent bg-transparent text-accent hover:bg-accent/10`;
    }
  });

  protected onClick(ev: MouseEvent): void {
    if (this.disabled()) {
      ev.preventDefault();
      ev.stopPropagation();
      return;
    }
    this.clicked.emit(ev);
  }
}
