import React from 'react';

import {
  AlertCircle,
  CheckCircle,
  FileSpreadsheet,
  Upload,
} from 'lucide-react';

import ProcessExcelWrapper from '@/components/excel/process-excel-wrapper';
import ServerStatus from '@/components/excel/server-status';
import UploadExcelWrapper from '@/components/excel/upload-excel-wrapper';

export const dynamic = 'force-dynamic';
export default function SubirExcelPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="bg-primary/10 rounded-full p-3">
          <FileSpreadsheet className="text-primary h-8 w-8" />
        </div>
        <div>
          <h1 className="text-base-content text-3xl font-bold">
            Subir Archivo Excel
          </h1>
          <p className="text-base-content/70">
            Importa datos de créditos desde un archivo Excel
          </p>
        </div>
      </div>

      {/* Server Status */}
      {/* <ServerStatus /> */}

      {/* Upload Component */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-8">
          <UploadExcelWrapper />
        </div>
      </div>

      {/* Process Excel Button */}
      {/* <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <FileSpreadsheet className="text-primary h-5 w-5" />
            Procesamiento Rápido
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="text-center">
            <p className="text-base-content/70 mb-4">
              Selecciona un archivo Excel para procesarlo directamente
            </p>
            <ProcessExcelWrapper />
          </div>
        </div>
      </div> */}

      {/* Information Cards */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {/* Success Info */}
        <div className="card bg-success/5 border-success/20 border">
          <div className="card-body p-6">
            <div className="mb-4 flex items-center gap-3">
              <CheckCircle className="text-success h-6 w-6" />
              <h3 className="text-success text-lg font-semibold">
                Proceso Exitoso
              </h3>
            </div>
            <ul className="text-base-content/70 space-y-2 text-sm">
              <li>• El archivo se procesará en segundo plano</li>
              <li>• Se validarán los formatos y tipos de datos</li>
              <li>• Se crearán los registros en la base de datos</li>
              <li>• El proceso puede tomar varios minutos</li>
              <li>• Recibirás un ID de tarea para seguimiento</li>
            </ul>
          </div>
        </div>

        {/* Error Info */}
        <div className="card bg-warning/5 border-warning/20 border">
          <div className="card-body p-6">
            <div className="mb-4 flex items-center gap-3">
              <AlertCircle className="text-warning h-6 w-6" />
              <h3 className="text-warning text-lg font-semibold">
                Posibles Errores
              </h3>
            </div>
            <ul className="text-base-content/70 space-y-2 text-sm">
              <li>• Formato de archivo no válido</li>
              <li>• Estructura de datos incorrecta</li>
              <li>• Campos obligatorios faltantes</li>
              <li>• Problemas de conexión con el servidor</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Help Section */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <Upload className="text-primary h-5 w-5" />
            Ayuda y Soporte
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <h4 className="text-base-content mb-3 font-semibold">
                Formato Requerido
              </h4>
              <div className="text-base-content/70 space-y-2 text-sm">
                <p>El archivo Excel debe contener las siguientes columnas:</p>
                <ul className="ml-4 list-inside list-disc space-y-1">
                  <li>ID del Cliente</li>
                  <li>Nombre del Cliente</li>
                  <li>Documento</li>
                  <li>Monto del Crédito</li>
                  <li>Fecha de Desembolso</li>
                  <li>Tasa de Interés</li>
                  <li>Número de Cuotas</li>
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
                <p>• No se permiten celdas vacías en campos obligatorios</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
