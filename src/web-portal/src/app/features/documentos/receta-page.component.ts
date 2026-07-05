import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { DocumentService } from '../../core/services/document.service';
import { LoadingService } from '../../core/services/loading.service';
import { PatientService } from '../../core/services/patient.service';
import { extractHttpError } from '../../core/utils/http-error';
import { UiButton, UiCard, UiInput } from '../../shared/ui';
import { DocumentUploadComponent } from './document-upload.component';

type Phase = 'upload' | 'reviewing' | 'done';

export interface PatientOption {
  id: number;
  full_name: string;
}

const str = (v: unknown): string =>
  v == null || String(v) === 'null' ? '' : String(v);

@Component({
  selector: 'app-receta-page',
  imports: [UiButton, UiCard, UiInput, DocumentUploadComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './receta-page.component.html',
})
export class RecetaPageComponent implements OnInit {
  protected readonly loading = inject(LoadingService);
  private readonly docSvc = inject(DocumentService);
  private readonly patientSvc = inject(PatientService);

  protected readonly phase = signal<Phase>('upload');
  protected readonly error = signal<string | null>(null);
  protected readonly warnings = signal<string[]>([]);
  protected readonly images = signal<string[]>([]);
  protected readonly sessionId = signal('');
  protected readonly savedId = signal<number | null>(null);

  protected readonly patients = signal<PatientOption[]>([]);
  protected readonly patientsLoading = signal(false);
  protected readonly patientsError = signal<string | null>(null);
  protected readonly selectedPatientId = signal<number | null>(null);

  protected readonly pacienteNombre = signal('');
  protected readonly pacienteEdad = signal('');
  protected readonly medicoNombre = signal('');
  protected readonly medicoCmp = signal('');
  protected readonly institucion = signal('');
  protected readonly fechaEmision = signal('');
  protected readonly diagnostico = signal('');
  protected readonly indicaciones = signal('');
  protected draftMedicamentos: unknown[] = [];

  async ngOnInit(): Promise<void> {
    this.patientsLoading.set(true);
    this.patientsError.set(null);
    try {
      const list = await this.patientSvc.list();
      this.patients.set(
        list.map((p) => ({ id: p.id, full_name: p.full_name })),
      );
    } catch {
      this.patientsError.set('No se pudo cargar la lista de pacientes.');
    } finally {
      this.patientsLoading.set(false);
    }
  }

  protected selectPatient(id: number): void {
    this.selectedPatientId.set(
      this.selectedPatientId() === id ? null : id,
    );
  }

  protected selectedPatientName(): string {
    const id = this.selectedPatientId();
    if (id == null) return '';
    return this.patients().find((p) => p.id === id)?.full_name ?? '';
  }

  protected onImagesSelected(images: string[]): void {
    this.images.set(images);
    this.error.set(null);
  }

  protected analyze(): void {
    if (!this.selectedPatientId()) {
      this.error.set('Seleccione un paciente antes de continuar.');
      return;
    }
    const imgs = this.images();
    if (!imgs.length || this.loading.visible()) return;
    this.error.set(null);
    this.loading.show('Estamos leyendo su documento. Esto puede tardar unos segundos…');
    void this.doAnalyze(imgs);
  }

  private async doAnalyze(imgs: string[]): Promise<void> {
    try {
      const res = await this.docSvc.analyze(
        'receta',
        imgs,
        this.selectedPatientId() ?? undefined,
      );
      const d = res.draft;
      this.sessionId.set(res.analysis_session_id);
      this.warnings.set(res.warnings);
      this.pacienteNombre.set(str(d['paciente_nombre']));
      this.pacienteEdad.set(str(d['paciente_edad']));
      this.medicoNombre.set(str(d['medico_nombre']));
      this.medicoCmp.set(str(d['medico_cmp']));
      this.institucion.set(str(d['institucion']));
      this.fechaEmision.set(str(d['fecha_emision']));
      this.diagnostico.set(str(d['diagnostico']));
      this.indicaciones.set(str(d['indicaciones']));
      this.draftMedicamentos = Array.isArray(d['medicamentos'])
        ? (d['medicamentos'] as unknown[])
        : [];
      this.phase.set('reviewing');
    } catch (err) {
      this.error.set(
        extractHttpError(
          err,
          'No pudimos procesar el documento. Compruebe la imagen e inténtelo de nuevo.',
        ),
      );
    } finally {
      this.loading.hide();
    }
  }

  protected medicamentosDisplay(): string {
    if (!this.draftMedicamentos.length) return '—';
    return this.draftMedicamentos
      .map((m) => {
        const item = m as Record<string, unknown>;
        const nombre = str(item['nombre']);
        const dosis = str(item['dosis']);
        const frecuencia = str(item['frecuencia']);
        const parts = [nombre, dosis, frecuencia].filter(Boolean);
        return parts.join(' · ');
      })
      .join('\n');
  }

  protected save(): void {
    if (!this.selectedPatientId()) {
      this.error.set('No hay paciente seleccionado.');
      return;
    }
    if (this.loading.visible()) return;
    this.error.set(null);
    this.loading.show('Guardando…');
    void this.doSave();
  }

  private async doSave(): Promise<void> {
    try {
      const res = await this.docSvc.saveReceta(
        this.sessionId(),
        this.selectedPatientId()!,
        {
          paciente_nombre: this.pacienteNombre() || null,
          paciente_edad: this.pacienteEdad() || null,
          medico_nombre: this.medicoNombre() || null,
          medico_cmp: this.medicoCmp() || null,
          institucion: this.institucion() || null,
          fecha_emision: this.fechaEmision() || null,
          diagnostico: this.diagnostico() || null,
          indicaciones: this.indicaciones() || null,
          medicamentos: this.draftMedicamentos,
        },
      );
      this.savedId.set(res.id);
      this.phase.set('done');
    } catch (err) {
      this.error.set(
        extractHttpError(err, 'No se pudo guardar el documento. Inténtelo de nuevo.'),
      );
    } finally {
      this.loading.hide();
    }
  }

  protected reset(): void {
    this.phase.set('upload');
    this.images.set([]);
    this.sessionId.set('');
    this.error.set(null);
    this.warnings.set([]);
    this.savedId.set(null);
    this.draftMedicamentos = [];
    this.selectedPatientId.set(null);
  }
}
