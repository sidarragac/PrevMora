import React from 'react';

import {
  Activity,
  Briefcase,
  Calendar,
  CheckCircle,
  Clock,
  DollarSign,
} from 'lucide-react';

import { Installment, Portfolio, Reconciliation } from '@/types/dashboard';

interface RecentActivityProps {
  installments: Installment[];
  portfolioManagements: Portfolio[];
  reconciliations: Reconciliation[];
  loading?: boolean;
}

export default function RecentActivity({
  installments,
  portfolioManagements,
  reconciliations,
  loading = false,
}: RecentActivityProps) {
  if (loading) {
    return (
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <Activity className="text-primary h-5 w-5" />
            Actividad Reciente
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, index) => (
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

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const getInstallmentStateColor = (state: string) => {
    switch (state.toLowerCase()) {
      case 'pagada':
        return 'badge-success';
      case 'pendiente':
        return 'badge-warning';
      case 'vencida':
        return 'badge-error';
      default:
        return 'badge-neutral';
    }
  };

  const getContactResultColor = (result: string) => {
    switch (result.toLowerCase()) {
      case 'efectiva':
        return 'badge-success';
      case 'promesa de pago':
        return 'badge-info';
      case 'no respuesta':
        return 'badge-warning';
      default:
        return 'badge-neutral';
    }
  };

  // Combinar todas las actividades y ordenar por fecha
  const allActivities = [
    ...installments.map((item) => ({
      type: 'installment' as const,
      data: item,
      date: item.due_date,
    })),
    ...portfolioManagements.map((item) => ({
      type: 'portfolio' as const,
      data: item,
      date: item.management_date,
    })),
    ...reconciliations.map((item) => ({
      type: 'reconciliation' as const,
      data: item,
      date: item.transaction_date,
    })),
  ].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  if (allActivities.length === 0) {
    return (
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <Activity className="text-primary h-5 w-5" />
            Actividad Reciente
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="py-8 text-center">
            <div className="text-base-300 mb-2 text-4xl">📊</div>
            <p className="text-base-content/70">No hay actividad reciente</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card bg-base-100 border-base-200 border shadow-sm">
      <div className="card-header bg-base-200 p-4">
        <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
          <Activity className="text-primary h-5 w-5" />
          Actividad Reciente
        </h3>
      </div>
      <div className="card-body p-6">
        <div className="space-y-3">
          {allActivities.slice(0, 8).map((activity, index) => (
            <div
              key={index}
              className="bg-base-50 hover:bg-base-100 flex items-center gap-3 rounded p-3 transition-colors"
            >
              <div className="flex-shrink-0">
                {activity.type === 'installment' && (
                  <Calendar className="text-info h-4 w-4" />
                )}
                {activity.type === 'portfolio' && (
                  <Briefcase className="text-secondary h-4 w-4" />
                )}
                {activity.type === 'reconciliation' && (
                  <DollarSign className="text-success h-4 w-4" />
                )}
              </div>
              <div className="min-w-0 flex-1">
                {activity.type === 'installment' && (
                  <>
                    <div className="mb-1 flex items-center gap-2">
                      <span className="text-base-content font-medium">
                        Cuota #{activity.data.installments_number}
                      </span>
                      <div
                        className={`badge badge-sm ${getInstallmentStateColor(
                          activity.data.installment_state
                        )}`}
                      >
                        {activity.data.installment_state}
                      </div>
                    </div>
                    <div className="text-base-content/70 text-sm">
                      Crédito #{activity.data.credit_id} -{' '}
                      {formatCurrency(
                        parseInt(activity.data.installments_value)
                      )}
                    </div>
                  </>
                )}
                {activity.type === 'portfolio' && (
                  <>
                    <div className="mb-1 flex items-center gap-2">
                      <span className="text-base-content font-medium">
                        Gestión de Cartera
                      </span>
                      <div
                        className={`badge badge-sm ${getContactResultColor(
                          activity.data.contact_result
                        )}`}
                      >
                        {activity.data.contact_result}
                      </div>
                    </div>
                    <div className="text-base-content/70 text-sm">
                      {activity.data.contact_method} - Gestor #
                      {activity.data.manager_id}
                    </div>
                  </>
                )}
                {activity.type === 'reconciliation' && (
                  <>
                    <div className="mb-1 flex items-center gap-2">
                      <span className="text-base-content font-medium">
                        Conciliación
                      </span>
                      <div className="badge badge-sm badge-success">
                        {activity.data.payment_channel}
                      </div>
                    </div>
                    <div className="text-base-content/70 text-sm">
                      {formatCurrency(activity.data.payment_amount)} - Ref:{' '}
                      {activity.data.payment_reference}
                    </div>
                  </>
                )}
              </div>
              <div className="flex-shrink-0 text-right">
                <div className="text-base-content/60 flex items-center gap-1 text-xs">
                  <Clock className="h-3 w-3" />
                  <span>{formatDate(activity.date)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        {allActivities.length > 8 && (
          <div className="mt-4 text-center">
            <button className="btn btn-outline btn-sm">
              Ver toda la actividad ({allActivities.length})
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
