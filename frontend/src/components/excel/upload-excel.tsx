'use client';

import React, { useCallback, useState } from 'react';

import {
  AlertCircle,
  CheckCircle,
  FileSpreadsheet,
  Loader2,
  Upload,
  X,
} from 'lucide-react';

import { ExcelService } from '@/services/excel-service';
import { UploadExcelResponse } from '@/types/excel';

interface UploadExcelProps {
  onUploadSuccess?: (response: UploadExcelResponse) => void;
  onUploadError?: (error: string) => void;
}

interface UploadState {
  isDragOver: boolean;
  isUploading: boolean;
  uploadProgress: number;
  error: string | null;
  success: boolean;
  fileName: string | null;
}

export default function UploadExcel({
  onUploadSuccess,
  onUploadError,
}: UploadExcelProps) {
  const [uploadState, setUploadState] = useState<UploadState>({
    isDragOver: false,
    isUploading: false,
    uploadProgress: 0,
    error: null,
    success: false,
    fileName: null,
  });

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setUploadState((prev) => ({ ...prev, isDragOver: true }));
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setUploadState((prev) => ({ ...prev, isDragOver: false }));
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setUploadState((prev) => ({ ...prev, isDragOver: false }));

    const files = Array.from(e.dataTransfer.files);
    const excelFile = files.find(
      (file) =>
        file.type ===
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
        file.type === 'application/vnd.ms-excel' ||
        file.name.endsWith('.xlsx') ||
        file.name.endsWith('.xls')
    );

    if (excelFile) {
      handleFileUpload(excelFile);
    } else {
      setUploadState((prev) => ({
        ...prev,
        error: 'Por favor, selecciona un archivo Excel válido (.xlsx o .xls)',
      }));
    }
  }, []);

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        handleFileUpload(file);
      }
    },
    []
  );

  const handleFileUpload = async (file: File) => {
    // Validate file first
    const validation = ExcelService.validateFile(file);
    if (!validation.valid) {
      setUploadState((prev) => ({
        ...prev,
        error: validation.error || 'Archivo no válido',
        success: false,
      }));
      onUploadError?.(validation.error || 'Archivo no válido');
      return;
    }

    // Reset state
    setUploadState({
      isDragOver: false,
      isUploading: true,
      uploadProgress: 0,
      error: null,
      success: false,
      fileName: file.name,
    });

    let progressInterval: NodeJS.Timeout | null = null;

    try {
      // Simulate progress
      progressInterval = setInterval(() => {
        setUploadState((prev) => ({
          ...prev,
          uploadProgress: Math.min(prev.uploadProgress + 10, 90),
        }));
      }, 200);

      // Use the Excel service
      const result = await ExcelService.uploadExcel(file);

      if (progressInterval) {
        clearInterval(progressInterval);
      }

      if (!result.success) {
        throw new Error(
          result.error || 'Error desconocido al subir el archivo'
        );
      }

      setUploadState((prev) => ({
        ...prev,
        isUploading: false,
        uploadProgress: 100,
        success: true,
        error: null,
      }));

      onUploadSuccess?.(result.data!);

      // Reset after 3 seconds
      setTimeout(() => {
        setUploadState({
          isDragOver: false,
          isUploading: false,
          uploadProgress: 0,
          error: null,
          success: false,
          fileName: null,
        });
      }, 3000);
    } catch (error) {
      if (progressInterval) {
        clearInterval(progressInterval);
      }

      const errorMessage =
        error instanceof Error
          ? error.message
          : 'Error desconocido al subir el archivo';

      setUploadState((prev) => ({
        ...prev,
        isUploading: false,
        uploadProgress: 0,
        error: errorMessage,
        success: false,
      }));

      onUploadError?.(errorMessage);
    }
  };

  const resetUpload = () => {
    setUploadState({
      isDragOver: false,
      isUploading: false,
      uploadProgress: 0,
      error: null,
      success: false,
      fileName: null,
    });
  };

  return (
    <div className="mx-auto w-full max-w-2xl">
      <div
        className={`relative rounded-lg border-2 border-dashed p-8 text-center transition-all duration-200 ${
          uploadState.isDragOver
            ? 'border-primary bg-primary/5'
            : 'border-base-300 hover:border-primary/50'
        } ${uploadState.isUploading ? 'pointer-events-none' : 'cursor-pointer'} ${uploadState.success ? 'border-success bg-success/5' : ''} ${uploadState.error ? 'border-error bg-error/5' : ''} `}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() =>
          !uploadState.isUploading &&
          document.getElementById('file-input')?.click()
        }
      >
        <input
          id="file-input"
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileSelect}
          className="hidden"
          disabled={uploadState.isUploading}
        />

        {/* Upload Icon */}
        <div className="mb-4 flex justify-center">
          {uploadState.isUploading ? (
            <Loader2 className="text-primary h-12 w-12 animate-spin" />
          ) : uploadState.success ? (
            <CheckCircle className="text-success h-12 w-12" />
          ) : uploadState.error ? (
            <AlertCircle className="text-error h-12 w-12" />
          ) : (
            <FileSpreadsheet className="text-primary h-12 w-12" />
          )}
        </div>

        {/* Upload Content */}
        {uploadState.isUploading ? (
          <div className="space-y-4">
            <h3 className="text-base-content text-lg font-semibold">
              Subiendo archivo...
            </h3>
            <p className="text-base-content/70">{uploadState.fileName}</p>
            <div className="bg-base-200 h-2 w-full rounded-full">
              <div
                className="bg-primary h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadState.uploadProgress}%` }}
              />
            </div>
            <p className="text-base-content/60 text-sm">
              {uploadState.uploadProgress}% completado
            </p>
          </div>
        ) : uploadState.success ? (
          <div className="space-y-4">
            <h3 className="text-success text-lg font-semibold">
              ¡Archivo subido exitosamente!
            </h3>
            <p className="text-base-content/70">{uploadState.fileName}</p>
            <button onClick={resetUpload} className="btn btn-outline btn-sm">
              Subir otro archivo
            </button>
          </div>
        ) : uploadState.error ? (
          <div className="space-y-4">
            <h3 className="text-error text-lg font-semibold">
              Error al subir archivo
            </h3>
            <p className="text-base-content/70">{uploadState.error}</p>
            <button onClick={resetUpload} className="btn btn-outline btn-sm">
              Intentar de nuevo
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <h3 className="text-base-content text-lg font-semibold">
              Subir archivo Excel
            </h3>
            <p className="text-base-content/70">
              Arrastra y suelta tu archivo Excel aquí, o haz clic para
              seleccionar
            </p>
            <div className="text-base-content/60 flex items-center justify-center gap-2 text-sm">
              <Upload className="h-4 w-4" />
              <span>Formatos soportados: .xlsx, .xls</span>
            </div>
          </div>
        )}

        {/* File Info */}
        {uploadState.fileName && !uploadState.isUploading && (
          <div className="bg-base-100 mt-4 rounded border p-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <FileSpreadsheet className="text-primary h-4 w-4" />
                <span className="text-sm font-medium">
                  {uploadState.fileName}
                </span>
              </div>
              {!uploadState.isUploading && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    resetUpload();
                  }}
                  className="btn btn-ghost btn-xs"
                >
                  <X className="h-3 w-3" />
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Instructions */}
      <div className="mt-6 text-center">
        <div className="text-base-content/60 text-sm">
          <p className="mb-2">
            <strong>Instrucciones:</strong>
          </p>
          <ul className="mx-auto max-w-md space-y-1 text-left">
            <li>• El archivo debe estar en formato Excel (.xlsx o .xls)</li>
            <li>
              • Asegúrate de que el archivo contenga los datos de créditos
            </li>
            <li>
              • El proceso puede tomar unos momentos dependiendo del tamaño del
              archivo
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
