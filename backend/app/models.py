from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, Decimal, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base

# Enum definitions
class EmploymentStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    terminated = "terminated"
    suspended = "suspended"

class EmploymentType(enum.Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    intern = "intern"
    consultant = "consultant"

class Gender(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class MaritalStatus(enum.Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    widowed = "widowed"

class LeaveStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"

class AttendanceStatus(enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    half_day = "half_day"
    work_from_home = "work_from_home"

class RecruitmentStatus(enum.Enum):
    applied = "applied"
    screening = "screening"
    interview_scheduled = "interview_scheduled"
    interviewed = "interviewed"
    selected = "selected"
    rejected = "rejected"
    offer_sent = "offer_sent"
    offer_accepted = "offer_accepted"
    joined = "joined"

class InterviewType(enum.Enum):
    phone = "phone"
    video = "video"
    in_person = "in_person"
    technical = "technical"
    hr = "hr"
    final = "final"

class PerformanceRating(enum.Enum):
    outstanding = "outstanding"
    exceeds_expectations = "exceeds_expectations"
    meets_expectations = "meets_expectations"
    below_expectations = "below_expectations"
    unsatisfactory = "unsatisfactory"

class PriorityLevel(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

# Models
class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    logo_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    departments = relationship("Department", back_populates="organization")
    employees = relationship("Employee", back_populates="organization")

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    manager_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"))
    budget = Column(Decimal(15, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="departments")
    employees = relationship("Employee", back_populates="department")
    manager = relationship("Employee", foreign_keys=[manager_id])

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    min_salary = Column(Decimal(12, 2))
    max_salary = Column(Decimal(12, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship("Department")
    employees = relationship("Employee", back_populates="position")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(String(50), unique=True, nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id", ondelete="SET NULL"))
    manager_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"))
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(SQLEnum(Gender))
    marital_status = Column(SQLEnum(MaritalStatus))
    nationality = Column(String(100))
    
    # Address Information
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    
    # Employment Information
    hire_date = Column(Date, nullable=False)
    employment_type = Column(SQLEnum(EmploymentType), nullable=False)
    employment_status = Column(SQLEnum(EmploymentStatus), default=EmploymentStatus.active)
    termination_date = Column(Date)
    termination_reason = Column(Text)
    
    # Emergency Contact
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relationship = Column(String(100))
    
    # Profile
    profile_picture_url = Column(String(500))
    bio = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="employees")
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    manager = relationship("Employee", remote_side=[id])
    user = relationship("User", back_populates="employee", uselist=False)

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON stored as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    check_in_time = Column(DateTime(timezone=True))
    check_out_time = Column(DateTime(timezone=True))
    break_duration = Column(Integer, default=0)  # in minutes
    total_hours = Column(Decimal(4, 2))
    status = Column(SQLEnum(AttendanceStatus), nullable=False)
    notes = Column(Text)
    location_check_in = Column(String(255))
    location_check_out = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    employee = relationship("Employee")

class LeaveType(Base):
    __tablename__ = "leave_types"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    max_days_per_year = Column(Integer)
    is_paid = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=True)
    advance_notice_days = Column(Integer, default=7)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"))
    leave_type_id = Column(UUID(as_uuid=True), ForeignKey("leave_types.id", ondelete="RESTRICT"))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(SQLEnum(LeaveStatus), default=LeaveStatus.pending)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"))
    approved_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    leave_type = relationship("LeaveType")
    approver = relationship("Employee", foreign_keys=[approved_by])

class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    location = Column(String(255))
    employment_type = Column(SQLEnum(EmploymentType), nullable=False)
    salary_min = Column(Decimal(12, 2))
    salary_max = Column(Decimal(12, 2))
    is_active = Column(Boolean, default=True)
    posted_date = Column(Date, server_default=func.current_date())
    closing_date = Column(Date)
    posted_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization")
    position = relationship("Position")

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id", ondelete="CASCADE"))
    
    # Applicant Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    resume_url = Column(String(500))
    cover_letter = Column(Text)
    
    # Application Status
    status = Column(SQLEnum(RecruitmentStatus), default=RecruitmentStatus.applied)
    applied_date = Column(Date, server_default=func.current_date())
    
    # AI Screening Results
    ai_screening_score = Column(Decimal(5, 2))
    ai_screening_notes = Column(Text)
    ai_screening_date = Column(DateTime(timezone=True))
    
    # Additional Info
    expected_salary = Column(Decimal(12, 2))
    available_start_date = Column(Date)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    job_posting = relationship("JobPosting")

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"))
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="SET NULL"))
    review_period_start = Column(Date, nullable=False)
    review_period_end = Column(Date, nullable=False)
    
    # Ratings
    overall_rating = Column(SQLEnum(PerformanceRating), nullable=False)
    technical_skills_rating = Column(SQLEnum(PerformanceRating))
    communication_rating = Column(SQLEnum(PerformanceRating))
    teamwork_rating = Column(SQLEnum(PerformanceRating))
    leadership_rating = Column(SQLEnum(PerformanceRating))
    
    # Goals and Feedback
    achievements = Column(Text)
    areas_for_improvement = Column(Text)
    goals_next_period = Column(Text)
    manager_feedback = Column(Text)
    employee_comments = Column(Text)
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_date = Column(Date)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", foreign_keys=[employee_id])
    reviewer = relationship("Employee", foreign_keys=[reviewer_id])

class Announcement(Base):
    __tablename__ = "announcements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(SQLEnum(PriorityLevel), default=PriorityLevel.medium)
    target_audience = Column(String(100))
    target_department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="SET NULL"))
    is_active = Column(Boolean, default=True)
    publish_date = Column(Date, server_default=func.current_date())
    expiry_date = Column(Date)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization")
    target_department = relationship("Department")
    creator = relationship("User")
