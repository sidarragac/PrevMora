from fastapi import APIRouter
from .v1.admin import router as admin_router

router = APIRouter()

router.include_router(admin_router, prefix="/admin", tags=["Admin"])

@router.get("/")
async def read_root():
    return {"message": "Hello World"}