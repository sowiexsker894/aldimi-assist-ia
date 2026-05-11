import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-guest-layout',
  imports: [RouterOutlet, RouterLink],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './guest-layout.component.html',
  styleUrl: './guest-layout.component.scss',
})
export class GuestLayoutComponent {}
