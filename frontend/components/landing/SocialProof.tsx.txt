// Task T-247: SocialProof component
// Displays stats and social proof (active users, tasks completed, uptime)

export function SocialProof() {
  return (
    <section className="py-20 dark:bg-gray-950/50 sm:py-32">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div className="text-center">
            <div className="text-4xl font-bold text-blue-600 dark:text-blue-400">
              10K+
            </div>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Active Users
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 dark:text-green-400">
              1M+
            </div>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Tasks Completed
            </p>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-purple-600 dark:text-purple-400">
              99.9%
            </div>
            <p className="mt-2 text-gray-600 dark:text-gray-300">
              Uptime
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
