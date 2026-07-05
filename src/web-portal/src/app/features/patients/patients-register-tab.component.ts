import {
  ChangeDetectionStrategy,
  Component,
  inject,
  output,
  signal,
} from '@angular/core';
import { DocumentService } from '../../core/services/document.service';
import {
  PatientFamilyService,
  type FamilyMemberCreatePayload,
} from '../../core/services/patient-family.service';
import { PatientService } from '../../core/services/patient.service';
import { extractHttpError } from '../../core/utils/http-error';
import { DniOcrFlowComponent } from '../documentos/dni-ocr-flow.component';
import {
  type DniFieldsConfirmedEvent,
  dniSavePayload,
  fullNameFromDniFields,
} from '../documentos/dni-ocr.models';
import { UiButton, UiCard, UiInput } from '../../shared/ui';

interface FamilyDraft {
  key: number;
  full_name: string;
  document_number: string;
  phone: string;
  email: string;
}

@Component({
  selector: 'app-patients-register-tab',
  imports: [DniOcrFlowComponent, UiButton, UiCard, UiInput],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="space-y-6">
      <app-dni-ocr-flow
        mode="prefill"
        [compact]="true"
        (fieldsConfirmed)="onDniConfirmed($event)"
      />

      @if (ocrApplied()) {
        <p class="text-sm text-primary" role="status">
          Datos del DNI cargados. Revise el formulario antes de registrar.
        </p>
      }

      <app-ui-card title="Datos del paciente" [padding]="'md'">
        <div class="grid gap-4 sm:grid-cols-2">
          <div class="sm:col-span-2">
            <app-ui-input
              label="Nombre completo"
              inputId="pat-full-name"
              [(value)]="fullName"
            />
          </div>
          <app-ui-input label="DNI" inputId="pat-dni" [(value)]="dni" />
          <app-ui-input label="Primer nombre" inputId="pat-pn" [(value)]="primerNombre" />
          <app-ui-input label="Segundo nombre" inputId="pat-sn" [(value)]="segundoNombre" />
          <app-ui-input label="Primer apellido" inputId="pat-pa" [(value)]="primerApellido" />
          <app-ui-input label="Segundo apellido" inputId="pat-sa" [(value)]="segundoApellido" />
          <app-ui-input label="Sexo" inputId="pat-sexo" [(value)]="sexo" />
          <app-ui-input
            label="Fecha nacimiento"
            inputId="pat-fn"
            placeholder="YYYY-MM-DD"
            [(value)]="fechaNacimiento"
          />
          <app-ui-input label="Nacionalidad" inputId="pat-nac" [(value)]="nacionalidad" />
          <app-ui-input label="Estado civil" inputId="pat-ec" [(value)]="estadoCivil" />
          <div class="sm:col-span-2">
            <app-ui-input label="Dirección" inputId="pat-dir" [(value)]="direccion" />
          </div>
        </div>
      </app-ui-card>

      <app-ui-card title="Familiares en el albergue" [padding]="'md'">
        <p class="mb-4 text-sm text-muted-foreground">
          Opcional. Registre familiares que acompañan al paciente.
        </p>
        @for (f of familyRows(); track f.key) {
          <div class="mb-4 rounded-md border border-border p-4">
            <div class="grid gap-3 sm:grid-cols-2">
              <app-ui-input
                label="Nombre completo"
                [inputId]="'fam-name-' + f.key"
                [value]="f.full_name"
                (valueChange)="updateFamily(f.key, 'full_name', $event)"
              />
              <app-ui-input
                label="Documento"
                [inputId]="'fam-doc-' + f.key"
                [value]="f.document_number"
                (valueChange)="updateFamily(f.key, 'document_number', $event)"
              />
              <app-ui-input
                label="Teléfono"
                [inputId]="'fam-phone-' + f.key"
                [value]="f.phone"
                (valueChange)="updateFamily(f.key, 'phone', $event)"
              />
              <app-ui-input
                label="Correo (opcional)"
                [inputId]="'fam-email-' + f.key"
                [value]="f.email"
                (valueChange)="updateFamily(f.key, 'email', $event)"
              />
            </div>
            <div class="mt-3">
              <app-ui-button variant="ghost" (clicked)="removeFamily(f.key)">
                Quitar familiar
              </app-ui-button>
            </div>
          </div>
        }
        <app-ui-button variant="secondary" (clicked)="addFamily()">
          Añadir familiar
        </app-ui-button>
      </app-ui-card>

      @if (errorMsg()) {
        <p class="text-sm text-accent" role="alert">{{ errorMsg() }}</p>
      }
      @if (message()) {
        <p class="text-sm text-foreground" role="status">{{ message() }}</p>
      }

      <app-ui-button variant="primary" (clicked)="submit()" [disabled]="busy()">
        {{ busy() ? 'Registrando…' : 'Registrar paciente' }}
      </app-ui-button>
    </div>
  `,
})
export class PatientsRegisterTabComponent {
  readonly registered = output<void>();

  private readonly patientSvc = inject(PatientService);
  private readonly familySvc = inject(PatientFamilyService);
  private readonly docSvc = inject(DocumentService);

  protected readonly fullName = signal('');
  protected readonly dni = signal('');
  protected readonly primerNombre = signal('');
  protected readonly segundoNombre = signal('');
  protected readonly primerApellido = signal('');
  protected readonly segundoApellido = signal('');
  protected readonly sexo = signal('');
  protected readonly fechaNacimiento = signal('');
  protected readonly nacionalidad = signal('');
  protected readonly estadoCivil = signal('');
  protected readonly direccion = signal('');

  protected readonly ocrApplied = signal(false);
  protected readonly ocrSessionId = signal<string | null>(null);
  protected readonly ocrFields = signal<Record<string, unknown> | null>(null);

  protected readonly familyRows = signal<FamilyDraft[]>([]);
  private familyKeySeq = 0;

  protected readonly busy = signal(false);
  protected readonly errorMsg = signal<string | null>(null);
  protected readonly message = signal<string | null>(null);

  protected onDniConfirmed(event: DniFieldsConfirmedEvent): void {
    const f = event.fields;
    this.ocrSessionId.set(event.sessionId);
    this.ocrFields.set(dniSavePayload(f));
    this.fullName.set(fullNameFromDniFields(f));
    this.dni.set(f.dni_number);
    this.primerNombre.set(f.nombre);
    this.primerApellido.set(f.apellido_paterno);
    this.segundoApellido.set(f.apellido_materno);
    this.sexo.set(f.sexo);
    this.fechaNacimiento.set(f.fecha_nacimiento);
    this.nacionalidad.set(f.nacionalidad);
    this.direccion.set(f.direccion);
    this.ocrApplied.set(true);
  }

  protected addFamily(): void {
    this.familyKeySeq += 1;
    this.familyRows.update((rows) => [
      ...rows,
      {
        key: this.familyKeySeq,
        full_name: '',
        document_number: '',
        phone: '',
        email: '',
      },
    ]);
  }

  protected removeFamily(key: number): void {
    this.familyRows.update((rows) => rows.filter((r) => r.key !== key));
  }

  protected updateFamily(
    key: number,
    field: keyof Omit<FamilyDraft, 'key'>,
    value: string,
  ): void {
    this.familyRows.update((rows) =>
      rows.map((r) => (r.key === key ? { ...r, [field]: value } : r)),
    );
  }

  protected async submit(): Promise<void> {
    this.errorMsg.set(null);
    this.message.set(null);
    const name = this.fullName().trim();
    if (!name) {
      this.errorMsg.set('El nombre completo es obligatorio.');
      return;
    }

    this.busy.set(true);
    try {
      let patientId: number;
      const sessionId = this.ocrSessionId();
      const ocrPayload = this.ocrFields();

      if (sessionId && ocrPayload) {
        const saved = await this.docSvc.saveDni(sessionId, {
          ...ocrPayload,
          nombre: this.primerNombre() || ocrPayload['nombre'],
          apellido_paterno: this.primerApellido() || ocrPayload['apellido_paterno'],
          apellido_materno: this.segundoApellido() || ocrPayload['apellido_materno'],
          dni_number: this.dni() || ocrPayload['dni_number'],
          sexo: this.sexo() || ocrPayload['sexo'],
          fecha_nacimiento: this.fechaNacimiento() || ocrPayload['fecha_nacimiento'],
          nacionalidad: this.nacionalidad() || ocrPayload['nacionalidad'],
          direccion: this.direccion() || ocrPayload['direccion'],
        });
        if (saved.patient_id == null) {
          throw new Error('No se obtuvo el paciente del DNI guardado.');
        }
        patientId = saved.patient_id;
      } else {
        const payload = {
          full_name: name,
          dni: this.dni() || undefined,
          primer_nombre: this.primerNombre() || undefined,
          segundo_nombre: this.segundoNombre() || undefined,
          primer_apellido: this.primerApellido() || undefined,
          segundo_apellido: this.segundoApellido() || undefined,
          sexo: this.sexo() || undefined,
          fecha_nacimiento: this.fechaNacimiento() || undefined,
          nacionalidad: this.nacionalidad() || undefined,
          estado_civil: this.estadoCivil() || undefined,
          direccion: this.direccion() || undefined,
        };
        const created = await this.patientSvc.create(payload);
        patientId = created.id;
      }

      await this.saveFamilyMembers(patientId);
      this.message.set(`Paciente registrado correctamente (id ${patientId}).`);
      this.resetForm();
      this.registered.emit();
    } catch (e: unknown) {
      this.errorMsg.set(extractHttpError(e, 'No se pudo registrar el paciente.'));
    } finally {
      this.busy.set(false);
    }
  }

  private async saveFamilyMembers(patientId: number): Promise<void> {
    const rows = this.familyRows().filter((r) => r.full_name.trim());
    for (const row of rows) {
      const payload: FamilyMemberCreatePayload = {
        full_name: row.full_name.trim(),
        document_number: row.document_number.trim() || undefined,
        phone: row.phone.trim() || undefined,
        email: row.email.trim() || undefined,
      };
      await this.familySvc.add(patientId, payload);
    }
  }

  private resetForm(): void {
    this.fullName.set('');
    this.dni.set('');
    this.primerNombre.set('');
    this.segundoNombre.set('');
    this.primerApellido.set('');
    this.segundoApellido.set('');
    this.sexo.set('');
    this.fechaNacimiento.set('');
    this.nacionalidad.set('');
    this.estadoCivil.set('');
    this.direccion.set('');
    this.ocrApplied.set(false);
    this.ocrSessionId.set(null);
    this.ocrFields.set(null);
    this.familyRows.set([]);
  }
}
