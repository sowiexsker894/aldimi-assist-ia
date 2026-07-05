import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { extractHttpError } from '../../core/utils/http-error';
import {
  VolunteerAdminService,
  type VolunteerRow,
} from '../../core/services/volunteer-admin.service';
import { DniOcrFlowComponent } from '../documentos/dni-ocr-flow.component';
import {
  type DniFieldsConfirmedEvent,
  fullNameFromDniFields,
} from '../documentos/dni-ocr.models';
import { UiButton, UiCard, UiInput, UiTabs } from '../../shared/ui';

@Component({
  selector: 'app-admin-volunteers',
  imports: [UiButton, UiCard, UiInput, UiTabs, DniOcrFlowComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="space-y-6 p-6">
      <app-ui-tabs
        [tabs]="tabs"
        [activeId]="activeTab()"
        (tabChange)="activeTab.set($event)"
      />

      @if (activeTab() === 'list') {
        <app-ui-card title="Listado de voluntarios" [padding]="'md'">
          @if (listError()) {
            <p class="text-sm text-accent" role="alert">{{ listError() }}</p>
          } @else if (listLoading()) {
            <p class="text-sm text-muted-foreground">Cargando…</p>
          } @else if (!volunteers().length) {
            <p class="text-sm text-muted-foreground">No hay voluntarios registrados.</p>
          } @else {
            <div class="overflow-x-auto">
              <table class="w-full min-w-[640px] text-left text-sm">
                <thead>
                  <tr class="border-b border-border text-muted-foreground">
                    <th class="px-3 py-2 font-medium">Nombre</th>
                    <th class="px-3 py-2 font-medium">Correo</th>
                    <th class="px-3 py-2 font-medium">Teléfono</th>
                    <th class="px-3 py-2 font-medium">Estado</th>
                    <th class="px-3 py-2 font-medium">Acción</th>
                  </tr>
                </thead>
                <tbody>
                  @for (v of volunteers(); track v.id) {
                    <tr class="border-b border-border last:border-0">
                      <td class="px-3 py-2 text-foreground">{{ v.full_name }}</td>
                      <td class="px-3 py-2 text-muted-foreground">{{ v.email }}</td>
                      <td class="px-3 py-2 text-muted-foreground">
                        {{ v.phone || '—' }}
                      </td>
                      <td class="px-3 py-2">
                        @if (v.is_active) {
                          <span
                            class="rounded-full bg-primary/15 px-2 py-0.5 text-xs font-medium text-primary"
                          >
                            Activo
                          </span>
                        } @else {
                          <span
                            class="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground"
                          >
                            Inactivo
                          </span>
                        }
                      </td>
                      <td class="px-3 py-2">
                        <app-ui-button
                          variant="secondary"
                          (clicked)="toggleActive(v)"
                          [disabled]="toggleBusyId() === v.id"
                        >
                          @if (toggleBusyId() === v.id) {
                            …
                          } @else if (v.is_active) {
                            Desactivar
                          } @else {
                            Activar
                          }
                        </app-ui-button>
                      </td>
                    </tr>
                  }
                </tbody>
              </table>
            </div>
          }
        </app-ui-card>
      } @else {
        <app-dni-ocr-flow
          mode="prefill"
          [compact]="true"
          (fieldsConfirmed)="onDniConfirmed($event)"
        />

        @if (ocrApplied()) {
          <p class="text-sm text-primary" role="status">
            Datos del DNI cargados. Complete correo y contraseña.
          </p>
        }

        <app-ui-card title="Datos del voluntario" [padding]="'md'">
          <app-ui-input
            label="Nombre completo"
            inputId="vol-name"
            placeholder="Nombre y apellidos"
            [(value)]="fullName"
          />
          <app-ui-input
            class="mt-4"
            label="Documento (DNI)"
            inputId="vol-doc"
            placeholder="Número de documento"
            [(value)]="documentNumber"
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
          <app-ui-input
            class="mt-4"
            label="Teléfono (opcional)"
            inputId="vol-phone"
            placeholder="999 999 999"
            [(value)]="phone"
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
      }
    </div>
  `,
})
export class AdminVolunteersComponent implements OnInit {
  private readonly volunteerSvc = inject(VolunteerAdminService);

  protected readonly tabs = [
    { id: 'list', label: 'Listado' },
    { id: 'register', label: 'Registro' },
  ];
  protected readonly activeTab = signal('list');

  protected readonly fullName = signal('');
  protected readonly email = signal('');
  protected readonly password = signal('');
  protected readonly phone = signal('');
  protected readonly documentNumber = signal('');
  protected readonly ocrApplied = signal(false);
  protected readonly busy = signal(false);
  protected readonly message = signal<string | null>(null);
  protected readonly errorMsg = signal<string | null>(null);

  protected readonly volunteers = signal<VolunteerRow[]>([]);
  protected readonly listLoading = signal(true);
  protected readonly listError = signal<string | null>(null);
  protected readonly toggleBusyId = signal<number | null>(null);

  async ngOnInit(): Promise<void> {
    await this.loadVolunteers();
  }

  protected onDniConfirmed(event: DniFieldsConfirmedEvent): void {
    this.fullName.set(fullNameFromDniFields(event.fields));
    this.documentNumber.set(event.fields.dni_number);
    this.ocrApplied.set(true);
  }

  protected async submit(): Promise<void> {
    this.message.set(null);
    this.errorMsg.set(null);
    this.busy.set(true);
    try {
      await this.volunteerSvc.create({
        full_name: this.fullName(),
        email: this.email(),
        password: this.password(),
        phone: this.phone() || undefined,
        document_number: this.documentNumber() || undefined,
      });
      this.message.set('Voluntario creado correctamente.');
      this.fullName.set('');
      this.email.set('');
      this.password.set('');
      this.phone.set('');
      this.documentNumber.set('');
      this.ocrApplied.set(false);
      await this.loadVolunteers();
      this.activeTab.set('list');
    } catch (e: unknown) {
      this.errorMsg.set(extractHttpError(e, 'No se pudo crear el voluntario.'));
    } finally {
      this.busy.set(false);
    }
  }

  protected async toggleActive(v: VolunteerRow): Promise<void> {
    this.listError.set(null);
    this.toggleBusyId.set(v.id);
    try {
      await this.volunteerSvc.setActive(v.id, !v.is_active);
      await this.loadVolunteers();
    } catch (e: unknown) {
      this.listError.set(
        extractHttpError(e, 'No se pudo actualizar el estado del voluntario.'),
      );
    } finally {
      this.toggleBusyId.set(null);
    }
  }

  private async loadVolunteers(): Promise<void> {
    this.listLoading.set(true);
    this.listError.set(null);
    try {
      this.volunteers.set(await this.volunteerSvc.list());
    } catch (e: unknown) {
      this.listError.set(extractHttpError(e, 'No se pudo cargar el listado de voluntarios.'));
    } finally {
      this.listLoading.set(false);
    }
  }
}
