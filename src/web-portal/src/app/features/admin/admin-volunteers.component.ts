import {
  ChangeDetectionStrategy,
  Component,
  inject,
  signal,
} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../../core/config/api-url';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

@Component({
  selector: 'app-admin-volunteers',
  imports: [UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="p-6">
      <app-ui-card title="Alta de voluntario" [padding]="'md'">
        <p class="mb-4 text-sm text-muted-foreground">
          Solo administradores. El voluntario podrá iniciar sesión si
          <code class="text-xs">is_active</code> es verdadero en el servidor.
        </p>
        <app-ui-input
          label="Nombre completo"
          inputId="vol-name"
          placeholder="Nombre y apellidos"
          [(value)]="fullName"
        />
        <app-ui-input
          class="mt-4"
          label="Correo"
          inputId="vol-email"
          type="email"
          placeholder="voluntario@ejemplo.org"
          [(value)]="email"
        />
        <app-ui-input
          class="mt-4"
          label="Contraseña inicial"
          inputId="vol-password"
          type="password"
          placeholder="Contraseña temporal"
          [(value)]="password"
        />
        @if (message()) {
          <p class="mt-3 text-sm text-foreground" role="status">{{ message() }}</p>
        }
        @if (errorMsg()) {
          <p class="mt-3 text-sm text-accent" role="alert">{{ errorMsg() }}</p>
        }
        <div class="mt-6">
          <app-ui-button
            variant="primary"
            (clicked)="submit()"
            [disabled]="busy()"
          >
            {{ busy() ? 'Creando…' : 'Crear voluntario' }}
          </app-ui-button>
        </div>
      </app-ui-card>
    </div>
  `,
})
export class AdminVolunteersComponent {
  private readonly http = inject(HttpClient);

  protected readonly fullName = signal('');
  protected readonly email = signal('');
  protected readonly password = signal('');
  protected readonly busy = signal(false);
  protected readonly message = signal<string | null>(null);
  protected readonly errorMsg = signal<string | null>(null);

  protected async submit(): Promise<void> {
    this.message.set(null);
    this.errorMsg.set(null);
    this.busy.set(true);
    try {
      const res = await firstValueFrom(
        this.http.post<{
          id: number;
          email: string;
          full_name: string;
          roles: string[];
        }>(apiUrl('/api/v1/admin/volunteers'), {
          full_name: this.fullName(),
          email: this.email(),
          password: this.password(),
        }),
      );
      this.message.set(`Creado: ${res.full_name} (${res.email}) · id ${res.id}`);
      this.password.set('');
    } catch (e: unknown) {
      const err = e as { error?: { detail?: string } };
      const detail =
        typeof err?.error?.detail === 'string'
          ? err.error.detail
          : 'No se pudo crear el voluntario.';
      this.errorMsg.set(detail);
    } finally {
      this.busy.set(false);
    }
  }
}
