import React from 'react';

export default function Loading() {
  return (
    <div className="space-y-6">
      {/* Header Skeleton */}
      <div className="flex items-center gap-4">
        <div className="skeleton h-14 w-14 shrink-0 rounded-full"></div>
        <div className="flex flex-col gap-2">
          <div className="skeleton h-8 w-56"></div>
          <div className="skeleton h-4 w-72"></div>
        </div>
      </div>

      {/* Upload Component Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-8">
          <div className="skeleton h-40 w-full"></div>
          <div className="mt-4 flex items-center justify-between">
            <div className="skeleton h-4 w-40"></div>
            <div className="skeleton h-10 w-32 rounded"></div>
          </div>
        </div>
      </div>

      {/* Information Cards Skeleton */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <div className="card border-success/20 bg-success/5 border">
          <div className="card-body p-6">
            <div className="mb-4 flex items-center gap-3">
              <div className="skeleton h-6 w-6 rounded"></div>
              <div className="skeleton h-6 w-40"></div>
            </div>
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="skeleton h-3 w-3/4"></div>
              ))}
            </div>
          </div>
        </div>

        <div className="card border-warning/20 bg-warning/5 border">
          <div className="card-body p-6">
            <div className="mb-4 flex items-center gap-3">
              <div className="skeleton h-6 w-6 rounded"></div>
              <div className="skeleton h-6 w-40"></div>
            </div>
            <div className="space-y-2">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="skeleton h-3 w-2/3"></div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Help Section Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <div className="flex items-center gap-2">
            <div className="skeleton h-5 w-5"></div>
            <div className="skeleton h-6 w-36"></div>
          </div>
        </div>
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <div className="skeleton mb-3 h-4 w-40"></div>
              <div className="space-y-2">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="skeleton h-3 w-4/5"></div>
                ))}
              </div>
            </div>
            <div>
              <div className="skeleton mb-3 h-4 w-48"></div>
              <div className="space-y-2">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="skeleton h-3 w-3/4"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
