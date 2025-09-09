from fastapi import APIRouter
from .v1.admin import router as admin_router
from .v1.credit_management import router as credit_management_router
from .v1.repository_tests import router as repository_tests_router

router = APIRouter()

router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(credit_management_router, prefix="/credit-management", tags=["Excel Credit Management"])
router.include_router(repository_tests_router, prefix="/repository-tests", tags=["Repository Tests"])

@router.get("/")
async def read_root():
    return {"message": "Hello World"}