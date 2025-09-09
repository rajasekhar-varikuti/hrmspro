from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import date
from app.database import get_db
from app.models import Attendance, Employee
from app.schemas import AttendanceCreate, AttendanceUpdate, AttendanceResponse, MessageResponse
from app.routers.auth import get_current_user
from app.models import User

router = APIRouter()

@router.get("/", response_model=List[AttendanceResponse])
async def get_attendance_records(
    employee_id: UUID = None,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attendance records with filtering."""
    query = db.query(Attendance)
    
    if employee_id:
        query = query.filter(Attendance.employee_id == employee_id)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)
    
    records = query.order_by(Attendance.date.desc()).all()
    return records

@router.post("/check-in", response_model=AttendanceResponse)
async def check_in(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Employee check-in."""
    # Check if already checked in today
    existing_record = db.query(Attendance).filter(
        Attendance.employee_id == attendance_data.employee_id,
        Attendance.date == attendance_data.date
    ).first()
    
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in for today"
        )
    
    db_attendance = Attendance(**attendance_data.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    
    return db_attendance

@router.put("/{attendance_id}/check-out", response_model=AttendanceResponse)
async def check_out(
    attendance_id: UUID,
    attendance_data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Employee check-out."""
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    # Calculate total hours
    if attendance.check_in_time and attendance_data.check_out_time:
        time_diff = attendance_data.check_out_time - attendance.check_in_time
        total_minutes = time_diff.total_seconds() / 60
        break_minutes = attendance_data.break_duration or 0
        total_hours = (total_minutes - break_minutes) / 60
        attendance.total_hours = round(total_hours, 2)
    
    update_data = attendance_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attendance, field, value)
    
    db.commit()
    db.refresh(attendance)
    
    return attendance
