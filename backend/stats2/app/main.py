from fastapi import FastAPI
from app.api.routes import router

def create_app() -> FastAPI:
    application = FastAPI(title="PrevMora-Stats2", version="0.1.0")
    application.include_router(router, prefix="/stats2", tags=["Stats2"])
    return application

app = create_app()