import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { UiGlobalLoader } from './shared/ui';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, UiGlobalLoader],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {}
