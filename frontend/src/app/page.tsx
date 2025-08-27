'use client';

// import { useLocalStorage } from '@/hooks/use-local-storage';

export default function Home() {
  return (
    <div className="">
      Tailwind + DaisyUI
      <div className="flex gap-2">
        <button className="btn">Default</button>
        <button className="btn btn-primary">Primary</button>
        <button className="btn btn-secondary">Secondary</button>
        <button className="btn btn-accent">Accent</button>
        <button className="btn btn-info">Info</button>
        <button className="btn btn-success">Success</button>
        <button className="btn btn-warning">Warning</button>
        <button className="btn btn-error">Error</button>
      </div>
    </div>
  );
}
