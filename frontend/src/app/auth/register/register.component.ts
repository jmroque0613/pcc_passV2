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
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';  // Add this


@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './register.component.html'
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  loading = false;
  errorMessage = '';
  successMessage = '';

  salaryGrades: string[] = [];
  jobCategories = ['Job Order', 'Regular Employee'];
  assignedUnits = ['CCRD', 'CCTSIRMD', 'ISSU', 'Office of the Exec. Director'];

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Generate salary grades SG 1 to SG 30
    for (let i = 1; i <= 30; i++) {
      this.salaryGrades.push(`SG ${i}`);
    }

    this.registerForm = this.formBuilder.group({
      surname: ['', [Validators.required, Validators.maxLength(100)]],
      first_name: ['', [Validators.required, Validators.maxLength(100)]],
      middle_name: [''],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required],
      position: ['', [Validators.required, Validators.maxLength(200)]],
      salary_grade: ['', Validators.required],
      starting_date: ['', Validators.required],
      job_category: ['', Validators.required],
      assigned_unit: ['', Validators.required]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('confirmPassword');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }

  get f() {
    return this.registerForm.controls;
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      Object.keys(this.registerForm.controls).forEach(key => {
        this.registerForm.controls[key].markAsTouched();
      });
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    const formValue = this.registerForm.value;
    const registerData = {
      surname: formValue.surname,
      first_name: formValue.first_name,
      middle_name: formValue.middle_name || undefined,
      email: formValue.email,
      password: formValue.password,
      position: formValue.position,
      salary_grade: formValue.salary_grade,
      starting_date: new Date(formValue.starting_date),
      job_category: formValue.job_category,
      assigned_unit: formValue.assigned_unit
    };

    this.authService.register(registerData).subscribe({
      next: (response) => {
        this.successMessage = 'Registration successful! Your account is pending admin approval.';
        this.loading = false;
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 3000);
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Registration failed. Please try again.';
        this.loading = false;
      }
    });
  }
}