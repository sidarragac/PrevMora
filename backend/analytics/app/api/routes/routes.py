from fastapi import APIRouter

from .v1 import v1_router
from .v1.admin import router as admin_router
from .v1.analytics import router as analytics_router

router = APIRouter()

router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)
router.include_router(v1_router, prefix="")