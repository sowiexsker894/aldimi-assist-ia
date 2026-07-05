import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { RouterLink } from '@angular/router';
import { extractHttpError } from '../../core/utils/http-error';
import { DailyReportService } from '../../core/services/daily-report.service';
import {
  PatientService,
  type PatientRow,
} from '../../core/services/patient.service';
import { UiButton, UiCard, UiTabs } from '../../shared/ui';

@Component({
  selector: 'app-patients-list-tab',
  imports: [RouterLink, UiButton, UiCard],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <app-ui-card title="Pacientes registrados" [padding]="'md'">
      @if (error()) {
        <p class="text-sm text-accent" role="alert">{{ error() }}</p>
      } @else if (loading()) {
        <p class="text-sm text-muted-foreground">Cargando…</p>
      } @else if (!rows().length) {
        <p class="text-sm text-muted-foreground">No hay pacientes registrados.</p>
      } @else {
        <div class="overflow-x-auto">
          <table class="w-full min-w-[720px] text-left text-sm">
            <thead>
              <tr class="border-b border-border text-muted-foreground">
                <th class="px-3 py-2 font-medium">Nombre</th>
                <th class="px-3 py-2 font-medium">DNI</th>
                <th class="px-3 py-2 font-medium">Ingreso</th>
                <th class="px-3 py-2 font-medium">Acciones</th>
              </tr>
            </thead>
            <tbody>
              @for (p of rows(); track p.id) {
                <tr class="border-b border-border align-top last:border-0">
                  <td class="px-3 py-3 font-medium text-foreground">{{ p.full_name }}</td>
                  <td class="px-3 py-3 text-muted-foreground">{{ p.dni || '—' }}</td>
                  <td class="px-3 py-3 text-muted-foreground">
                    {{ formatDate(p.created_at) }}
                  </td>
                  <td class="px-3 py-3">
                    <div class="flex flex-wrap gap-2">
                      <app-ui-button variant="secondary" (clicked)="openReport(p.id)">
                        Reporte
                      </app-ui-button>
                      <a
                        [routerLink]="['/app/pacientes', p.id]"
                        class="inline-flex items-center justify-center rounded-lg border-2 border-primary px-4 py-2 text-sm font-medium text-primary hover:bg-primary/5"
                      >
                        Ver más
                      </a>
                    </div>
                    @if (reportPatientId() === p.id) {
                      <div class="mt-3 rounded-md border border-border bg-surface-elevated p-3">
                        <textarea
                          class="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
                          rows="2"
                          maxlength="500"
                          placeholder="Reporte corto del día (1–3 oraciones)"
                          [value]="reportText()"
                          (input)="onReportInput($event)"
                        ></textarea>
                        @if (reportError()) {
                          <p class="mt-2 text-sm text-accent" role="alert">
                            {{ reportError() }}
                          </p>
                        }
                        <div class="mt-2 flex gap-2">
                          <app-ui-button
                            variant="primary"
                            (clicked)="saveReport(p.id)"
                            [disabled]="reportBusy()"
                          >
                            {{ reportBusy() ? 'Guardando…' : 'Guardar' }}
                          </app-ui-button>
                          <app-ui-button variant="ghost" (clicked)="closeReport()">
                            Cancelar
                          </app-ui-button>
                        </div>
                      </div>
                    }
                  </td>
                </tr>
              }
            </tbody>
          </table>
        </div>
      }
    </app-ui-card>
  `,
})
export class PatientsListTabComponent implements OnInit {
  private readonly patientSvc = inject(PatientService);
  private readonly dailyReportSvc = inject(DailyReportService);

  protected readonly rows = signal<PatientRow[]>([]);
  protected readonly loading = signal(true);
  protected readonly error = signal<string | null>(null);

  protected readonly reportPatientId = signal<number | null>(null);
  protected readonly reportText = signal('');
  protected readonly reportBusy = signal(false);
  protected readonly reportError = signal<string | null>(null);

  async ngOnInit(): Promise<void> {
    await this.load();
  }

  async load(): Promise<void> {
    this.loading.set(true);
    this.error.set(null);
    try {
      this.rows.set(await this.patientSvc.list());
    } catch (e: unknown) {
      this.error.set(extractHttpError(e, 'No se pudo cargar la lista de pacientes.'));
    } finally {
      this.loading.set(false);
    }
  }

  protected formatDate(iso: string): string {
    return new Date(iso).toLocaleDateString('es-PE', { dateStyle: 'medium' });
  }

  protected openReport(patientId: number): void {
    this.reportPatientId.set(patientId);
    this.reportText.set('');
    this.reportError.set(null);
  }

  protected closeReport(): void {
    this.reportPatientId.set(null);
    this.reportText.set('');
    this.reportError.set(null);
  }

  protected onReportInput(event: Event): void {
    this.reportText.set((event.target as HTMLTextAreaElement).value);
  }

  protected async saveReport(patientId: number): Promise<void> {
    const text = this.reportText().trim();
    if (!text) {
      this.reportError.set('Escriba un reporte antes de guardar.');
      return;
    }
    this.reportBusy.set(true);
    this.reportError.set(null);
    try {
      await this.dailyReportSvc.create(patientId, text);
      this.closeReport();
    } catch (e: unknown) {
      this.reportError.set(extractHttpError(e, 'No se pudo guardar el reporte.'));
    } finally {
      this.reportBusy.set(false);
    }
  }
}
