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
  recentHRFiles: any[] = [];
  hrFilesList: any[] = [];
  equipmentByType: any[] = [];

  // Table columns for equipment - FIXED COLUMNS
  equipmentColumns: string[] = [
    'property_number',
    'gsd_code',
    'equipment_type',
    'brand',
    'model',
    'assigned_date',
    'previous_recipient',
    'actions'
  ];

  constructor(
    private authService: AuthService,
    private equipmentService: EquipmentService,
    private router: Router
  ) {
    this.currentUser = this.authService.currentUserValue;
    
    if (!this.currentUser) {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit(): void {
    console.log('User Dashboard initialized');
    console.log('Current User:', this.currentUser);
    this.loadMyEquipment();
    this.loadMyFurniture();
  }

  loadMyEquipment(): void {
    this.loading = true;
    console.log('Loading equipment for user:', this.currentUser?.id);
    
    this.equipmentService.getMyEquipment().subscribe({
      next: (data) => {
        console.log('Equipment loaded:', data);
        this.equipmentList = data;
        this.equipmentCount = data.length;
        this.calculateEquipmentByType(data);
        this.loading = false;
      },
      error: (error) => {
        console.error('Failed to load equipment:', error);
        this.loading = false;
      }
    });
  }

  loadMyFurniture(): void {
    console.log('Loading furniture for user:', this.currentUser?.id);
    
    this.equipmentService.getMyFurniture().subscribe({
      next: (data) => {
        console.log('Furniture loaded:', data);
        this.furnitureList = data;
        this.furnitureCount = data.length;
      },
      error: (error) => {
        console.error('Failed to load furniture:', error);
      }
    });
  }

  calculateEquipmentByType(equipment: Equipment[]): void {
    const typeMap = new Map<string, number>();
    equipment.forEach(eq => {
      typeMap.set(eq.equipment_type, (typeMap.get(eq.equipment_type) || 0) + 1);
    });
    
    this.equipmentByType = Array.from(typeMap.entries()).map(([type, count]) => ({
      type,
      count
    })).slice(0, 5); // Show top 5 types
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

  downloadFile(fileId: string): void {
    console.log('Download file:', fileId);
  }

  logout(): void {
    this.authService.logout();
  }

  // Inline Styles Method
  getStyles(element: string, variant?: any): string {
    const styles: { [key: string]: string } = {
      // Layout
      'wrapper': 'display: flex; min-height: 100vh; background: #f5f7fb; margin: 0; padding: 0; box-sizing: border-box;',
      
      // Sidebar
      'sidebar': 'width: 280px; background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); color: white; display: flex; flex-direction: column; box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1); position: fixed; height: 100vh; overflow-y: auto;',
      'logoSection': 'padding: 30px 20px; text-align: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1);',
      'logoIcon': 'width: 60px; height: 60px; background: white; color: #6366f1; border-radius: 15px; display: inline-flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 700; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);',
      'navMenu': 'flex: 1; padding: 20px 0;',
      'sidebarFooter': 'padding: 20px 0; border-top: 1px solid rgba(255, 255, 255, 0.1);',
      
      // Main Content
      'mainContent': 'flex: 1; margin-left: 280px; display: flex; flex-direction: column;',
      'topBar': 'background: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); position: sticky; top: 0; z-index: 10;',
      'userSection': 'display: flex; align-items: center; gap: 20px;',
      'userInfo': 'display: flex; align-items: center; gap: 12px;',
      'userAvatar': 'width: 45px; height: 45px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;',
      'userDetails': 'display: flex; flex-direction: column;',
      'userName': 'font-weight: 600; font-size: 14px; color: #1f2937;',
      'userRole': 'font-size: 12px; color: #6b7280;',
      
      // Content Area
      'contentArea': 'padding: 30px 40px; flex: 1;',
      
      // Welcome Card
      'welcomeCard': 'background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 30px; border-radius: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);',
      'welcomeTitle': 'font-size: 28px; margin-bottom: 8px; margin: 0;',
      'welcomeText': 'opacity: 0.9; font-size: 15px; margin: 0;',
      'welcomeDate': 'display: flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.2); padding: 12px 20px; border-radius: 12px;',
      
      // Stats Grid
      'statsGrid': 'display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;',
      'statDetails': 'flex: 1;',
      'statValue': 'font-size: 32px; font-weight: 700; color: #1f2937;',
      'statLabel': 'font-size: 14px; color: #6b7280; margin-top: 4px;',
      'statIconMat': 'font-size: 30px; width: 30px; height: 30px;',
      
      // Dashboard Grid
      'dashboardGrid': 'display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px;',
      'dashboardCard': 'background: white; border-radius: 16px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); overflow: hidden;',
      'cardHeader': 'padding: 20px 25px; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; align-items: center;',
      'cardTitle': 'font-size: 16px; font-weight: 600; color: #1f2937; display: flex; align-items: center; gap: 10px; margin: 0;',
      'cardLink': 'color: #6366f1; text-decoration: none; font-size: 14px; font-weight: 500;',
      'cardContent': 'padding: 20px 25px;',
      
      // File List
      'fileList': 'display: flex; flex-direction: column; gap: 15px;',
      'fileItem': 'display: flex; align-items: center; gap: 15px; padding: 15px; background: #f9fafb; border-radius: 12px; transition: all 0.3s ease;',
      'fileIcon': 'width: 45px; height: 45px; background: rgba(99, 102, 241, 0.1); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #6366f1;',
      'fileInfo': 'flex: 1;',
      'fileName': 'font-size: 14px; font-weight: 500; color: #1f2937; margin-bottom: 4px;',
      'fileMeta': 'font-size: 12px; color: #6b7280;',
      
      // Equipment Summary
      'equipmentSummary': 'display: flex; flex-direction: column; gap: 15px;',
      'equipmentType': 'display: flex; justify-content: space-between; align-items: center; padding: 15px; background: #f9fafb; border-radius: 12px;',
      'typeInfo': 'display: flex; align-items: center; gap: 12px; color: #4b5563;',
      'typeCount': 'font-size: 18px; font-weight: 600; color: #6366f1;',
      
      // Profile Card
      'profileCard': 'background: white; border-radius: 16px; padding: 30px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);',
      'profileHeader': 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;',
      'profileTitle': 'font-size: 18px; font-weight: 600; color: #1f2937; margin: 0;',
      'profileGrid': 'display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px;',
      'profileItem': 'display: flex; align-items: flex-start; gap: 15px;',
      'profileIcon': 'color: #6366f1; margin-top: 2px;',
      'profileInfo': 'flex: 1;',
      'infoLabel': 'font-size: 12px; color: #6b7280; margin-bottom: 4px;',
      'infoValue': 'font-size: 14px; font-weight: 500; color: #1f2937;',
      
      // Page Header
      'pageHeader': 'margin-bottom: 25px;',
      'pageTitle': 'font-size: 26px; font-weight: 600; color: #1f2937; margin-bottom: 8px; margin: 0 0 8px 0;',
      'pageSubtitle': 'color: #6b7280; font-size: 14px; margin: 0;',
      
      // Table Card
      'tableCard': 'background: white; border-radius: 16px; padding: 25px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); overflow-x: auto;',
      'equipmentBadge': 'display: inline-block; padding: 6px 12px; background: rgba(99, 102, 241, 0.1); color: #6366f1; border-radius: 8px; font-size: 12px; font-weight: 500;',
      'noPar': 'color: #9ca3af; font-size: 12px; font-style: italic;',
      
      // File Grid
      'fileGrid': 'display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px;',
      'fileCard': 'background: #f9fafb; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; align-items: center; text-align: center; transition: all 0.3s ease; border: 2px solid transparent;',
      'fileCardIcon': 'width: 60px; height: 60px; background: rgba(99, 102, 241, 0.1); border-radius: 15px; display: flex; align-items: center; justify-content: center; color: #6366f1; margin-bottom: 15px;',
      'fileCardIconMat': 'font-size: 32px; width: 32px; height: 32px;',
      'fileCardInfo': 'flex: 1; margin-bottom: 15px;',
      'fileCardTitle': 'font-size: 14px; font-weight: 600; color: #1f2937; margin-bottom: 4px; margin: 0 0 4px 0;',
      'fileCardType': 'font-size: 12px; color: #6b7280; margin-bottom: 8px; margin: 0 0 8px 0;',
      'fileDate': 'font-size: 11px; color: #9ca3af;',
      
      // Furniture Grid
      'furnitureGrid': 'display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;',
      'furnitureCard': 'background: white; border: 2px solid #f3f4f6; border-radius: 12px; padding: 20px; display: flex; align-items: center; gap: 15px; transition: all 0.3s ease;',
      'furnitureIcon': 'width: 50px; height: 50px; background: rgba(245, 158, 11, 0.1); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #f59e0b;',
      'furnitureIconMat': 'font-size: 28px; width: 28px; height: 28px;',
      'furnitureInfo': 'flex: 1;',
      'furnitureTitle': 'font-size: 15px; font-weight: 600; color: #1f2937; margin-bottom: 4px; margin: 0 0 4px 0;',
      'furnitureType': 'font-size: 13px; color: #6b7280; margin-bottom: 6px; margin: 0 0 6px 0;',
      'furnitureDate': 'font-size: 11px; color: #9ca3af;',
      
      // Empty State
      'emptyState': 'text-align: center; padding: 60px 20px; color: #9ca3af;',
      'emptyIcon': 'font-size: 80px; width: 80px; height: 80px; opacity: 0.3; margin-bottom: 15px;',
      'emptyTitle': 'font-size: 18px; margin-bottom: 8px; color: #4b5563; margin: 0 0 8px 0;',
      'emptyText': 'font-size: 14px; margin: 0;',
    };

    // Handle nav item with active state
    if (element === 'navItem') {
      return variant 
        ? 'display: flex; align-items: center; gap: 15px; padding: 15px 25px; color: white; text-decoration: none; transition: all 0.3s ease; border-left: 3px solid white; background: rgba(255, 255, 255, 0.15); cursor: pointer;'
        : 'display: flex; align-items: center; gap: 15px; padding: 15px 25px; color: rgba(255, 255, 255, 0.8); text-decoration: none; transition: all 0.3s ease; border-left: 3px solid transparent; cursor: pointer;';
    }

    // Handle stat cards with color variants
    if (element === 'statCard') {
      const borderColors: { [key: string]: string } = {
        'purple': '#8b5cf6',
        'blue': '#3b82f6',
        'orange': '#f59e0b'
      };
      const borderColor = borderColors[variant] || '#8b5cf6';
      return `background: white; padding: 25px; border-radius: 16px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); display: flex; align-items: center; gap: 20px; position: relative; overflow: hidden; border-left: 4px solid ${borderColor};`;
    }

    // Handle stat icons with color variants
    if (element === 'statIcon') {
      const colors: { [key: string]: { bg: string; color: string } } = {
        'purple': { bg: 'rgba(139, 92, 246, 0.1)', color: '#8b5cf6' },
        'blue': { bg: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6' },
        'orange': { bg: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b' }
      };
      const style = colors[variant] || colors['purple'];
      return `width: 60px; height: 60px; border-radius: 15px; display: flex; align-items: center; justify-content: center; background: ${style.bg}; color: ${style.color};`;
    }

    // Handle stat charts with color variants
    if (element === 'statChart') {
      const colors: { [key: string]: string } = {
        'purple': '#8b5cf6',
        'blue': '#3b82f6',
        'orange': '#f59e0b'
      };
      const color = colors[variant] || '#8b5cf6';
      return `position: absolute; right: 20px; bottom: 0; width: 100px; height: 40px; opacity: 0.3; color: ${color};`;
    }

    return styles[element] || '';
  }
}