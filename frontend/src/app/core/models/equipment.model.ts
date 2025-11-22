// frontend/src/app/core/models/equipment.model.ts

export interface Equipment {
  id?: string;
  property_number: string;
  gsd_code?: string;
  item_number?: string;
  equipment_type: string;
  brand: string;
  model: string;
  serial_number?: string;
  specifications?: string;
  acquisition_date?: string;
  acquisition_cost?: number;
  assigned_to_user_id?: string;
  assigned_to_name?: string;
  assigned_date?: string;
  assignment_type?: 'PAR' | 'Job Order';  // NEW
  previous_recipient?: string;
  condition: string;
  status: string;
  remarks?: string;
  par_file_path?: string;
  par_number?: string;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface EquipmentCreate {
  property_number: string;
  gsd_code: string;
  item_number: string;
  equipment_type: string;
  brand: string;
  model: string;
  serial_number: string;
  specifications?: string;
  acquisition_date: Date | string;
  acquisition_cost: number;
  condition?: string;
  status?: string;
  remarks?: string;
}

export interface EquipmentAssign {
  assigned_to_user_id: string;
  assigned_to_name: string;
  assigned_date: Date | string;
  previous_recipient?: string;
  par_number?: string;
}

export interface Furniture {
  id?: string;
  property_number: string;
  gsd_code?: string;
  item_number?: string;
  furniture_type: string;
  description: string;
  brand?: string;
  material?: string;
  color?: string;
  dimensions?: string;
  acquisition_date?: string;
  acquisition_cost?: number;
  assigned_to_user_id?: string;
  assigned_to_name?: string;
  assigned_date?: string;
  assignment_type?: 'PAR' | 'Job Order';  // NEW
  location?: string;
  condition: string;
  status: string;
  remarks?: string;
  par_file_path?: string;
  par_number?: string;
  created_by?: string;
  created_at?: string;
  updated_at?: string;
}

export interface FurnitureCreate {
  property_number: string;
  gsd_code: string;
  item_number: string;
  furniture_type: string;
  description: string;
  brand?: string;
  material?: string;
  color?: string;
  dimensions?: string;
  acquisition_date: Date | string;
  acquisition_cost: number;
  condition?: string;
  status?: string;
  remarks?: string;
}

export interface FurnitureAssign {
  assigned_to_user_id: string;
  assigned_to_name: string;
  assigned_date: Date | string;
  location?: string;
  par_number?: string;
}

export interface AssignEquipmentData {
  assigned_to_user_id: string;
  assigned_to_name: string;
  assigned_date: string;
  assignment_type: 'PAR' | 'Job Order';
  previous_recipient?: string;
  par_number?: string;
}

export interface AssignFurnitureData {
  assigned_to_user_id: string;
  assigned_to_name: string;
  assigned_date: string;
  assignment_type: 'PAR' | 'Job Order';
  location?: string;
  par_number?: string;
}

// Dropdown Options
export const EQUIPMENT_TYPES = [
  'Desktop Computer',
  'Laptop',
  'Monitor',
  'Keyboard',
  'Mouse',
  'Printer',
  'Scanner',
  'UPS',
  'External Hard Drive',
  'Network Device',
  'Projector',
  'Webcam',
  'Headset',
  'Other IT Equipment'
];

export const FURNITURE_TYPES = [
  'Office Chair',
  'Executive Chair',
  'Office Desk',
  'Conference Table',
  'Filing Cabinet',
  'Bookshelf',
  'Storage Cabinet',
  'Drawer',
  'Workstation',
  'Partition',
  'Other Furniture'
];

export const CONDITIONS = [
  'New',
  'Good',
  'Fair',
  'For Repair',
  'For Disposal'
];

export const STATUSES = [
  'Available',
  'Assigned',
  'Under Repair',
  'Disposed'
];

