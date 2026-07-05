import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../config/api-url';

export type DocumentType = 'dni' | 'boleta' | 'receta';

export interface DocumentAnalyzeResponse {
  analysis_session_id: string;
  document_type: DocumentType;
  draft: Record<string, unknown>;
  warnings: string[];
  metadata: Record<string, unknown>;
}

export interface DocumentSaveResponse {
  id: number;
  document_type: DocumentType;
  patient_id: number | null;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class DocumentService {
  private readonly http = inject(HttpClient);

  analyze(
    documentType: DocumentType,
    imagesBase64: string[],
    patientId?: number,
  ): Promise<DocumentAnalyzeResponse> {
    const body: Record<string, unknown> = {
      document_type: documentType,
      images_base64: imagesBase64,
    };
    if (patientId !== undefined) {
      body['patient_id'] = patientId;
    }
    return firstValueFrom(
      this.http.post<DocumentAnalyzeResponse>(apiUrl('/api/v1/documents/analyze'), body),
    );
  }

  saveDni(
    analysisSessionId: string,
    confirmedFields: Record<string, unknown>,
  ): Promise<DocumentSaveResponse> {
    return firstValueFrom(
      this.http.post<DocumentSaveResponse>(apiUrl('/api/v1/documents/dni'), {
        analysis_session_id: analysisSessionId,
        confirmed_fields: confirmedFields,
      }),
    );
  }

  saveBoleta(
    analysisSessionId: string,
    confirmedFields: Record<string, unknown>,
  ): Promise<DocumentSaveResponse> {
    return firstValueFrom(
      this.http.post<DocumentSaveResponse>(apiUrl('/api/v1/documents/boleta'), {
        analysis_session_id: analysisSessionId,
        confirmed_fields: confirmedFields,
      }),
    );
  }

  saveReceta(
    analysisSessionId: string,
    patientId: number,
    confirmedFields: Record<string, unknown>,
  ): Promise<DocumentSaveResponse> {
    return firstValueFrom(
      this.http.post<DocumentSaveResponse>(apiUrl('/api/v1/documents/receta'), {
        analysis_session_id: analysisSessionId,
        patient_id: patientId,
        confirmed_fields: confirmedFields,
      }),
    );
  }
}
