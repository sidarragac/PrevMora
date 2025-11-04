import os
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
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


@router.post("/generate")
async def generate_report(
    request: GenerateReportRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Generate and download a portfolio report as PDF
    
    - **report_title**: Custom title for the report (default: "Reporte de Cartera")
    - **period_start**: Start date for the report period (required, format: YYYY-MM-DD)
    - **period_end**: End date for the report period (required, format: YYYY-MM-DD)
    - **filters**: Optional filters object
    
    **Available Filters:**
    - credit_state (string): Filter by credit state (e.g., "Vigente", "Pendiente", "Cancelado")
    - client_zone (string): Filter by client zone (e.g., "Rural", "Urbano")
    - manager_id (integer): Filter by manager ID
    - debt_age_min (integer): Minimum debt age in days (based on disbursement date)
    - debt_age_max (integer): Maximum debt age in days (based on disbursement date)
    
    **Returns:** PDF file download
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
        
        # Get file path
        file_path = result["file_path"]
        
        # Verify file exists
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=500,
                detail="Report file was generated but not found"
            )
        
        # Generate clean filename for download
        filename = os.path.basename(file_path)
        
        # Return file as download response
        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=filename,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )
