import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../../core/config/api-url';
import { UiCard } from '../../shared/ui';

export interface PatientRow {
  id: number;
  full_name: string;
  dni: string | null;
}

@Component({
  selector: 'app-patients-list',
  imports: [RouterLink, UiCard],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="p-6">
      <app-ui-card title="Pacientes" [padding]="'md'">
        @if (error()) {
          <p class="text-sm text-accent" role="alert">{{ error() }}</p>
        } @else if (loading()) {
          <p class="text-sm text-muted-foreground">Cargando…</p>
        } @else if (!rows().length) {
          <p class="text-sm text-muted-foreground">No hay pacientes registrados.</p>
        } @else {
          <ul class="divide-y divide-border rounded-md border border-border">
            @for (p of rows(); track p.id) {
              <li>
                <a
                  [routerLink]="['/app/pacientes', p.id]"
                  class="flex items-center justify-between px-4 py-3 text-sm transition-colors hover:bg-muted/40"
                >
                  <span class="font-medium text-foreground">{{ p.full_name }}</span>
                  <span class="text-muted-foreground">
                    @if (p.dni) {
                      DNI {{ p.dni }}
                    } @else {
                      #{{ p.id }}
                    }
                  </span>
                </a>
              </li>
            }
          </ul>
        }
      </app-ui-card>
    </div>
  `,
})
export class PatientsListComponent implements OnInit {
  private readonly http = inject(HttpClient);

  protected readonly rows = signal<PatientRow[]>([]);
  protected readonly loading = signal(true);
  protected readonly error = signal<string | null>(null);

  async ngOnInit(): Promise<void> {
    this.loading.set(true);
    this.error.set(null);
    try {
      const list = await firstValueFrom(
        this.http.get<PatientRow[]>(apiUrl('/api/v1/patients')),
      );
      this.rows.set(list);
    } catch {
      this.error.set('No se pudo cargar la lista de pacientes.');
    } finally {
      this.loading.set(false);
    }
  }
}
