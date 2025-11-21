import { Routes } from '@angular/router';
import { userGuard } from './core/guards/user.guard';
import { adminGuard } from './core/guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { 
    path: 'login', 
    loadComponent: () => import('./auth/login/login.component').then(m => m.LoginComponent)
  },
  { 
    path: 'register', 
    loadComponent: () => import('./auth/register/register.component').then(m => m.RegisterComponent)
  },
  { 
    path: 'admin-register', 
    loadComponent: () => import('./auth/admin-register/admin-register.component').then(m => m.AdminRegisterComponent)
  },
  { 
    path: 'admin/dashboard',  // ADD THIS ROUTE
    loadComponent: () => import('./dashboard/admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent),
    canActivate: [adminGuard]
  },
    { 
    path: 'admin/equipment', 
    loadComponent: () => import('./dashboard/admin-equipment/admin-equipment.component').then(m => m.AdminEquipmentComponent),
    canActivate: [adminGuard]
  },
  { 
    path: 'admin/furniture', 
    loadComponent: () => import('./dashboard/admin-furniture/admin-furniture.component').then(m => m.AdminFurnitureComponent),
    canActivate: [adminGuard]
  },
  { 
    path: 'user/dashboard', 
    loadComponent: () => import('./dashboard/user-dashboard/user-dashboard.component').then(m => m.UserDashboardComponent),
    canActivate: [userGuard]
  },
  { path: '**', redirectTo: '/login' }
];