"""
Script de ejemplo para generar reportes de cartera usando el endpoint de analytics.

Este script muestra cómo:
1. Conectarse al endpoint de reportes
2. Generar un reporte con diferentes filtros
3. Manejar la respuesta y verificar el PDF generado
"""

import json
from datetime import date, timedelta

import requests


def generate_report(
    base_url: str = "http://localhost:8000",
    report_title: str = "Reporte de Cartera",
    period_start: date = None,
    period_end: date = None,
    filters: dict = None,
):
    """
    Genera un reporte de cartera.

    Args:
        base_url: URL base del servicio analytics
        report_title: Título del reporte
        period_start: Fecha de inicio del período
        period_end: Fecha de fin del período
        filters: Diccionario con filtros opcionales

    Returns:
        dict: Respuesta del servidor con metadata del reporte
    """
    # Usar fechas del último mes por defecto
    if period_end is None:
        period_end = date.today()
    if period_start is None:
        period_start = period_end - timedelta(days=30)

    # Construir payload
    payload = {
        "report_title": report_title,
        "period_start": str(period_start),
        "period_end": str(period_end),
    }

    if filters:
        payload["filters"] = filters

    # Hacer request
    endpoint = f"{base_url}/api/analytics/v1/analytics/reports/generate"

    print(f"\n{'='*60}")
    print(f"Generando reporte: {report_title}")
    print(f"{'='*60}")
    print(f"\nEndpoint: {endpoint}")
    print(f"Período: {period_start} → {period_end}")

    if filters:
        print(f"\nFiltros aplicados:")
        for key, value in filters.items():
            print(f"  - {key}: {value}")

    try:
        response = requests.post(
            endpoint, json=payload, headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Reporte generado exitosamente!")
            print(f"\nResultados:")
            print(f"  - Archivo: {result['file_path']}")
            print(f"  - Tamaño: {result['file_size']:,} bytes")
            print(f"  - Total clientes: {result['total_clients']}")
            print(f"  - Total créditos: {result['total_credits']}")
            print(f"  - Monto total: ${result['total_amount']:,}")
            print(f"  - Estado: {result['status']}")
            return result
        else:
            print(f"\n❌ Error al generar reporte")
            print(f"Status code: {response.status_code}")
            print(f"Respuesta: {response.text}")
            return None

    except requests.exceptions.ConnectionError:
        print(
            f"\n❌ Error de conexión. Verifica que el servidor esté corriendo en {base_url}"
        )
        return None
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        return None


if __name__ == "__main__":
    # Ejemplo 1: Reporte básico del último mes
    print("\n" + "=" * 60)
    print("EJEMPLO 1: Reporte básico del último mes")
    print("=" * 60)

    generate_report(report_title="Reporte Mensual Básico")

    # Ejemplo 2: Reporte de cartera activa en zona Norte
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Cartera activa zona Norte")
    print("=" * 60)

    generate_report(
        report_title="Cartera Activa - Zona Norte",
        period_start=date(2024, 1, 1),
        period_end=date(2024, 12, 31),
        filters={"credit_state": "Activo", "client_zone": "Norte"},
    )

    # Ejemplo 3: Reporte de cartera vencida (30-90 días)
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Cartera vencida 30-90 días")
    print("=" * 60)

    generate_report(
        report_title="Cartera Vencida 30-90 días",
        period_start=date(2024, 1, 1),
        period_end=date.today(),
        filters={
            "credit_state": "Vencido",
            "debt_age_min": 30,
            "debt_age_max": 90,
        },
    )

    # Ejemplo 4: Reporte por gestor específico
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Reporte por gestor")
    print("=" * 60)

    generate_report(
        report_title="Reporte Gestor ID 1",
        period_start=date(2024, 1, 1),
        period_end=date.today(),
        filters={"manager_id": 1},
    )

    # Ejemplo 5: Reporte de alto riesgo (>90 días)
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Cartera de alto riesgo")
    print("=" * 60)

    generate_report(
        report_title="Cartera Alto Riesgo (+90 días)",
        period_start=date(2023, 1, 1),
        period_end=date.today(),
        filters={"credit_state": "Activo", "debt_age_min": 90},
    )

    print("\n" + "=" * 60)
    print("Todos los ejemplos completados")
    print("=" * 60)
    print("\nVerifica los PDFs generados en el directorio 'reports/'")
