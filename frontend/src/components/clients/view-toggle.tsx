'use client';

import React, { useState } from 'react';

import { Grid, List } from 'lucide-react';

import { Client } from '@/types/client';

import ClientCard from './client-card';
import ClientsTable from './clients-table';

interface ViewToggleProps {
  clients: Client[];
  loading?: boolean;
}

type ViewMode = 'list' | 'grid';

export default function ViewToggle({
  clients,
  loading = false,
}: ViewToggleProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('list');

  return (
    <div className="space-y-4">
      {/* View Toggle Controls */}
      <div className="flex items-center justify-between">
        <div className="text-base-content/70 text-sm">
          Mostrando {clients.length} clientes
        </div>
        <div className="btn-group flex items-center gap-2">
          <button
            onClick={() => setViewMode('list')}
            className={`btn btn-sm gap-2 ${
              viewMode === 'list' ? 'btn-active' : 'btn-outline'
            }`}
          >
            <List className="h-4 w-4" />
            Lista
          </button>
          <button
            onClick={() => setViewMode('grid')}
            className={`btn btn-sm gap-2 ${
              viewMode === 'grid' ? 'btn-active' : 'btn-outline'
            }`}
          >
            <Grid className="h-4 w-4" />
            Cuadrícula
          </button>
        </div>
      </div>

      {/* Content based on view mode */}
      {viewMode === 'list' ? (
        <ClientsTable clients={clients} loading={loading} />
      ) : (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {loading ? (
            Array.from({ length: 6 }).map((_, index) => (
              <div
                key={index}
                className="card bg-base-100 border-base-200 animate-pulse border shadow-md"
              >
                <div className="card-body p-6">
                  <div className="mb-4 flex items-center gap-3">
                    <div className="bg-base-300 h-12 w-12 rounded-full"></div>
                    <div className="flex-1">
                      <div className="bg-base-300 mb-2 h-4 rounded"></div>
                      <div className="bg-base-300 h-3 w-2/3 rounded"></div>
                    </div>
                  </div>
                  <div className="mb-4 space-y-2">
                    <div className="bg-base-300 h-3 rounded"></div>
                    <div className="bg-base-300 h-3 rounded"></div>
                    <div className="bg-base-300 h-3 w-3/4 rounded"></div>
                  </div>
                  <div className="bg-base-300 h-8 rounded"></div>
                </div>
              </div>
            ))
          ) : clients.length === 0 ? (
            <div className="col-span-full py-12 text-center">
              <div className="text-base-300 mb-4 text-6xl">👥</div>
              <h3 className="text-base-content mb-2 text-xl font-semibold">
                No hay clientes
              </h3>
              <p className="text-base-content/70">
                No se encontraron clientes en la base de datos.
              </p>
            </div>
          ) : (
            clients.map((client) => (
              <ClientCard key={client.id} client={client} />
            ))
          )}
        </div>
      )}
    </div>
  );
}
