'use client';

import React from 'react';

import { useAutoAnimate } from '@formkit/auto-animate/react';

export default function AnimationProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [renderPage] = useAutoAnimate({
    duration: 150,
    easing: 'ease-in-out',
  });
  return <div ref={renderPage}>{children}</div>;
}
