import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { finalize } from 'rxjs/operators';

import { LoadingService } from '../../core/services/loading.service';
import {
  DniExtractedDto,
  VisionAnalyzeService,
} from '../../core/services/vision-analyze.service';
import { UiButton, UiCard } from '../../shared/ui';

@Component({
  selector: 'app-demo',
  imports: [UiButton, UiCard],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './demo.component.html',
})
export class DemoComponent {
  private readonly maxVisionFiles = 8;
  private readonly maxVisionBytesPerFile = 5 * 1024 * 1024;

  private readonly visionSvc = inject(VisionAnalyzeService);
  protected readonly loading = inject(LoadingService);

  protected readonly visionSelectedNames = signal<string[]>([]);
  protected readonly visionImagesBase64 = signal<string[]>([]);
  protected readonly visionError = signal<string | null>(null);
  protected readonly visionResult = signal<DniExtractedDto | null>(null);

  protected onVisionFilesSelected(ev: Event): void {
    void this.loadVisionFiles(ev);
  }

  private async loadVisionFiles(ev: Event): Promise<void> {
    this.visionError.set(null);
    this.visionResult.set(null);
    const input = ev.target as HTMLInputElement;
    const files = input.files;
    if (!files?.length) {
      this.visionImagesBase64.set([]);
      this.visionSelectedNames.set([]);
      input.value = '';
      return;
    }
    try {
      const list = Array.from(files);
      if (list.length > this.maxVisionFiles) {
        throw new Error(
          `Solo puede adjuntar hasta ${this.maxVisionFiles} imágenes. Inténtelo de nuevo.`,
        );
      }
      for (const f of list) {
        if (!f.type.startsWith('image/')) {
          throw new Error(`"${f.name}" no es una imagen válida.`);
        }
        if (f.size > this.maxVisionBytesPerFile) {
          throw new Error(
            `"${f.name}" es demasiado grande. Cada foto debe ser menor de ${Math.round(this.maxVisionBytesPerFile / (1024 * 1024))} MB.`,
          );
        }
      }
      const urls = await Promise.all(
        list.map(
          (f) =>
            new Promise<string>((resolve, reject) => {
              const r = new FileReader();
              r.onload = () => resolve(typeof r.result === 'string' ? r.result : '');
              r.onerror = () =>
                reject(new Error(`No se pudo leer el archivo "${f.name}".`));
              r.readAsDataURL(f);
            }),
        ),
      );
      this.visionImagesBase64.set(urls);
      this.visionSelectedNames.set(list.map((f) => f.name));
    } catch (e) {
      this.visionError.set(e instanceof Error ? e.message : String(e));
      this.visionImagesBase64.set([]);
      this.visionSelectedNames.set([]);
    } finally {
      input.value = '';
    }
  }

  protected analyzeVision(): void {
    const imgs = this.visionImagesBase64();
    if (!imgs.length || this.loading.visible()) {
      return;
    }
    this.visionError.set(null);
    this.visionResult.set(null);
    this.loading.show('Estamos leyendo su documento. Esto puede tardar unos segundos…');
    this.visionSvc
      .analyze({ images_base64: imgs })
      .pipe(finalize(() => this.loading.hide()))
      .subscribe({
        next: (res) => {
          this.visionResult.set(res.data);
        },
        error: (err: HttpErrorResponse) => {
          const detail =
            err.error &&
            typeof err.error === 'object' &&
            err.error !== null &&
            'detail' in err.error
              ? (err.error as { detail: unknown }).detail
              : undefined;
          const msg =
            typeof detail === 'string'
              ? detail
              : detail !== undefined
                ? JSON.stringify(detail)
                : err.message ||
                  'No pudimos procesar el documento. Compruebe la imagen e inténtelo de nuevo.';
          this.visionError.set(msg);
        },
      });
  }

  protected dniDisplayRows(): { label: string; value: string }[] {
    const d = this.visionResult();
    if (!d) {
      return [];
    }
    const v = (x: string | null | undefined) =>
      x != null && String(x).trim() !== '' ? String(x) : '—';
    return [
      { label: 'Nombres', value: v(d.nombre) },
      { label: 'Apellido paterno', value: v(d.apellido_paterno) },
      { label: 'Apellido materno', value: v(d.apellido_materno) },
      { label: 'DNI', value: v(d.dni_number) },
      { label: 'Sexo', value: v(d.sexo) },
      { label: 'Nacionalidad', value: v(d.nacionalidad) },
      { label: 'Fecha de nacimiento', value: v(d.fecha_nacimiento) },
      { label: 'Fecha de vencimiento', value: v(d.fecha_expiracion) },
      { label: 'Lugar de nacimiento', value: v(d.lugar_nacimiento) },
      { label: 'Dirección', value: v(d.direccion) },
    ];
  }
}
