// Task T-249: Landing page navigation bar
// Header with logo and CTA buttons for unauthenticated users

import { Button } from "@/components/ui/button"

export function LandingNavBar() {
  return (
    <nav className="border-b border-gray-200 bg-white/80 backdrop-blur dark:border-gray-800 dark:bg-gray-950/80 sticky top-0 z-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <h1 className="text-2xl font-bold text-blue-600 dark:text-blue-400">
            Evo-TODO
          </h1>
          <div className="flex gap-3">
            <Button variant="outline" asChild>
              <a href="/login">Sign In</a>
            </Button>
            <Button asChild>
              <a href="/signup">Get Started</a>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
