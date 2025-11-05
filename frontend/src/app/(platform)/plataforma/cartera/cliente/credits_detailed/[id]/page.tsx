import Link from 'next/link';
import { notFound } from 'next/navigation';
import React from 'react';

import {
  ArrowLeft,
  Calendar,
  CreditCard,
  TrendingDown,
  TrendingUp,
} from 'lucide-react';

interface CreditDetailed {
  id: number;
  client_id: number;
  disbursement_amount: number;
  payment_reference: string;
  interest_rate: number;
  total_quotas: number;
  disbursement_date: string;
  credit_state: string;
  created_at: string;
  updated_at: string;
  installments: InstallmentDetailed[];
  total_paid: number;
  total_pending: number;
}

interface InstallmentDetailed {
  id: number;
  credit_id: number;
  installment_state: string;
  installments_number: number;
  installments_value: string;
  due_date: string;
  payment_date: string | null;
  created_at: string;
  updated_at: string;
  portfolio: PortfolioItem[];
}

interface PortfolioItem {
  id: number;
  installment_id: number;
  manager_id: number;
  manager_name: string;
  contact_method: string;
  contact_result: string;
  management_date: string;
  observation: string | null;
  payment_promise_date: string | null;
  created_at: string;
  updated_at: string;
}

export const dynamic = 'force-dynamic';

async function getCreditsDetailed(id: string): Promise<CreditDetailed[]> {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
    const result = await fetch(
      `${baseUrl}/clients/get_credits_detailed/${id}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!result.ok) {
      return [];
    }

    return await result.json();
  } catch (error) {
    console.error('Error fetching credits detailed:', error);
    return [];
  }
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const creditsDetailed = await getCreditsDetailed(id);

  if (!creditsDetailed || creditsDetailed.length === 0) {
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

  // Calculate totals
  const totalPaid = creditsDetailed.reduce(
    (sum, credit) => sum + credit.total_paid,
    0
  );
  const totalPending = creditsDetailed.reduce(
    (sum, credit) => sum + credit.total_pending,
    0
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-6 flex items-center gap-4">
        <Link
          href={`/plataforma/cartera/cliente/${id}`}
          className="btn btn-ghost btn-sm gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Volver
        </Link>
        <div className="divider divider-horizontal"></div>
        <h1 className="text-base-content text-2xl font-bold">
          Créditos Detallados
        </h1>
      </div>

      {/* Summary Stats */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="stat bg-base-200 rounded-lg p-4">
              <div className="stat-figure text-success">
                <TrendingUp className="h-8 w-8" />
              </div>
              <div className="stat-title">Total Pagado</div>
              <div className="stat-value text-success text-2xl">
                {formatCurrency(totalPaid)}
              </div>
            </div>
            <div className="stat bg-base-200 rounded-lg p-4">
              <div className="stat-figure text-error">
                <TrendingDown className="h-8 w-8" />
              </div>
              <div className="stat-title">Total Pendiente</div>
              <div className="stat-value text-error text-2xl">
                {formatCurrency(totalPending)}
              </div>
            </div>
            <div className="stat bg-base-200 rounded-lg p-4">
              <div className="stat-figure text-primary">
                <CreditCard className="h-8 w-8" />
              </div>
              <div className="stat-title">Total Créditos</div>
              <div className="stat-value text-primary text-2xl">
                {creditsDetailed.length}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Credits List */}
      <div className="space-y-6">
        {creditsDetailed.map((credit) => (
          <div
            key={credit.id}
            className="card bg-base-100 border-base-200 border shadow-lg"
          >
            <div className="card-header bg-base-200 flex items-center justify-between p-4">
              <div className="flex items-center gap-3">
                <CreditCard className="text-primary h-5 w-5" />
                <div>
                  <h3 className="card-title text-lg font-semibold">
                    Crédito #{credit.id}
                  </h3>
                  <p className="text-base-content/70 text-sm">
                    Ref: {credit.payment_reference}
                  </p>
                </div>
              </div>
              <div className="badge badge-outline badge-lg">
                {credit.credit_state}
              </div>
            </div>

            <div className="card-body p-6">
              {/* Credit Summary */}
              <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">
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
                <div>
                  <div className="text-base-content/70 text-sm">
                    Fecha Desembolso
                  </div>
                  <div className="font-semibold">
                    {formatDate(credit.disbursement_date)}
                  </div>
                </div>
              </div>

              {/* Credit Totals */}
              <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2">
                <div className="bg-success/10 border-success/20 rounded-lg border p-4">
                  <div className="flex items-center gap-2">
                    <TrendingUp className="text-success h-5 w-5" />
                    <div>
                      <div className="text-base-content/70 text-sm">
                        Total Pagado
                      </div>
                      <div className="text-success text-xl font-semibold">
                        {formatCurrency(credit.total_paid)}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-error/10 border-error/20 rounded-lg border p-4">
                  <div className="flex items-center gap-2">
                    <TrendingDown className="text-error h-5 w-5" />
                    <div>
                      <div className="text-base-content/70 text-sm">
                        Total Pendiente
                      </div>
                      <div className="text-error text-xl font-semibold">
                        {formatCurrency(credit.total_pending)}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Installments */}
              <div>
                <div className="mb-4 flex items-center gap-2">
                  <Calendar className="text-primary h-5 w-5" />
                  <h4 className="text-base-content text-lg font-semibold">
                    Cuotas ({credit.installments.length})
                  </h4>
                </div>
                <div className="space-y-4">
                  {credit.installments.map((installment) => (
                    <div key={installment.id} className="space-y-2">
                      <div className="bg-base-50 border-base-200 flex items-center justify-between rounded border p-4">
                        <div className="flex items-center gap-3">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-semibold">
                                Cuota {installment.installments_number}
                              </span>
                              <div
                                className={`badge ${
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
                              {installment.portfolio.length > 0 && (
                                <div className="badge badge-success badge-outline">
                                  ⤵︎
                                </div>
                              )}
                            </div>
                            <div className="text-base-content/70 mt-1 text-sm">
                              <div>
                                Valor:{' '}
                                {formatCurrency(
                                  parseInt(installment.installments_value)
                                )}
                              </div>
                              <div>
                                Vence: {formatDate(installment.due_date)}
                              </div>
                              {installment.payment_date && (
                                <div>
                                  Pagado: {formatDate(installment.payment_date)}
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Portfolio Management */}
                      {installment.portfolio.length > 0 && (
                        <div className="bg-base-50 border-base-200 space-y-2 rounded border p-4">
                          <div className="text-base-content/70 mb-2 text-sm font-semibold">
                            Gestión de Cartera
                          </div>
                          {installment.portfolio.map((pf) => (
                            <div
                              key={pf.id}
                              className="bg-base-100 border-base-200 flex items-start justify-between gap-3 rounded border p-3"
                            >
                              <div className="min-w-0 flex-1">
                                <div className="text-base-content flex flex-wrap items-center gap-2 text-sm">
                                  <span className="font-semibold">
                                    {pf.manager_name ||
                                      `Gestor #${pf.manager_id}`}
                                  </span>
                                  <span className="text-base-content/60">
                                    •
                                  </span>
                                  <span className="badge badge-outline badge-sm">
                                    {pf.contact_method}
                                  </span>
                                  <span className="text-base-content/60">
                                    •
                                  </span>
                                  <span className="badge badge-outline badge-sm">
                                    {pf.contact_result}
                                  </span>
                                </div>
                                {pf.observation && (
                                  <div className="text-base-content/70 mt-1 text-xs">
                                    {pf.observation}
                                  </div>
                                )}
                              </div>
                              <div className="text-right">
                                <div className="text-base-content/70 text-xs">
                                  Fecha: {formatDate(pf.management_date)}
                                </div>
                                {pf.payment_promise_date && (
                                  <div className="text-base-content/70 text-xs">
                                    Promesa:{' '}
                                    {formatDate(pf.payment_promise_date)}
                                  </div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
