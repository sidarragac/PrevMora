from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ....models.base import Base
from ....config.database import get_db_session, sessionmanager
from ....models import (
    Alert,
    Alert_Type,
    Client_State,
    Client,
    Contact_Method,
    Contact_Result,
    Credit_State,
    Credit,
    Installment_State,
    Installment,
    Manager_Zone,
    Manager,
    Payment_Channel,
    Portfolio,
    Reconciliation
)

router = APIRouter()

@router.post("/create-tables-safe")
async def create_tables_safe():
    """Crear tablas de forma segura, una por una"""
    
    # Orden correcto para evitar problemas de FK
    table_order = [
        "alert_type",
        "client_state", 
        "contact_method",
        "contact_result",
        "credit_state",
        "installment_state",
        "manager_zone",
        "payment_channel",
        "client",
        "manager",
        "portfolio",
        "credit",
        "installment",
        "alert",
        "reconciliation"
    ]
    
    created_tables = []
    
    try:
        async with sessionmanager.connect() as connection:
            for table_name in table_order:
                if table_name in Base.metadata.tables:
                    table = Base.metadata.tables[table_name]
                    try:
                        await connection.run_sync(table.create, checkfirst=True)
                        created_tables.append(table_name)
                    except Exception as table_error:
                        print(f"Error creando tabla {table_name}: {table_error}")
                        continue
            
            await connection.commit()
            
        return {
            "message": "Proceso de creación completado",
            "created_tables": created_tables,
            "total_created": len(created_tables)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proceso de creación: {str(e)}")

@router.get("/check-tables")
async def check_existing_tables():
    """Verificar qué tablas existen en la base de datos"""
    try:
        async with sessionmanager.session() as session:
            # Para SQL Server
            result = await session.execute(text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' 
                AND TABLE_SCHEMA = 'dbo'
                ORDER BY TABLE_NAME
            """))
            
            existing_tables = [row[0] for row in result.fetchall()]
            
            # Comparar con modelos definidos
            defined_tables = list(Base.metadata.tables.keys())
            
            return {
                "existing_tables": existing_tables,
                "defined_in_models": defined_tables,
                "missing_tables": [t for t in defined_tables if t not in existing_tables],
                "extra_tables": [t for t in existing_tables if t not in defined_tables]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando tablas: {str(e)}")

@router.post("/drop-tables-safe")
async def drop_tables_safe():
    """Eliminar tablas en orden inverso para evitar problemas de FK"""
    
    table_order = [
        "reconciliation",
        "alert", 
        "installment",
        "credit",
        "portfolio",
        "manager",
        "client",
        "payment_channel",
        "manager_zone",
        "installment_state",
        "credit_state",
        "contact_result",
        "contact_method",
        "client_state",
        "alert_type"
    ]
    
    dropped_tables = []
    
    try:
        async with sessionmanager.connect() as connection:
            for table_name in table_order:
                if table_name in Base.metadata.tables:
                    try:
                        await connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                        dropped_tables.append(table_name)
                    except Exception as table_error:
                        print(f"Error eliminando tabla {table_name}: {table_error}")
                        continue
            
            await connection.commit()
            
        return {
            "message": "Tablas eliminadas exitosamente",
            "dropped_tables": dropped_tables
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando tablas: {str(e)}")

@router.get("/debug-foreign-keys")
async def debug_foreign_keys():
    """Debug de foreign keys para identificar problemas"""
    try:
        fk_info = []
        for table_name, table in Base.metadata.tables.items():
            table_fks = []
            for fk in table.foreign_keys:
                table_fks.append({
                    "column": fk.parent.name,
                    "references": f"{fk.column.table.name}.{fk.column.name}"
                })
            
            if table_fks:
                fk_info.append({
                    "table": table_name,
                    "foreign_keys": table_fks
                })
        
        return {"foreign_key_relationships": fk_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando FK: {str(e)}")