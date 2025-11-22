// src/app/dashboard/admin-dashboard/dialogs/assign-equipment-dialog.component.ts
import { Component, Inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatRadioModule } from '@angular/material/radio';
import { AdminService } from '../../../core/services/admin.service';

@Component({
  selector: 'app-assign-equipment-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatDatepickerModule,
    MatRadioModule
  ],
  template: `
    <h2 mat-dialog-title>Assign Equipment</h2>
    <mat-dialog-content>
      <form [formGroup]="assignForm">
        <!-- User Selection -->
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Select User</mat-label>
          <mat-select formControlName="assigned_to_user_id" (selectionChange)="onUserChange($event)">
            <mat-option *ngFor="let user of users" [value]="user.id">
              {{ user.first_name }} {{ user.surname }} - {{ user.position }}
            </mat-option>
          </mat-select>
          <mat-error *ngIf="assignForm.get('assigned_to_user_id')?.hasError('required')">
            Please select a user
          </mat-error>
        </mat-form-field>

        <!-- Assignment Type -->
        <mat-radio-group formControlName="assignment_type" class="assignment-type-group">
          <label class="group-label">Assignment Type:</label>
          <mat-radio-button value="PAR">PAR (Regular Employee)</mat-radio-button>
          <mat-radio-button value="Job Order">Job Order Assignment</mat-radio-button>
        </mat-radio-group>

        <!-- PAR Number (only for PAR assignments) -->
        <mat-form-field appearance="outline" class="full-width" *ngIf="assignForm.get('assignment_type')?.value === 'PAR'">
          <mat-label>PAR Number</mat-label>
          <input matInput formControlName="par_number" placeholder="Enter PAR number">
          <mat-error *ngIf="assignForm.get('par_number')?.hasError('required')">
            PAR number is required for PAR assignments
          </mat-error>
        </mat-form-field>

        <!-- Assignment Date -->
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Assignment Date</mat-label>
          <input matInput [matDatepicker]="picker" formControlName="assigned_date">
          <mat-datepicker-toggle matSuffix [for]="picker"></mat-datepicker-toggle>
          <mat-datepicker #picker></mat-datepicker>
          <mat-error *ngIf="assignForm.get('assigned_date')?.hasError('required')">
            Assignment date is required
          </mat-error>
        </mat-form-field>

        <!-- Previous Recipient -->
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Previous Recipient (Optional)</mat-label>
          <input matInput formControlName="previous_recipient" placeholder="Previous recipient name">
        </mat-form-field>

        <!-- Info Box -->
        <div class="info-box" [class.par]="assignForm.get('assignment_type')?.value === 'PAR'">
          <mat-icon>info</mat-icon>
          <div class="info-text">
            <strong *ngIf="assignForm.get('assignment_type')?.value === 'PAR'">PAR Assignment:</strong>
            <strong *ngIf="assignForm.get('assignment_type')?.value === 'Job Order'">Job Order Assignment:</strong>
            <p *ngIf="assignForm.get('assignment_type')?.value === 'PAR'">
              This equipment will be assigned with a Property Accountability Record (PAR). 
              The employee will be held accountable for this property. A PAR document will be required.
            </p>
            <p *ngIf="assignForm.get('assignment_type')?.value === 'Job Order'">
              This is a temporary assignment for job order employees. 
              No PAR document is required, and the employee will not have property accountability.
            </p>
          </div>
        </div>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-raised-button color="primary" (click)="onAssign()" [disabled]="!assignForm.valid">
        Assign Equipment
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    .full-width {
      width: 100%;
      margin-bottom: 15px;
    }

    .assignment-type-group {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 20px;
      padding: 15px;
      background: #f5f7fb;
      border-radius: 8px;
    }

    .group-label {
      font-weight: 600;
      margin-bottom: 8px;
      color: #1f2937;
    }

    mat-radio-button {
      margin: 5px 0;
    }

    .info-box {
      display: flex;
      gap: 12px;
      padding: 15px;
      background: #e0f2fe;
      border-left: 4px solid #0284c7;
      border-radius: 8px;
      margin-top: 15px;
    }

    .info-box.par {
      background: #fef3c7;
      border-left-color: #f59e0b;
    }

    .info-box mat-icon {
      color: #0284c7;
      margin-top: 2px;
    }

    .info-box.par mat-icon {
      color: #f59e0b;
    }

    .info-text {
      flex: 1;
    }

    .info-text strong {
      display: block;
      margin-bottom: 5px;
      font-size: 14px;
    }

    .info-text p {
      margin: 0;
      font-size: 13px;
      color: #4b5563;
      line-height: 1.5;
    }

    mat-dialog-content {
      min-height: 400px;
      padding-top: 20px;
    }
  `]
})
export class AssignEquipmentDialogComponent implements OnInit {
  assignForm: FormGroup;
  users: any[] = [];

  constructor(
    private fb: FormBuilder,
    private adminService: AdminService,
    private dialogRef: MatDialogRef<AssignEquipmentDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.assignForm = this.fb.group({
      assigned_to_user_id: ['', Validators.required],
      assigned_to_name: ['', Validators.required],
      assignment_type: ['PAR', Validators.required],
      assigned_date: [new Date(), Validators.required],
      previous_recipient: [''],
      par_number: ['']
    });

    // Watch assignment type changes
    this.assignForm.get('assignment_type')?.valueChanges.subscribe(type => {
      const parNumberControl = this.assignForm.get('par_number');
      if (type === 'PAR') {
        parNumberControl?.setValidators([Validators.required]);
      } else {
        parNumberControl?.clearValidators();
        parNumberControl?.setValue('');
      }
      parNumberControl?.updateValueAndValidity();
    });
  }

  ngOnInit(): void {
    this.loadApprovedUsers();
  }

  loadApprovedUsers(): void {
    this.adminService.getApprovedUsers().subscribe({
      next: (users) => {
        this.users = users;
      },
      error: (error) => {
        console.error('Failed to load users:', error);
      }
    });
  }

  onUserChange(event: any): void {
    const selectedUser = this.users.find(u => u.id === event.value);
    if (selectedUser) {
      this.assignForm.patchValue({
        assigned_to_name: `${selectedUser.first_name} ${selectedUser.middle_name || ''} ${selectedUser.surname}`.trim()
      });
    }
  }

  onAssign(): void {
    if (this.assignForm.valid) {
      const formValue = this.assignForm.value;
      
      // Format the date
      const assignedDate = new Date(formValue.assigned_date);
      
      const result = {
        assigned_to_user_id: formValue.assigned_to_user_id,
        assigned_to_name: formValue.assigned_to_name,
        assignment_type: formValue.assignment_type,
        assigned_date: assignedDate.toISOString(),
        previous_recipient: formValue.previous_recipient || null,
        par_number: formValue.assignment_type === 'PAR' ? formValue.par_number : null
      };
      
      this.dialogRef.close(result);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}