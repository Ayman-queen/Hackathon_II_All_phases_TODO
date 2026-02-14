// Task T-239: Empty state component for lists with no data
// Shows friendly message when todos list is empty, search has no results, etc.

"use client"

import { ReactNode } from 'react'
import { AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"

export interface EmptyStateProps {
  title: string
  description?: string
  icon?: ReactNode
  action?: {
    label: string
    onClick: () => void
  }
}

/**
 * Task T-239: EmptyState component
 * - Displays when list/collection is empty
 * - Customizable icon, title, description
 * - Optional action button (e.g., "Create First Todo")
 * - Dark mode support
 * - Responsive centered layout
 */
export function EmptyState({
  title,
  description,
  icon,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-gray-200 bg-gray-50 py-12 text-center dark:border-gray-700 dark:bg-gray-900">
      <div className="mb-4 text-gray-400 dark:text-gray-500">
        {icon || <AlertCircle className="h-12 w-12 mx-auto" />}
      </div>

      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
        {title}
      </h3>

      {description && (
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          {description}
        </p>
      )}

      {action && (
        <Button
          onClick={action.onClick}
          className="mt-6"
          variant="default"
        >
          {action.label}
        </Button>
      )}
    </div>
  )
}
