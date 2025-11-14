import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
    // Rutas de autenticación
  {
    path: 'auth',
    loadChildren: () => import('./features/auth/app.routes').then(m => m.authRoutes)
  },

  {
    path: 'usuarios',
    loadComponent: () => import('./features/usuario/usuario-list/usuario-list.component').then(m => m.ProductoListComponent)
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];