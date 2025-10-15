import React from 'react';

export default function Loading() {
  return (
    <div className="space-y-6">
      {/* Header Skeleton */}
      <div className="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <div className="flex items-center gap-3">
            <div className="skeleton h-8 w-8 rounded-full"></div>
            <div className="skeleton h-8 w-48"></div>
          </div>
          <div className="skeleton mt-2 h-4 w-64"></div>
        </div>

        <div className="flex items-center gap-2">
          <div className="stats shadow-sm">
            <div className="stat px-4 py-2">
              <div className="skeleton h-3 w-24"></div>
              <div className="skeleton mt-2 h-6 w-10"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-sm">
        <div className="card-body p-4">
          <div className="flex flex-col gap-4 sm:flex-row">
            <div className="flex-1">
              <div className="relative">
                <div className="skeleton absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 transform"></div>
                <div className="skeleton h-12 w-full"></div>
              </div>
            </div>
            <div className="flex gap-2">
              <div className="skeleton h-9 w-28"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Clients Content Skeleton */}
      <div className="card bg-base-100 border-base-200 border shadow-lg">
        <div className="card-body p-6">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="card border-base-200 border shadow-sm">
                <div className="card-body p-4">
                  <div className="flex items-center gap-3">
                    <div className="skeleton h-12 w-12 rounded-full"></div>
                    <div className="flex-1">
                      <div className="skeleton h-4 w-32"></div>
                      <div className="skeleton mt-2 h-3 w-24"></div>
                    </div>
                  </div>
                  <div className="mt-4 grid grid-cols-2 gap-3">
                    <div className="skeleton h-3 w-20"></div>
                    <div className="skeleton h-3 w-16"></div>
                    <div className="skeleton h-3 w-24"></div>
                    <div className="skeleton h-3 w-12"></div>
                  </div>
                  <div className="mt-4 flex gap-2">
                    <div className="skeleton h-8 w-20 rounded"></div>
                    <div className="skeleton h-8 w-24 rounded"></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
