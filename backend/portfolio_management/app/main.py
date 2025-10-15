from fastapi import APIRouter, FastAPI

from .api.routes.routes import router as principal_router
from .config.settings import settings


def create_app() -> FastAPI:
    application = FastAPI(**settings.fastapi_kwargs)

    application.include_router(principal_router, prefix=f"/api/{settings.APP_NAME}/v1")

    return application


app = create_app()
