from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import Employee, Department, Position, Organization
from app.schemas import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, 
    MessageResponse, PaginatedResponse
)
from app.routers.auth import get_current_user
from app.models import User

router = APIRouter()

@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department_id: Optional[UUID] = None,
    employment_status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of employees with filtering and pagination."""
    query = db.query(Employee)
    
    # Apply filters
    if department_id:
        query = query.filter(Employee.department_id == department_id)
    
    if employment_status:
        query = query.filter(Employee.employment_status == employment_status)
    
    if search:
        search_filter = or_(
            Employee.first_name.ilike(f"%{search}%"),
            Employee.last_name.ilike(f"%{search}%"),
            Employee.email.ilike(f"%{search}%"),
            Employee.employee_id.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get employee by ID."""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return employee

@router.post("/", response_model=EmployeeResponse)
async def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new employee."""
    # Check if employee ID already exists
    existing_employee = db.query(Employee).filter(
        Employee.employee_id == employee_data.employee_id
    ).first()
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    # Check if email already exists
    existing_email = db.query(Employee).filter(
        Employee.email == employee_data.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Verify organization exists
    organization = db.query(Organization).filter(
        Organization.id == employee_data.organization_id
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Verify department exists if provided
    if employee_data.department_id:
        department = db.query(Department).filter(
            Department.id == employee_data.department_id
        ).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
    
    # Verify position exists if provided
    if employee_data.position_id:
        position = db.query(Position).filter(
            Position.id == employee_data.position_id
        ).first()
        if not position:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Position not found"
            )
    
    # Create employee
    db_employee = Employee(**employee_data.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: UUID,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update employee information."""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Check if email is being updated and already exists
    if employee_data.email and employee_data.email != employee.email:
        existing_email = db.query(Employee).filter(
            and_(Employee.email == employee_data.email, Employee.id != employee_id)
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    # Update employee fields
    update_data = employee_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    db.commit()
    db.refresh(employee)
    
    return employee

@router.delete("/{employee_id}", response_model=MessageResponse)
async def delete_employee(
    employee_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete employee (soft delete by setting employment_status to terminated)."""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    # Soft delete by updating employment status
    from app.models import EmploymentStatus
    from datetime import date
    employee.employment_status = EmploymentStatus.terminated
    employee.termination_date = date.today()
    
    db.commit()
    
    return {"message": "Employee terminated successfully", "success": True}

@router.get("/search/by-manager/{manager_id}", response_model=List[EmployeeResponse])
async def get_employees_by_manager(
    manager_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all employees under a specific manager."""
    employees = db.query(Employee).filter(Employee.manager_id == manager_id).all()
    return employees

@router.get("/department/{department_id}", response_model=List[EmployeeResponse])
async def get_employees_by_department(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all employees in a specific department."""
    employees = db.query(Employee).filter(Employee.department_id == department_id).all()
    return employees
