import { Suspense } from 'react';

import { UserButton } from '@clerk/nextjs';

// import GetPath from '@/components/GetPath';
// import HamMenu from '@/components/sidebar/HamMenu';

export default function Header() {
  return (
    <header className="bg-base-100 px-2 py-2 sm:px-2">
      <nav className="flex h-full items-center">
        <div className="hidden w-full items-center lg:flex lg:justify-between">
          <div className="w-[32px]"></div>
          <div className="flex h-12 items-center justify-center">
            {/* <GetPath /> */}
          </div>
          <div className="flex h-full w-[147.14px] items-center">
            <Suspense>
              <UserButton
                appearance={{
                  elements: {
                    userButtonAvatarBox: {
                      width: '40px',
                      height: '40px',
                    },
                  },
                }}
                showName
              />
            </Suspense>
          </div>
        </div>
        <div className="flex h-12 w-full items-center justify-between gap-4 lg:hidden">
          {/* <HamMenu /> */}
          {/* <Link href="/" className="btn btn-primary text-xl">
            <p className="flex items-center gap-2">
              <HandCoins className="size-6" />
              PrevMora
            </p>
          </Link> */}

          <div className="unselectable">{/* <GetPath /> */}</div>

          <div className="flex h-full w-10 items-center">
            <Suspense>
              <UserButton
                appearance={{
                  elements: {
                    userButtonAvatarBox: {
                      width: '40px',
                      height: '40px',
                    },
                  },
                }}
              />
            </Suspense>
          </div>
        </div>
      </nav>
    </header>
  );
}
