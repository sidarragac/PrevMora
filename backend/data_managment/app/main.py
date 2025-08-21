import fastapi
import uvicorn
import logging
from fastapi.middleware.cors import CORSMiddleware
from api.main import router as api_endpoint_router

from config.settings import settings

def setup_logging():
    logging.basicConfig(
        level=settings.LOGGING_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def execute_server_event_handler():
    """Se ejecuta al iniciar la aplicación."""
    print("Iniciando aplicación...")


async def terminate_server_event_handler():
    """Se ejecuta al cerrar la aplicación."""
    print("Aplicación cerrada correctamente")

def create_app() -> fastapi.FastAPI:
    setup_logging()
    app = fastapi.FastAPI(**settings.fastapi_kwargs)

    app.add_middleware(
        CORSMiddleware,
        **settings.cors_config
    )

    app.add_event_handler("startup", execute_server_event_handler)
    app.add_event_handler("shutdown", terminate_server_event_handler)

    app.include_router(router=api_endpoint_router, prefix=f"{settings.API_PREFIX}/{settings.APP_NAME}/{settings.APP_VERSION}")

    return app

app: fastapi.FastAPI = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )