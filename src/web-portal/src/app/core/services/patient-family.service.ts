import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../config/api-url';

export interface FamilyMemberRow {
  id: number;
  full_name: string;
  document_number: string | null;
  phone: string | null;
  email: string;
}

export interface FamilyMemberCreatePayload {
  full_name: string;
  document_number?: string;
  phone?: string;
  email?: string;
}

@Injectable({ providedIn: 'root' })
export class PatientFamilyService {
  private readonly http = inject(HttpClient);

  list(patientId: number): Promise<FamilyMemberRow[]> {
    return firstValueFrom(
      this.http.get<FamilyMemberRow[]>(
        apiUrl(`/api/v1/patients/${patientId}/family-members`),
      ),
    );
  }

  add(patientId: number, payload: FamilyMemberCreatePayload): Promise<FamilyMemberRow> {
    return firstValueFrom(
      this.http.post<FamilyMemberRow>(
        apiUrl(`/api/v1/patients/${patientId}/family-members`),
        payload,
      ),
    );
  }
}
