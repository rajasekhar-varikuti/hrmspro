from fastapi import APIRouter

router = APIRouter()

# Training management endpoints will be implemented here
@router.get("/")
async def get_training_programs():
    return {"message": "Training management endpoints coming soon"}
