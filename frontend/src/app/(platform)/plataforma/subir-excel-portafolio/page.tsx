import React from 'react';

import { FileSpreadsheet } from 'lucide-react';

import UploadExcelWrapper from '@/components/excel/upload-excel-wrapper';

export const dynamic = 'force-dynamic';
export default function SubirExcelPortafolioPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="bg-primary/10 rounded-full p-3">
          <FileSpreadsheet className="text-primary h-8 w-8" />
        </div>
        <div>
          <h1 className="text-base-content text-3xl font-bold">
            Subir Portafolio (Excel)
          </h1>
          <p className="text-base-content/70">
            Importa gestiones de cartera desde un archivo Excel
          </p>
        </div>
      </div>

      {/* Upload Component using Portfolio endpoint */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-8">
          <UploadExcelWrapper variant="portfolio" />
        </div>
      </div>

      {/* Help Section */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title text-lg font-semibold">Guía rápida</h3>
        </div>
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <h4 className="text-base-content mb-3 font-semibold">
                Formato Requerido
              </h4>
              <div className="text-base-content/70 space-y-2 text-sm">
                <p>El Excel debe contener al menos estas columnas:</p>
                <ul className="ml-4 list-inside list-disc space-y-1">
                  <li>ID de Cuota</li>
                  <li>ID de Gestor</li>
                  <li>Método de Contacto</li>
                  <li>Resultado del Contacto</li>
                  <li>Fecha de Gestión</li>
                  <li>Observación</li>
                  <li>Fecha Promesa de Pago (opcional)</li>
                </ul>
              </div>
            </div>
            <div>
              <h4 className="text-base-content mb-3 font-semibold">
                Límites y Restricciones
              </h4>
              <div className="text-base-content/70 space-y-2 text-sm">
                <p>• Tamaño máximo: 10MB</p>
                <p>• Máximo 10,000 registros por archivo</p>
                <p>• Solo archivos .xlsx y .xls</p>
                <p>• Primera fila debe contener los encabezados</p>
                <p>• Validar datos requeridos antes de subir</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
