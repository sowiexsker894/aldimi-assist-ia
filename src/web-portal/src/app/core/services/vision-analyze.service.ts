import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { visionApiUrl } from '../config/vision-api-url';

/** Alineado con service-vision `DniExtracted`. */
export interface DniExtractedDto {
  nombre: string | null;
  apellido_paterno: string | null;
  apellido_materno: string | null;
  dni_number: string | null;
  sexo: string | null;
  nacionalidad: string | null;
  fecha_nacimiento: string | null;
  fecha_expiracion: string | null;
  lugar_nacimiento: string | null;
  direccion: string | null;
}

export interface VisionAnalyzeRequest {
  images_base64: string[];
}

export interface VisionAnalyzeResponse {
  data: DniExtractedDto;
}

@Injectable({ providedIn: 'root' })
export class VisionAnalyzeService {
  private readonly http = inject(HttpClient);

  analyze(body: VisionAnalyzeRequest): Observable<VisionAnalyzeResponse> {
    return this.http.post<VisionAnalyzeResponse>(visionApiUrl('v1/analyze'), body);
  }
}
