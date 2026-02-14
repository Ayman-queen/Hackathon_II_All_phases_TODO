'use client'

import { Menu, LogOut, Sun, Moon } from 'lucide-react'
import { useTheme } from 'next-themes'
import { useSession, signOut } from '@/lib/auth-client'
import { useState, useEffect } from 'react'

interface NavbarProps {
  onMenuToggle: () => void
}

export function Navbar({ onMenuToggle }: NavbarProps) {
  const { data: session, isPending } = useSession()
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleLogout = async () => {
    try {
      await signOut()
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  const handleThemeToggle = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark')
  }

  return (
    <nav className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
      <div className="flex items-center gap-4">
        <button onClick={onMenuToggle} className="sm:hidden p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" aria-label="Toggle sidebar">
          <Menu className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold text-gray-900 dark:text-white">Evo-TODO</h1>
      </div>

      <div className="flex items-center gap-4">
        {!isPending && session?.user && (
          <div className="hidden sm:flex items-center gap-2">
            <div className="flex flex-col items-end">
              <p className="text-sm font-medium text-gray-900 dark:text-white">{session.user.name || session.user.email}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">{session.user.email}</p>
            </div>
            <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-semibold">
              {session.user.name?.[0]?.toUpperCase() || session.user.email?.[0]?.toUpperCase() || 'U'}
            </div>
          </div>
        )}

        {mounted && (
          <button onClick={handleThemeToggle} className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" aria-label="Toggle theme">
            {theme === 'dark' ? (
              <Sun className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            ) : (
              <Moon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            )}
          </button>
        )}

        <button onClick={handleLogout} className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" aria-label="Logout">
          <LogOut className="w-4 h-4" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </nav>
  )
}
