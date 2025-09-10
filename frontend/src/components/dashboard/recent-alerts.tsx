import React from 'react';

import { AlertTriangle, Clock, CreditCard, User } from 'lucide-react';

import { Alert } from '@/types/dashboard';

interface RecentAlertsProps {
  alerts: Alert[];
  loading?: boolean;
}

export default function RecentAlerts({
  alerts,
  loading = false,
}: RecentAlertsProps) {
  if (loading) {
    return (
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <AlertTriangle className="text-warning h-5 w-5" />
            Alertas Recientes
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="space-y-3">
            {Array.from({ length: 3 }).map((_, index) => (
              <div
                key={index}
                className="bg-base-50 flex items-center gap-3 rounded p-3"
              >
                <div className="bg-base-300 h-4 w-4 animate-pulse rounded"></div>
                <div className="flex-1">
                  <div className="bg-base-300 mb-1 h-4 animate-pulse rounded"></div>
                  <div className="bg-base-300 h-3 w-2/3 animate-pulse rounded"></div>
                </div>
                <div className="bg-base-300 h-6 w-16 animate-pulse rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-CO', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getAlertTypeColor = (alertType: string) => {
    switch (alertType.toLowerCase()) {
      case 'riesgo de mora':
        return 'badge-error';
      case 'no respuesta':
        return 'badge-warning';
      case 'promesa de pago':
        return 'badge-info';
      default:
        return 'badge-neutral';
    }
  };

  if (!alerts || alerts.length === 0) {
    return (
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <AlertTriangle className="text-warning h-5 w-5" />
            Alertas Recientes
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="py-8 text-center">
            <div className="text-base-300 mb-2 text-4xl">✅</div>
            <p className="text-base-content/70">No hay alertas pendientes</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card bg-base-100 border-base-200 border shadow-sm">
      <div className="card-header bg-base-200 p-4">
        <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
          <AlertTriangle className="text-warning h-5 w-5" />
          Alertas Recientes ({alerts.length})
        </h3>
      </div>
      <div className="card-body p-6">
        <div className="space-y-3">
          {alerts.slice(0, 5).map((alert) => (
            <div
              key={alert.id}
              className="bg-warning/5 border-warning/20 hover:bg-warning/10 flex items-center gap-3 rounded border p-3 transition-colors"
            >
              <div className="flex-shrink-0">
                <AlertTriangle className="text-warning h-4 w-4" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="mb-1 flex items-center gap-2">
                  <span className="text-base-content font-medium">
                    {alert.alert_type}
                  </span>
                  <div
                    className={`badge badge-sm ${getAlertTypeColor(alert.alert_type)}`}
                  >
                    {alert.manually_generated ? 'Manual' : 'Auto'}
                  </div>
                </div>
                <div className="text-base-content/70 flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-1">
                    <User className="h-3 w-3" />
                    <span>Cliente #{alert.client_id}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <CreditCard className="h-3 w-3" />
                    <span>Crédito #{alert.credit_id}</span>
                  </div>
                </div>
              </div>
              <div className="flex-shrink-0 text-right">
                <div className="text-base-content/60 flex items-center gap-1 text-xs">
                  <Clock className="h-3 w-3" />
                  <span>{formatDate(alert.alert_date)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        {alerts.length > 5 && (
          <div className="mt-4 text-center">
            <button className="btn btn-outline btn-sm">
              Ver todas las alertas ({alerts.length})
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
