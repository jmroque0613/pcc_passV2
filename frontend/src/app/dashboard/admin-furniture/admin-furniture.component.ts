// frontend/src/app/dashboard/admin-furniture/admin-furniture.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { EquipmentService } from '../../core/services/equipment.service';
import { AdminService } from '../../core/services/admin.service';
import { AuthService } from '../../core/services/auth.service';
import { Furniture, FURNITURE_TYPES, CONDITIONS, STATUSES } from '../../core/models/equipment.model';
import { User } from '../../core/models/user.model';
import { FilterPipe } from '../../core/pipes/filter.pipe';

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

@Component({
  selector: 'app-admin-furniture',
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
  templateUrl: './admin-furniture.component.html'
})
export class AdminFurnitureComponent implements OnInit {
  furnitureList: Furniture[] = [];
  allUsers: User[] = [];
  loading = false;
  showAddForm = false;
  showAssignForm = false;
  successMessage = '';
  errorMessage = '';
  
  furnitureForm!: FormGroup;
  assignForm!: FormGroup;
  selectedFurniture: Furniture | null = null;
  selectedFile: File | null = null;
  
  // Dropdowns
  furnitureTypes = FURNITURE_TYPES;
  conditions = CONDITIONS;
  statuses = STATUSES;
  
  // Table columns
  displayedColumns: string[] = [
    'property_number',
    'furniture_type',
    'description',
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
    this.loadFurniture();
    this.loadUsers();
  }

  initForms(): void {
    // Furniture Form
    this.furnitureForm = this.fb.group({
      property_number: ['', [Validators.required]],
      gsd_code: ['', [Validators.required]],
      item_number: ['', [Validators.required]],
      furniture_type: ['', [Validators.required]],
      description: ['', [Validators.required]],
      brand: [''],
      material: [''],
      color: [''],
      dimensions: [''],
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
      assignment_type: ['PAR', [Validators.required]],
      location: [''],
      par_number: ['']
    });
  }

  loadFurniture(): void {
    this.loading = true;
    this.equipmentService.getAllFurniture().subscribe({
      next: (data) => {
        this.furnitureList = data;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = 'Failed to load furniture';
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
    if (this.furnitureForm.invalid) {
      Object.keys(this.furnitureForm.controls).forEach(key => {
        this.furnitureForm.controls[key].markAsTouched();
      });
      return;
    }

    this.loading = true;
    const formData = this.furnitureForm.value;

    if (this.selectedFurniture && this.selectedFurniture.id) {
      // Update existing furniture - FIXED
      this.equipmentService.updateFurniture(this.selectedFurniture.id, formData).subscribe({
        next: (response) => {
          this.successMessage = 'Furniture updated successfully!';
          this.showAddForm = false;
          this.selectedFurniture = null;
          this.furnitureForm.reset();
          this.loadFurniture();
          this.clearMessageAfterDelay();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to update furniture';
          this.loading = false;
          this.clearMessageAfterDelay();
        }
      });
    } else {
      // Create new furniture
      this.equipmentService.createFurniture(formData).subscribe({
        next: (response) => {
          this.successMessage = 'Furniture added successfully!';
          this.showAddForm = false;
          this.furnitureForm.reset();
          this.loadFurniture();
          this.clearMessageAfterDelay();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to add furniture';
          this.loading = false;
          this.clearMessageAfterDelay();
        }
      });
    }
  }

  editFurniture(furniture: Furniture): void {
    if (!furniture.id) {
      this.errorMessage = 'Invalid furniture data';
      this.clearMessageAfterDelay();
      return;
    }

    this.selectedFurniture = furniture;
    this.showAddForm = true;
    
    this.furnitureForm.patchValue({
      property_number: furniture.property_number,
      gsd_code: furniture.gsd_code,
      item_number: furniture.item_number,
      furniture_type: furniture.furniture_type,
      description: furniture.description,
      brand: furniture.brand,
      material: furniture.material,
      color: furniture.color,
      dimensions: furniture.dimensions,
      acquisition_date: furniture.acquisition_date ? new Date(furniture.acquisition_date) : null, // FIXED
      acquisition_cost: furniture.acquisition_cost,
      condition: furniture.condition,
      status: furniture.status,
      remarks: furniture.remarks
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  deleteFurniture(furniture: Furniture): void {
    if (!furniture.id) {
      this.errorMessage = 'Invalid furniture data';
      this.clearMessageAfterDelay();
      return;
    }

    if (!confirm(`Are you sure you want to delete ${furniture.property_number}?`)) {
      return;
    }

    this.equipmentService.deleteFurniture(furniture.id).subscribe({
      next: () => {
        this.successMessage = 'Furniture deleted successfully';
        this.loadFurniture();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to delete furniture';
        this.clearMessageAfterDelay();
      }
    });
  }

  openAssignDialog(furniture: Furniture): void {
    if (!furniture.id) {
      this.errorMessage = 'Invalid furniture data';
      this.clearMessageAfterDelay();
      return;
    }

    this.selectedFurniture = furniture;
    this.showAssignForm = true;
    this.assignForm.reset({
      assigned_to_user_id: '',
      assigned_date: new Date(),
      assignment_type: 'PAR',
      location: '',
      par_number: ''
    });
  }

  onAssignSubmit(): void {
    if (this.assignForm.invalid || !this.selectedFurniture || !this.selectedFurniture.id) {
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
      assignment_type: this.assignForm.value.assignment_type,
      location: this.assignForm.value.location,
      par_number: this.assignForm.value.par_number
    };

    this.equipmentService.assignFurniture(this.selectedFurniture.id, assignData).subscribe({
      next: (response) => {
        this.successMessage = 'Furniture assigned successfully!';
        this.showAssignForm = false;
        this.selectedFurniture = null;
        this.assignForm.reset();
        this.loadFurniture();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to assign furniture';
        this.clearMessageAfterDelay();
      }
    });
  }

  unassignFurniture(furniture: Furniture): void {
    if (!furniture.id) {
      this.errorMessage = 'Invalid furniture data';
      this.clearMessageAfterDelay();
      return;
    }

    if (!confirm(`Unassign furniture from ${furniture.assigned_to_name}?`)) {
      return;
    }

    this.equipmentService.unassignFurniture(furniture.id).subscribe({
      next: () => {
        this.successMessage = 'Furniture unassigned successfully';
        this.loadFurniture();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to unassign furniture';
        this.clearMessageAfterDelay();
      }
    });
  }

  onFileSelected(event: any, furniture: Furniture): void {
    if (!furniture.id) {
      this.errorMessage = 'Invalid furniture data';
      this.clearMessageAfterDelay();
      return;
    }

    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      this.uploadPAR(furniture);
    } else {
      this.errorMessage = 'Please select a PDF file';
      this.clearMessageAfterDelay();
    }
  }

  uploadPAR(furniture: Furniture): void {
    if (!this.selectedFile || !furniture.id) return;

    this.equipmentService.uploadFurniturePAR(furniture.id, this.selectedFile).subscribe({
      next: () => {
        this.successMessage = 'PAR document uploaded successfully';
        this.selectedFile = null;
        this.loadFurniture();
        this.clearMessageAfterDelay();
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Failed to upload PAR';
        this.clearMessageAfterDelay();
      }
    });
  }

  downloadPAR(furniture: Furniture): void {
    if (!furniture.id) {
      this.errorMessage = 'Invalid furniture data';
      this.clearMessageAfterDelay();
      return;
    }

    this.equipmentService.downloadFurniturePAR(furniture.id).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `PAR_${furniture.property_number}.pdf`;
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
    this.selectedFurniture = null;
    this.furnitureForm.reset({
      condition: 'New',
      status: 'Available'
    });
    this.assignForm.reset({
      assignment_type: 'PAR',
      assigned_date: new Date()
    });
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