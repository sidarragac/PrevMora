from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ReportFilters(BaseModel):
    """Filtros para generar reportes de cartera"""
    
    # Filtros opcionales
    credit_state: Optional[str] = Field(None, description="Estado del crédito")
    client_zone: Optional[str] = Field(None, description="Zona del cliente")
    manager_id: Optional[int] = Field(None, description="ID del gestor responsable")
    debt_age_min: Optional[int] = Field(None, ge=0, description="Mínimo de días de antigüedad de deuda")
    debt_age_max: Optional[int] = Field(None, ge=0, description="Máximo de días de antigüedad de deuda")

    class Config:
        from_attributes = True
