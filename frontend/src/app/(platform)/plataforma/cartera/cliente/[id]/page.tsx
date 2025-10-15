import Link from 'next/link';
import { notFound } from 'next/navigation';
import React from 'react';

import {
  AlertTriangle,
  ArrowLeft,
  Calendar,
  CreditCard,
  DollarSign,
  FileText,
  Mail,
  MapPin,
  Phone,
} from 'lucide-react';

import EditClientButton from '@/components/clients/edit-client-button';
import UpdateInstallmentDueDate from '@/components/clients/update-installment-due-date';

import { ClientCompleteData } from '@/types/client';

interface ClientDetailPageProps {
  params: Promise<{
    id: string;
  }>;
}

export const dynamic = 'force-dynamic';
async function getClientData(id: string): Promise<ClientCompleteData | null> {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
    const response = await fetch(
      `${baseUrl}/clients/get_client_complete_data/${id}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        cache: 'no-store', // Para desarrollo, en producción usar revalidate
      }
    );

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching client data:', error);
    return null;
  }
}

export default async function ClientDetailPage({
  params,
}: ClientDetailPageProps) {
  const { id } = await params;
  const clientData = await getClientData(id);

  if (!clientData) {
    notFound();
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-CO', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-6 flex items-center gap-4">
        <Link href="/plataforma/cartera" className="btn btn-ghost btn-sm gap-2">
          <ArrowLeft className="h-4 w-4" />
          Volver
        </Link>
        <div className="divider divider-horizontal"></div>
        <h1 className="text-base-content text-2xl font-bold">
          Detalle del Cliente
        </h1>
      </div>

      {/* Client Info Card */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-6">
          <div className="mb-6 flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-primary text-primary-content flex size-16 items-center justify-center rounded-full">
                <span className="text-xl font-semibold">
                  {clientData.name
                    .split(' ')
                    .map((n) => n[0])
                    .join('')
                    .toUpperCase()
                    .slice(0, 2)}
                </span>
              </div>
              <div>
                <h2 className="text-base-content text-2xl font-bold">
                  {clientData.name}
                </h2>
                <p className="text-base-content/70">ID: {clientData.id}</p>
                <div className="badge badge-success badge-outline mt-2">
                  {clientData.status}
                </div>
              </div>
            </div>
            <EditClientButton
              clientId={clientData.id}
              initialEmail={clientData.email}
              initialPhone={clientData.phone}
              initialAddress={clientData.address}
              initialZone={clientData.zone}
              initialStatus={clientData.status}
            />
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm">
                <FileText className="text-primary h-4 w-4" />
                <span className="font-semibold">Documento:</span>
                <span className="font-mono">{clientData.document}</span>
              </div>

              <div className="flex items-center gap-2 text-sm">
                <Mail className="text-primary h-4 w-4" />
                <span className="font-semibold">Email:</span>
                <span>{clientData.email}</span>
              </div>

              <div className="flex items-center gap-2 text-sm">
                <Phone className="text-primary h-4 w-4" />
                <span className="font-semibold">Teléfono:</span>
                <span>{clientData.phone}</span>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-start gap-2 text-sm">
                <MapPin className="text-primary mt-0.5 h-4 w-4" />
                <div>
                  <div className="font-semibold">Dirección:</div>
                  <div>{clientData.address}</div>
                  <div className="text-base-content/70 text-xs">
                    {clientData.zone}
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="stats stats-vertical shadow-sm">
                <div className="stat py-2">
                  <div className="stat-title text-xs">Total Créditos</div>
                  <div className="stat-value text-primary text-lg">
                    {clientData.total_credits}
                  </div>
                </div>
                <div className="stat py-2">
                  <div className="stat-title text-xs">Total Cuotas</div>
                  <div className="stat-value text-secondary text-lg">
                    {clientData.total_installments}
                  </div>
                </div>
                <div className="stat py-2">
                  <div className="stat-title text-xs">Alertas</div>
                  <div className="stat-value text-warning text-lg">
                    {clientData.total_alerts}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Credits Section */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <CreditCard className="text-primary h-5 w-5" />
            Créditos ({clientData.credits.length})
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="space-y-4">
            {clientData.credits.map((credit) => (
              <div
                key={credit.id}
                className="card bg-base-50 border-base-200 border"
              >
                <div className="card-body p-4">
                  <div className="mb-4 flex items-start justify-between">
                    <div>
                      <h4 className="text-base-content font-semibold">
                        Crédito #{credit.id}
                      </h4>
                      <p className="text-base-content/70 text-sm">
                        Referencia: {credit.payment_reference}
                      </p>
                    </div>
                    <div className="badge badge-outline">
                      {credit.credit_state}
                    </div>
                  </div>

                  <div className="mb-4 grid grid-cols-1 gap-4 md:grid-cols-3">
                    <div>
                      <div className="text-base-content/70 text-sm">
                        Monto Desembolsado
                      </div>
                      <div className="text-primary text-lg font-semibold">
                        {formatCurrency(credit.disbursement_amount)}
                      </div>
                    </div>
                    <div>
                      <div className="text-base-content/70 text-sm">
                        Tasa de Interés
                      </div>
                      <div className="font-semibold">
                        {(credit.interest_rate * 100).toFixed(2)}%
                      </div>
                    </div>
                    <div>
                      <div className="text-base-content/70 text-sm">
                        Total Cuotas
                      </div>
                      <div className="font-semibold">{credit.total_quotas}</div>
                    </div>
                  </div>

                  <div>
                    <div className="text-base-content/70 mb-2 text-sm">
                      Cuotas
                    </div>
                    <div className="space-y-2">
                      {credit.installments.map((installment) => (
                        <div
                          key={installment.id}
                          className="bg-base-100 flex items-center justify-between rounded p-2"
                        >
                          <div className="flex items-center gap-2">
                            <span className="font-medium">
                              Cuota {installment.installments_number}
                            </span>
                            <div
                              className={`badge badge-sm ${
                                installment.installment_state === 'Pagada'
                                  ? 'badge-success'
                                  : installment.installment_state ===
                                      'Pendiente'
                                    ? 'badge-warning'
                                    : 'badge-error'
                              }`}
                            >
                              {installment.installment_state}
                            </div>
                          </div>
                          <div className="flex items-center gap-3">
                            <div className="text-right">
                              <div className="font-semibold">
                                {formatCurrency(
                                  parseInt(installment.installments_value)
                                )}
                              </div>
                              <div className="text-base-content/70 text-xs">
                                Vence: {formatDate(installment.due_date)}
                              </div>
                            </div>
                            {installment.installment_state !== 'Pagada' && (
                              <UpdateInstallmentDueDate
                                installmentId={installment.id}
                                currentDueDate={installment.due_date}
                              />
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Alerts Section */}
      {clientData.alerts.length > 0 && (
        <div className="card bg-base-100 border-base-200 border shadow-lg">
          <div className="card-header bg-base-200 p-4">
            <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
              <AlertTriangle className="text-warning h-5 w-5" />
              Alertas ({clientData.alerts.length})
            </h3>
          </div>
          <div className="card-body p-6">
            <div className="space-y-3">
              {clientData.alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="bg-warning/10 border-warning/20 flex items-center justify-between rounded border p-3"
                >
                  <div>
                    <div className="text-warning font-semibold">
                      {alert.alert_type}
                    </div>
                    <div className="text-base-content/70 text-sm">
                      Crédito #{alert.credit_id} -{' '}
                      {formatDate(alert.alert_date)}
                    </div>
                  </div>
                  <div className="badge badge-warning badge-outline">
                    {alert.manually_generated ? 'Manual' : 'Automática'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Reconciliations Section */}
      {clientData.reconciliations.length > 0 && (
        <div className="card bg-base-100 border-base-200 border shadow-lg">
          <div className="card-header bg-base-200 p-4">
            <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
              <DollarSign className="text-success h-5 w-5" />
              Conciliaciones ({clientData.reconciliations.length})
            </h3>
          </div>
          <div className="card-body p-6">
            <div className="space-y-3">
              {clientData.reconciliations.map((reconciliation) => (
                <div
                  key={reconciliation.id}
                  className="bg-success/10 border-success/20 flex items-center justify-between rounded border p-3"
                >
                  <div>
                    <div className="text-success font-semibold">
                      {formatCurrency(reconciliation.payment_amount)}
                    </div>
                    <div className="text-base-content/70 text-sm">
                      Ref: {reconciliation.payment_reference} -{' '}
                      {formatDate(reconciliation.transaction_date)}
                    </div>
                  </div>
                  <div className="badge badge-success badge-outline">
                    {reconciliation.payment_channel}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
