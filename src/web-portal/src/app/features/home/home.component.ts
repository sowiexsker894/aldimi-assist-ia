import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { AuthService } from '../../core/services/auth.service';
import { UiCard } from '../../shared/ui';

@Component({
  selector: 'app-home',
  imports: [UiCard],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="p-6">
      <app-ui-card title="Inicio" [padding]="'md'">
        <p class="text-sm text-muted-foreground">
          Sesión como
          <span class="font-medium text-foreground">{{ user()?.email }}</span>
          @if (user()?.roles?.length) {
            <span class="text-muted-foreground">
              · roles:
              <span class="text-foreground">{{ user()?.roles?.join(', ') }}</span>
            </span>
          }
        </p>
        <p class="mt-4 text-sm text-foreground">
          Usa el menú lateral para navegar según tu rol. Los permisos de API se
          aplican además del menú.
        </p>
      </app-ui-card>
    </div>
  `,
})
export class HomeComponent {
  private readonly auth = inject(AuthService);
  protected readonly user = this.auth.user;
}
