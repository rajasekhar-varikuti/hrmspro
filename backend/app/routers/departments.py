from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.database import get_db
from app.models import Department, Organization, Employee
from app.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse, MessageResponse
from app.routers.auth import get_current_user
from app.models import User

router = APIRouter()

@router.get("/", response_model=List[DepartmentResponse])
async def get_departments(
    organization_id: UUID = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of departments."""
    query = db.query(Department)
    if organization_id:
        query = query.filter(Department.organization_id == organization_id)
    departments = query.all()
    return departments

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get department by ID."""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    return department

@router.post("/", response_model=DepartmentResponse)
async def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new department."""
    # Verify organization exists
    organization = db.query(Organization).filter(
        Organization.id == department_data.organization_id
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Verify manager exists if provided
    if department_data.manager_id:
        manager = db.query(Employee).filter(
            Employee.id == department_data.manager_id
        ).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager not found"
            )
    
    db_department = Department(**department_data.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    
    return db_department

@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: UUID,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update department information."""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # Verify manager exists if provided
    if department_data.manager_id:
        manager = db.query(Employee).filter(
            Employee.id == department_data.manager_id
        ).first()
        if not manager:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Manager not found"
            )
    
    update_data = department_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(department, field, value)
    
    db.commit()
    db.refresh(department)
    
    return department

@router.delete("/{department_id}", response_model=MessageResponse)
async def delete_department(
    department_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete department."""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    # Check if department has employees
    employees_count = db.query(Employee).filter(Employee.department_id == department_id).count()
    if employees_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete department with {employees_count} employees. Please reassign employees first."
        )
    
    db.delete(department)
    db.commit()
    
    return {"message": "Department deleted successfully", "success": True}
