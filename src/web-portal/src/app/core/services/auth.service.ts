import { HttpClient } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { apiUrl } from '../config/api-url';
import type { LoginResponse, MeResponse, MenuNodeDto, UserSummaryDto } from '../models/auth.models';

const TOKEN_KEY = 'aldimi_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);

  readonly token = signal<string | null>(globalThis.localStorage?.getItem(TOKEN_KEY) ?? null);
  readonly menu = signal<MenuNodeDto[]>([]);
  readonly user = signal<Pick<UserSummaryDto, 'email' | 'full_name' | 'roles'> | null>(null);

  async login(email: string, password: string): Promise<void> {
    const res = await firstValueFrom(
      this.http.post<LoginResponse>(apiUrl('/api/v1/auth/login'), { email, password }),
    );
    globalThis.localStorage?.setItem(TOKEN_KEY, res.access_token);
    this.token.set(res.access_token);
    this.user.set({
      email: res.user.email,
      full_name: res.user.full_name,
      roles: res.user.roles,
    });
    this.menu.set(res.menu);
    await this.router.navigateByUrl('/app');
  }

  async refreshProfile(): Promise<void> {
    if (!this.token()) {
      return;
    }
    const res = await firstValueFrom(
      this.http.get<MeResponse>(apiUrl('/api/v1/auth/me')),
    );
    this.user.set({
      email: res.user.email,
      full_name: res.user.full_name,
      roles: res.user.roles,
    });
    this.menu.set(res.menu);
  }

  logout(): void {
    globalThis.localStorage?.removeItem(TOKEN_KEY);
    this.token.set(null);
    this.user.set(null);
    this.menu.set([]);
    void this.router.navigateByUrl('/');
  }

  isAuthenticated(): boolean {
    return !!this.token();
  }
}
