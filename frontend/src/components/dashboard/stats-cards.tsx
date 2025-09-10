import React from 'react';

import {
  AlertTriangle,
  Briefcase,
  Calendar,
  CreditCard,
  DollarSign,
  UserCheck,
  Users,
} from 'lucide-react';

import { DashboardStats } from '@/types/dashboard';

interface StatsCardsProps {
  stats: DashboardStats;
  loading?: boolean;
}

export default function StatsCards({
  stats,
  loading = false,
}: StatsCardsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 7 }).map((_, index) => (
          <div
            key={index}
            className="card bg-base-100 border-base-200 border shadow-sm"
          >
            <div className="card-body p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="bg-base-300 mb-2 h-4 animate-pulse rounded"></div>
                  <div className="bg-base-300 h-8 animate-pulse rounded"></div>
                </div>
                <div className="bg-base-300 h-12 w-12 animate-pulse rounded-full"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  const cards = [
    {
      title: 'Total Clientes',
      value: stats.totalClients,
      icon: Users,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      borderColor: 'border-primary/20',
    },
    {
      title: 'Créditos Activos',
      value: stats.totalCredits,
      icon: CreditCard,
      color: 'text-success',
      bgColor: 'bg-success/10',
      borderColor: 'border-success/20',
    },
    {
      title: 'Alertas Pendientes',
      value: stats.totalAlerts,
      icon: AlertTriangle,
      color: 'text-warning',
      bgColor: 'bg-warning/10',
      borderColor: 'border-warning/20',
    },
    {
      title: 'Total Cuotas',
      value: stats.totalInstallments,
      icon: Calendar,
      color: 'text-info',
      bgColor: 'bg-info/10',
      borderColor: 'border-info/20',
    },
    {
      title: 'Gestiones de Cartera',
      value: stats.totalPortfolioManagements,
      icon: Briefcase,
      color: 'text-secondary',
      bgColor: 'bg-secondary/10',
      borderColor: 'border-secondary/20',
    },
    {
      title: 'Conciliaciones',
      value: stats.totalReconciliations,
      icon: DollarSign,
      color: 'text-accent',
      bgColor: 'bg-accent/10',
      borderColor: 'border-accent/20',
    },
    {
      title: 'Gestores Activos',
      value: stats.totalManagers,
      icon: UserCheck,
      color: 'text-neutral',
      bgColor: 'bg-neutral/10',
      borderColor: 'border-neutral/20',
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card, index) => {
        const IconComponent = card.icon;
        return (
          <div
            key={index}
            className={`card bg-base-100 border shadow-sm transition-all hover:shadow-md ${card.borderColor}`}
          >
            <div className="card-body p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="text-base-content/70 mb-1 text-sm font-medium">
                    {card.title}
                  </h3>
                  <p className={`text-2xl font-bold ${card.color}`}>
                    {card.value.toLocaleString()}
                  </p>
                </div>
                <div
                  className={`rounded-full p-3 ${card.bgColor} ${card.color}`}
                >
                  <IconComponent className="h-6 w-6" />
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
