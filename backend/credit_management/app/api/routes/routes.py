from fastapi import APIRouter

router = APIRouter()

#router.include_router(excel_router, prefix="/excel", tags=["excel"])

@router.get("/")
async def read_root():
    return {"message": "Hello World"}