export interface UserRegister {
  surname: string;
  first_name: string;
  middle_name?: string;
  email: string;
  password: string;
  position: string;
  salary_grade: string;
  starting_date: Date;
  job_category: string;
  assigned_unit: string;
}

export interface AdminRegister {
  email: string;
  password: string;
  admin_key: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface User {
  id: string;
  surname: string;
  first_name: string;
  middle_name?: string;
  email: string;
  position: string;
  salary_grade: string;
  starting_date: Date;
  job_category: string;
  assigned_unit: string;
  role: string;
  is_approved: boolean;
  is_active: boolean;
  created_at: Date;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface PendingUser {
  id: string;
  full_name: string;
  email: string;
  position: string;
  salary_grade: string;
  job_category: string;
  assigned_unit: string;
  created_at: Date;
}