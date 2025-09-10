'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

import { useUser } from '@clerk/nextjs';

export default function NavBtn({
  text,
  goto = '',
  iconActive,
  iconInactive,
  restringed = false,
}: {
  text: string;
  goto: string;
  iconActive: React.ReactNode;
  iconInactive: React.ReactNode;
  restringed: boolean;
}) {
  const { user } = useUser();
  const pathname = usePathname();

  if (restringed && user?.publicMetadata?.user !== 'admin') return null;

  return (
    <li>
      <Link
        // prefetch={false}
        className={`btn-nav flex !justify-start ${pathname === goto && 'btn-nav-active'}`}
        href={goto}
      >
        {pathname === goto ? iconActive : iconInactive} {text}
      </Link>
    </li>
  );
}
