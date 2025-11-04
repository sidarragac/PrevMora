from typing import Any, Dict

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.logger import logger
from ..models.Credit import Credit
from ..models.Reconciliation import Reconciliation


class ReconciliationExcelService:
    """
    Service for loading reconciliation data from Excel files.
    
    Expected Excel format:
    - Fecha (Date): Transaction date
    - Referencia_Pago (String): Payment reference
    - Valor (Number): Payment amount
    - Canal_Pago (String): Payment channel (Oficina, Corresponsal, Transferencia, Sucursal)
    - Observaciones (String, optional): Observations
    """

    def __init__(self):
        self.channel_mapping = {
            "Oficina": "Oficina",
            "Corresponsal": "Corresponsal",
            "Transferencia": "Transferencia",
            "Sucursal": "Sucursal",
            "oficina": "Oficina",
            "corresponsal": "Corresponsal",
            "transferencia": "Transferencia",
            "sucursal": "Sucursal",
        }

    async def load_reconciliations_from_excel(
        self, file_path: str, session: AsyncSession
    ) -> Dict[str, Any]:
        """
        Load reconciliation data from an Excel file into the database.

        Args:
            file_path: Path to the Excel file
            session: Database session

        Returns:
            Dictionary with results including count of loaded records and errors
        """
        try:
            # Read Excel file - can be single sheet or named sheet
            excel_data = pd.read_excel(file_path, sheet_name=0)

            results = {
                "reconciliations_loaded": 0,
                "reconciliations_skipped": 0,
                "errors": [],
                "warnings": [],
                "created_ids": [],  # Lista de IDs de reconciliaciones creadas
                "invalid_references": [],  # Referencias de pago no encontradas
                "credits_updated": 0,  # Número de créditos actualizados a "Cancelado"
                "updated_credit_ids": [],  # IDs de créditos actualizados
            }

            # Validate required columns
            required_columns = ["Fecha", "Referencia_Pago", "Valor", "Canal_Pago"]
            missing_columns = [
                col for col in required_columns if col not in excel_data.columns
            ]

            if missing_columns:
                error_msg = f"Columnas requeridas faltantes: {', '.join(missing_columns)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                return results

            logger.info(f"Procesando {len(excel_data)} filas de conciliaciones")

            # Process each row
            i: int = 2 # Row counter to track logs
            for index, row in excel_data.iterrows():
                try:
                    # Skip empty rows
                    if pd.isna(row["Fecha"]) or pd.isna(row["Referencia_Pago"]):
                        results["reconciliations_skipped"] += 1
                        results["warnings"].append(
                            f"Fila {i}: Datos incompletos (Fecha o Referencia_Pago vacíos)"
                        )
                        continue

                    # Parse transaction date
                    try:
                        transaction_date = pd.to_datetime(
                            row["Fecha"], dayfirst=True
                        ).date()
                    except Exception as e:
                        results["errors"].append(
                            f"Fila {i}: Error al parsear fecha '{row['Fecha']}': {str(e)}"
                        )
                        results["reconciliations_skipped"] += 1
                        continue

                    # Get payment reference
                    payment_reference = str(row["Referencia_Pago"]).strip()

                    # Verify that a credit with this payment_reference exists
                    stmt = select(Credit).where(Credit.payment_reference == payment_reference)
                    result = await session.execute(stmt)
                    credit = result.scalar_one_or_none()

                    if credit is None:
                        results["reconciliations_skipped"] += 1
                        results["invalid_references"].append(payment_reference)
                        results["errors"].append(
                            f"Fila {i}: No existe un crédito con la referencia de pago '{payment_reference}'"
                        )
                        continue

                    # Parse payment amount
                    try:
                        payment_amount = int(float(row["Valor"]))
                        if payment_amount <= 0:
                            results["warnings"].append(
                                f"Fila {i}: Valor de pago es {payment_amount}, debería ser positivo"
                            )
                    except Exception as e:
                        results["errors"].append(
                            f"Fila {i}: Error al parsear valor '{row['Valor']}': {str(e)}"
                        )
                        results["reconciliations_skipped"] += 1
                        continue

                    # Get payment channel
                    raw_channel = str(row["Canal_Pago"]).strip()
                    payment_channel = self.channel_mapping.get(raw_channel, "Oficina")

                    if raw_channel not in self.channel_mapping:
                        results["warnings"].append(
                            f"Fila {i}: Canal de pago '{raw_channel}' no reconocido, usando 'Oficina' por defecto"
                        )

                    # Get observation (optional)
                    observation = None
                    if "Observaciones" in row and pd.notna(row["Observaciones"]):
                        observation = str(row["Observaciones"]).strip()

                    # Create reconciliation record
                    reconciliation = Reconciliation(
                        transaction_date=transaction_date,
                        payment_reference=payment_reference,
                        payment_amount=payment_amount,
                        payment_channel=payment_channel,
                        observation=observation,
                    )

                    session.add(reconciliation)
                    await session.flush()  # Flush to get the ID before commit
                    
                    # Update credit state to "Cancelado"
                    credit.credit_state = "Cancelado"
                    session.add(credit)
                    
                    # Store the generated ID and track updated credit
                    results["created_ids"].append(reconciliation.id)
                    results["updated_credit_ids"].append(credit.id)
                    results["credits_updated"] += 1
                    results["reconciliations_loaded"] += 1

                except Exception as e:
                    error_msg = f"Fila {i}: Error procesando registro: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    results["reconciliations_skipped"] += 1

                i += 1  # Increment row counter

            # Commit all changes
            await session.commit()
            logger.info(
                f"Proceso completado: {results['reconciliations_loaded']} registros cargados, "
                f"{results['reconciliations_skipped']} omitidos. "
                f"{results['credits_updated']} créditos actualizados a 'Cancelado'. "
                f"IDs reconciliaciones: {results['created_ids'][:10]}{'...' if len(results['created_ids']) > 10 else ''}"
            )

            return results

        except Exception as e:
            await session.rollback()
            error_msg = f"Error crítico en el proceso de carga: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
            raise

    def validate_excel_format(self, file_path: str) -> Dict[str, Any]:
        """
        Validate the Excel file format without loading to database.

        Args:
            file_path: Path to the Excel file

        Returns:
            Dictionary with validation results
        """
        try:
            excel_data = pd.read_excel(file_path, sheet_name=0)

            validation = {
                "valid": True,
                "total_rows": len(excel_data),
                "columns_found": list(excel_data.columns),
                "errors": [],
                "warnings": [],
            }

            # Check required columns
            required_columns = ["Fecha", "Referencia_Pago", "Valor", "Canal_Pago"]
            missing_columns = [
                col for col in required_columns if col not in excel_data.columns
            ]

            if missing_columns:
                validation["valid"] = False
                validation["errors"].append(
                    f"Columnas requeridas faltantes: {', '.join(missing_columns)}"
                )

            # Check for empty file
            if len(excel_data) == 0:
                validation["valid"] = False
                validation["errors"].append("El archivo Excel está vacío")

            # Check for duplicate references
            if "Referencia_Pago" in excel_data.columns:
                duplicates = excel_data["Referencia_Pago"].duplicated().sum()
                if duplicates > 0:
                    validation["warnings"].append(
                        f"Se encontraron {duplicates} referencias de pago duplicadas"
                    )

            return validation

        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Error al validar archivo: {str(e)}"],
                "warnings": [],
            }
