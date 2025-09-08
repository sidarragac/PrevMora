class HealthController:
    def get_status(self) -> dict[str, str]:
        return {"status": "ok"}

