import Link from 'next/link';
import React, { Suspense } from 'react';

import { SignUp } from '@clerk/nextjs';
import { ChevronLeft } from 'lucide-react';

import AnimationProvider from '@/providers/animation-provider';

export default function Page() {
  return (
    <main
      className="flex min-h-screen w-screen items-center justify-center overflow-y-auto"
      id="landing-main-content"
    >
      <div className="flex flex-col gap-4">
        <Link href="/" className="btn btn-primary text-xl">
          <p className="flex items-center gap-2">
            <ChevronLeft />
            Volver
          </p>
        </Link>
        <Suspense
          fallback={
            <span className="loading loading-spinner loading-xl text-primary text-center"></span>
          }
        >
          <AnimationProvider>
            <div className="flex w-full items-center justify-center"></div>
            <SignUp />
          </AnimationProvider>
        </Suspense>
      </div>
    </main>
  );
}
