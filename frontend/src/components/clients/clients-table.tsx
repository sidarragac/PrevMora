import Link from 'next/link';
import React from 'react';

import { Eye, Mail, MapPin, Phone } from 'lucide-react';

import { Client } from '@/types/client';

interface ClientsTableProps {
  clients: Client[];
  loading?: boolean;
}

export default function ClientsTable({
  clients,
  loading = false,
}: ClientsTableProps) {
  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="loading loading-spinner loading-lg text-primary"></div>
      </div>
    );
  }

  if (!clients || clients.length === 0) {
    return (
      <div className="py-12 text-center">
        <div className="text-base-300 mb-4 text-6xl">👥</div>
        <h3 className="text-base-content mb-2 text-xl font-semibold">
          No hay clientes
        </h3>
        <p className="text-base-content/70">
          No se encontraron clientes en la base de datos.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="table-zebra table w-full">
        <thead>
          <tr className="bg-base-200">
            <th className="text-base-content font-semibold">Cliente</th>
            <th className="text-base-content font-semibold">Documento</th>
            <th className="text-base-content font-semibold">Contacto</th>
            <th className="text-base-content font-semibold">Ubicación</th>
            <th className="text-base-content font-semibold">Estado</th>
            <th className="text-base-content font-semibold">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((client) => (
            <tr key={client.id} className="hover:bg-base-100 transition-colors">
              <td>
                <div className="flex items-center gap-3">
                  <div className="bg-primary text-primary-content flex size-10 items-center justify-center rounded-full">
                    <span className="text-sm font-semibold">
                      {client.name
                        .split(' ')
                        .map((n) => n[0])
                        .join('')
                        .toUpperCase()
                        .slice(0, 2)}
                    </span>
                  </div>
                  <div>
                    <div className="text-base-content font-semibold">
                      {client.name}
                    </div>
                    <div className="text-base-content/70 text-sm">
                      ID: {client.id}
                    </div>
                  </div>
                </div>
              </td>
              <td>
                <div className="font-mono text-sm">{client.document}</div>
              </td>
              <td>
                <div className="space-y-1">
                  <div className="flex items-center gap-2 text-sm">
                    <Mail className="text-primary h-4 w-4" />
                    <span className="text-base-content/80">{client.email}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Phone className="text-primary h-4 w-4" />
                    <span className="text-base-content/80">{client.phone}</span>
                  </div>
                </div>
              </td>
              <td>
                <div className="flex items-center gap-2 text-sm">
                  <MapPin className="text-primary h-4 w-4" />
                  <div>
                    <div className="text-base-content/80">{client.address}</div>
                    <div className="text-base-content/60 text-xs">
                      {client.zone}
                    </div>
                  </div>
                </div>
              </td>
              <td>
                <div className="badge badge-success badge-outline">
                  {client.status}
                </div>
              </td>
              <td>
                <Link
                  href={`/plataforma/cartera/cliente/${client.id}`}
                  className="btn btn-primary btn-sm gap-2"
                >
                  <Eye className="h-4 w-4" />
                  Ver detalles
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
