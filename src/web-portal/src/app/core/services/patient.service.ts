import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../config/api-url';

export interface PatientRow {
  id: number;
  full_name: string;
  dni: string | null;
  primer_apellido: string | null;
  segundo_apellido: string | null;
  primer_nombre: string | null;
  segundo_nombre: string | null;
  sexo: string | null;
  fecha_nacimiento: string | null;
  nacionalidad: string | null;
  estado_civil: string | null;
  direccion: string | null;
  ubigeo: string | null;
  created_at: string;
}

export interface PatientCreatePayload {
  full_name: string;
  dni?: string;
  primer_apellido?: string;
  segundo_apellido?: string;
  primer_nombre?: string;
  segundo_nombre?: string;
  sexo?: string;
  fecha_nacimiento?: string;
  nacionalidad?: string;
  estado_civil?: string;
  direccion?: string;
  ubigeo?: string;
}

@Injectable({ providedIn: 'root' })
export class PatientService {
  private readonly http = inject(HttpClient);
  private readonly base = '/api/v1/patients/';

  list(): Promise<PatientRow[]> {
    return firstValueFrom(this.http.get<PatientRow[]>(apiUrl(this.base)));
  }

  get(id: number): Promise<PatientRow> {
    return firstValueFrom(this.http.get<PatientRow>(apiUrl(`${this.base}${id}`)));
  }

  create(payload: PatientCreatePayload): Promise<PatientRow> {
    return firstValueFrom(this.http.post<PatientRow>(apiUrl(this.base), payload));
  }
}
