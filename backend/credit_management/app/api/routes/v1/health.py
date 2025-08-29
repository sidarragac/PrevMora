from fastapi import APIRouter, Depends, Request
from app.controllers import HealthController


router = APIRouter(tags=["health"])


def get_health_controller(request: Request) -> HealthController:
    return request.app.state.health_controller


@router.get("/health", summary="Health check")
def health(controller: HealthController = Depends(get_health_controller)) -> dict[str, str]:
    return controller.get_status()

