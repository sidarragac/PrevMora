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
    const paginationParams = { page: 1, page_size: 10 };

    // Fetch all data in parallel
    const [
      clientsResponse,
      creditsResponse,
      alertsResponse,
      installmentsResponse,
      portfolioResponse,
      reconciliationsResponse,
      managersResponse,
    ] = await Promise.all([
      fetch(`${baseUrl}/clients/get_clients`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
      fetch(`${baseUrl}/credits/get_credits`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
      fetch(`${baseUrl}/alerts/get_alerts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
      fetch(`${baseUrl}/installments/get_installments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
      fetch(`${baseUrl}/portfolios/get_portfolios`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
      fetch(`${baseUrl}/reconciliations/get_reconciliations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
      fetch(`${baseUrl}/managers/get_managers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(paginationParams),
        cache: 'no-store',
      }),
    ]);

    // Check if all requests were successful
    if (
      !clientsResponse.ok ||
      !creditsResponse.ok ||
      !alertsResponse.ok ||
      !installmentsResponse.ok ||
      !portfolioResponse.ok ||
      !reconciliationsResponse.ok ||
      !managersResponse.ok
    ) {
      throw new Error('One or more API requests failed');
    }

    // Parse all responses
    const [
      clientsData,
      creditsData,
      alertsData,
      installmentsData,
      portfolioData,
      reconciliationsData,
      managersData,
    ] = await Promise.all([
      clientsResponse.json(),
      creditsResponse.json(),
      alertsResponse.json(),
      installmentsResponse.json(),
      portfolioResponse.json(),
      reconciliationsResponse.json(),
      managersResponse.json(),
    ]);

    // Build stats object
    const stats: DashboardStats = {
      totalClients: clientsData.total || 0,
      totalCredits: creditsData.total || 0,
      totalAlerts: alertsData.total || 0,
      totalInstallments: installmentsData.total || 0,
      totalPortfolioManagements: portfolioData.total || 0,
      totalReconciliations: reconciliationsData.total || 0,
      totalManagers: managersData.total || 0,
    };

    return {
      stats,
      recentAlerts: alertsData.items || [],
      recentInstallments: installmentsData.items || [],
      recentPortfolioManagements: portfolioData.items || [],
      recentReconciliations: reconciliationsData.items || [],
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
