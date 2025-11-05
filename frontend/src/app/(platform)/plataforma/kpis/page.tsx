import React from 'react';

import { BarChart3, TrendingDown, TrendingUp } from 'lucide-react';

import MonthCompareControls from '@/components/kpis/month-compare-controls';

export const dynamic = 'force-dynamic';

type OverdueResponse = {
  installments: Record<string, [number, number, string]>; // { Mes: [monto, cantidad, porcentaje] }
  comparison: {
    reference_month: string;
    compare_month: string;
    ref_count: number;
    cmp_count: number;
    delta_abs: number;
    direction: 'mayor' | 'menor' | 'igual' | string;
    delta_percent: string;
  };
};

async function fetchOverdue(searchParams?: {
  month_ref?: string;
  month_cmp?: string;
}): Promise<OverdueResponse | null> {
  try {
    const base =
      process.env.NEXT_PUBLIC_STATS_BASE_URL ||
      'http://localhost:8002/api/stats/v1';
    const url = new URL(`${base}/overdue-installments`);
    if (searchParams?.month_ref)
      url.searchParams.set('month_ref', searchParams.month_ref);
    if (searchParams?.month_cmp)
      url.searchParams.set('month_cmp', searchParams.month_cmp);
    const res = await fetch(url.toString(), {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) throw new Error('Failed to fetch overdue installments');
    return await res.json();
  } catch (e) {
    console.error('Error fetching KPIs:', e);
    return null;
  }
}

function formatCurrency(amount: number) {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
  }).format(amount || 0);
}

interface KpisPageProps {
  searchParams?: Promise<{ month_ref?: string; month_cmp?: string }>;
}

export default async function KpisPage({ searchParams }: KpisPageProps) {
  const resolvedSearchParams = await searchParams;
  const data = await fetchOverdue(resolvedSearchParams);

  if (!data) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="bg-primary/10 rounded-full p-3">
            <BarChart3 className="text-primary h-8 w-8" />
          </div>
          <div>
            <h1 className="text-base-content text-3xl font-bold">KPIs</h1>
            <p className="text-base-content/70">Indicadores de mora</p>
          </div>
        </div>

        <div className="card bg-base-100 border-base-200 border shadow-sm">
          <div className="card-body p-12 text-center">
            <div className="text-base-300 mb-4 text-6xl">⚠️</div>
            <h3 className="text-base-content mb-2 text-xl font-semibold">
              No se pudo cargar la información
            </h3>
            <p className="text-base-content/70 mb-6">
              Verifica que el servicio de estadísticas esté disponible.
            </p>
            <button
              className="btn btn-primary"
              onClick={() => globalThis.location?.reload?.()}
            >
              Reintentar
            </button>
          </div>
        </div>
      </div>
    );
  }

  const months = Object.keys(data.installments);
  const rows = months.map((m) => {
    const [amount, count, pct] = data.installments[m];
    return { month: m, amount, count, pct };
  });

  const isUp = data.comparison.direction === 'mayor';
  const isDown = data.comparison.direction === 'menor';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="bg-primary/10 rounded-full p-3">
          <BarChart3 className="text-primary h-8 w-8" />
        </div>
        <div>
          <h1 className="text-base-content text-3xl font-bold">KPIs</h1>
          <p className="text-base-content/70">Indicadores de cuotas en mora</p>
        </div>
      </div>

      {/* Comparison Summary */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-body p-6">
          <MonthCompareControls
            defaultRef={data.comparison.reference_month}
            defaultCmp={data.comparison.compare_month}
          />
          <div className="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
            <div className="flex items-center gap-3">
              {isUp && <TrendingUp className="text-error h-6 w-6" />}
              {isDown && <TrendingDown className="text-success h-6 w-6" />}
              {!isUp && !isDown && (
                <TrendingUp className="text-base-content/50 h-6 w-6 rotate-90" />
              )}
              <div>
                <div className="text-base-content text-lg font-semibold">
                  Comparación: {data.comparison.reference_month} vs{' '}
                  {data.comparison.compare_month}
                </div>
                <div className="text-base-content/70 text-sm">
                  Cantidades: {data.comparison.ref_count} →{' '}
                  {data.comparison.cmp_count} | Cambio:{' '}
                  {data.comparison.delta_abs} ({data.comparison.delta_percent})
                  — Dirección: {data.comparison.direction}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Table by Month */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title text-lg font-semibold">
            Cuotas en mora por mes
          </h3>
        </div>
        <div className="card-body p-0">
          <div className="overflow-x-auto">
            <table className="table-zebra table">
              <thead>
                <tr>
                  <th>Mes</th>
                  <th>Monto</th>
                  <th>Cantidad</th>
                  <th>Variación</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.month}>
                    <td className="font-medium">{r.month}</td>
                    <td>{formatCurrency(r.amount)}</td>
                    <td>
                      <div className="badge badge-outline">{r.count}</div>
                    </td>
                    <td>
                      <div
                        className={`badge ${
                          (r.pct || '').startsWith('-')
                            ? 'badge-success'
                            : (r.pct || '').startsWith('0')
                              ? 'badge-neutral'
                              : 'badge-error'
                        }`}
                      >
                        {r.pct}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
