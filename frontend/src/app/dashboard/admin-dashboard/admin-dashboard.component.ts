// frontend/src/app/dashboard/admin-dashboard/admin-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { AdminService } from '../../core/services/admin.service';
import { User, PendingUser } from '../../core/models/user.model';

// Material Imports
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatBadgeModule } from '@angular/material/badge';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatMenuModule } from '@angular/material/menu';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatIconModule,
    MatButtonModule,
    MatTableModule,
    MatCardModule,
    MatBadgeModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatMenuModule
  ],
  templateUrl: './admin-dashboard.component.html'
})
export class AdminDashboardComponent implements OnInit {
  currentAdmin: any;
  currentDate = new Date();
  activePage = 'dashboard';
  sidebarOpen = true;
  loading = false;
  successMessage = '';
  errorMessage = '';

  // Data
  pendingUsers: PendingUser[] = [];
  allUsers: User[] = [];
  
  // Stats
  stats = {
    totalUsers: 0,
    pendingApprovals: 0,
    activeUsers: 0,
    inactiveUsers: 0
  };

  // Table columns
  userColumns: string[] = ['name', 'email', 'position', 'grade', 'unit', 'status', 'actions'];

  constructor(
    private authService: AuthService,
    private adminService: AdminService,
    private router: Router
  ) {
    this.currentAdmin = this.authService.currentUserValue;
    
    // Redirect if not admin
    if (!this.currentAdmin || this.currentAdmin.role !== 'admin') {
      this.router.navigate(['/login']);
    }
  }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;

    // Load pending users
    this.adminService.getPendingUsers().subscribe({
      next: (users) => {
        this.pendingUsers = users;
        this.stats.pendingApprovals = users.length;
      },
      error: (error) => {
        console.error('Error loading pending users:', error);
        this.errorMessage = 'Failed to load pending users';
        this.loading = false;
      }
    });

    // Load all users
    this.adminService.getAllUsers().subscribe({
      next: (users) => {
        this.allUsers = users;
        this.stats.totalUsers = users.length;
        this.stats.activeUsers = users.filter(u => u.is_active && u.is_approved).length;
        this.stats.inactiveUsers = users.filter(u => !u.is_active && u.is_approved).length;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading all users:', error);
        this.errorMessage = 'Failed to load users';
        this.loading = false;
      }
    });
  }

  approveUser(userId: string): void {
    if (confirm('Approve this user?')) {
      this.adminService.approveUser(userId).subscribe({
        next: (response) => {
          this.successMessage = 'User approved successfully!';
          this.clearMessageAfterDelay();
          this.loadDashboardData();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to approve user';
          this.clearMessageAfterDelay();
        }
      });
    }
  }

  rejectUser(userId: string): void {
    if (confirm('Are you sure you want to reject this user? This action cannot be undone.')) {
      this.adminService.rejectUser(userId).subscribe({
        next: (response) => {
          this.successMessage = 'User rejected and removed';
          this.clearMessageAfterDelay();
          this.loadDashboardData();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to reject user';
          this.clearMessageAfterDelay();
        }
      });
    }
  }

  deactivateUser(userId: string): void {
    if (confirm('Are you sure you want to deactivate this user?')) {
      this.adminService.deactivateUser(userId).subscribe({
        next: (response) => {
          this.successMessage = 'User deactivated successfully';
          this.clearMessageAfterDelay();
          this.loadDashboardData();
        },
        error: (error) => {
          this.errorMessage = error.error?.detail || 'Failed to deactivate user';
          this.clearMessageAfterDelay();
        }
      });
    }
  }

  clearMessageAfterDelay(): void {
    setTimeout(() => {
      this.successMessage = '';
      this.errorMessage = '';
    }, 3000);
  }

  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }

  setActivePage(page: string): void {
    this.activePage = page;
  }

  logout(): void {
    this.authService.logout();
  }

  getUserInitial(name: string): string {
    return name.charAt(0).toUpperCase();
  }

  formatDate(date: Date | string): string {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  }

  getStatusColor(user: User): string {
    if (user.is_approved && user.is_active) return 'approved';
    if (!user.is_approved) return 'pending';
    return 'inactive';
  }

  getStatusText(user: User): string {
    if (user.is_approved && user.is_active) return 'Active';
    if (!user.is_approved) return 'Pending';
    return 'Inactive';
  }
}