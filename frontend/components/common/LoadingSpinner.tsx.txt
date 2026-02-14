// Task T-238: Loading spinner component for async operations
// Provides visual feedback during data fetching, form submission, etc.
// Supports different sizes and variants

"use client"

interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg"
  variant?: "default" | "overlay"
  label?: string
}

/**
 * Task T-238: LoadingSpinner component
 * - Animated spinner using CSS
 * - Multiple size options (sm/md/lg)
 * - Two variants: default (inline) and overlay (full screen)
 * - Optional accessibility label
 * - Dark mode support
 */
export function LoadingSpinner({
  size = "md",
  variant = "default",
  label,
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-8 w-8",
    lg: "h-12 w-12",
  }

  const spinner = (
    <div
      className={`${sizeClasses[size]} animate-spin rounded-full border-2 border-gray-200 border-t-blue-600 dark:border-gray-700 dark:border-t-blue-400`}
      role="status"
      aria-label={label || "Loading"}
    >
      <span className="sr-only">{label || "Loading..."}</span>
    </div>
  )

  if (variant === "overlay") {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-black/20 dark:bg-black/40">
        <div className="rounded-lg bg-white p-8 dark:bg-gray-900 dark:text-white">
          {spinner}
          {label && <p className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">{label}</p>}
        </div>
      </div>
    )
  }

  return <div className="flex items-center justify-center">{spinner}</div>
}
