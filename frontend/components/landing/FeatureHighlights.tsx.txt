// Task T-246: FeatureHighlights component
// Displays 3-4 feature cards highlighting key benefits

import { Shield, Filter, Moon } from "lucide-react"

export function FeatureHighlights() {
  return (
    <section className="border-t border-gray-200 bg-white py-20 dark:border-gray-800 dark:bg-gray-900/50 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h3 className="text-center text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
          Powerful Features
        </h3>

        <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-gray-600 dark:text-gray-300">
          Everything you need to stay organized and productive
        </p>

        {/* Feature Grid */}
        <div className="mt-16 grid gap-8 sm:grid-cols-1 lg:grid-cols-3">
          {/* Feature 1: Secure Auth */}
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-8 dark:border-gray-700 dark:bg-gray-800/50">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30">
              <Shield className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h4 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
              Secure Authentication
            </h4>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Enterprise-grade JWT authentication keeps your data safe. Only you can
              access your tasks.
            </p>
          </div>

          {/* Feature 2: Smart Filtering */}
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-8 dark:border-gray-700 dark:bg-gray-800/50">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-green-100 dark:bg-green-900/30">
              <Filter className="h-6 w-6 text-green-600 dark:text-green-400" />
            </div>
            <h4 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
              Smart Filtering
            </h4>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Filter and sort tasks by status, priority, and due date. Focus on what
              matters most.
            </p>
          </div>

          {/* Feature 3: Dark Mode */}
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-8 dark:border-gray-700 dark:bg-gray-800/50">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900/30">
              <Moon className="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h4 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
              Beautiful Dark Mode
            </h4>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Comfortable on the eyes with automatic dark mode that respects your
              system preferences.
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
