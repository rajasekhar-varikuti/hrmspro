from fastapi import APIRouter

router = APIRouter()

# Recruitment endpoints will be implemented here
@router.get("/")
async def get_job_applications():
    return {"message": "Recruitment endpoints coming soon"}
