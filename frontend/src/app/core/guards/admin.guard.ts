import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const adminGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  
  const currentUser = authService.currentUserValue;
  
  console.log('Admin guard - currentUser:', currentUser); // Debug
  console.log('Admin guard - role:', currentUser?.role); // Debug
  
  if (currentUser && currentUser.role === 'admin') {
    console.log('Admin guard - ALLOWED'); // Debug
    return true;
  }

  console.log('Admin guard - BLOCKED'); // Debug
  router.navigate(['/login']);
  return false;
};