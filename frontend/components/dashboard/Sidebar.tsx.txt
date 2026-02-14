'use client'

import { LayoutGrid, CheckSquare, X } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface SidebarProps {
  onClose: () => void
}

/**
 * Task T020: Sidebar Component
 *
 * Features:
 * 1. Navigation menu with main sections
 * 2. Active link highlighting based on current route
 * 3. Responsive design with close button for mobile
 * 4. Icons for each navigation item
 * 5. Proper dark mode support
 *
 * Navigation Items:
 * - Dashboard (/dashboard) - Overview and task summary
 * - Todos (/dashboard/todos) - Full task management interface
 */
export function Sidebar({ onClose }: SidebarProps) {
  const pathname = usePathname()

  // Determine which link is active
  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return pathname === '/dashboard'
    }
    return pathname.startsWith(href)
  }

  const navItems = [
    { href: '/dashboard', icon: LayoutGrid, label: 'Dashboard' },
    { href: '/dashboard/todos', icon: CheckSquare, label: 'Tasks' },
  ]

  return (
    <aside className="flex flex-col h-full w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800">
      {/* Close button for mobile */}
      <div className="flex items-center justify-between h-16 px-4 sm:hidden border-b border-gray-200 dark:border-gray-800">
        <h2 className="text-lg font-bold text-gray-900 dark:text-white">Menu</h2>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          aria-label="Close sidebar"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Navigation items */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map(({ href, icon: Icon, label }) => {
          const active = isActive(href)
          return (
            <Link
              key={href}
              href={href}
              onClick={onClose}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors ${
                active
                  ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Footer info */}
      <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-800">
        <p className="text-xs text-gray-500 dark:text-gray-400">
          © 2024 Evo-TODO. All rights reserved.
        </p>
      </div>
    </aside>
  )
}
