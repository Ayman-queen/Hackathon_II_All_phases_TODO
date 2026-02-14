'use client'

import { Todo } from '@/lib/hooks/useTodos'
import { TaskItem } from './TaskItem'
import { EmptyState } from '@/components/common/EmptyState'

interface TaskListProps {
  tasks: Todo[]
  onEdit?: (task: Todo) => void
  onTaskUpdate?: () => void
  isLoading?: boolean
  emptyMessage?: string
}

/**
 * Task T028: TaskList Component
 *
 * Features:
 * 1. Display multiple tasks in a list
 * 2. Render TaskItem for each task
 * 3. Show empty state when no tasks
 * 4. Support for loading state
 * 5. Responsive layout
 */
export function TaskList({
  tasks,
  onEdit,
  onTaskUpdate,
  isLoading = false,
  emptyMessage = 'No tasks yet. Create one to get started!',
}: TaskListProps) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="h-24 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse"
          />
        ))}
      </div>
    )
  }

  if (tasks.length === 0) {
    return <EmptyState title={emptyMessage} />
  }

  // Group tasks by status
  const completedTasks = tasks.filter((t) => t.status === 'completed')
  const pendingTasks = tasks.filter((t) => t.status === 'pending')

  return (
    <div className="space-y-6">
      {/* Pending tasks */}
      {pendingTasks.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Active Tasks ({pendingTasks.length})
          </h3>
          <div className="space-y-3">
            {pendingTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={onEdit}
                onTaskUpdate={onTaskUpdate}
              />
            ))}
          </div>
        </section>
      )}

      {/* Completed tasks */}
      {completedTasks.length > 0 && (
        <section>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
            Completed ({completedTasks.length})
          </h3>
          <div className="space-y-3">
            {completedTasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onEdit={onEdit}
                onTaskUpdate={onTaskUpdate}
              />
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
