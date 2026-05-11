import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UiButton, UiCard, UiInput } from './shared/ui';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, UiButton, UiCard, UiInput],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('ALDIMI-Assist');
  protected readonly demoField = signal('');
  /** Prueba de UiInput con mensaje de error si el texto tiene menos de 3 caracteres. */
  protected readonly demoFieldError = signal('');

  protected onDemoClick(_ev: MouseEvent): void {
    // placeholder for future analytics / actions
  }
}
