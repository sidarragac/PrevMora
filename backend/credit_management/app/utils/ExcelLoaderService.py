import pandas as pd
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession


from ..config.logger import logger
from ..config.database import sessionmanager

from ..models.Alert import AlertTypeEnum, Alert
from ..models.Client import ClientStateEnum, Client
from ..models.Credit import CreditStateEnum, Credit, INTEREST_RATE_MULTIPLIER
from ..models.Installment import InstallmentStateEnum, Installment
from ..models.Manager import ManagerZoneEnum, Manager
from ..models.Portfolio import ContactMethodEnum, ContactResultEnum, Portfolio
from ..models.Reconciliation import PaymentChanelEnum, Reconciliation

# INTEREST_RATE_MULTIPLIER = 10000

class ExcelLoaderService:
    def __init__(self):
        self.client_mapping = {}  # For mapping client IDs
        self.credit_mapping = {}  # For mapping credit IDs
        self.installment_mapping = {}  # For mapping installment IDs
        self.manager_mapping = {}  # For mapping manager IDs

    async def load_excel_to_database(self, file_path: str, session: AsyncSession) -> Dict[str, Any]:
        try:
            excel_data = pd.read_excel(file_path, sheet_name=None)
            
            results = {
                "clients": 0,
                "credits": 0,
                "installments": 0,
                "managers": 0,
                "portfolios": 0,
                "alerts": 0,
                "reconciliations": 0,
                "errors": []
            }

            await self._process_clients(excel_data.get('Clientes', pd.DataFrame()), session, results)
            await self._process_managers(excel_data.get('Gestores', pd.DataFrame()), session, results)
            await self._process_credits(excel_data.get('Créditos', pd.DataFrame()), session, results)
            await self._process_installments(excel_data.get('Detalle cuotas', pd.DataFrame()), session, results)
            await self._process_portfolio(excel_data.get('Cartera', pd.DataFrame()), session, results)
            await self._process_alerts(excel_data.get('Alertas', pd.DataFrame()), session, results)
            await self._process_reconciliations(excel_data.get('Conciliaciones', pd.DataFrame()), session, results)

            await session.commit()
            logger.info(f"Proceso completado exitosamente: {results}")
            return results

        except Exception as e:
            await session.rollback()
            logger.error(f"Error en el proceso de carga: {str(e)}")
            raise

    async def _process_clients(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de clientes")
            return

        for _, row in df.iterrows():
            try:
                state_mapping = {
                    "Activo": ClientStateEnum.ACTIVE,
                    "Castigado": ClientStateEnum.PUNISHED,
                    "En mora": ClientStateEnum.OVERDUE,
                    "En Mora": ClientStateEnum.OVERDUE
                }

                client = Client(
                    name=str(row['Nombre']).strip(),
                    document=str(row['Documento']).strip(),
                    phone=str(row['Teléfono']).strip(),
                    email=str(row['Correo']).strip(),
                    address=str(row['Dirección']).strip() if pd.notna(row['Dirección']) else "",
                    zone=str(row['Zona']).strip() if pd.notna(row['Zona']) else None,
                    client_state=state_mapping.get(str(row['Estado_Cliente']).strip(), ClientStateEnum.ACTIVE)
                )

                session.add(client)
                await session.flush()
                
                self.client_mapping[int(row['ID_Cliente'])] = client.id
                results["clients"] += 1

            except Exception as e:
                error_msg = f"Error procesando cliente {row.get('ID_Cliente', 'N/A')}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

    async def _process_managers(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de gestores")
            return

        for _, row in df.iterrows():
            try:
                zone_mapping = {
                    "Rural": ManagerZoneEnum.RURAL,
                    "Urbana": ManagerZoneEnum.URBAN,
                    "Urbano": ManagerZoneEnum.URBAN
                }

                manager = Manager(
                    name=str(row['Nombre_Gestor']).strip(),
                    manager_zone=zone_mapping.get(str(row['Zona_Asignada']).strip(), ManagerZoneEnum.RURAL)
                )

                session.add(manager)
                await session.flush()
                
                self.manager_mapping[int(row['Numero_Gestor'])] = manager.id
                results["managers"] += 1

            except Exception as e:
                error_msg = f"Error procesando gestor {row.get('Numero_Gestor', 'N/A')}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

    async def _process_credits(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de créditos")
            return

        for _, row in df.iterrows():
            try:
                state_mapping = {
                    "Vigente": CreditStateEnum.APPROVED,
                    "Cancelado": CreditStateEnum.CANCELED,
                    "En Mora": CreditStateEnum.MORA,
                    "Pendiente": CreditStateEnum.PENDING
                }

                original_client_id = int(row['Numero_Cliente'])
                if original_client_id not in self.client_mapping:
                    raise ValueError(f"Cliente {original_client_id} no encontrado")

                disbursement_date = pd.to_datetime(row['Fecha_Desembolso'], dayfirst=True).date()

                credit = Credit(
                    client_id=self.client_mapping[original_client_id],
                    credit_state=state_mapping.get(str(row['Estado_Credito']).strip(), CreditStateEnum.PENDING),
                    disbursement_amount=int(float(row['Monto_Original'])),
                    payment_reference=int(row['Referencia_Pago']),
                    disbursement_date=disbursement_date,
                    interest_rate=int(float(row['Tasa_Interes']) * INTEREST_RATE_MULTIPLIER),
                    total_quotas=int(row['Cuotas_Totales'])
                )

                session.add(credit)
                await session.flush()
                
                self.credit_mapping[int(row['Numero_Credito'])] = credit.id
                results["credits"] += 1

            except Exception as e:
                error_msg = f"Error procesando crédito {row.get('Numero_Credito', 'N/A')}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

    async def _process_installments(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de cuotas")
            return

        for _, row in df.iterrows():
            try:
                state_mapping = {
                    "Pagada": InstallmentStateEnum.PAID,
                    "Pendiente": InstallmentStateEnum.PENDING,
                    "Vencida": InstallmentStateEnum.OVERDUE,
                    "Promesa de pago": InstallmentStateEnum.PROMISE
                }

                original_credit_id = int(row['Numero_Credito'])
                if original_credit_id not in self.credit_mapping:
                    raise ValueError(f"Crédito {original_credit_id} no encontrado")

                due_date = pd.to_datetime(row['Fecha_Vencimiento'], dayfirst=True).date()
                payment_date = None
                if pd.notna(row['Fecha_Pago']) and str(row['Fecha_Pago']).strip():
                    payment_date = pd.to_datetime(row['Fecha_Pago'], dayfirst=True).date()

                installment = Installment(
                    credit_id=self.credit_mapping[original_credit_id],
                    installment_state=state_mapping.get(str(row['Estado_Cuota']).strip(), InstallmentStateEnum.PENDING),
                    installment_number=int(row['Numero_Cuota2']),
                    installment_value=int(float(row['Valor_Cuota'])),
                    due_date=due_date,
                    payment_date=payment_date
                )

                session.add(installment)
                await session.flush()
                
                self.installment_mapping[int(row['Numero_Cuota'])] = installment.id
                results["installments"] += 1

            except Exception as e:
                error_msg = f"Error procesando cuota {row.get('Numero_Cuota', 'N/A')}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

    async def _process_portfolio(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de gestiones")
            return

        for _, row in df.iterrows():
            try:
                contact_method_mapping = {
                    "Telefono": ContactMethodEnum.PHONE,
                    "Correo": ContactMethodEnum.EMAIL,
                    "WhatsApp": ContactMethodEnum.WHATSAPP,
                    "Visita": ContactMethodEnum.VISIT
                }

                contact_result_mapping = {
                    "Efectiva": ContactResultEnum.SUCCESFUL,
                    "Sin respuesta": ContactResultEnum.NO_ANSWER,
                    "Numero errado": ContactResultEnum.BAD_CONTACT_INFORMATION,
                    "Promesa de pago": ContactResultEnum.PROMISE_TO_PAY
                }

                original_installment_id = int(row['Numero_Cuota'])
                original_manager_id = int(row['Numero del Gestor'])

                if original_installment_id not in self.installment_mapping:
                    raise ValueError(f"Cuota {original_installment_id} no encontrada")
                if original_manager_id not in self.manager_mapping:
                    raise ValueError(f"Gestor {original_manager_id} no encontrado")

                management_date = pd.to_datetime(row['Fecha_Gestion'], dayfirst=True).date()

                portfolio = Portfolio(
                    installment_id=self.installment_mapping[original_installment_id],
                    manager_id=self.manager_mapping[original_manager_id],
                    contact_method=contact_method_mapping.get(str(row['Medio_Contacto']).strip(), ContactMethodEnum.PHONE),
                    contact_result=contact_result_mapping.get(str(row['Resultado']).strip(), ContactResultEnum.NO_ANSWER),
                    management_date=management_date,
                    observation=str(row['Observaciones']).strip() if pd.notna(row['Observaciones']) else None,
                    payment_promise_date=None
                )

                session.add(portfolio)
                results["portfolios"] += 1

            except Exception as e:
                error_msg = f"Error procesando gestión {row.get('Numero_Gestion', 'N/A')}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

    async def _process_alerts(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de alertas")
            return

        for _, row in df.iterrows():
            try:
                alert_type_mapping = {
                    "No respuesta": AlertTypeEnum.NO_ANSWER,
                    "Riesgo de mora": AlertTypeEnum.WARNING,
                    "Requiere visita": AlertTypeEnum.VISIT_REQUIRED
                }

                original_credit_id = int(row['Numero_Credito'])
                if original_credit_id not in self.credit_mapping:
                    raise ValueError(f"Crédito {original_credit_id} no encontrado")

                alert_date = pd.to_datetime(row['Fecha_Alerta'], dayfirst=True).date()
                manually_generated = str(row['Generada_Manualmente']).strip().lower() in ['si', 'yes', 'true']

                alert = Alert(
                    credit_id=self.credit_mapping[original_credit_id],
                    alert_type=alert_type_mapping.get(str(row['Tipo_Alerta']).strip(), AlertTypeEnum.NO_ANSWER),
                    manually_generated=manually_generated,
                    alert_date=alert_date
                )

                session.add(alert)
                results["alerts"] += 1

            except Exception as e:
                error_msg = f"Error procesando alerta: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)

    async def _process_reconciliations(self, df: pd.DataFrame, session: AsyncSession, results: Dict[str, Any]):
        if df.empty:
            logger.warning("No se encontraron datos de transacciones")
            return

        for _, row in df.iterrows():
            try:
                channel_mapping = {
                    "Oficina": PaymentChanelEnum.OFFICE,
                    "Corresponsal": PaymentChanelEnum.CORRESPONDENT,
                    "Transferencia": PaymentChanelEnum.TRANSFER,
                    "Sucursal": PaymentChanelEnum.BRANCH
                }

                transaction_date = pd.to_datetime(row['Fecha_Transaccion'], dayfirst=True).date()
                payment_reference = int(row['Referencia_Pago'])

                reconciliation = Reconciliation(
                    payment_channel=channel_mapping.get(str(row['Canal_Pago']).strip(), PaymentChanelEnum.OFFICE),
                    payment_reference=payment_reference,
                    payment_amount=int(float(row['Valor_Pagado'])),
                    transaction_date=transaction_date,
                    observation=str(row['Observaciones']).strip() if pd.notna(row['Observaciones']) else None
                )

                session.add(reconciliation)
                results["reconciliations"] += 1

            except Exception as e:
                error_msg = f"Error procesando transacción {row.get('Transaccion', 'N/A')}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)