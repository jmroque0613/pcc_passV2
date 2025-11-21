// src/app/dashboard/user-dashboard/user-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { EquipmentService } from '../../core/services/equipment.service';
import { Equipment, Furniture } from '../../core/models/equipment.model';

// Material Imports
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatTableModule } from '@angular/material/table';
import { MatBadgeModule } from '@angular/material/badge';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-user-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatTableModule,
    MatBadgeModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './user-dashboard.component.html'
})
export class UserDashboardComponent implements OnInit {
  currentUser: any;
  currentDate = new Date();
  activePage = 'dashboard';
  loading = false;

  // Stats
  hrFilesCount = 0;
  equipmentCount = 0;
  furnitureCount = 0;

  // Equipment & Furniture Lists
  equipmentList: Equipment[] = [];
  furnitureList: Furniture[] = [];

  // Table columns for equipment
  equipmentColumns: string[] = [
    'property_number',
    'equipment_type',
    'brand',
    'model',
    'date_received',
    'actions'
  ];

  constructor(
    private authService: AuthService,
    private equipmentService: EquipmentService,
    private router: Router
  ) {
    this.currentUser = this.authService.currentUserValue;
    
    // Redirect if not logged in
    if (!this.currentUser) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit(): void {
    this.loadMyEquipment();
    this.loadMyFurniture();
  }

  loadMyEquipment(): void {
    this.loading = true;
    this.equipmentService.getMyEquipment().subscribe({
      next: (data) => {
        this.equipmentList = data;
        this.equipmentCount = data.length;
        this.loading = false;
      },
      error: (error) => {
        console.error('Failed to load equipment:', error);
        this.loading = false;
      }
    });
  }

  loadMyFurniture(): void {
    this.equipmentService.getMyFurniture().subscribe({
      next: (data) => {
        this.furnitureList = data;
        this.furnitureCount = data.length;
      },
      error: (error) => {
        console.error('Failed to load furniture:', error);
      }
    });
  }

  getEquipmentIcon(type: string): string {
    const iconMap: { [key: string]: string } = {
      'Desktop Computer': 'computer',
      'Laptop': 'laptop',
      'Monitor': 'monitor',
      'Keyboard': 'keyboard',
      'Mouse': 'mouse',
      'Printer': 'print',
      'Scanner': 'scanner',
      'UPS': 'power',
      'External Hard Drive': 'storage',
      'Network Device': 'router',
      'Projector': 'videocam',
      'Webcam': 'videocam',
      'Headset': 'headset'
    };
    return iconMap[type] || 'devices';
  }

  getFurnitureIcon(type: string): string {
    const iconMap: { [key: string]: string } = {
      'Office Chair': 'chair',
      'Executive Chair': 'chair',
      'Office Desk': 'desk',
      'Conference Table': 'table_restaurant',
      'Filing Cabinet': 'shelves',
      'Bookshelf': 'shelves',
      'Storage Cabinet': 'shelves',
      'Drawer': 'shelves',
      'Workstation': 'desk',
      'Partition': 'vertical_split'
    };
    return iconMap[type] || 'chair';
  }

  downloadPAR(equipmentId: string): void {
    this.equipmentService.downloadEquipmentPAR(equipmentId).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `PAR_Equipment_${equipmentId}.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        console.error('Failed to download PAR:', error);
        alert('Failed to download PAR document');
      }
    });
  }

  downloadFurniturePAR(furnitureId: string): void {
    this.equipmentService.downloadFurniturePAR(furnitureId).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `PAR_Furniture_${furnitureId}.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        console.error('Failed to download PAR:', error);
        alert('Failed to download PAR document');
      }
    });
  }

  logout(): void {
    this.authService.logout();
  }
}