import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

// Material Imports
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';  // Add this


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = false;
  errorMessage = '';
  hidePassword = true;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    // Redirect if already logged in
    if (this.authService.currentUserValue) {
      if (this.authService.isAdmin) {
        this.router.navigate(['/admin/dashboard']);
      } else {
        this.router.navigate(['/user/dashboard']);
      }
    }
  }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  get f() {
    return this.loginForm.controls;
  }

onSubmit(): void {
  if (this.loginForm.invalid) {
    Object.keys(this.loginForm.controls).forEach(key => {
      this.loginForm.controls[key].markAsTouched();
    });
    return;
  }

  this.loading = true;
  this.errorMessage = '';

  this.authService.login(this.loginForm.value).subscribe({
    next: (response) => {
      console.log('Login successful!');
      console.log('Full response:', response);
      console.log('User:', response.user);
      console.log('User role:', response.user.role);
      
      if (response.user.role === 'admin') {
        console.log('Attempting to navigate to /admin/dashboard');
        this.router.navigate(['/admin/dashboard']).then(
          success => console.log('Navigation success:', success),
          error => console.error('Navigation error:', error)
        );
      } else {
        console.log('Attempting to navigate to /user/dashboard');
        this.router.navigate(['/user/dashboard']).then(
          success => console.log('Navigation success:', success),
          error => console.error('Navigation error:', error)
        );
      }
    },
    error: (error) => {
      console.error('Login error:', error);
      this.errorMessage = error.error?.detail || 'Login failed. Please check your credentials.';
      this.loading = false;
    }
  });
}
}