// frontend/src/app/core/services/admin.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User, PendingUser } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://localhost:8000/api/admin';

  constructor(private http: HttpClient) {}

  // Get all pending users (not approved)
  getPendingUsers(): Observable<PendingUser[]> {
    return this.http.get<PendingUser[]>(`${this.apiUrl}/pending-users`);
  }

  // Get all users (approved and pending)
  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}/all-users`);
  }

  // Approve a pending user
  approveUser(userId: string): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/approve-user/${userId}`, {});
  }

  // Reject a pending user (delete)
  rejectUser(userId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/reject-user/${userId}`);
  }

  // Deactivate an active user
  deactivateUser(userId: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/deactivate-user/${userId}`, {});
  }

  // Get dashboard statistics
  getDashboardStats(): Observable<any> {
    // This endpoint would return stats like total users, pending approvals, etc.
    // For now, we'll calculate it on frontend
    return this.http.get<any>(`${this.apiUrl}/stats`);
  }
}