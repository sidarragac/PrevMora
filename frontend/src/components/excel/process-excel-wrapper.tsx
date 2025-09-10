'use client';

import React from 'react';

import { UploadExcelResponse } from '@/types/excel';

import ProcessExcelButton from './process-excel-button';

export default function ProcessExcelWrapper() {
  const handleProcessComplete = (response: UploadExcelResponse) => {
    console.log('Process completed:', response);
    // Aquí puedes manejar la respuesta exitosa
    // Por ejemplo, mostrar un toast de éxito o actualizar el estado
  };

  const handleProcessError = (error: string) => {
    console.error('Process error:', error);
    // Aquí puedes manejar el error
    // Por ejemplo, mostrar un toast de error
  };

  return (
    <ProcessExcelButton
      onProcessComplete={handleProcessComplete}
      onProcessError={handleProcessError}
    />
  );
}
