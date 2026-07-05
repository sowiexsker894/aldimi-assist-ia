import {
  ChangeDetectionStrategy,
  Component,
  inject,
  input,
  output,
  signal,
} from '@angular/core';
import { DocumentService } from '../../core/services/document.service';
import { LoadingService } from '../../core/services/loading.service';
import { extractHttpError } from '../../core/utils/http-error';
import { UiButton, UiCard, UiInput } from '../../shared/ui';
import { DocumentUploadComponent } from './document-upload.component';
import {
  type DniConfirmedFields,
  type DniFieldsConfirmedEvent,
  type DniOcrMode,
  type DniPatientSavedEvent,
  strField,
} from './dni-ocr.models';

type Phase = 'upload' | 'reviewing' | 'done';

@Component({
  selector: 'app-dni-ocr-flow',
  imports: [UiButton, UiCard, UiInput, DocumentUploadComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './dni-ocr-flow.component.html',
})
export class DniOcrFlowComponent {
  readonly mode = input<DniOcrMode>('savePatient');
  readonly compact = input(false);

  readonly fieldsConfirmed = output<DniFieldsConfirmedEvent>();
  readonly patientSaved = output<DniPatientSavedEvent>();

  protected readonly loading = inject(LoadingService);
  private readonly docSvc = inject(DocumentService);

  protected readonly phase = signal<Phase>('upload');
  protected readonly error = signal<string | null>(null);
  protected readonly warnings = signal<string[]>([]);
  protected readonly images = signal<string[]>([]);
  protected readonly sessionId = signal('');
  protected readonly savedId = signal<number | null>(null);
  protected readonly savedPatientId = signal<number | null>(null);

  protected readonly nombre = signal('');
  protected readonly apellidoPaterno = signal('');
  protected readonly apellidoMaterno = signal('');
  protected readonly dniNumber = signal('');
  protected readonly sexo = signal('');
  protected readonly nacionalidad = signal('');
  protected readonly fechaNacimiento = signal('');
  protected readonly fechaExpiracion = signal('');
  protected readonly lugarNacimiento = signal('');
  protected readonly direccion = signal('');

  protected onImagesSelected(images: string[]): void {
    this.images.set(images);
    this.error.set(null);
  }

  protected analyze(): void {
    const imgs = this.images();
    if (!imgs.length || this.loading.visible()) return;
    this.error.set(null);
    this.loading.show('Estamos leyendo su documento. Esto puede tardar unos segundos…');
    void this.doAnalyze(imgs);
  }

  private async doAnalyze(imgs: string[]): Promise<void> {
    try {
      const res = await this.docSvc.analyze('dni', imgs);
      const d = res.draft;
      this.sessionId.set(res.analysis_session_id);
      this.warnings.set(res.warnings);
      this.nombre.set(strField(d['nombre']));
      this.apellidoPaterno.set(strField(d['apellido_paterno']));
      this.apellidoMaterno.set(strField(d['apellido_materno']));
      this.dniNumber.set(strField(d['dni_number']));
      this.sexo.set(strField(d['sexo']));
      this.nacionalidad.set(strField(d['nacionalidad']));
      this.fechaNacimiento.set(strField(d['fecha_nacimiento']));
      this.fechaExpiracion.set(strField(d['fecha_expiracion']));
      this.lugarNacimiento.set(strField(d['lugar_nacimiento']));
      this.direccion.set(strField(d['direccion']));
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

  protected confirm(): void {
    if (this.mode() === 'prefill') {
      this.fieldsConfirmed.emit({
        sessionId: this.sessionId(),
        fields: this.currentFields(),
        warnings: this.warnings(),
      });
      return;
    }
    this.save();
  }

  protected save(): void {
    if (this.loading.visible()) return;
    this.error.set(null);
    this.loading.show('Guardando…');
    void this.doSave();
  }

  private async doSave(): Promise<void> {
    try {
      const res = await this.docSvc.saveDni(this.sessionId(), this.currentFieldsAsSavePayload());
      this.savedId.set(res.id);
      this.savedPatientId.set(res.patient_id);
      this.phase.set('done');
      if (res.patient_id != null) {
        this.patientSaved.emit({ patientId: res.patient_id, documentId: res.id });
      }
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
    this.savedPatientId.set(null);
    this.nombre.set('');
    this.apellidoPaterno.set('');
    this.apellidoMaterno.set('');
    this.dniNumber.set('');
    this.sexo.set('');
    this.nacionalidad.set('');
    this.fechaNacimiento.set('');
    this.fechaExpiracion.set('');
    this.lugarNacimiento.set('');
    this.direccion.set('');
  }

  currentFields(): DniConfirmedFields {
    return {
      nombre: this.nombre(),
      apellido_paterno: this.apellidoPaterno(),
      apellido_materno: this.apellidoMaterno(),
      dni_number: this.dniNumber(),
      sexo: this.sexo(),
      nacionalidad: this.nacionalidad(),
      fecha_nacimiento: this.fechaNacimiento(),
      fecha_expiracion: this.fechaExpiracion(),
      lugar_nacimiento: this.lugarNacimiento(),
      direccion: this.direccion(),
    };
  }

  private currentFieldsAsSavePayload(): Record<string, unknown> {
    const f = this.currentFields();
    return {
      nombre: f.nombre || null,
      apellido_paterno: f.apellido_paterno || null,
      apellido_materno: f.apellido_materno || null,
      dni_number: f.dni_number || null,
      sexo: f.sexo || null,
      nacionalidad: f.nacionalidad || null,
      fecha_nacimiento: f.fecha_nacimiento || null,
      fecha_expiracion: f.fecha_expiracion || null,
      lugar_nacimiento: f.lugar_nacimiento || null,
      direccion: f.direccion || null,
    };
  }
}
