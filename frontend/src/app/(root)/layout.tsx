import React from 'react';

import Navbar from '@/components/landing/navbar';

export default function layout({ children }: { children: React.ReactNode }) {
  return (
    <main className="" id="landing-main-content">
      <div className="p-4">
        <Navbar />
      </div>
      <div className="container mx-auto mt-4">{children}</div>
    </main>
  );
}
