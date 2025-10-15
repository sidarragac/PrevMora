'use client';

import React, { useState } from 'react';

import { AlertCircle, CheckCircle, Info } from 'lucide-react';

import { ExcelService } from '@/services/excel-service';
import { UploadExcelResponse } from '@/types/excel';

import UploadExcel from './upload-excel';

interface UploadResult {
  type: 'success' | 'error' | 'info';
  title: string;
  message: string;
  details?: string[];
}

export default function UploadExcelWrapper({
  uploader,
  variant,
}: {
  uploader?: (file: File) => Promise<{
    success: boolean;
    data?: UploadExcelResponse;
    error?: string;
  }>;
  variant?: 'credit' | 'portfolio';
}) {
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);

  const handleUploadSuccess = (response: UploadExcelResponse) => {
    console.log('Upload successful:', response);

    // Process the response and create a user-friendly result
    let result: UploadResult;

    if (response.status === 'processing') {
      result = {
        type: 'info',
        title: 'Archivo recibido',
        message:
          response.message ||
          'El archivo está siendo procesado en segundo plano.',
        details: [
          `ID de tarea: ${response.task_id}`,
          'El procesamiento puede tomar varios minutos.',
          'Recibirás una notificación cuando esté listo.',
        ],
      };
    } else if (response.status === 'completed') {
      result = {
        type: 'success',
        title: '¡Archivo procesado exitosamente!',
        message: response.message || 'El archivo se procesó correctamente.',
        details: [],
      };

      // Add details based on response
      if (response.processed_records) {
        result.details?.push(
          `Registros procesados: ${response.processed_records}`
        );
      }

      if (response.warnings && response.warnings.length > 0) {
        result.details?.push(`Advertencias: ${response.warnings.length}`);
        result.details?.push(...response.warnings);
      }

      if (response.errors && response.errors.length > 0) {
        result.type = 'error';
        result.title = 'Archivo procesado con errores';
        result.message = 'El archivo se procesó pero contiene algunos errores:';
        result.details?.push(...response.errors);
      }
    } else {
      // Default case
      result = {
        type: 'success',
        title: '¡Archivo subido exitosamente!',
        message: response.message || 'El archivo se procesó correctamente.',
        details: [],
      };
    }

    setUploadResult(result);

    // Auto-hide after different delays based on status
    let hideDelay = 10000; // Default 10 seconds
    if (result.type === 'info') {
      hideDelay = 15000; // 15 seconds for processing status
    } else if (result.type === 'error') {
      hideDelay = 20000; // 20 seconds for errors
    }

    setTimeout(() => {
      setUploadResult(null);
    }, hideDelay);
  };

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error);

    const result: UploadResult = {
      type: 'error',
      title: 'Error al subir archivo',
      message: error,
      details: [],
    };

    setUploadResult(result);

    // Auto-hide after 10 seconds
    setTimeout(() => {
      setUploadResult(null);
    }, 10000);
  };

  const dismissResult = () => {
    setUploadResult(null);
  };

  return (
    <div className="space-y-6">
      {/* Upload Component */}
      <UploadExcel
        onUploadSuccess={handleUploadSuccess}
        onUploadError={handleUploadError}
        uploader={
          uploader ??
          (variant === 'portfolio'
            ? ExcelService.uploadPortfolioExcel
            : ExcelService.uploadExcel)
        }
      />

      {/* Upload Result Display */}
      {uploadResult && (
        <div
          className={`card border shadow-lg ${
            uploadResult.type === 'success'
              ? 'bg-success/5 border-success/20'
              : uploadResult.type === 'error'
                ? 'bg-error/5 border-error/20'
                : 'bg-info/5 border-info/20'
          }`}
        >
          <div className="card-body p-6">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                {uploadResult.type === 'success' && (
                  <CheckCircle className="text-success h-6 w-6" />
                )}
                {uploadResult.type === 'error' && (
                  <AlertCircle className="text-error h-6 w-6" />
                )}
                {uploadResult.type === 'info' && (
                  <Info className="text-info h-6 w-6" />
                )}
              </div>

              <div className="flex-1">
                <h3
                  className={`text-lg font-semibold ${
                    uploadResult.type === 'success'
                      ? 'text-success'
                      : uploadResult.type === 'error'
                        ? 'text-error'
                        : 'text-info'
                  }`}
                >
                  {uploadResult.title}
                </h3>

                <p className="text-base-content/80 mt-1">
                  {uploadResult.message}
                </p>

                {uploadResult.details && uploadResult.details.length > 0 && (
                  <div className="mt-4">
                    <ul className="space-y-1">
                      {uploadResult.details.map((detail, index) => (
                        <li
                          key={index}
                          className="text-base-content/70 text-sm"
                        >
                          • {detail}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              <button
                onClick={dismissResult}
                className="btn btn-ghost btn-sm flex-shrink-0"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Additional Info */}
      {/* <div className="text-center">
        <p className="text-base-content/60 text-sm">
          El archivo se enviará al endpoint:
          <code className="bg-base-200 ml-1 rounded px-2 py-1 text-xs">
            /api/PrevMora-Template/v1/credit-management/upload-excel
          </code>
        </p>
      </div> */}
    </div>
  );
}
