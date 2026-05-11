import {
  ChangeDetectionStrategy,
  Component,
  forwardRef,
  input,
} from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import type { MenuNodeDto } from '../models/auth.models';

@Component({
  selector: 'app-shell-nav-item',
  imports: [
    RouterLink,
    RouterLinkActive,
    forwardRef(() => ShellNavItemComponent),
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (item of items(); track item.id) {
      <div class="mb-0.5">
        <a
          [routerLink]="item.path"
          [attr.title]="collapsed() ? item.label : null"
          routerLinkActive="bg-white/15 shadow-inner"
          [routerLinkActiveOptions]="{ exact: item.path === '/app' }"
          class="flex items-center gap-2 rounded-md px-2 py-2 text-sm text-white/90 transition-colors hover:bg-white/10"
          [class.justify-center]="collapsed()"
          [class.px-2]="collapsed()"
        >
          <span
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-white/10 text-xs font-semibold uppercase text-white/95"
            [class.mx-auto]="collapsed()"
          >
            {{ navGlyph(item) }}
          </span>
          @if (!collapsed()) {
            <span class="truncate">{{ item.label }}</span>
          }
        </a>
        @if (item.children.length) {
          <div class="mt-1 border-l border-white/15 pl-2">
            <app-shell-nav-item [items]="item.children" [collapsed]="collapsed()" />
          </div>
        }
      </div>
    }
  `,
})
export class ShellNavItemComponent {
  readonly items = input.required<MenuNodeDto[]>();
  readonly collapsed = input(false);

  protected navGlyph(item: MenuNodeDto): string {
    const raw = (item.icon ?? '').trim();
    if (raw.length > 0) {
      return raw.slice(0, 1).toUpperCase();
    }
    const label = item.label.trim();
    return label.length > 0 ? label.slice(0, 1).toUpperCase() : '·';
  }
}
