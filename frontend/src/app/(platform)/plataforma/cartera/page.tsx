import React from 'react';

import { Filter, Search, Users } from 'lucide-react';

import ViewToggle from '@/components/clients/view-toggle';

import { ClientsResponse } from '@/types/client';

export const dynamic = 'force-dynamic';
async function getClients(): Promise<ClientsResponse | null> {
  try {
    const response = await fetch(
      'http://localhost:8000/api/PrevMora-Template/v1/clients/get_clients',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          page: 1,
          page_size: 50,
        }),
        cache: 'no-store', // Para desarrollo, en producción usar revalidate
      }
    );

    if (!response.ok) {
      throw new Error('Failed to fetch clients');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching clients:', error);
    return null;
  }
}

export default async function CarteraPage() {
  const clientsData = await getClients();
  const clients = clientsData?.items || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-base-content flex items-center gap-3 text-3xl font-bold">
            <Users className="text-primary h-8 w-8" />
            Cartera de Clientes
          </h1>
          <p className="text-base-content/70 mt-1">
            Gestiona y visualiza la información de tus clientes
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="stats shadow-sm">
            <div className="stat px-4 py-2">
              <div className="stat-title text-xs">Total Clientes</div>
              <div className="stat-value text-primary text-lg">
                {clientsData?.total || 0}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-body p-4">
          <div className="flex flex-col gap-4 sm:flex-row">
            <div className="flex-1">
              <div className="relative">
                <Search className="text-base-content/50 absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 transform" />
                <input
                  type="text"
                  placeholder="Buscar clientes por nombre, documento o email..."
                  className="input input-bordered w-full pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <button className="btn btn-outline btn-sm gap-2">
                <Filter className="h-4 w-4" />
                Filtros
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Clients Content */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-6">
          {clientsData ? (
            <ViewToggle clients={clients} />
          ) : (
            <div className="py-12 text-center">
              <div className="text-base-300 mb-4 text-6xl">⚠️</div>
              <h3 className="text-base-content mb-2 text-xl font-semibold">
                Error al cargar clientes
              </h3>
              <p className="text-base-content/70">
                No se pudo conectar con el servidor. Verifica que el backend
                esté ejecutándose.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
