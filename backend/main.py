from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import uvicorn

from app.database import engine, get_db
from app.models import Base
from app.routers import (
    auth, 
    employees, 
    departments, 
    attendance, 
    payroll, 
    leave, 
    recruitment, 
    performance,
    training,
    announcements
)
from app.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 HRMS Backend starting up...")
    yield
    # Shutdown
    print("👋 HRMS Backend shutting down...")

app = FastAPI(
    title="HRMS API",
    description="Human Resource Management System API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(departments.router, prefix="/api/departments", tags=["Departments"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["Attendance"])
app.include_router(payroll.router, prefix="/api/payroll", tags=["Payroll"])
app.include_router(leave.router, prefix="/api/leave", tags=["Leave Management"])
app.include_router(recruitment.router, prefix="/api/recruitment", tags=["Recruitment"])
app.include_router(performance.router, prefix="/api/performance", tags=["Performance"])
app.include_router(training.router, prefix="/api/training", tags=["Training"])
app.include_router(announcements.router, prefix="/api/announcements", tags=["Announcements"])

@app.get("/")
async def root():
    return {
        "message": "HRMS API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Simple database connectivity check
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
