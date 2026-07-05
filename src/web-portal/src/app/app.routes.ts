import { Routes } from '@angular/router';

import { authGuard, adminGuard, guestEntryGuard, loginGuard } from './core/guards/auth.guard';
import { GuestLayoutComponent } from './core/layout/guest-layout.component';
import { ShellComponent } from './core/layout/shell.component';
import { AdminVolunteersComponent } from './features/admin/admin-volunteers.component';
import { LoginComponent } from './features/auth/login.component';
import { BoletaPageComponent } from './features/documentos/boleta-page.component';
import { DniPageComponent } from './features/documentos/dni-page.component';
import { RecetaPageComponent } from './features/documentos/receta-page.component';
import { GuestChatComponent } from './features/guest/guest-chat.component';
import { HomeComponent } from './features/home/home.component';
import { PatientsPageComponent } from './features/patients/patients-page.component';
import { PatientDetailComponent } from './features/patients/patient-detail.component';

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
      { path: 'pacientes', component: PatientsPageComponent },
      { path: 'pacientes/:id', component: PatientDetailComponent },
      { path: 'documentos/dni', component: DniPageComponent },
      { path: 'documentos/boleta', component: BoletaPageComponent },
      { path: 'documentos/receta', component: RecetaPageComponent },
      { path: 'demo', redirectTo: 'documentos/dni' },
      {
        path: 'admin/volunteers',
        component: AdminVolunteersComponent,
        canActivate: [adminGuard],
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
