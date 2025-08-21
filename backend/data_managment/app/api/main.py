from fastapi import APIRouter

router = APIRouter()

#router.include_router(books.router, prefix="/books", tags=["books"])

@router.get("/")
async def read_root():
    return {"message": "Hello World"}