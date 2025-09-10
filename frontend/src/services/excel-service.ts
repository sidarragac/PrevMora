import { UploadExcelError, UploadExcelResponse } from '@/types/excel';

const API_BASE_URL = 'http://localhost:8000/api/PrevMora-Template/v1';

export class ExcelService {
  /**
   * Upload Excel file to the backend
   * @param file - The Excel file to upload
   * @returns Promise with upload response or error
   */
  static async uploadExcel(file: File): Promise<{
    success: boolean;
    data?: UploadExcelResponse;
    error?: string;
  }> {
    try {
      // Validate file type
      const allowedTypes = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel',
      ];

      const allowedExtensions = ['.xlsx', '.xls'];
      const fileExtension = file.name
        .toLowerCase()
        .substring(file.name.lastIndexOf('.'));

      if (
        !allowedTypes.includes(file.type) &&
        !allowedExtensions.includes(fileExtension)
      ) {
        return {
          success: false,
          error:
            'Tipo de archivo no válido. Solo se permiten archivos .xlsx y .xls',
        };
      }

      // Validate file size (10MB limit)
      const maxSize = 10 * 1024 * 1024; // 10MB in bytes
      if (file.size > maxSize) {
        return {
          success: false,
          error:
            'El archivo es demasiado grande. El tamaño máximo permitido es 10MB',
        };
      }

      // Create FormData
      const formData = new FormData();
      formData.append('file', file);

      // Make the request
      const response = await fetch(
        `${API_BASE_URL}/credit-management/upload-excel`,
        {
          method: 'POST',
          body: formData,
          // Don't set Content-Type header, let the browser set it with boundary
        }
      );

      if (!response.ok) {
        let errorMessage = `Error ${response.status}: ${response.statusText}`;

        try {
          const errorData: UploadExcelError = await response.json();

          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (Array.isArray(errorData.detail)) {
            // Handle validation errors
            errorMessage = errorData.detail
              .map((err) => `${err.loc.join('.')}: ${err.msg}`)
              .join(', ');
          }
        } catch {
          // If we can't parse the error response, use the default message
        }

        return {
          success: false,
          error: errorMessage,
        };
      }

      // Parse successful response
      const data: UploadExcelResponse = await response.json();

      // Check if the response indicates processing status
      if (data.status === 'processing') {
        return {
          success: true,
          data: {
            ...data,
            message:
              data.message || 'Archivo recibido y en proceso de análisis',
          },
        };
      }

      // If status is completed or failed, return accordingly
      if (data.status === 'completed') {
        return {
          success: true,
          data: {
            ...data,
            message: data.message || 'Archivo procesado exitosamente',
          },
        };
      }

      if (data.status === 'failed') {
        return {
          success: false,
          error: data.message || 'Error al procesar el archivo',
        };
      }

      // Default case - treat as success if we get here
      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('Excel upload error:', error);

      let errorMessage = 'Error desconocido al subir el archivo';

      if (error instanceof Error) {
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
          errorMessage =
            'No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose en http://localhost:8000';
        } else if (
          error.name === 'TypeError' &&
          error.message.includes('Failed to fetch')
        ) {
          errorMessage =
            'Error de conexión. Asegúrate de que el backend esté ejecutándose y sea accesible.';
        } else {
          errorMessage = error.message;
        }
      }

      return {
        success: false,
        error: errorMessage,
      };
    }
  }

  /**
   * Format file size for display
   * @param bytes - File size in bytes
   * @returns Formatted file size string
   */
  static formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  /**
   * Check task status (if backend provides this endpoint)
   * @param taskId - Task ID to check
   * @returns Promise with task status
   */
  static async checkTaskStatus(taskId: string): Promise<{
    success: boolean;
    data?: UploadExcelResponse;
    error?: string;
  }> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/credit-management/task-status/${taskId}`,
        {
          method: 'GET',
        }
      );

      if (!response.ok) {
        return {
          success: false,
          error: `Error ${response.status}: ${response.statusText}`,
        };
      }

      const data: UploadExcelResponse = await response.json();

      return {
        success: true,
        data,
      };
    } catch (error) {
      console.error('Task status check error:', error);
      return {
        success: false,
        error: 'Error al verificar el estado de la tarea',
      };
    }
  }

  /**
   * Validate Excel file before upload
   * @param file - File to validate
   * @returns Validation result
   */
  static validateFile(file: File): { valid: boolean; error?: string } {
    // Check file type
    const allowedTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel',
    ];

    const allowedExtensions = ['.xlsx', '.xls'];
    const fileExtension = file.name
      .toLowerCase()
      .substring(file.name.lastIndexOf('.'));

    if (
      !allowedTypes.includes(file.type) &&
      !allowedExtensions.includes(fileExtension)
    ) {
      return {
        valid: false,
        error:
          'Tipo de archivo no válido. Solo se permiten archivos .xlsx y .xls',
      };
    }

    // Check file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
      return {
        valid: false,
        error: `El archivo es demasiado grande (${this.formatFileSize(file.size)}). El tamaño máximo permitido es 10MB`,
      };
    }

    return { valid: true };
  }
}
