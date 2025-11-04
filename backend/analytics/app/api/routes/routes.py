from fastapi import APIRouter

from .v1 import v1_router
from .v1.admin import router as admin_router
from .v1.portfolio_management import router as portfolio_management_router

router = APIRouter()

router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(
    portfolio_management_router,
    prefix="/analytics",
    tags=["Analytics"],
)
router.include_router(v1_router, prefix="")