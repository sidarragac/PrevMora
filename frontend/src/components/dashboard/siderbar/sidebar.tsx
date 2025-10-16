import Link from 'next/link';
import React from 'react';

import { SignOutButton } from '@clerk/nextjs';
import {
  BookOpenCheck,
  ChartBar,
  File,
  FileArchive,
  HandCoins,
  Home,
  LogOut,
  Wallet,
} from 'lucide-react';

import Header from '@/components/dashboard/siderbar/header';
import NavBtn from '@/components/dashboard/siderbar/nav-btn';

import AnimationProvider from '@/providers/animation-provider';

export default function Sidebar({ children }: { children: React.ReactNode }) {
  return (
    <div className="drawer lg:drawer-open overflow-hidden">
      <input id="my-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content">
        <input id="sidebar" type="checkbox" className="drawer-toggle" />
        <div className="drawer-content overflow-hidden">
          {/* Page content here */}
          <Header />
          <div className="bg-base-100 h-[calc(100dvh-64px)] ps-2 pe-2 pt-0 pb-2">
            <div className="relative h-full w-full overflow-hidden rounded-md rounded-b-[28px] bg-white sm:rounded-b-md">
              <div className="absolute h-full w-full bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] [background-size:16px_16px]"></div>
              <div
                className="my-side-container absolute top-0 left-0 h-full w-full overflow-x-hidden rounded-md p-2 pt-6 sm:p-8"
                style={{ scrollbarGutter: 'stable' }}
              >
                <div
                  className="container mx-auto pb-24"
                  // style={{ contentVisibility: 'auto' }}
                >
                  <AnimationProvider>{children}</AnimationProvider>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="drawer-side">
        <label
          htmlFor="my-drawer"
          aria-label="close sidebar"
          className="drawer-overlay"
        ></label>
        <ul className="menu bg-base-100 text-base-content flex min-h-full w-60 flex-col gap-4 p-4">
          {/* Sidebar content here */}

          <div className="mb-6 flex w-full justify-center">
            <Link href="/" className="btn btn-primary max-w-min text-xl">
              <p className="flex items-center gap-2">
                <HandCoins className="size-6" />
                PrevMora
              </p>
            </Link>
          </div>
          <NavBtn
            text="Inicio"
            goto="/plataforma"
            iconActive={<Home className="size-6" />}
            iconInactive={<Home className="size-6" />}
            restringed={false}
          />
          <NavBtn
            text="Cartera"
            goto="/plataforma/cartera"
            iconActive={<Wallet className="size-6" />}
            iconInactive={<Wallet className="size-6" />}
            restringed={false}
          />
          <NavBtn
            text="Kpis"
            goto="/plataforma/kpis"
            iconActive={<ChartBar className="size-6" />}
            iconInactive={<ChartBar className="size-6" />}
            restringed={false}
          />
          <ul className="menu bg-base-200 rounded-box w-56">
            <li>
              <details open>
                <summary>
                  <BookOpenCheck /> Subir Excel
                </summary>
                <ul className="flex flex-col gap-2">
                  <NavBtn
                    text="Excel Principal"
                    goto="/plataforma/subir-excel"
                    iconActive={<File className="size-6" />}
                    iconInactive={<File className="size-6" />}
                    restringed={false}
                  />
                  <NavBtn
                    text="Excel Portafolio"
                    goto="/plataforma/subir-excel-portafolio"
                    iconActive={<FileArchive className="size-6" />}
                    iconInactive={<FileArchive className="size-6" />}
                    restringed={false}
                  />
                </ul>
              </details>
            </li>
          </ul>

          {/* Spacer to push logout button to bottom */}
          <div className="flex-1"></div>

          <div className="flex gap-2">
            {/* <UserButton className='btn-nav' /> */}
            <SignOutButton>
              <button className="btn btn-primary flex w-full">
                <LogOut className="size-5" />
                Cerrar sesión
              </button>
            </SignOutButton>
          </div>
        </ul>
      </div>
    </div>
  );
}
