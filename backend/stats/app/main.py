from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router


def create_app() -> FastAPI:
    application = FastAPI(title="PrevMora-Stats", version="0.1.0")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes under a versioned prefix
    application.include_router(router, prefix="/api/stats/v1", tags=["Stats"])

    return application


app = create_app()
