from fastapi import APIRouter

router = APIRouter()

# Payroll management endpoints will be implemented here
@router.get("/")
async def get_payroll_records():
    return {"message": "Payroll endpoints coming soon"}
