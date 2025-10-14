'use client';

import { useRouter } from 'next/navigation';
import React from 'react';

export default function NewClientButton() {
  const router = useRouter();
  const [open, setOpen] = React.useState(false);
  const [submitting, setSubmitting] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const [name, setName] = React.useState('');
  const [documentId, setDocumentId] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [phone, setPhone] = React.useState('');
  const [address, setAddress] = React.useState('');
  const [zone, setZone] = React.useState('');
  const [status, setStatus] = React.useState('');

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const body = {
        name,
        document: documentId,
        email,
        phone,
        address,
        zone,
        status,
      };

      const res = await fetch(`${baseUrl}/clients/create_client`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Error creando el cliente');
      }

      setOpen(false);
      // Limpia el formulario después de crear
      setName('');
      setDocumentId('');
      setEmail('');
      setPhone('');
      setAddress('');
      setZone('');
      setStatus('');
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
        Nuevo cliente
      </button>

      {open && (
        <div className="modal modal-open">
          <div className="modal-box max-w-xl">
            <h3 className="text-lg font-bold">Crear nuevo cliente</h3>
            <form
              className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2"
              onSubmit={onSubmit}
            >
              <div className="form-control md:col-span-2">
                <label className="label">
                  <span className="label-text">Nombre</span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Documento</span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full"
                  value={documentId}
                  onChange={(e) => setDocumentId(e.target.value)}
                  required
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Email</span>
                </label>
                <input
                  type="email"
                  className="input input-bordered w-full"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
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
                <div className="md:col-span-2">
                  <div className="alert alert-error text-sm">
                    <span>{error}</span>
                  </div>
                </div>
              )}

              <div className="modal-action md:col-span-2">
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
                  {submitting ? 'Creando...' : 'Crear'}
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
