// frontend/src/app/dashboard/admin-equipment/admin-equipment.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { EquipmentService } from '../../core/services/equipment.service';
import { AdminService } from '../../core/services/admin.service';
import { AuthService } from '../../core/services/auth.service';
import { Equipment, EQUIPMENT_TYPES, CONDITIONS, STATUSES } from '../../core/models/equipment.model';
import { User } from '../../core/models/user.model';

// Material Imports
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatMenuModule } from '@angular/material/menu';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { FilterPipe } from '../../core/pipes/filter.pipe';

@Component({
  selector: 'app-admin-equipment',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatProgressSpinnerModule,
    MatMenuModule,
    MatChipsModule,
    MatDividerModule,
    FilterPipe
  ],
  templateUrl: './admin-equipment.component.html'
})
export class AdminEquipmentComponent implements OnInit {
  equipmentList: Equipment[] = [];
  allUsers: User[] = [];
  loading = false;
  showAddForm = false;
  showAssignForm = false;
  successMessage = '';
  errorMessage = '';
  
  equipmentForm!: FormGroup;
  assignForm!: FormGroup;
  selectedEquipment: Equipment | null = null;
  selectedFile: File | null = null;
  
  // Dropdowns
  equipmentTypes = EQUIPMENT_TYPES;
  conditions = CONDITIONS;
  statuses = STATUSES;
  
  // Table columns
  displayedColumns: string[] = [
    'property_number',
    'equipment_type',
    'brand',
    'model',
    'status',
    'assigned_to',
    'actions'
  ];

  constructor(
    private fb: FormBuilder,
    private equipmentService: EquipmentService,
    private adminService: AdminService,
    private authService: AuthService,
    private router: Router,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.initForms();
    this.loadEquipment();
    this.loadUsers();
  }

  initForms(): void {
    // Equipment Form
    this.equipmentForm = this.fb.group({
      property_number: ['', [Validators.required]],
      gsd_code: ['', [Validators.required]],
      item_number: ['', [Validators.required]],
      equipment_type: ['', [Validators.required]],
      brand: ['', [Validators.required]],
      model: ['', [Validators.required]],
      serial_number: ['', [Validators.required]],
      specifications: [''],
      acquisition_date: ['', [Validators.required]],
      acquisition_cost: ['', [Validators.required, Validators.min(0)]],
      condition: ['New', [Validators.required]],
      status: ['Available', [Validators.required]],
      remarks: ['']
    });

    // Assign Form
    this.assignForm = this.fb.group({
      assigned_to_user_id: ['', [Validators.required]],
      assigned_date: [new Date(), [Validators.required]],
      par_number: [''],
      previous_recipient: ['']
    });
  }

  loadEquipment(): void {
    this.loading = true;
    this.equipmentService.getAllEquipment().subscribe({
      next: (data) => {
        this.equipmentList = data;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to load equipment';
        this.loading = false;
        console.error(error);
      }
    });
  }

  loadUsers(): void {
    this.adminService.getAllUsers().subscribe({
      next: (users) => {
        this.allUsers = users.filter(u => u.is_approved && u.is_active);
      },
      error: (error) => {
        console.error('Failed to load users:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.equipmentForm.invalid) {
      Object.keys(this.equipmentForm.controls).forEach(key => {
        this.equipmentForm.controls[key].markAsTouched();
      });
      return;
    }

    this.loading = true;
    const formData = this.equipmentForm.value;

    if (this.selectedEquipment) {
      // Update existing equipment
      this.equipmentService.updateEquipment(this.selectedEquipment.id, formData).subscribe({
        next: (response) => {
          this.successMessage = 'Equipment updated successfully!';
          this.showAddForm = false;
          this.selectedEquipment = null;
          this.equipmentForm.reset();
          this.loadEquipment();
          this.clearMessageAfterDelay();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to update equipment';
          this.loading = false;
          this.clearMessageAfterDelay();
        }
      });
    } else {
      // Create new equipment
      this.equipmentService.createEquipment(formData).subscribe({
        next: (response) => {
          this.successMessage = 'Equipment added successfully!';
          this.showAddForm = false;
          this.equipmentForm.reset();
          this.loadEquipment();
          this.clearMessageAfterDelay();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to add equipment';
          this.loading = false;
          this.clearMessageAfterDelay();
        }
      });
    }
  }

  editEquipment(equipment: Equipment): void {
    this.selectedEquipment = equipment;
    this.showAddForm = true;
    
    this.equipmentForm.patchValue({
      property_number: equipment.property_number,
      gsd_code: equipment.gsd_code,
      item_number: equipment.item_number,
      equipment_type: equipment.equipment_type,
      brand: equipment.brand,
      model: equipment.model,
      serial_number: equipment.serial_number,
      specifications: equipment.specifications,
      acquisition_date: new Date(equipment.acquisition_date),
      acquisition_cost: equipment.acquisition_cost,
      condition: equipment.condition,
      status: equipment.status,
      remarks: equipment.remarks
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  deleteEquipment(equipment: Equipment): void {
    if (!confirm(`Are you sure you want to delete ${equipment.property_number}?`)) {
      return;
    }

    this.equipmentService.deleteEquipment(equipment.id).subscribe({
      next: () => {
        this.successMessage = 'Equipment deleted successfully';
        this.loadEquipment();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to delete equipment';
        this.clearMessageAfterDelay();
      }
    });
  }

  openAssignDialog(equipment: Equipment): void {
    const dialogRef = this.dialog.open(AssignEquipmentDialogComponent, {
      width: '600px',
      data: { equipment }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.assignEquipment(equipment.id!, result);
      }
    });
  }

  onAssignSubmit(): void {
    if (this.assignForm.invalid || !this.selectedEquipment) {
      return;
    }

    const selectedUser = this.allUsers.find(u => u.id === this.assignForm.value.assigned_to_user_id);
    if (!selectedUser) {
      this.errorMessage = 'User not found';
      return;
    }

    const assignData = {
      assigned_to_user_id: this.assignForm.value.assigned_to_user_id,
      assigned_to_name: `${selectedUser.first_name} ${selectedUser.surname}`,
      assigned_date: this.assignForm.value.assigned_date,
      previous_recipient: this.assignForm.value.previous_recipient,
      par_number: this.assignForm.value.par_number
    };

    this.equipmentService.assignEquipment(this.selectedEquipment.id, assignData).subscribe({
      next: (response) => {
        this.successMessage = 'Equipment assigned successfully!';
        this.showAssignForm = false;
        this.selectedEquipment = null;
        this.assignForm.reset();
        this.loadEquipment();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to assign equipment';
        this.clearMessageAfterDelay();
      }
    });
  }

  unassignEquipment(equipment: Equipment): void {
    if (!confirm(`Unassign equipment from ${equipment.assigned_to_name}?`)) {
      return;
    }

    this.equipmentService.unassignEquipment(equipment.id).subscribe({
      next: () => {
        this.successMessage = 'Equipment unassigned successfully';
        this.loadEquipment();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to unassign equipment';
        this.clearMessageAfterDelay();
      }
    });
  }

  onFileSelected(event: any, equipment: Equipment): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      this.uploadPAR(equipment);
    } else {
      this.errorMessage = 'Please select a PDF file';
      this.clearMessageAfterDelay();
    }
  }

  uploadPAR(equipment: Equipment): void {
    if (!this.selectedFile) return;

    this.equipmentService.uploadEquipmentPAR(equipment.id, this.selectedFile).subscribe({
      next: () => {
        this.successMessage = 'PAR document uploaded successfully';
        this.selectedFile = null;
        this.loadEquipment();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to upload PAR';
        this.clearMessageAfterDelay();
      }
    });
  }

  downloadPAR(equipment: Equipment): void {
    this.equipmentService.downloadEquipmentPAR(equipment.id).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `PAR_${equipment.property_number}.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        this.errorMessage = 'Failed to download PAR document';
        this.clearMessageAfterDelay();
      }
    });
  }

  cancelForm(): void {
    this.showAddForm = false;
    this.showAssignForm = false;
    this.selectedEquipment = null;
    this.equipmentForm.reset({
      condition: 'New',
      status: 'Available'
    });
    this.assignForm.reset();
  }

  clearMessageAfterDelay(): void {
    setTimeout(() => {
      this.successMessage = '';
      this.errorMessage = '';
    }, 3000);
  }

  getStatusColor(status: string): string {
    const colors: any = {
      'Available': 'success',
      'Assigned': 'primary',
      'Under Repair': 'warning',
      'Disposed': 'danger'
    };
    return colors[status] || 'default';
  }

  goBack(): void {
    this.router.navigate(['/admin/dashboard']);
  }
}