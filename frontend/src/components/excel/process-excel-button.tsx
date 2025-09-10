'use client';

import React, { useState } from 'react';

import {
  AlertCircle,
  CheckCircle,
  FileSpreadsheet,
  Loader2,
  Upload,
} from 'lucide-react';

import { ExcelService } from '@/services/excel-service';
import { UploadExcelResponse } from '@/types/excel';

interface ProcessExcelButtonProps {
  onProcessComplete?: (response: UploadExcelResponse) => void;
  onProcessError?: (error: string) => void;
  className?: string;
}

interface ProcessState {
  isProcessing: boolean;
  status: 'idle' | 'processing' | 'success' | 'error';
  message: string;
  taskId?: string;
}

export default function ProcessExcelButton({
  onProcessComplete,
  onProcessError,
  className = '',
}: ProcessExcelButtonProps) {
  const [processState, setProcessState] = useState<ProcessState>({
    isProcessing: false,
    status: 'idle',
    message: '',
  });

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleProcessExcel(file);
    }
  };

  const handleProcessExcel = async (file: File) => {
    // Reset state
    setProcessState({
      isProcessing: true,
      status: 'processing',
      message: 'Validando archivo...',
    });

    try {
      // Use the Excel service to process the file
      const result = await ExcelService.uploadExcel(file);

      if (!result.success) {
        throw new Error(result.error || 'Error al procesar el archivo');
      }

      const response = result.data!;

      setProcessState({
        isProcessing: false,
        status: 'success',
        message: response.message || 'Archivo procesado exitosamente',
        taskId: response.task_id,
      });

      onProcessComplete?.(response);

      // Reset after 8 seconds
      setTimeout(() => {
        setProcessState({
          isProcessing: false,
          status: 'idle',
          message: '',
        });
      }, 8000);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Error desconocido';

      setProcessState({
        isProcessing: false,
        status: 'error',
        message: errorMessage,
      });

      onProcessError?.(errorMessage);

      // Reset after 8 seconds
      setTimeout(() => {
        setProcessState({
          isProcessing: false,
          status: 'idle',
          message: '',
        });
      }, 8000);
    }
  };

  const getButtonContent = () => {
    if (processState.isProcessing) {
      return (
        <>
          <Loader2 className="h-4 w-4 animate-spin" />
          Procesando...
        </>
      );
    }

    switch (processState.status) {
      case 'success':
        return (
          <>
            <CheckCircle className="h-4 w-4" />
            Procesado
          </>
        );
      case 'error':
        return (
          <>
            <AlertCircle className="h-4 w-4" />
            Error
          </>
        );
      default:
        return (
          <>
            <FileSpreadsheet className="h-4 w-4" />
            Procesar Excel
          </>
        );
    }
  };

  const getButtonClass = () => {
    const baseClass = 'btn gap-2';

    switch (processState.status) {
      case 'success':
        return `${baseClass} btn-success`;
      case 'error':
        return `${baseClass} btn-error`;
      case 'processing':
        return `${baseClass} btn-primary loading`;
      default:
        return `${baseClass} btn-primary`;
    }
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Hidden file input */}
      <input
        type="file"
        accept=".xlsx,.xls"
        onChange={handleFileSelect}
        className="hidden"
        id="process-excel-input"
        disabled={processState.isProcessing}
      />

      {/* Button */}
      <label
        htmlFor="process-excel-input"
        className={`cursor-pointer ${getButtonClass()} ${
          processState.isProcessing ? 'pointer-events-none' : ''
        }`}
      >
        {getButtonContent()}
      </label>

      {/* Status Message */}
      {processState.message && (
        <div
          className={`alert ${
            processState.status === 'success'
              ? 'alert-success'
              : processState.status === 'error'
                ? 'alert-error'
                : 'alert-info'
          }`}
        >
          <div className="flex items-center gap-2">
            {processState.status === 'success' && (
              <CheckCircle className="h-4 w-4" />
            )}
            {processState.status === 'error' && (
              <AlertCircle className="h-4 w-4" />
            )}
            {processState.status === 'processing' && (
              <Loader2 className="h-4 w-4 animate-spin" />
            )}
            <span className="text-sm">{processState.message}</span>
          </div>
        </div>
      )}

      {/* Task ID Display */}
      {processState.taskId && (
        <div className="alert alert-info">
          <div className="flex items-center gap-2">
            <FileSpreadsheet className="h-4 w-4" />
            <div className="text-sm">
              <strong>ID de Tarea:</strong> {processState.taskId}
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="text-center">
        <p className="text-base-content/60 text-xs">
          Haz clic para seleccionar un archivo Excel y procesarlo
        </p>
      </div>
    </div>
  );
}
