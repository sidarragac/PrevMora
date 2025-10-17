from fastapi import FastAPI

from .api.routes import router


def create_app() -> FastAPI:
    application = FastAPI(title="PrevMora-Stats", version="0.1.0")

    # Include routes under a versioned prefix
    application.include_router(router, prefix="/api/stats/v1", tags=["Stats"])

    return application


app = create_app()


