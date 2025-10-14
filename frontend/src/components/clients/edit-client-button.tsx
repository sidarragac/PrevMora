'use client';

import { useRouter } from 'next/navigation';
import React from 'react';

type EditClientButtonProps = {
  clientId: string | number;
  initialEmail: string;
  initialPhone: string;
  initialAddress: string;
  initialZone: string;
  initialStatus: string;
};

export default function EditClientButton({
  clientId,
  initialEmail,
  initialPhone,
  initialAddress,
  initialZone,
  initialStatus,
}: EditClientButtonProps) {
  const router = useRouter();
  const [open, setOpen] = React.useState(false);
  const [email, setEmail] = React.useState(initialEmail || '');
  const [phone, setPhone] = React.useState(initialPhone || '');
  const [address, setAddress] = React.useState(initialAddress || '');
  const [zone, setZone] = React.useState(initialZone || '');
  const [status, setStatus] = React.useState(initialStatus || '');
  const [submitting, setSubmitting] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    const body = { email, phone, address, zone, status };

    try {
      const res = await fetch(`${baseUrl}/clients/update_client/${clientId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Error actualizando el cliente');
      }

      setOpen(false);
      router.refresh();
    } catch (err: any) {
      setError(err.message || 'Error desconocido');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <button className="btn btn-primary btn-sm" onClick={() => setOpen(true)}>
        Editar
      </button>

      {open && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="text-lg font-bold">Editar cliente</h3>

            <form className="mt-4 space-y-4" onSubmit={onSubmit}>
              <div className="form-control">
                <label className="label">
                  <span className="label-text">Email</span>
                </label>
                <input
                  type="email"
                  className="input input-bordered w-full"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Teléfono</span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Dirección</span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full"
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Zona</span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full"
                  value={zone}
                  onChange={(e) => setZone(e.target.value)}
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Estado</span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full"
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                />
              </div>

              {error && (
                <div className="alert alert-error text-sm">
                  <span>{error}</span>
                </div>
              )}

              <div className="modal-action">
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={() => setOpen(false)}
                  disabled={submitting}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
          <div className="modal-backdrop" onClick={() => setOpen(false)}></div>
        </div>
      )}
    </div>
  );
}
