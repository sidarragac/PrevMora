'use client';

import React, { useEffect, useState } from 'react';

import { AlertCircle, CheckCircle, Loader2, Server } from 'lucide-react';

export default function ServerStatus() {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>(
    'checking'
  );
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkServerStatus = async () => {
    setStatus('checking');
    try {
      const response = await fetch(
        'http://localhost:8000/api/PrevMora-Template/v1/admin/check-tables',
        {
          method: 'GET',
          signal: AbortSignal.timeout(5000), // 5 second timeout
        }
      );

      if (response.ok) {
        setStatus('online');
      } else {
        setStatus('offline');
      }
    } catch (error) {
      setStatus('offline');
    }
    setLastChecked(new Date());
  };

  useEffect(() => {
    checkServerStatus();
    // Check every 30 seconds
    const interval = setInterval(checkServerStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = () => {
    switch (status) {
      case 'checking':
        return <Loader2 className="h-4 w-4 animate-spin" />;
      case 'online':
        return <CheckCircle className="text-success h-4 w-4" />;
      case 'offline':
        return <AlertCircle className="text-error h-4 w-4" />;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'checking':
        return 'Verificando servidor...';
      case 'online':
        return 'Servidor en línea';
      case 'offline':
        return 'Servidor fuera de línea';
    }
  };

  const getStatusClass = () => {
    switch (status) {
      case 'checking':
        return 'alert-info';
      case 'online':
        return 'alert-success';
      case 'offline':
        return 'alert-error';
    }
  };

  return (
    <div className={`alert ${getStatusClass()}`}>
      <div className="flex items-center gap-2">
        <Server className="h-4 w-4" />
        {getStatusIcon()}
        <span className="text-sm font-medium">{getStatusText()}</span>
        <span className="text-xs opacity-70">
          {lastChecked &&
            `Última verificación: ${lastChecked.toLocaleTimeString()}`}
        </span>
      </div>
      <div className="mt-2 flex items-center gap-2">
        <button
          onClick={checkServerStatus}
          disabled={status === 'checking'}
          className="btn btn-xs btn-outline"
        >
          {status === 'checking' ? 'Verificando...' : 'Verificar ahora'}
        </button>
        {status === 'offline' && (
          <span className="text-xs">
            Asegúrate de que el backend esté ejecutándose en
            http://localhost:8000
          </span>
        )}
      </div>
    </div>
  );
}
