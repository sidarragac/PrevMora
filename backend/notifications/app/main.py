from fastapi import FastAPI

from .api.routes import router
from .config.settings import settings


def create_app() -> FastAPI:
    application = FastAPI(**settings.fastapi_kwargs)

    # Include the main router
    application.include_router(
        router, prefix="/api/notifications/v1", tags=["Notifications"]
    )

    return application


app = create_app()
