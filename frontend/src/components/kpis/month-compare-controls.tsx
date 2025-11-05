'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import React from 'react';

const MONTHS = [
  'Enero',
  'Febrero',
  'Marzo',
  'Abril',
  'Mayo',
  'Junio',
  'Julio',
  'Agosto',
  'Septiembre',
  'Octubre',
  'Noviembre',
  'Diciembre',
] as const;

export default function MonthCompareControls({
  defaultRef,
  defaultCmp,
}: {
  defaultRef?: string;
  defaultCmp?: string;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();

  const [refMonth, setRefMonth] = React.useState<string>(
    params.get('month_ref') || defaultRef || 'Enero'
  );
  const [cmpMonth, setCmpMonth] = React.useState<string>(
    params.get('month_cmp') || defaultCmp || 'Febrero'
  );

  const applyQuery = (refVal: string, cmpVal: string) => {
    const sp = new URLSearchParams(params.toString());
    sp.set('month_ref', refVal);
    sp.set('month_cmp', cmpVal);
    router.replace(`${pathname}?${sp.toString()}`);
  };

  return (
    <div className="bg-base-100 border-base-200 flex flex-wrap items-end gap-3 rounded border p-3">
      <div className="form-control w-48">
        <label className="label">
          <span className="label-text">Mes referencia</span>
        </label>
        <select
          className="select select-bordered"
          value={refMonth}
          onChange={(e) => {
            const v = e.target.value;
            setRefMonth(v);
            applyQuery(v, cmpMonth);
          }}
        >
          {MONTHS.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </div>

      <div className="form-control w-48">
        <label className="label">
          <span className="label-text">Mes comparación</span>
        </label>
        <select
          className="select select-bordered"
          value={cmpMonth}
          onChange={(e) => {
            const v = e.target.value;
            setCmpMonth(v);
            applyQuery(refMonth, v);
          }}
        >
          {MONTHS.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
