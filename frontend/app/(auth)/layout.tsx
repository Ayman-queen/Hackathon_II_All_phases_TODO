// Task T-242 + T-251: Auth routes layout
// Provides consistent layout for authentication pages (signup, login)
// Centered card layout with responsive design
// Reference: plan.md project structure - (auth) route group for public pages

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-950 dark:to-gray-900 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow-lg p-8">
          {children}
        </div>
      </div>
    </div>
  )
}
