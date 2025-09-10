import Link from 'next/link';
import React from 'react';

import { Eye, FileText, Mail, MapPin, Phone } from 'lucide-react';

import { Client } from '@/types/client';

interface ClientCardProps {
  client: Client;
}

export default function ClientCard({ client }: ClientCardProps) {
  return (
    <div className="card bg-base-100 border-base-200 border shadow-md transition-shadow hover:shadow-lg">
      <div className="card-body p-6">
        <div className="mb-4 flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-primary text-primary-content flex size-12 items-center justify-center rounded-full">
              <span className="text-lg font-semibold">
                {client.name
                  .split(' ')
                  .map((n) => n[0])
                  .join('')
                  .toUpperCase()
                  .slice(0, 2)}
              </span>
            </div>
            <div>
              <h3 className="card-title text-base-content text-lg font-semibold">
                {client.name}
              </h3>
              <p className="text-base-content/70 text-sm">ID: {client.id}</p>
            </div>
          </div>
          <div className="badge badge-success badge-outline">
            {client.status}
          </div>
        </div>

        <div className="mb-4 space-y-3">
          <div className="flex items-center gap-2 text-sm">
            <FileText className="text-primary h-4 w-4" />
            <span className="text-base-content/80 font-mono">
              {client.document}
            </span>
          </div>

          <div className="flex items-center gap-2 text-sm">
            <Mail className="text-primary h-4 w-4" />
            <span className="text-base-content/80">{client.email}</span>
          </div>

          <div className="flex items-center gap-2 text-sm">
            <Phone className="text-primary h-4 w-4" />
            <span className="text-base-content/80">{client.phone}</span>
          </div>

          <div className="flex items-start gap-2 text-sm">
            <MapPin className="text-primary mt-0.5 h-4 w-4" />
            <div>
              <div className="text-base-content/80">{client.address}</div>
              <div className="text-base-content/60 text-xs">{client.zone}</div>
            </div>
          </div>
        </div>

        <div className="card-actions justify-end">
          <Link
            href={`/plataforma/cartera/cliente/${client.id}`}
            className="btn btn-primary btn-sm gap-2"
          >
            <Eye className="h-4 w-4" />
            Ver detalles
          </Link>
        </div>
      </div>
    </div>
  );
}
