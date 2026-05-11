import { ChangeDetectionStrategy, Component, input, model } from '@angular/core';

@Component({
  selector: 'app-ui-input',
  standalone: true,
  templateUrl: './ui-input.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UiInput {
  readonly value = model<string>('');
  readonly label = input.required<string>();
  readonly inputId = input.required<string>();
  readonly placeholder = input('');
  readonly type = input('text');
  readonly errorMessage = input<string | null>(null);

  protected onInput(ev: Event): void {
    const el = ev.target as HTMLInputElement;
    this.value.set(el.value);
  }
}
