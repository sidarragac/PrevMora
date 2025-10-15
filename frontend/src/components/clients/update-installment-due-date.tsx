'use client';

import { useRouter } from 'next/navigation';
import React from 'react';

type UpdateInstallmentDueDateProps = {
  installmentId: string | number;
  currentDueDate?: string; // ISO string (YYYY-MM-DD)
  currentState?: string;
  disabled?: boolean;
};

export default function UpdateInstallmentDueDate({
  installmentId,
  currentDueDate,
  currentState,
  disabled,
}: UpdateInstallmentDueDateProps) {
  const router = useRouter();
  const [open, setOpen] = React.useState(false);
  const [dueDate, setDueDate] = React.useState<string>(
    currentDueDate ? currentDueDate.slice(0, 10) : ''
  );
  const [installmentState, setInstallmentState] = React.useState<string>(
    currentState || 'Pendiente'
  );
  const [submitting, setSubmitting] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch(
        `${baseUrl}/installments/update_installment/${installmentId}`,
        {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            due_date: dueDate,
            installment_state: installmentState,
          }),
        }
      );

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Error actualizando la cuota');
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
      <button
        className="btn btn-ghost btn-xs"
        onClick={() => setOpen(true)}
        disabled={disabled}
      >
        Actualizar
      </button>

      {open && (
        <div className="modal modal-open">
          <div className="modal-box">
            <h3 className="text-lg font-bold">Actualizar cuota</h3>
            <form className="mt-4 space-y-4" onSubmit={onSubmit}>
              <div className="form-control">
                <label className="label">
                  <span className="label-text">Nueva fecha</span>
                </label>
                <input
                  type="date"
                  className="input input-bordered w-full"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                  required
                />
              </div>

              <div className="form-control">
                <label className="label">
                  <span className="label-text">Estado</span>
                </label>
                <select
                  className="select select-bordered w-full"
                  value={installmentState}
                  onChange={(e) => setInstallmentState(e.target.value)}
                  required
                >
                  <option value="Pendiente">Pendiente</option>
                  <option value="Pagada">Pagada</option>
                  <option value="Vencida">Vencida</option>
                </select>
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
