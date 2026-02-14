'use client'

import { useState } from 'react'
import { ReactNode } from 'react'
import { Navbar } from './Navbar'
import { Sidebar } from './Sidebar'

export function DashboardUI({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  return (
    <div className='flex h-screen bg-white dark:bg-gray-950'>
      <aside className={'fixed inset-y-0 left-0 z-40 w-64 transform ' + (sidebarOpen ? 'translate-x-0' : '-translate-x-full') + ' sm:relative sm:translate-x-0'}>
        <Sidebar onClose={() => setSidebarOpen(false)} />
      </aside>
      {sidebarOpen && <div className='fixed inset-0 z-30 bg-black/50 sm:hidden' onClick={() => setSidebarOpen(false)} />}
      <div className='flex flex-col flex-1'>
        <header className='sticky top-0 z-20'>
          <Navbar onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
        </header>
        <main className='flex-1 overflow-y-auto'>
          <div className='p-4 sm:p-6'>{children}</div>
        </main>
      </div>
    </div>
  )
}
