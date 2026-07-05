import {
  ChangeDetectionStrategy,
  Component,
  signal,
} from '@angular/core';
import { UiTabs } from '../../shared/ui';
import { PatientsListTabComponent } from './patients-list-tab.component';
import { PatientsRegisterTabComponent } from './patients-register-tab.component';

@Component({
  selector: 'app-patients-page',
  imports: [UiTabs, PatientsListTabComponent, PatientsRegisterTabComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="space-y-6 p-6">
      <app-ui-tabs
        [tabs]="tabs"
        [activeId]="activeTab()"
        (tabChange)="activeTab.set($event)"
      />

      @if (activeTab() === 'list') {
        <app-patients-list-tab />
      } @else {
        <app-patients-register-tab (registered)="activeTab.set('list')" />
      }
    </div>
  `,
})
export class PatientsPageComponent {
  protected readonly tabs = [
    { id: 'list', label: 'Listado' },
    { id: 'register', label: 'Registro' },
  ];
  protected readonly activeTab = signal('list');
}
