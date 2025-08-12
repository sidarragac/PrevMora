from fastapi import FastAPI

from app.config.settings import settings
from app.api.routes.v1 import router as v1_router
from app.controllers import ItemsController


def create_app() -> FastAPI:
    application = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

    application.include_router(v1_router, prefix="/api/v1")

    # Wire shared dependencies
    application.state.items_controller = ItemsController()

    return application


app = create_app()

