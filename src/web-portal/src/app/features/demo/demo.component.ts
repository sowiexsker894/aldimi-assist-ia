import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

@Component({
  selector: 'app-demo',
  imports: [UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './demo.component.html',
})
export class DemoComponent {
  protected readonly demoField = signal('');
  protected readonly demoFieldError = signal('');

  protected onDemoClick(_ev: MouseEvent): void {
    // reservado p. ej. analítica
  }
}
