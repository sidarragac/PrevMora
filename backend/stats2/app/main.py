from fastapi import FastAPI

from .api.routes.money_recovery import router as money_recovery
from .api.routes.num_clients import router as num_clients
from .api.routes.stats_by_month_mora import router as stats_by_month_mora
from .models import *  # noqa: F401,F403 - ensure all mappers are imported


def create_app() -> FastAPI:
    application = FastAPI(title="PrevMora-Stats2", version="0.1.0")
    application.include_router(stats_by_month_mora, prefix="/stats2", tags=["Stats2"])
    application.include_router(money_recovery, prefix="/stats2", tags=["Stats2"])
    application.include_router(num_clients, prefix="/stats2", tags=["Stats2"])
    return application


app = create_app()
