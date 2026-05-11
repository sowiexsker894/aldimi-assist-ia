import {
  ChangeDetectionStrategy,
  Component,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { ShellNavItemComponent } from './shell-nav-item.component';

const SIDEBAR_COLLAPSED_KEY = 'aldimi_sidebar_collapsed';

@Component({
  selector: 'app-shell',
  imports: [RouterOutlet, ShellNavItemComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './shell.component.html',
  styleUrl: './shell.component.scss',
})
export class ShellComponent implements OnInit {
  private readonly auth = inject(AuthService);

  protected readonly menu = this.auth.menu;
  protected readonly user = this.auth.user;

  protected readonly sidebarCollapsed = signal(
    globalThis.localStorage?.getItem(SIDEBAR_COLLAPSED_KEY) === '1',
  );

  async ngOnInit(): Promise<void> {
    if (this.auth.isAuthenticated() && this.auth.menu().length === 0) {
      await this.auth.refreshProfile();
    }
  }

  protected toggleSidebar(): void {
    this.sidebarCollapsed.update((v) => {
      const next = !v;
      globalThis.localStorage?.setItem(SIDEBAR_COLLAPSED_KEY, next ? '1' : '0');
      return next;
    });
  }

  protected logout(): void {
    this.auth.logout();
  }
}
