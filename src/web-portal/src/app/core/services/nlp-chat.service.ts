import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { nlpApiUrl } from '../config/nlp-api-url';

export interface NlpChatHistoryItem {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface NlpChatRequest {
  message: string;
  history: NlpChatHistoryItem[];
}

export interface NlpChatResponse {
  reply: string;
}

@Injectable({ providedIn: 'root' })
export class NlpChatService {
  private readonly http = inject(HttpClient);

  chat(body: NlpChatRequest): Observable<NlpChatResponse> {
    return this.http.post<NlpChatResponse>(nlpApiUrl('v1/chat'), body);
  }
}
