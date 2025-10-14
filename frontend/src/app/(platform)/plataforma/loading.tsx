import React from 'react';

export default function Loading() {
  return (
    <div className="space-y-6">
      {/* Header Skeleton */}
      <div className="flex items-center gap-4">
        <div className="skeleton h-14 w-14 shrink-0 rounded-full"></div>
        <div className="flex flex-col gap-2">
          <div className="skeleton h-8 w-40"></div>
          <div className="skeleton h-5 w-56"></div>
        </div>
      </div>

      {/* Stats Cards Skeleton */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div
            key={i}
            className="card bg-base-100 border-base-200 border shadow-sm"
          >
            <div className="card-body p-6">
              <div className="flex items-center justify-between">
                <div className="flex flex-col gap-2">
                  <div className="skeleton h-4 w-24"></div>
                  <div className="skeleton h-8 w-16"></div>
                </div>
                <div className="skeleton h-12 w-12 shrink-0 rounded-lg"></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Content Grid Skeleton */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Alerts Skeleton */}
        <div className="card bg-base-100 border-base-200 border shadow-sm">
          <div className="card-header bg-base-200 p-4">
            <div className="flex items-center gap-2">
              <div className="skeleton h-5 w-5 shrink-0 rounded"></div>
              <div className="skeleton h-6 w-32"></div>
            </div>
          </div>
          <div className="card-body p-6">
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div
                  key={i}
                  className="border-base-200 flex items-start gap-3 rounded-lg border p-4"
                >
                  <div className="skeleton h-10 w-10 shrink-0 rounded-full"></div>
                  <div className="flex-1 space-y-2">
                    <div className="skeleton h-4 w-3/4"></div>
                    <div className="skeleton h-3 w-1/2"></div>
                    <div className="skeleton h-3 w-1/4"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Activity Skeleton */}
        <div className="card bg-base-100 border-base-200 border shadow-sm">
          <div className="card-header bg-base-200 p-4">
            <div className="flex items-center gap-2">
              <div className="skeleton h-5 w-5 shrink-0 rounded"></div>
              <div className="skeleton h-6 w-40"></div>
            </div>
          </div>
          <div className="card-body p-6">
            <div className="space-y-4">
              {[...Array(4)].map((_, i) => (
                <div
                  key={i}
                  className="border-base-200 flex items-center justify-between rounded-lg border p-4"
                >
                  <div className="flex items-center gap-3">
                    <div className="skeleton h-10 w-10 shrink-0 rounded"></div>
                    <div className="space-y-2">
                      <div className="skeleton h-4 w-32"></div>
                      <div className="skeleton h-3 w-24"></div>
                    </div>
                  </div>
                  <div className="skeleton h-6 w-16 rounded-full"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-header bg-base-200 p-4">
          <div className="flex items-center gap-2">
            <div className="skeleton h-5 w-5 shrink-0 rounded"></div>
            <div className="skeleton h-6 w-36"></div>
          </div>
        </div>
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="skeleton h-12 w-full rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
