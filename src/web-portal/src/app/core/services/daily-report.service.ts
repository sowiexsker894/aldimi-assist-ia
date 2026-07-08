import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../config/api-url';

export interface EmotionItem {
  emotion: string | null;
  probability: number | null;
  percent: number | null;
  present: boolean;
}

export interface SentimentDetails {
  top_emotion: string | null;
  top_probability: number | null;
  risk_score: number | null;
  alert_flag: boolean;
  emotions: EmotionItem[];
}

export interface DailyReportRow {
  id: number;
  user_id: number | null;
  patient_id: number | null;
  text_content: string;
  sentiment_label: string | null;
  sentiment_score: number | null;
  sentiment_details: SentimentDetails | null;
  alert_flag: boolean;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class DailyReportService {
  private readonly http = inject(HttpClient);

  list(patientId: number): Promise<DailyReportRow[]> {
    return firstValueFrom(
      this.http.get<DailyReportRow[]>(
        apiUrl(`/api/v1/patients/${patientId}/daily-reports`),
      ),
    );
  }

  create(patientId: number, textContent: string): Promise<DailyReportRow> {
    return firstValueFrom(
      this.http.post<DailyReportRow>(
        apiUrl(`/api/v1/patients/${patientId}/daily-reports`),
        { text_content: textContent },
      ),
    );
  }
}
