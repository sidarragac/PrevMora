import React from 'react';

import { CreditCard, TrendingDown, TrendingUp } from 'lucide-react';

export default function Loading() {
  return (
    <div className="animate-pulse space-y-6">
      {/* Header */}
      <div className="mb-6 flex items-center gap-4">
        <div className="bg-base-300 h-9 w-24 rounded"></div>
        <div className="divider divider-horizontal"></div>
        <div className="bg-base-300 h-8 w-48 rounded"></div>
      </div>

      {/* Summary Stats */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="stat bg-base-200 rounded-lg p-4">
              <div className="stat-figure text-success">
                <TrendingUp className="h-8 w-8" />
              </div>
              <div className="stat-title">
                <div className="bg-base-300 h-4 w-24 rounded"></div>
              </div>
              <div className="stat-value">
                <div className="bg-base-300 h-8 w-32 rounded"></div>
              </div>
            </div>
            <div className="stat bg-base-200 rounded-lg p-4">
              <div className="stat-figure text-error">
                <TrendingDown className="h-8 w-8" />
              </div>
              <div className="stat-title">
                <div className="bg-base-300 h-4 w-24 rounded"></div>
              </div>
              <div className="stat-value">
                <div className="bg-base-300 h-8 w-32 rounded"></div>
              </div>
            </div>
            <div className="stat bg-base-200 rounded-lg p-4">
              <div className="stat-figure text-primary">
                <CreditCard className="h-8 w-8" />
              </div>
              <div className="stat-title">
                <div className="bg-base-300 h-4 w-24 rounded"></div>
              </div>
              <div className="stat-value">
                <div className="bg-base-300 h-8 w-32 rounded"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Loading Credits */}
      {[1, 2].map((i) => (
        <div
          key={i}
          className="card bg-base-100 border-base-200 border shadow-lg"
        >
          <div className="card-header bg-base-200 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="bg-base-300 h-5 w-5 rounded"></div>
                <div className="space-y-2">
                  <div className="bg-base-300 h-6 w-32 rounded"></div>
                  <div className="bg-base-300 h-4 w-40 rounded"></div>
                </div>
              </div>
              <div className="bg-base-300 h-6 w-24 rounded"></div>
            </div>
          </div>

          <div className="card-body space-y-6 p-6">
            {/* Credit Summary */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
              {[1, 2, 3, 4].map((j) => (
                <div key={j} className="space-y-2">
                  <div className="bg-base-300 h-4 w-32 rounded"></div>
                  <div className="bg-base-300 h-6 w-24 rounded"></div>
                </div>
              ))}
            </div>

            {/* Credit Totals */}
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {[1, 2].map((j) => (
                <div key={j} className="bg-base-200 h-20 rounded-lg"></div>
              ))}
            </div>

            {/* Installments */}
            <div className="space-y-4">
              <div className="bg-base-300 h-6 w-32 rounded"></div>
              {[1, 2, 3].map((j) => (
                <div key={j} className="space-y-2">
                  <div className="bg-base-50 h-20 rounded border"></div>
                  <div className="bg-base-50 h-24 rounded border"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
