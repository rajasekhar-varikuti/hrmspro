import axios, { AxiosResponse } from 'axios';
import { LoginRequest, LoginResponse, User, Employee, Department } from '../types';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response: AxiosResponse<LoginResponse> = await api.post('/auth/login', credentials);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response: AxiosResponse<User> = await api.get('/auth/me');
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
    localStorage.removeItem('access_token');
  },
};

// Employees API
export const employeesAPI = {
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    department_id?: string;
    employment_status?: string;
    search?: string;
  }): Promise<Employee[]> => {
    const response: AxiosResponse<Employee[]> = await api.get('/employees', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Employee> => {
    const response: AxiosResponse<Employee> = await api.get(`/employees/${id}`);
    return response.data;
  },

  create: async (data: Partial<Employee>): Promise<Employee> => {
    const response: AxiosResponse<Employee> = await api.post('/employees', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Employee>): Promise<Employee> => {
    const response: AxiosResponse<Employee> = await api.put(`/employees/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/employees/${id}`);
  },

  getByDepartment: async (departmentId: string): Promise<Employee[]> => {
    const response: AxiosResponse<Employee[]> = await api.get(`/employees/department/${departmentId}`);
    return response.data;
  },

  getByManager: async (managerId: string): Promise<Employee[]> => {
    const response: AxiosResponse<Employee[]> = await api.get(`/employees/search/by-manager/${managerId}`);
    return response.data;
  },
};

// Departments API
export const departmentsAPI = {
  getAll: async (organizationId?: string): Promise<Department[]> => {
    const params = organizationId ? { organization_id: organizationId } : {};
    const response: AxiosResponse<Department[]> = await api.get('/departments', { params });
    return response.data;
  },

  getById: async (id: string): Promise<Department> => {
    const response: AxiosResponse<Department> = await api.get(`/departments/${id}`);
    return response.data;
  },

  create: async (data: Partial<Department>): Promise<Department> => {
    const response: AxiosResponse<Department> = await api.post('/departments', data);
    return response.data;
  },

  update: async (id: string, data: Partial<Department>): Promise<Department> => {
    const response: AxiosResponse<Department> = await api.put(`/departments/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/departments/${id}`);
  },
};

// Attendance API (placeholder)
export const attendanceAPI = {
  getRecords: async () => {
    const response = await api.get('/attendance');
    return response.data;
  },

  checkIn: async (data: any) => {
    const response = await api.post('/attendance/check-in', data);
    return response.data;
  },

  checkOut: async (id: string, data: any) => {
    const response = await api.put(`/attendance/${id}/check-out`, data);
    return response.data;
  },
};

// Leave API (placeholder)
export const leaveAPI = {
  getRequests: async () => {
    const response = await api.get('/leave');
    return response.data;
  },
};

// Recruitment API (placeholder)
export const recruitmentAPI = {
  getApplications: async () => {
    const response = await api.get('/recruitment');
    return response.data;
  },
};

// Performance API (placeholder)
export const performanceAPI = {
  getReviews: async () => {
    const response = await api.get('/performance');
    return response.data;
  },
};

export default api;
