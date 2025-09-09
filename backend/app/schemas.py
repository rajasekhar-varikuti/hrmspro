from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from app.models import (
    EmploymentStatus, EmploymentType, Gender, MaritalStatus,
    LeaveStatus, AttendanceStatus, RecruitmentStatus, PerformanceRating
)

# Base schemas
class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

# Organization schemas
class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None

class OrganizationResponse(OrganizationBase, TimestampMixin):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

# Department schemas
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    budget: Optional[float] = None

class DepartmentCreate(DepartmentBase):
    organization_id: UUID
    manager_id: Optional[UUID] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[UUID] = None
    budget: Optional[float] = None

class DepartmentResponse(DepartmentBase, TimestampMixin):
    id: UUID
    organization_id: UUID
    manager_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)

# Employee schemas
class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    employee_id: str = Field(..., min_length=1, max_length=50)
    organization_id: UUID
    department_id: Optional[UUID] = None
    position_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    hire_date: date
    employment_type: EmploymentType

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    department_id: Optional[UUID] = None
    position_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    employment_type: Optional[EmploymentType] = None
    employment_status: Optional[EmploymentStatus] = None
    termination_date: Optional[date] = None
    termination_reason: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None

class EmployeeResponse(EmployeeBase, TimestampMixin):
    id: UUID
    employee_id: str
    organization_id: UUID
    department_id: Optional[UUID] = None
    position_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    hire_date: date
    employment_type: EmploymentType
    employment_status: EmploymentStatus
    termination_date: Optional[date] = None
    termination_reason: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    employee_id: UUID

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase, TimestampMixin):
    id: UUID
    employee_id: UUID
    last_login: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Attendance schemas
class AttendanceBase(BaseModel):
    date: date
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    break_duration: int = 0
    status: AttendanceStatus
    notes: Optional[str] = None
    location_check_in: Optional[str] = None
    location_check_out: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    employee_id: UUID

class AttendanceUpdate(BaseModel):
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    break_duration: Optional[int] = None
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None
    location_check_in: Optional[str] = None
    location_check_out: Optional[str] = None

class AttendanceResponse(AttendanceBase, TimestampMixin):
    id: UUID
    employee_id: UUID
    total_hours: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

# Leave schemas
class LeaveTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    max_days_per_year: Optional[int] = None
    is_paid: bool = True
    requires_approval: bool = True
    advance_notice_days: int = 7
    is_active: bool = True

class LeaveTypeCreate(LeaveTypeBase):
    organization_id: UUID

class LeaveTypeResponse(LeaveTypeBase, TimestampMixin):
    id: UUID
    organization_id: UUID
    model_config = ConfigDict(from_attributes=True)

class LeaveRequestBase(BaseModel):
    start_date: date
    end_date: date
    total_days: int
    reason: str = Field(..., min_length=1)

class LeaveRequestCreate(LeaveRequestBase):
    employee_id: UUID
    leave_type_id: UUID

class LeaveRequestUpdate(BaseModel):
    status: Optional[LeaveStatus] = None
    rejection_reason: Optional[str] = None

class LeaveRequestResponse(LeaveRequestBase, TimestampMixin):
    id: UUID
    employee_id: UUID
    leave_type_id: UUID
    status: LeaveStatus
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# Job Application schemas
class JobApplicationBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    resume_url: Optional[str] = None
    cover_letter: Optional[str] = None
    expected_salary: Optional[float] = None
    available_start_date: Optional[date] = None
    notes: Optional[str] = None

class JobApplicationCreate(JobApplicationBase):
    job_posting_id: UUID

class JobApplicationUpdate(BaseModel):
    status: Optional[RecruitmentStatus] = None
    ai_screening_score: Optional[float] = None
    ai_screening_notes: Optional[str] = None
    notes: Optional[str] = None

class JobApplicationResponse(JobApplicationBase, TimestampMixin):
    id: UUID
    job_posting_id: UUID
    status: RecruitmentStatus
    applied_date: date
    ai_screening_score: Optional[float] = None
    ai_screening_notes: Optional[str] = None
    ai_screening_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

# Performance Review schemas
class PerformanceReviewBase(BaseModel):
    review_period_start: date
    review_period_end: date
    overall_rating: PerformanceRating
    technical_skills_rating: Optional[PerformanceRating] = None
    communication_rating: Optional[PerformanceRating] = None
    teamwork_rating: Optional[PerformanceRating] = None
    leadership_rating: Optional[PerformanceRating] = None
    achievements: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    goals_next_period: Optional[str] = None
    manager_feedback: Optional[str] = None
    employee_comments: Optional[str] = None

class PerformanceReviewCreate(PerformanceReviewBase):
    employee_id: UUID
    reviewer_id: UUID

class PerformanceReviewUpdate(BaseModel):
    overall_rating: Optional[PerformanceRating] = None
    technical_skills_rating: Optional[PerformanceRating] = None
    communication_rating: Optional[PerformanceRating] = None
    teamwork_rating: Optional[PerformanceRating] = None
    leadership_rating: Optional[PerformanceRating] = None
    achievements: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    goals_next_period: Optional[str] = None
    manager_feedback: Optional[str] = None
    employee_comments: Optional[str] = None
    is_completed: Optional[bool] = None
    completed_date: Optional[date] = None

class PerformanceReviewResponse(PerformanceReviewBase, TimestampMixin):
    id: UUID
    employee_id: UUID
    reviewer_id: Optional[UUID] = None
    is_completed: bool
    completed_date: Optional[date] = None
    model_config = ConfigDict(from_attributes=True)

# Generic response schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    per_page: int
    pages: int
