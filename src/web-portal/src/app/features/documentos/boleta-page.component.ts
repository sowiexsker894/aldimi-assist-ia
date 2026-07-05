import {
  ChangeDetectionStrategy,
  Component,
  inject,
  signal,
} from '@angular/core';
import { DocumentService } from '../../core/services/document.service';
import { LoadingService } from '../../core/services/loading.service';
import { extractHttpError } from '../../core/utils/http-error';
import { UiButton, UiCard, UiInput } from '../../shared/ui';
import { DocumentUploadComponent } from './document-upload.component';

type Phase = 'upload' | 'reviewing' | 'done';

const str = (v: unknown): string =>
  v == null || String(v) === 'null' ? '' : String(v);

@Component({
  selector: 'app-boleta-page',
  imports: [UiButton, UiCard, UiInput, DocumentUploadComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './boleta-page.component.html',
})
export class BoletaPageComponent {
  protected readonly loading = inject(LoadingService);
  private readonly docSvc = inject(DocumentService);

  protected readonly phase = signal<Phase>('upload');
  protected readonly error = signal<string | null>(null);
  protected readonly warnings = signal<string[]>([]);
  protected readonly images = signal<string[]>([]);
  protected readonly sessionId = signal('');
  protected readonly savedId = signal<number | null>(null);

  protected readonly tipoComprobante = signal('');
  protected readonly numeroComprobante = signal('');
  protected readonly fechaEmision = signal('');
  protected readonly emisorRazonSocial = signal('');
  protected readonly clienteNombre = signal('');
  protected readonly total = signal('');
  protected readonly metodoPago = signal('');
  protected readonly observaciones = signal('');

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
      const res = await this.docSvc.analyze('boleta', imgs);
      const d = res.draft;
      this.sessionId.set(res.analysis_session_id);
      this.warnings.set(res.warnings);
      this.tipoComprobante.set(str(d['tipo_comprobante']));
      this.numeroComprobante.set(str(d['numero_comprobante']));
      this.fechaEmision.set(str(d['fecha_emision']));
      this.emisorRazonSocial.set(str(d['emisor_razon_social']));
      this.clienteNombre.set(str(d['cliente_nombre']));
      this.total.set(str(d['total']));
      this.metodoPago.set(str(d['metodo_pago']));
      this.observaciones.set(str(d['observaciones']));
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

  protected save(): void {
    if (this.loading.visible()) return;
    this.error.set(null);
    this.loading.show('Guardando…');
    void this.doSave();
  }

  private async doSave(): Promise<void> {
    try {
      const res = await this.docSvc.saveBoleta(this.sessionId(), {
        tipo_comprobante: this.tipoComprobante() || null,
        numero_comprobante: this.numeroComprobante() || null,
        fecha_emision: this.fechaEmision() || null,
        emisor_razon_social: this.emisorRazonSocial() || null,
        cliente_nombre: this.clienteNombre() || null,
        total: this.total() || null,
        metodo_pago: this.metodoPago() || null,
        observaciones: this.observaciones() || null,
      });
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
  }
}
