import Link from 'next/link';
import React from 'react';

import { AlertCircle, BarChart3, TrendingUp } from 'lucide-react';

import RecentActivity from '@/components/dashboard/recent-activity';
import RecentAlerts from '@/components/dashboard/recent-alerts';
import StatsCards from '@/components/dashboard/stats-cards';

import { DashboardData, DashboardStats } from '@/types/dashboard';

export const dynamic = 'force-dynamic';
async function fetchDashboardData(): Promise<DashboardData | null> {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;
    const res = await fetch(`${baseUrl}/dashboard/get_dashboard_data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        page: 1,
        page_size: 50,
      }),
      cache: 'no-store',
    });

    if (!res.ok) {
      throw new Error('Failed to fetch dashboard');
    }

    const data = await res.json();

    const stats: DashboardStats = {
      totalClients: data.stats?.total_clients ?? 0,
      totalCredits: data.stats?.total_credits ?? 0,
      totalAlerts: data.stats?.total_alerts ?? 0,
      totalInstallments: data.stats?.total_installments ?? 0,
      totalPortfolioManagements: data.stats?.total_portfolio_managements ?? 0,
      totalReconciliations: data.stats?.total_reconciliations ?? 0,
      totalManagers: data.stats?.total_managers ?? 0,
    };

    return {
      stats,
      recentAlerts: data.recent_alerts ?? [],
      recentInstallments: data.recent_installments ?? [],
      recentPortfolioManagements: data.recent_portfolio_managements ?? [],
      recentReconciliations: data.recent_reconciliations ?? [],
    };
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    return null;
  }
}

export default async function DashboardPage() {
  const dashboardData = await fetchDashboardData();

  if (!dashboardData) {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center gap-4">
          <div className="bg-primary/10 rounded-full p-3">
            <BarChart3 className="text-primary h-8 w-8" />
          </div>
          <div>
            <h1 className="text-base-content text-3xl font-bold">Dashboard</h1>
            <p className="text-base-content/70">Panel de control de PrevMora</p>
          </div>
        </div>

        {/* Error State */}
        <div className="card bg-base-100 border-base-200 border shadow-sm">
          <div className="card-body p-12 text-center">
            <div className="text-base-300 mb-4 text-6xl">⚠️</div>
            <h3 className="text-base-content mb-2 text-xl font-semibold">
              Error al cargar el dashboard
            </h3>
            <p className="text-base-content/70 mb-6">
              No se pudo conectar con el servidor. Verifica que el backend esté
              ejecutándose.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="btn btn-primary"
            >
              Reintentar
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="bg-primary/10 rounded-full p-3">
          <BarChart3 className="text-primary h-8 w-8" />
        </div>
        <div>
          <h1 className="text-base-content text-3xl font-bold">Dashboard</h1>
          <p className="text-base-content/70">Panel de control de PrevMora</p>
        </div>
      </div>

      {/* Stats Cards */}
      <StatsCards stats={dashboardData.stats} />

      {/* Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Alerts */}
        <RecentAlerts alerts={dashboardData.recentAlerts} />

        {/* Recent Activity */}
        <RecentActivity
          installments={dashboardData.recentInstallments}
          portfolioManagements={dashboardData.recentPortfolioManagements}
          reconciliations={dashboardData.recentReconciliations}
        />
      </div>

      {/* Quick Actions */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <h3 className="card-title flex items-center gap-2 text-lg font-semibold">
            <TrendingUp className="text-primary h-5 w-5" />
            Acciones Rápidas
          </h3>
        </div>
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <Link href="/plataforma/cartera" className="btn btn-primary gap-2">
              <BarChart3 className="h-4 w-4" />
              Ver Cartera
            </Link>
            <button className="btn btn-warning btn-outline gap-2">
              <AlertCircle className="h-4 w-4" />
              Gestionar Alertas
            </button>
            <button className="btn btn-success btn-outline gap-2">
              <TrendingUp className="h-4 w-4" />
              Nuevo Crédito
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
