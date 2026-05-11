import { Routes } from '@angular/router';

import { authGuard, guestEntryGuard, loginGuard } from './core/guards/auth.guard';
import { GuestLayoutComponent } from './core/layout/guest-layout.component';
import { ShellComponent } from './core/layout/shell.component';
import { AdminVolunteersComponent } from './features/admin/admin-volunteers.component';
import { LoginComponent } from './features/auth/login.component';
import { DemoComponent } from './features/demo/demo.component';
import { GuestChatComponent } from './features/guest/guest-chat.component';
import { HomeComponent } from './features/home/home.component';
import { PatientsListComponent } from './features/patients/patients-list.component';

export const routes: Routes = [
  {
    path: '',
    component: GuestLayoutComponent,
    canActivate: [guestEntryGuard],
    children: [
      { path: '', pathMatch: 'full', component: GuestChatComponent },
    ],
  },
  { path: 'login', component: LoginComponent, canActivate: [loginGuard] },
  {
    path: 'app',
    component: ShellComponent,
    canActivate: [authGuard],
    children: [
      { path: '', pathMatch: 'full', component: HomeComponent },
      { path: 'pacientes', component: PatientsListComponent },
      { path: 'demo', component: DemoComponent },
      { path: 'admin/volunteers', component: AdminVolunteersComponent },
    ],
  },
  { path: '**', redirectTo: '' },
];
