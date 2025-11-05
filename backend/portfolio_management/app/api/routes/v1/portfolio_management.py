import os
import tempfile
import uuid
from typing import Any, Dict

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ....config.database import get_db_session
from ....utils.ExcelLoaderService import ReconciliationExcelService

router = APIRouter()

loading_tasks = {}


@router.post("/upload-excel", response_model=Dict[str, Any])
async def upload_excel(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session),
):
    """
    Upload an Excel file with reconciliation data.

    Expected Excel columns:
    - Fecha: Transaction date
    - Referencia_Pago: Payment reference
    - Valor: Payment amount
    - Canal_Pago: Payment channel (Oficina, Corresponsal, Transferencia, Sucursal)
    - Observaciones: Observations (optional)
    """
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)"
        )

    try:
        task_id = str(uuid.uuid4())

        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Initialize task tracking
        loading_tasks[task_id] = {
            "status": "processing",
            "filename": file.filename,
            "results": None,
            "error": None,
        }

        # Process in background
        background_tasks.add_task(
            process_excel_background, task_id, tmp_file_path, session
        )

        return {
            "task_id": task_id,
            "status": "processing",
            "message": f"Archivo {file.filename} está siendo procesado",
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error procesando archivo: {str(e)}"
        )


@router.post("/validate-reconciliation-excel", response_model=Dict[str, Any])
async def validate_reconciliation_excel(file: UploadFile = File(...)):
    """
    Validate an Excel file format without uploading to database.
    """
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)"
        )

    try:
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Validate format
        service = ReconciliationExcelService()
        validation_result = service.validate_excel_format(tmp_file_path)

        # Clean up
        os.unlink(tmp_file_path)

        return validation_result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error validando archivo: {str(e)}"
        )


async def process_excel_background(task_id: str, file_path: str, session: AsyncSession):
    """
    Background task to process reconciliation Excel file.
    """
    try:
        loading_tasks[task_id]["status"] = "processing"

        loader = ReconciliationExcelService()
        results = await loader.load_reconciliations_from_excel(file_path, session)
        # Llamar funcion para actualizar creditos.

        loading_tasks[task_id]["status"] = "completed"
        loading_tasks[task_id]["results"] = results

    except Exception as e:
        loading_tasks[task_id]["status"] = "error"
        loading_tasks[task_id]["error"] = str(e)

    finally:
        # Clean up temporary file
        try:
            os.unlink(file_path)
        except Exception:
            pass
