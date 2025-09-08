from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, BackgroundTasks, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import tempfile
import os
from typing import Dict, Any
import uuid

from ....utils.ExcelLoaderService import ExcelLoaderService
from ....config.database import get_db_session

from ....schemas.Client import ClientResponse
from ....repository.base import BaseRepository
from ....models.Client import Client

router = APIRouter()

loading_tasks = {}

@router.get("/get_client_by_id/{client_id}", response_model=ClientResponse)
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_db_session)):
    repository = BaseRepository(Client)
    client = await repository.get_by_id(session, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/upload-excel", response_model=Dict[str, Any])
async def upload_excel(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db_session)
):
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400, 
            detail="El archivo debe ser un Excel (.xlsx o .xls)"
        )
    
    try:
        task_id = str(uuid.uuid4())
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        loading_tasks[task_id] = {
            "status": "processing",
            "filename": file.filename,
            "results": None,
            "error": None
        }
        
        background_tasks.add_task(
            process_excel_background,
            task_id,
            tmp_file_path,
            session
        )
        
        return {
            "task_id": task_id,
            "status": "processing",
            "message": f"Archivo {file.filename} está siendo procesado"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {str(e)}")
    
async def process_excel_background(task_id: str, file_path: str, session: AsyncSession):
    try:
        loading_tasks[task_id]["status"] = "processing"
        
        loader = ExcelLoaderService()
        
        results = await loader.load_excel_to_database(file_path, session)
        
        loading_tasks[task_id]["status"] = "completed"
        loading_tasks[task_id]["results"] = results
        
    except Exception as e:
        loading_tasks[task_id]["status"] = "error"
        loading_tasks[task_id]["error"] = str(e)
        
    finally:
        try:
            os.unlink(file_path)
        except:
            pass