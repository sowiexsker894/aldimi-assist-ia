import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';

@Component({
  selector: 'app-ui-card',
  standalone: true,
  templateUrl: './ui-card.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UiCard {
  readonly title = input<string>('');
  readonly padding = input<'none' | 'sm' | 'md' | 'lg'>('md');

  protected readonly bodyPaddingClass = computed(() => {
    switch (this.padding()) {
      case 'none':
        return '';
      case 'sm':
        return 'p-3';
      case 'md':
        return 'p-5';
      case 'lg':
        return 'p-8';
    }
  });
}
