import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

@Component({
  selector: 'app-login',
  imports: [UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div
      class="flex min-h-dvh items-center justify-center bg-surface p-6"
    >
      <app-ui-card class="w-full max-w-md" title="Iniciar sesión" [padding]="'md'">
        <p class="mb-4 text-sm text-muted-foreground">
          Usa las credenciales del entorno (p. ej. semilla
          <code class="text-xs">admin@aldimi.local</code>
          tras migración 002).
        </p>
        <app-ui-input
          label="Correo"
          inputId="login-email"
          placeholder="correo@ejemplo.org"
          type="email"
          [(value)]="email"
        />
        <app-ui-input
          class="mt-4"
          label="Contraseña"
          inputId="login-password"
          placeholder="Contraseña"
          type="password"
          [(value)]="password"
        />
        @if (errorMsg()) {
          <p class="mt-3 text-sm text-accent" role="alert">{{ errorMsg() }}</p>
        }
        <div class="mt-6">
          <app-ui-button
            class="w-full"
            variant="primary"
            (clicked)="submit()"
            [disabled]="loading()"
          >
            {{ loading() ? 'Entrando…' : 'Entrar' }}
          </app-ui-button>
        </div>
      </app-ui-card>
    </div>
  `,
})
export class LoginComponent {
  private readonly auth = inject(AuthService);

  protected readonly email = signal('');
  protected readonly password = signal('');
  protected readonly errorMsg = signal<string | null>(null);
  protected readonly loading = signal(false);

  protected async submit(): Promise<void> {
    this.errorMsg.set(null);
    this.loading.set(true);
    try {
      await this.auth.login(this.email(), this.password());
    } catch {
      this.errorMsg.set('No se pudo iniciar sesión. Revisa credenciales.');
    } finally {
      this.loading.set(false);
    }
  }
}
