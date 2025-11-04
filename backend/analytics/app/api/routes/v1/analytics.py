from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....schemas.Report import ReportFilters
from ....utils.ReportGeneratorService import ReportGeneratorService

router = APIRouter(prefix="/analytics/reports", tags=["Analytics Reports"])


class GenerateReportRequest(BaseModel):
    """Request para generar un reporte"""
    
    report_title: str = Field("Reporte de Cartera", description="Título del reporte")
    period_start: date = Field(..., description="Fecha de inicio del período")
    period_end: date = Field(..., description="Fecha de fin del período")
    filters: Optional[ReportFilters] = Field(None, description="Filtros opcionales")
    
    class Config:
        from_attributes = True


class ReportStatistics(BaseModel):
    """Estadísticas del reporte"""
    
    total_clients: int
    total_credits: int
    total_amount: int
    
    class Config:
        from_attributes = True


class GenerateReportResponse(BaseModel):
    """Respuesta de generación de reporte"""
    
    file_path: str
    file_size: int
    total_clients: int
    total_credits: int
    total_amount: int
    status: str
    
    class Config:
        from_attributes = True


@router.post("/generate", response_model=GenerateReportResponse)
async def generate_report(
    request: GenerateReportRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Generate a portfolio report based on filters
    
    - **report_title**: Custom title for the report (default: "Reporte de Cartera")
    - **period_start**: Start date for the report period (required, format: YYYY-MM-DD)
    - **period_end**: End date for the report period (required, format: YYYY-MM-DD)
    - **filters**: Optional filters object
    
    **Available Filters:**
    - credit_state (string): Filter by credit state (e.g., "Activo", "Pendiente", "Vencido", "Cancelado")
    - client_zone (string): Filter by client zone (e.g., "Norte", "Sur", "Centro")
    - manager_id (integer): Filter by manager ID
    - debt_age_min (integer): Minimum debt age in days
    - debt_age_max (integer): Maximum debt age in days
    
    **Returns:**
    - file_path: Path to generated PDF
    - file_size: Size of PDF in bytes
    - total_clients: Number of unique clients
    - total_credits: Number of credits
    - total_amount: Total disbursed amount
    - status: Generation status ("completed" or "failed")
    """
    try:
        # Initialize service
        report_service = ReportGeneratorService()
        
        # Generate report
        result = await report_service.generate_report(
            session=session,
            report_name=request.report_title,
            filters=request.filters,
            period_start=request.period_start,
            period_end=request.period_end,
        )
        
        # Check if generation failed
        if result.get("status") == "failed":
            raise HTTPException(
                status_code=500,
                detail=result.get("error_message", "Unknown error generating report")
            )
        
        return GenerateReportResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )
