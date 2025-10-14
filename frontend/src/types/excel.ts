// Types for Excel upload functionality

export interface UploadExcelRequest {
  file: File;
}

export interface UploadExcelResponse {
  task_id: string;
  status: 'processing' | 'completed' | 'failed';
  message: string;
  processed_records?: number;
  errors?: string[];
  warnings?: string[];
  [key: string]: any; // For additional response fields
}

export interface UploadExcelError {
  detail:
    | string
    | Array<{
        loc: string[];
        msg: string;
        type: string;
      }>;
}
