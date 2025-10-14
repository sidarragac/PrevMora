import React from 'react';

export default function Loading() {
  return (
    <div className="space-y-6">
      {/* Header Skeleton */}
      <div className="mb-6 flex items-center gap-4">
        <div className="skeleton h-8 w-24 rounded"></div>
        <div className="divider divider-horizontal"></div>
        <div className="skeleton h-8 w-40"></div>
      </div>

      {/* Client Info Card Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-6">
          <div className="mb-6 flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="skeleton size-16 rounded-full"></div>
              <div>
                <div className="skeleton h-6 w-48"></div>
                <div className="skeleton mt-2 h-4 w-24"></div>
                <div className="skeleton mt-2 h-6 w-28"></div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm">
                <div className="skeleton h-4 w-4 rounded"></div>
                <div className="skeleton h-4 w-24"></div>
                <div className="skeleton h-4 w-20"></div>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="skeleton h-4 w-4 rounded"></div>
                <div className="skeleton h-4 w-24"></div>
                <div className="skeleton h-4 w-28"></div>
              </div>
              <div className="flex items-center gap-2 text-sm">
                <div className="skeleton h-4 w-4 rounded"></div>
                <div className="skeleton h-4 w-24"></div>
                <div className="skeleton h-4 w-24"></div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-start gap-2 text-sm">
                <div className="skeleton h-4 w-4 rounded"></div>
                <div className="space-y-2">
                  <div className="skeleton h-4 w-24"></div>
                  <div className="skeleton h-4 w-40"></div>
                  <div className="skeleton h-3 w-20"></div>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <div className="stats stats-vertical shadow-sm">
                <div className="stat py-2">
                  <div className="skeleton h-3 w-24"></div>
                  <div className="skeleton mt-2 h-6 w-10"></div>
                </div>
                <div className="stat py-2">
                  <div className="skeleton h-3 w-24"></div>
                  <div className="skeleton mt-2 h-6 w-10"></div>
                </div>
                <div className="stat py-2">
                  <div className="skeleton h-3 w-24"></div>
                  <div className="skeleton mt-2 h-6 w-10"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Credits Section Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-header bg-base-200 p-4">
          <div className="flex items-center gap-2">
            <div className="skeleton h-5 w-5"></div>
            <div className="skeleton h-6 w-48"></div>
          </div>
        </div>
        <div className="card-body p-6">
          <div className="space-y-4">
            {[...Array(2)].map((_, i) => (
              <div key={i} className="card border-base-200 border">
                <div className="card-body p-4">
                  <div className="mb-4 flex items-start justify-between">
                    <div>
                      <div className="skeleton h-4 w-32"></div>
                      <div className="skeleton mt-2 h-3 w-40"></div>
                    </div>
                    <div className="skeleton h-6 w-20 rounded"></div>
                  </div>

                  <div className="mb-4 grid grid-cols-1 gap-4 md:grid-cols-3">
                    <div>
                      <div className="skeleton h-3 w-28"></div>
                      <div className="skeleton mt-2 h-5 w-24"></div>
                    </div>
                    <div>
                      <div className="skeleton h-3 w-24"></div>
                      <div className="skeleton mt-2 h-5 w-16"></div>
                    </div>
                    <div>
                      <div className="skeleton h-3 w-24"></div>
                      <div className="skeleton mt-2 h-5 w-12"></div>
                    </div>
                  </div>

                  <div>
                    <div className="skeleton mb-2 h-3 w-16"></div>
                    <div className="space-y-2">
                      {[...Array(3)].map((_, j) => (
                        <div
                          key={j}
                          className="flex items-center justify-between rounded p-2"
                        >
                          <div className="flex items-center gap-2">
                            <div className="skeleton h-4 w-12"></div>
                            <div className="skeleton h-4 w-20"></div>
                          </div>
                          <div className="text-right">
                            <div className="skeleton h-4 w-24"></div>
                            <div className="skeleton mt-1 h-3 w-28"></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Alerts Section Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-header bg-base-200 p-4">
          <div className="flex items-center gap-2">
            <div className="skeleton h-5 w-5"></div>
            <div className="skeleton h-6 w-40"></div>
          </div>
        </div>
        <div className="card-body p-6">
          <div className="space-y-3">
            {[...Array(2)].map((_, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded border p-3"
              >
                <div>
                  <div className="skeleton h-4 w-32"></div>
                  <div className="skeleton mt-1 h-3 w-40"></div>
                </div>
                <div className="skeleton h-6 w-24 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Reconciliations Section Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-header bg-base-200 p-4">
          <div className="flex items-center gap-2">
            <div className="skeleton h-5 w-5"></div>
            <div className="skeleton h-6 w-48"></div>
          </div>
        </div>
        <div className="card-body p-6">
          <div className="space-y-3">
            {[...Array(2)].map((_, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded border p-3"
              >
                <div>
                  <div className="skeleton h-5 w-24"></div>
                  <div className="skeleton mt-1 h-3 w-40"></div>
                </div>
                <div className="skeleton h-6 w-24 rounded"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
