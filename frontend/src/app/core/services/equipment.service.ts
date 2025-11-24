// frontend/src/app/core/services/equipment.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.prod';
import { Equipment, EquipmentCreate, EquipmentAssign, Furniture, FurnitureCreate, FurnitureAssign } from '../models/equipment.model';

@Injectable({
  providedIn: 'root'
})
export class EquipmentService {
  private apiUrl = `${environment.apiUrl}/api/admin`;

  constructor(private http: HttpClient) {}

  // ============ EQUIPMENT ENDPOINTS ============

  // Get all equipment (Admin)
  getAllEquipment(): Observable<Equipment[]> {
    return this.http.get<Equipment[]>(`${this.apiUrl}/equipment/`);
  }

  // Get available equipment (Admin)
  getAvailableEquipment(): Observable<Equipment[]> {
    return this.http.get<Equipment[]>(`${this.apiUrl}/equipment/available`);
  }

  // Get single equipment (Admin)
  getEquipment(id: string): Observable<Equipment> {
    return this.http.get<Equipment>(`${this.apiUrl}/equipment/${id}`);
  }

  // Create equipment (Admin)
  createEquipment(data: EquipmentCreate): Observable<Equipment> {
    return this.http.post<Equipment>(`${this.apiUrl}/equipment/`, data);
  }

  // Update equipment (Admin)
  updateEquipment(id: string, data: Partial<EquipmentCreate>): Observable<Equipment> {
    return this.http.put<Equipment>(`${this.apiUrl}/equipment/${id}`, data);
  }

  // Delete equipment (Admin)
  deleteEquipment(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/equipment/${id}`);
  }

  // Assign equipment to user (Admin)
  assignEquipment(id: string, data: EquipmentAssign): Observable<Equipment> {
    return this.http.post<Equipment>(`${this.apiUrl}/equipment/${id}/assign`, data);
  }

  // Unassign equipment (Admin)
  unassignEquipment(id: string): Observable<Equipment> {
    return this.http.post<Equipment>(`${this.apiUrl}/equipment/${id}/unassign`, {});
  }

  // Get my equipment (User)
  getMyEquipment(): Observable<Equipment[]> {
    return this.http.get<Equipment[]>(`${this.apiUrl}/equipment/my-equipment`);
  }

  // Upload PAR document (Admin)
  uploadEquipmentPAR(id: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/equipment/${id}/upload-par`, formData);
  }

  // Download PAR document (User or Admin)
  downloadEquipmentPAR(id: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/equipment/${id}/download-par`, {
      responseType: 'blob'
    });
  }

  // Get equipment types
  getEquipmentTypes(): Observable<{ equipment_types: string[] }> {
    return this.http.get<{ equipment_types: string[] }>(`${this.apiUrl}/equipment/types/list`);
  }

  // ============ FURNITURE ENDPOINTS ============

  // Get all furniture (Admin)
  getAllFurniture(): Observable<Furniture[]> {
    return this.http.get<Furniture[]>(`${this.apiUrl}/furniture/`);
  }

  // Get available furniture (Admin)
  getAvailableFurniture(): Observable<Furniture[]> {
    return this.http.get<Furniture[]>(`${this.apiUrl}/furniture/available`);
  }

  // Get single furniture (Admin)
  getFurniture(id: string): Observable<Furniture> {
    return this.http.get<Furniture>(`${this.apiUrl}/furniture/${id}`);
  }

  // Create furniture (Admin)
  createFurniture(data: FurnitureCreate): Observable<Furniture> {
    return this.http.post<Furniture>(`${this.apiUrl}/furniture/`, data);
  }

  // Update furniture (Admin)
  updateFurniture(id: string, data: Partial<FurnitureCreate>): Observable<Furniture> {
    return this.http.put<Furniture>(`${this.apiUrl}/furniture/${id}`, data);
  }

  // Delete furniture (Admin)
  deleteFurniture(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/furniture/${id}`);
  }

  // Assign furniture to user (Admin)
  assignFurniture(id: string, data: FurnitureAssign): Observable<Furniture> {
    return this.http.post<Furniture>(`${this.apiUrl}/furniture/${id}/assign`, data);
  }

  // Unassign furniture (Admin)
  unassignFurniture(id: string): Observable<Furniture> {
    return this.http.post<Furniture>(`${this.apiUrl}/furniture/${id}/unassign`, {});
  }

  // Get my furniture (User)
  getMyFurniture(): Observable<Furniture[]> {
    return this.http.get<Furniture[]>(`${this.apiUrl}/furniture/my-furniture`);
  }

  // Upload PAR document (Admin)
  uploadFurniturePAR(id: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.apiUrl}/furniture/${id}/upload-par`, formData);
  }

  // Download PAR document (User or Admin)
  downloadFurniturePAR(id: string): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/furniture/${id}/download-par`, {
      responseType: 'blob'
    });
  }

  // Get furniture types
  getFurnitureTypes(): Observable<{ furniture_types: string[] }> {
    return this.http.get<{ furniture_types: string[] }>(`${this.apiUrl}/furniture/types/list`);
  }
}