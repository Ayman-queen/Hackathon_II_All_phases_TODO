'use client'

import { useState } from 'react'
import { Todo, useTodos } from '@/lib/hooks/useTodos'
import { toast } from 'sonner'
import { Edit2, Trash2, CheckCircle2, Circle } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface TaskItemProps {
  task: Todo
  onEdit?: (task: Todo) => void
  onTaskUpdate?: () => void
}

/**
 * Task T029: TaskItem Component
 *
 * Features:
 * 1. Display individual task with title, description
 * 2. Toggle task completion status
 * 3. Edit button to open edit modal/form
 * 4. Delete button with confirmation
 * 5. Visual feedback with icons
 */
export function TaskItem({ task, onEdit, onTaskUpdate }: TaskItemProps) {
  const { updateTodo, deleteTodo } = useTodos()
  const [isUpdating, setIsUpdating] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  const handleToggleComplete = async () => {
    try {
      setIsUpdating(true)
      await updateTodo(task.id, {
        status: task.status === 'completed' ? 'pending' : 'completed',
      })
      toast.success(
        task.status === 'completed'
          ? 'Task marked as pending'
          : 'Task marked as completed'
      )
      onTaskUpdate?.()
    } catch (error) {
      console.error('Failed to update task:', error)
      toast.error('Failed to update task')
    } finally {
      setIsUpdating(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      setIsDeleting(true)
      await deleteTodo(task.id)
      toast.success('Task deleted successfully')
      onTaskUpdate?.()
    } catch (error) {
      console.error('Failed to delete task:', error)
      toast.error('Failed to delete task')
    } finally {
      setIsDeleting(false)
    }
  }

  return (
    <div
      className={`flex items-start gap-4 p-4 border rounded-lg transition-all ${
        task.status === 'completed'
          ? 'bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700'
          : 'bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600'
      }`}
    >
      {/* Completion toggle */}
      <button
        onClick={handleToggleComplete}
        disabled={isUpdating}
        className="flex-shrink-0 mt-1 hover:opacity-70 transition-opacity"
        aria-label={task.status === 'completed' ? 'Mark as pending' : 'Mark as complete'}
      >
        {task.status === 'completed' ? (
          <CheckCircle2 className="w-6 h-6 text-green-500" />
        ) : (
          <Circle className="w-6 h-6 text-gray-400 dark:text-gray-600" />
        )}
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <h3
          className={`font-semibold text-lg truncate ${
            task.status === 'completed'
              ? 'line-through text-gray-500 dark:text-gray-400'
              : 'text-gray-900 dark:text-white'
          }`}
        >
          {task.title}
        </h3>

        {task.description && (
          <p className={`text-sm mt-1 line-clamp-2 ${
            task.status === 'completed'
              ? 'text-gray-400 dark:text-gray-500'
              : 'text-gray-600 dark:text-gray-400'
          }`}>
            {task.description}
          </p>
        )}

        {/* Metadata */}
        <div className="flex flex-wrap gap-2 mt-2">
        </div>
      </div>

      {/* Actions */}
      <div className="flex-shrink-0 flex gap-2">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => onEdit?.(task)}
          className="text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20"
          disabled={isUpdating || isDeleting}
        >
          <Edit2 className="w-4 h-4" />
        </Button>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleDelete}
          className="text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20"
          disabled={isUpdating || isDeleting}
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </div>
  )
}
