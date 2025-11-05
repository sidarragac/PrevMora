from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.routes import router as principal_router
from .config.settings import settings


def create_app() -> FastAPI:
    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(principal_router, prefix=f"/api/{settings.APP_NAME}/v1")

    return application


app = create_app()
