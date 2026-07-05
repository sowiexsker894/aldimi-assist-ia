import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { extractHttpError } from '../../core/utils/http-error';
import {
  DailyReportService,
  type DailyReportRow,
} from '../../core/services/daily-report.service';
import {
  PatientFamilyService,
  type FamilyMemberRow,
} from '../../core/services/patient-family.service';
import {
  PatientService,
  type PatientRow,
} from '../../core/services/patient.service';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

@Component({
  selector: 'app-patient-detail',
  imports: [RouterLink, UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="space-y-6 p-6">
      <a
        routerLink="/app/pacientes"
        class="inline-block text-sm text-primary hover:underline"
      >
        ← Volver a pacientes
      </a>

      @if (loadError()) {
        <p class="text-sm text-accent" role="alert">{{ loadError() }}</p>
      } @else if (loading()) {
        <p class="text-sm text-muted-foreground">Cargando…</p>
      } @else if (patient()) {
        <app-ui-card [title]="patient()!.full_name" [padding]="'md'">
          <dl class="grid gap-2 text-sm sm:grid-cols-2">
            <div>
              <dt class="text-muted-foreground">DNI</dt>
              <dd class="font-medium text-foreground">{{ patient()!.dni || '—' }}</dd>
            </div>
            <div>
              <dt class="text-muted-foreground">Fecha de ingreso</dt>
              <dd class="font-medium text-foreground">
                {{ formatDate(patient()!.created_at) }}
              </dd>
            </div>
            <div>
              <dt class="text-muted-foreground">Sexo</dt>
              <dd class="font-medium text-foreground">{{ patient()!.sexo || '—' }}</dd>
            </div>
            <div>
              <dt class="text-muted-foreground">Fecha nacimiento</dt>
              <dd class="font-medium text-foreground">
                {{ patient()!.fecha_nacimiento || '—' }}
              </dd>
            </div>
            <div class="sm:col-span-2">
              <dt class="text-muted-foreground">Dirección</dt>
              <dd class="font-medium text-foreground">
                {{ patient()!.direccion || '—' }}
              </dd>
            </div>
          </dl>
        </app-ui-card>

        <app-ui-card title="Familiares" [padding]="'md'">
          @if (familyLoading()) {
            <p class="text-sm text-muted-foreground">Cargando familiares…</p>
          } @else if (!family().length) {
            <p class="text-sm text-muted-foreground">Sin familiares registrados.</p>
          } @else {
            <ul class="divide-y divide-border rounded-md border border-border">
              @for (f of family(); track f.id) {
                <li class="px-4 py-3 text-sm">
                  <p class="font-medium text-foreground">{{ f.full_name }}</p>
                  <p class="text-muted-foreground">
                    Doc: {{ f.document_number || '—' }} · Tel:
                    {{ f.phone || '—' }}
                  </p>
                </li>
              }
            </ul>
          }

          @if (showFamilyForm()) {
            <div class="mt-4 grid gap-3 rounded-md border border-border p-4 sm:grid-cols-2">
              <app-ui-input
                label="Nombre completo"
                inputId="fam-add-name"
                [(value)]="famName"
              />
              <app-ui-input
                label="Documento"
                inputId="fam-add-doc"
                [(value)]="famDoc"
              />
              <app-ui-input label="Teléfono" inputId="fam-add-phone" [(value)]="famPhone" />
              <app-ui-input
                label="Correo (opcional)"
                inputId="fam-add-email"
                [(value)]="famEmail"
              />
              @if (familyError()) {
                <p class="sm:col-span-2 text-sm text-accent" role="alert">
                  {{ familyError() }}
                </p>
              }
              <div class="flex gap-2 sm:col-span-2">
                <app-ui-button
                  variant="primary"
                  (clicked)="saveFamily()"
                  [disabled]="familyBusy()"
                >
                  Guardar familiar
                </app-ui-button>
                <app-ui-button variant="ghost" (clicked)="showFamilyForm.set(false)">
                  Cancelar
                </app-ui-button>
              </div>
            </div>
          } @else {
            <div class="mt-4">
              <app-ui-button variant="secondary" (clicked)="showFamilyForm.set(true)">
                Añadir familiar
              </app-ui-button>
            </div>
          }
        </app-ui-card>

        <app-ui-card title="Reportes diarios" [padding]="'md'">
          <label
            class="mb-1.5 block text-sm font-medium text-foreground"
            for="daily-report-text"
          >
            Nuevo reporte
          </label>
          <textarea
            id="daily-report-text"
            class="w-full rounded-lg border border-border bg-surface-elevated px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
            rows="3"
            maxlength="500"
            placeholder="Reporte corto del día (1–3 oraciones)"
            [value]="reportText()"
            (input)="onReportInput($event)"
          ></textarea>
          @if (reportError()) {
            <p class="mt-2 text-sm text-accent" role="alert">{{ reportError() }}</p>
          }
          @if (reportMessage()) {
            <p class="mt-2 text-sm text-foreground" role="status">{{ reportMessage() }}</p>
          }
          <div class="mt-4">
            <app-ui-button
              variant="primary"
              (clicked)="saveReport()"
              [disabled]="reportBusy()"
            >
              {{ reportBusy() ? 'Guardando…' : 'Guardar reporte' }}
            </app-ui-button>
          </div>

          <div class="mt-8">
            <h3 class="mb-3 text-sm font-semibold text-foreground">
              Historial de análisis
            </h3>
            @if (reportsLoading()) {
              <p class="text-sm text-muted-foreground">Cargando historial…</p>
            } @else if (!reports().length) {
              <p class="text-sm text-muted-foreground">Sin reportes registrados.</p>
            } @else {
              <ul class="divide-y divide-border rounded-md border border-border">
                @for (r of reports(); track r.id) {
                  <li class="px-4 py-3 text-sm">
                    <div class="mb-1 flex flex-wrap items-center gap-2">
                      <time class="text-muted-foreground">{{
                        formatDateTime(r.created_at)
                      }}</time>
                      @if (r.sentiment_label) {
                        <span
                          class="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-foreground"
                        >
                          {{ r.sentiment_label }}
                        </span>
                      }
                    </div>
                    <p class="text-foreground">{{ r.text_content }}</p>
                  </li>
                }
              </ul>
            }
          </div>
        </app-ui-card>
      }
    </div>
  `,
})
export class PatientDetailComponent implements OnInit {
  private readonly patientSvc = inject(PatientService);
  private readonly route = inject(ActivatedRoute);
  private readonly dailyReportSvc = inject(DailyReportService);
  private readonly familySvc = inject(PatientFamilyService);

  protected readonly patient = signal<PatientRow | null>(null);
  protected readonly loading = signal(true);
  protected readonly loadError = signal<string | null>(null);

  protected readonly family = signal<FamilyMemberRow[]>([]);
  protected readonly familyLoading = signal(true);
  protected readonly showFamilyForm = signal(false);
  protected readonly famName = signal('');
  protected readonly famDoc = signal('');
  protected readonly famPhone = signal('');
  protected readonly famEmail = signal('');
  protected readonly familyBusy = signal(false);
  protected readonly familyError = signal<string | null>(null);

  protected readonly reports = signal<DailyReportRow[]>([]);
  protected readonly reportsLoading = signal(true);
  protected readonly reportText = signal('');
  protected readonly reportBusy = signal(false);
  protected readonly reportError = signal<string | null>(null);
  protected readonly reportMessage = signal<string | null>(null);

  private patientId = 0;

  async ngOnInit(): Promise<void> {
    const idParam = this.route.snapshot.paramMap.get('id');
    this.patientId = Number(idParam);
    if (!this.patientId || Number.isNaN(this.patientId)) {
      this.loadError.set('Identificador de paciente inválido.');
      this.loading.set(false);
      return;
    }
    await Promise.all([this.loadPatient(), this.loadReports(), this.loadFamily()]);
  }

  protected onReportInput(event: Event): void {
    this.reportText.set((event.target as HTMLTextAreaElement).value);
  }

  protected async saveReport(): Promise<void> {
    this.reportError.set(null);
    this.reportMessage.set(null);
    const text = this.reportText().trim();
    if (!text) {
      this.reportError.set('Escriba un reporte antes de guardar.');
      return;
    }
    this.reportBusy.set(true);
    try {
      await this.dailyReportSvc.create(this.patientId, text);
      this.reportText.set('');
      this.reportMessage.set('Reporte guardado.');
      await this.loadReports();
    } catch (e: unknown) {
      this.reportError.set(extractHttpError(e, 'No se pudo guardar el reporte.'));
    } finally {
      this.reportBusy.set(false);
    }
  }

  protected async saveFamily(): Promise<void> {
    const name = this.famName().trim();
    if (!name) {
      this.familyError.set('El nombre del familiar es obligatorio.');
      return;
    }
    this.familyBusy.set(true);
    this.familyError.set(null);
    try {
      await this.familySvc.add(this.patientId, {
        full_name: name,
        document_number: this.famDoc().trim() || undefined,
        phone: this.famPhone().trim() || undefined,
        email: this.famEmail().trim() || undefined,
      });
      this.famName.set('');
      this.famDoc.set('');
      this.famPhone.set('');
      this.famEmail.set('');
      this.showFamilyForm.set(false);
      await this.loadFamily();
    } catch (e: unknown) {
      this.familyError.set(extractHttpError(e, 'No se pudo registrar el familiar.'));
    } finally {
      this.familyBusy.set(false);
    }
  }

  protected formatDate(iso: string): string {
    return new Date(iso).toLocaleDateString('es-PE', { dateStyle: 'medium' });
  }

  protected formatDateTime(iso: string): string {
    return new Date(iso).toLocaleString('es-PE', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  }

  private async loadPatient(): Promise<void> {
    this.loading.set(true);
    this.loadError.set(null);
    try {
      this.patient.set(await this.patientSvc.get(this.patientId));
    } catch (e: unknown) {
      this.loadError.set(extractHttpError(e, 'No se pudo cargar el paciente.'));
    } finally {
      this.loading.set(false);
    }
  }

  private async loadFamily(): Promise<void> {
    this.familyLoading.set(true);
    try {
      this.family.set(await this.familySvc.list(this.patientId));
    } catch {
      this.family.set([]);
    } finally {
      this.familyLoading.set(false);
    }
  }

  private async loadReports(): Promise<void> {
    this.reportsLoading.set(true);
    try {
      this.reports.set(await this.dailyReportSvc.list(this.patientId));
    } catch {
      this.reports.set([]);
    } finally {
      this.reportsLoading.set(false);
    }
  }
}
