import React from 'react';

import Sidebar from '@/components/dashboard/siderbar/sidebar';

export default function Layout({ children }: { children: React.ReactNode }) {
  return <Sidebar>{children}</Sidebar>;
}
