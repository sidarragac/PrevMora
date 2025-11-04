import datetime
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.logger import logger
from ..models.Client import Client
from ..models.Credit import Credit
from ..models.Installment import Installment
from ..models.Manager import Manager
from ..models.Portfolio import Portfolio
from ..schemas.Report import ReportFilters


class ReportGeneratorService:
    """
    Service for generating PDF reports with customizable filters.
    """

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_report(
        self,
        session: AsyncSession,
        report_name: str,
        filters: Optional[ReportFilters] = None,
        period_start: Optional[datetime.date] = None,
        period_end: Optional[datetime.date] = None,
    ) -> Dict[str, Any]:
        """
        Generate a PDF report with given filters.

        Args:
            session: Database session
            report_name: Name of the report
            filters: Filters to apply
            period_start: Start date for period filter
            period_end: End date for period filter

        Returns:
            Dictionary with report metadata and statistics
        """
        try:
            logger.info(f"Starting report generation: {report_name}")

            # Collect data based on filters
            data = await self._collect_data(session, filters, period_start, period_end)

            # Generate filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_name.replace(' ', '_')}_{timestamp}.pdf"
            filepath = self.output_dir / filename

            # Generate PDF
            self._generate_pdf(
                filepath=str(filepath),
                report_name=report_name,
                data=data,
                filters=filters,
                period_start=period_start,
                period_end=period_end,
            )

            # Get file size
            file_size = os.path.getsize(filepath)

            logger.info(f"Report generated successfully: {filepath}")

            return {
                "file_path": str(filepath),
                "file_size": file_size,
                "total_clients": data["statistics"]["total_clients"],
                "total_credits": data["statistics"]["total_credits"],
                "total_amount": data["statistics"]["total_amount"],
                "status": "completed",
            }

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {
                "status": "failed",
                "error_message": str(e),
            }

    async def _collect_data(
        self,
        session: AsyncSession,
        filters: Optional[ReportFilters],
        period_start: Optional[datetime.date],
        period_end: Optional[datetime.date],
    ) -> Dict[str, Any]:
        """Collect data from database based on filters"""

        # Simple approach: Get credits with client info, then get manager separately if needed
        query = (
            select(
                Credit.id.label("credit_id"),
                Credit.payment_reference,
                Credit.disbursement_amount,
                Credit.disbursement_date,
                Credit.credit_state,
                Credit.total_quotas,
                Client.id.label("client_id"),
                Client.name.label("client_name"),
                Client.document.label("client_document"),
                Client.zone.label("client_zone"),
                Client.status.label("client_status"),
            )
            .join(Client, Credit.client_id == Client.id)
            .distinct()
        )

        conditions = []

        # Apply filters
        if filters:
            if filters.credit_state:
                conditions.append(Credit.credit_state == filters.credit_state)

            if filters.client_zone:
                conditions.append(Client.zone == filters.client_zone)

            if filters.debt_age_min is not None or filters.debt_age_max is not None:
                today = datetime.date.today()
                if filters.debt_age_min is not None:
                    min_date = today - datetime.timedelta(days=filters.debt_age_min)
                    conditions.append(Credit.disbursement_date <= min_date)
                if filters.debt_age_max is not None:
                    max_date = today - datetime.timedelta(days=filters.debt_age_max)
                    conditions.append(Credit.disbursement_date >= max_date)

        # Apply period filters
        if period_start:
            conditions.append(Credit.disbursement_date >= period_start)
        if period_end:
            conditions.append(Credit.disbursement_date <= period_end)
        
        # Handle manager filter with a subquery
        if filters and filters.manager_id:
            # Only include credits that have at least one installment managed by this manager
            manager_subquery = (
                select(Credit.id)
                .join(Installment, Credit.id == Installment.credit_id)
                .join(Portfolio, Installment.id == Portfolio.installment_id)
                .where(Portfolio.manager_id == filters.manager_id)
            )
            conditions.append(Credit.id.in_(manager_subquery))

        if conditions:
            query = query.where(and_(*conditions))

        # Execute query
        result = await session.execute(query)
        records = result.all()

        # If manager info is needed, get it separately for each credit
        credit_managers = {}
        if records:
            # Get manager info for all credits
            credit_ids = [r.credit_id for r in records]
            manager_query = (
                select(
                    Credit.id.label("credit_id"),
                    Manager.name.label("manager_name")
                )
                .join(Installment, Credit.id == Installment.credit_id)
                .join(Portfolio, Installment.id == Portfolio.installment_id)
                .join(Manager, Portfolio.manager_id == Manager.id)
                .where(Credit.id.in_(credit_ids))
                .distinct()
            )
            manager_result = await session.execute(manager_query)
            for row in manager_result:
                if row.credit_id not in credit_managers:
                    credit_managers[row.credit_id] = row.manager_name

        # Process data
        credits_data = []
        total_amount = 0
        clients_set = set()

        for record in records:
            manager_name = credit_managers.get(record.credit_id, "Sin asignar")
            
            credits_data.append(
                {
                    "credit_id": record.credit_id,
                    "payment_reference": record.payment_reference,
                    "client_name": record.client_name,
                    "client_document": record.client_document,
                    "disbursement_amount": record.disbursement_amount,
                    "disbursement_date": record.disbursement_date,
                    "credit_state": record.credit_state,
                    "client_zone": record.client_zone,
                    "manager_name": manager_name,
                }
            )
            total_amount += record.disbursement_amount or 0
            clients_set.add(record.client_id)

        return {
            "credits": credits_data,
            "statistics": {
                "total_clients": len(clients_set),
                "total_credits": len(credits_data),
                "total_amount": total_amount,
            },
        }

    def _generate_pdf(
        self,
        filepath: str,
        report_name: str,
        data: Dict[str, Any],
        filters: Optional[ReportFilters],
        period_start: Optional[datetime.date],
        period_end: Optional[datetime.date],
    ):
        """Generate PDF document"""

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a237e"),
            spaceAfter=30,
            alignment=1,  # Center
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#283593"),
            spaceAfter=12,
        )

        # Title
        story.append(Paragraph(report_name, title_style))
        story.append(
            Paragraph(
                f"Generado el: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.3 * inch))

        # Period information
        if period_start or period_end:
            period_text = "Período: "
            if period_start:
                period_text += f"Desde {period_start.strftime('%d/%m/%Y')} "
            if period_end:
                period_text += f"Hasta {period_end.strftime('%d/%m/%Y')}"
            story.append(Paragraph(period_text, styles["Normal"]))
            story.append(Spacer(1, 0.2 * inch))

        # Filters applied
        if filters:
            story.append(Paragraph("Filtros Aplicados:", heading_style))
            filter_data = []
            if filters.credit_state:
                filter_data.append(["Estado de Crédito:", filters.credit_state])
            if filters.client_zone:
                filter_data.append(["Zona de Cliente:", filters.client_zone])
            if filters.manager_id:
                filter_data.append(["ID de Gestor:", str(filters.manager_id)])
            if filters.debt_age_min is not None:
                filter_data.append(
                    ["Antigüedad Mínima (días):", str(filters.debt_age_min)]
                )
            if filters.debt_age_max is not None:
                filter_data.append(
                    ["Antigüedad Máxima (días):", str(filters.debt_age_max)]
                )

            if filter_data:
                filter_table = Table(filter_data, colWidths=[2.5 * inch, 3 * inch])
                filter_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, -1), 10),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ]
                    )
                )
                story.append(filter_table)
                story.append(Spacer(1, 0.3 * inch))

        # Statistics
        story.append(Paragraph("Resumen Estadístico:", heading_style))
        stats = data["statistics"]
        stats_data = [
            ["Total de Clientes:", f"{stats['total_clients']:,}"],
            ["Total de Créditos:", f"{stats['total_credits']:,}"],
            [
                "Monto Total:",
                f"${stats['total_amount']:,}",
            ],
        ]

        stats_table = Table(stats_data, colWidths=[2.5 * inch, 3 * inch])
        stats_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e3f2fd")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        story.append(stats_table)
        story.append(Spacer(1, 0.4 * inch))

        # Credits table
        if data["credits"]:
            story.append(Paragraph("Detalle de Créditos:", heading_style))
            story.append(Spacer(1, 0.1 * inch))

            # Table headers
            table_data = [
                [
                    "Ref. Pago",
                    "Cliente",
                    "Documento",
                    "Monto",
                    "Fecha",
                    "Estado",
                    "Gestor",
                ]
            ]

            # Add data rows
            for credit in data["credits"][:100]:  # Limit to first 100 for PDF size
                table_data.append(
                    [
                        credit["payment_reference"][:15],
                        credit["client_name"][:20],
                        credit["client_document"],
                        f"${credit['disbursement_amount']:,}",
                        credit["disbursement_date"].strftime("%d/%m/%Y"),
                        credit["credit_state"],
                        credit["manager_name"][:15],
                    ]
                )

            credits_table = Table(
                table_data,
                colWidths=[1 * inch, 1.2 * inch, 0.9 * inch, 0.9 * inch, 0.8 * inch, 0.8 * inch, 1 * inch],
            )
            credits_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a237e")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 9),
                        ("FONTSIZE", (0, 1), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                    ]
                )
            )
            story.append(credits_table)

            if len(data["credits"]) > 100:
                story.append(Spacer(1, 0.2 * inch))
                story.append(
                    Paragraph(
                        f"<i>Mostrando los primeros 100 créditos de {len(data['credits'])} totales.</i>",
                        styles["Italic"],
                    )
                )

        # Build PDF
        doc.build(story)
