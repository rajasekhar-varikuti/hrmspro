from fastapi import APIRouter

router = APIRouter()

# Announcements endpoints will be implemented here
@router.get("/")
async def get_announcements():
    return {"message": "Announcements endpoints coming soon"}
