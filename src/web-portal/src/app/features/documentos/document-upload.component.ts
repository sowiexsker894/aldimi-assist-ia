import {
  ChangeDetectionStrategy,
  Component,
  input,
  output,
  signal,
} from '@angular/core';

const MAX_FILES = 8;
const MAX_BYTES_PER_FILE = 5 * 1024 * 1024;

@Component({
  selector: 'app-document-upload',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="flex flex-col gap-3">
      <div class="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center">
        <label
          class="inline-flex cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-primary/40 bg-surface-elevated px-5 py-2.5 text-sm font-medium text-foreground transition-colors hover:border-primary hover:bg-primary/5"
          [class.pointer-events-none]="disabled()"
          [class.opacity-50]="disabled()"
        >
          <span>Seleccionar fotos</span>
          <input
            type="file"
            class="sr-only"
            accept="image/*"
            multiple
            [disabled]="disabled()"
            (change)="onFilesSelected($event)"
          />
        </label>
      </div>

      @if (selectedNames().length) {
        <p class="text-sm text-muted-foreground">
          Ha seleccionado
          <strong class="text-foreground">{{ selectedNames().length }}</strong>
          archivo(s):
          <span class="text-foreground">{{ selectedNames().join(', ') }}</span>
        </p>
      }

      @if (uploadError()) {
        <p
          class="rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive"
          role="alert"
        >
          {{ uploadError() }}
        </p>
      }
    </div>
  `,
})
export class DocumentUploadComponent {
  readonly disabled = input(false);
  readonly imagesSelected = output<string[]>();

  protected readonly selectedNames = signal<string[]>([]);
  protected readonly uploadError = signal<string | null>(null);

  protected onFilesSelected(ev: Event): void {
    void this.processFiles(ev);
  }

  private async processFiles(ev: Event): Promise<void> {
    this.uploadError.set(null);
    const input = ev.target as HTMLInputElement;
    const files = input.files;
    if (!files?.length) {
      this.selectedNames.set([]);
      this.imagesSelected.emit([]);
      input.value = '';
      return;
    }
    try {
      const list = Array.from(files);
      if (list.length > MAX_FILES) {
        throw new Error(
          `Solo puede adjuntar hasta ${MAX_FILES} imágenes. Inténtelo de nuevo.`,
        );
      }
      for (const f of list) {
        if (!f.type.startsWith('image/')) {
          throw new Error(`"${f.name}" no es una imagen válida.`);
        }
        if (f.size > MAX_BYTES_PER_FILE) {
          throw new Error(
            `"${f.name}" es demasiado grande. Cada foto debe ser menor de ${Math.round(MAX_BYTES_PER_FILE / (1024 * 1024))} MB.`,
          );
        }
      }
      const urls = await Promise.all(
        list.map(
          (f) =>
            new Promise<string>((resolve, reject) => {
              const r = new FileReader();
              r.onload = () =>
                resolve(typeof r.result === 'string' ? r.result : '');
              r.onerror = () =>
                reject(new Error(`No se pudo leer el archivo "${f.name}".`));
              r.readAsDataURL(f);
            }),
        ),
      );
      this.selectedNames.set(list.map((f) => f.name));
      this.imagesSelected.emit(urls);
    } catch (e) {
      this.uploadError.set(e instanceof Error ? e.message : String(e));
      this.selectedNames.set([]);
      this.imagesSelected.emit([]);
    } finally {
      input.value = '';
    }
  }
}
