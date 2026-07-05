import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../config/api-url';

export interface VolunteerRow {
  id: number;
  email: string;
  full_name: string;
  phone: string | null;
  document_number: string | null;
  is_active: boolean;
  roles: string[];
}

export interface CreateVolunteerPayload {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  document_number?: string;
}

@Injectable({ providedIn: 'root' })
export class VolunteerAdminService {
  private readonly http = inject(HttpClient);

  list(): Promise<VolunteerRow[]> {
    return firstValueFrom(
      this.http.get<VolunteerRow[]>(apiUrl('/api/v1/admin/volunteers')),
    );
  }

  create(payload: CreateVolunteerPayload): Promise<VolunteerRow> {
    return firstValueFrom(
      this.http.post<VolunteerRow>(apiUrl('/api/v1/admin/volunteers'), payload),
    );
  }

  setActive(userId: number, isActive: boolean): Promise<VolunteerRow> {
    return firstValueFrom(
      this.http.patch<VolunteerRow>(apiUrl(`/api/v1/admin/volunteers/${userId}`), {
        is_active: isActive,
      }),
    );
  }
}
