// Core types
export interface User {
  id: string;
  username: string;
  email: string;
  employee_id: string;
  is_active: boolean;
  last_login?: string;
  created_at: string;
  updated_at: string;
}

export interface Employee {
  id: string;
  employee_id: string;
  organization_id: string;
  department_id?: string;
  position_id?: string;
  manager_id?: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  date_of_birth?: string;
  gender?: 'male' | 'female' | 'other' | 'prefer_not_to_say';
  marital_status?: 'single' | 'married' | 'divorced' | 'widowed';
  nationality?: string;
  address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  hire_date: string;
  employment_type: 'full_time' | 'part_time' | 'contract' | 'intern' | 'consultant';
  employment_status: 'active' | 'inactive' | 'terminated' | 'suspended';
  termination_date?: string;
  termination_reason?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  emergency_contact_relationship?: string;
  profile_picture_url?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

export interface Department {
  id: string;
  organization_id: string;
  name: string;
  description?: string;
  manager_id?: string;
  budget?: number;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  description?: string;
  address?: string;
  phone?: string;
  email?: string;
  website?: string;
  logo_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Attendance {
  id: string;
  employee_id: string;
  date: string;
  check_in_time?: string;
  check_out_time?: string;
  break_duration: number;
  total_hours?: number;
  status: 'present' | 'absent' | 'late' | 'half_day' | 'work_from_home';
  notes?: string;
  location_check_in?: string;
  location_check_out?: string;
  created_at: string;
  updated_at: string;
}

export interface LeaveRequest {
  id: string;
  employee_id: string;
  leave_type_id: string;
  start_date: string;
  end_date: string;
  total_days: number;
  reason: string;
  status: 'pending' | 'approved' | 'rejected' | 'cancelled';
  approved_by?: string;
  approved_at?: string;
  rejection_reason?: string;
  created_at: string;
  updated_at: string;
}

export interface JobApplication {
  id: string;
  job_posting_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  resume_url?: string;
  cover_letter?: string;
  status: 'applied' | 'screening' | 'interview_scheduled' | 'interviewed' | 'selected' | 'rejected' | 'offer_sent' | 'offer_accepted' | 'joined';
  applied_date: string;
  ai_screening_score?: number;
  ai_screening_notes?: string;
  ai_screening_date?: string;
  expected_salary?: number;
  available_start_date?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface PerformanceReview {
  id: string;
  employee_id: string;
  reviewer_id?: string;
  review_period_start: string;
  review_period_end: string;
  overall_rating: 'outstanding' | 'exceeds_expectations' | 'meets_expectations' | 'below_expectations' | 'unsatisfactory';
  technical_skills_rating?: 'outstanding' | 'exceeds_expectations' | 'meets_expectations' | 'below_expectations' | 'unsatisfactory';
  communication_rating?: 'outstanding' | 'exceeds_expectations' | 'meets_expectations' | 'below_expectations' | 'unsatisfactory';
  teamwork_rating?: 'outstanding' | 'exceeds_expectations' | 'meets_expectations' | 'below_expectations' | 'unsatisfactory';
  leadership_rating?: 'outstanding' | 'exceeds_expectations' | 'meets_expectations' | 'below_expectations' | 'unsatisfactory';
  achievements?: string;
  areas_for_improvement?: string;
  goals_next_period?: string;
  manager_feedback?: string;
  employee_comments?: string;
  is_completed: boolean;
  completed_date?: string;
  created_at: string;
  updated_at: string;
}

// API Response types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface ApiResponse<T> {
  data?: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

// Form types
export interface EmployeeFormData {
  employee_id: string;
  organization_id: string;
  department_id?: string;
  position_id?: string;
  manager_id?: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  marital_status?: string;
  nationality?: string;
  address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  hire_date: string;
  employment_type: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  emergency_contact_relationship?: string;
  bio?: string;
}

export interface DepartmentFormData {
  organization_id: string;
  name: string;
  description?: string;
  manager_id?: string;
  budget?: number;
}

// Auth Context types
export interface AuthContextType {
  user: User | null;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

// Navigation types
export interface NavigationItem {
  name: string;
  href: string;
  icon: any; // Using any instead of React.ComponentType for compatibility
  current?: boolean;
}
