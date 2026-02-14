// Task T-241: Root layout with Providers (Better Auth, next-themes, Sonner)
// This root layout wraps all routes with necessary providers:
// - ThemeProvider: enables dark/light mode support with system detection
// - Toaster: Sonner toast notifications for user feedback
// - Additional providers can be added as needed

import type { Metadata, Viewport } from 'next'
import { ThemeProvider } from 'next-themes'
import { Toaster } from 'sonner'
import './globals.css'

export const metadata: Metadata = {
  title: 'Evo-TODO - Task Management',
  description: 'Phase II: Full-stack todo application with JWT authentication and Better Auth',
  authors: [{ name: 'Evo-TODO Team' }],
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* Task T-241: Suppress hydration warning due to theme detection */}
      </head>
      <body className="bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-50">
        {/* Task T-241: ThemeProvider from next-themes for dark/light mode */}
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          enableColorScheme={false}
          disableTransitionOnChange
        >
          {/* Task T-237: Better Auth client is initialized in lib/auth-client.ts */}
          {/* Task T-238: API client is initialized in lib/api-client.ts */}
          {/* Task T015: Sonner toast provider for notifications */}
          <Toaster richColors position="top-right" />
          {/* Render all child routes with providers active */}
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
