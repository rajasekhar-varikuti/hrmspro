from fastapi import APIRouter

router = APIRouter()

# Performance management endpoints will be implemented here
@router.get("/")
async def get_performance_reviews():
    return {"message": "Performance management endpoints coming soon"}
