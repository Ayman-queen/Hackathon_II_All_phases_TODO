'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { AlertCircle } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { cn } from '@/lib/utils'
import { Todo } from '@/lib/hooks/useTodos'

// Zod validation schema matching backend constraints
// Note: Priority and dueDate are NOT supported by backend (removed from schema)
const taskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(500, 'Title must be under 500 characters'),
  description: z.string().max(2000, 'Description must be under 2000 characters').optional(),
  status: z.enum(['pending', 'completed']).default('pending'),
})

type TaskFormData = z.infer<typeof taskSchema>

interface TaskFormProps {
  onSuccess: (data: TaskFormData) => Promise<void> | void
  onCancel?: () => void
  initialData?: Partial<Todo>
  isEditing?: boolean
}

/**
 * TaskForm Component - Enhanced with full dark mode support
 *
 * Features:
 * - Full dark mode support with proper contrast using shadcn/ui components.
 * - Client-side validation with zod + react-hook-form
 * - Title field (1-500 characters)
 * - Description field with 4 rows (0-2000 characters, optional)
 * - Status selector (pending/completed)
 * - Loading state feedback
 * - Error message display with icons
 * - Responsive design
 * - Accessibility features (labels, ARIA attributes)
 *
 * Note: Priority and dueDate are NOT supported by backend schema
 * Backend only accepts: title, description, is_complete
 */
export function TaskForm({
  onSuccess,
  onCancel,
  initialData,
  isEditing = false,
}: TaskFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: initialData?.title || '',
      description: initialData?.description || '',
      status: initialData?.status || 'pending',
    },
  })

  const descriptionValue = watch('description', '')

  const onSubmitForm = async (data: TaskFormData) => {
    try {
      // Convert form data to match backend expectations
      // Description should be undefined if empty string
      const submitData = {
        title: data.title,
        description: data.description || undefined,
        status: data.status,
      }

      // Call parent's onSuccess callback with the form data
      await onSuccess(submitData)
    } catch (error) {
      console.error('Form submission error:', error)
    }
  }

  const handleCancel = () => {
    if (onCancel) {
      onCancel()
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-6">
      {/* Title Field */}
      <div>
        <Label htmlFor="title" className="font-semibold">
          Task Title <span className="text-red-500">*</span>
        </Label>
        <Input
          id="title"
          type="text"
          placeholder="What needs to be done?"
          {...register('title')}
          className={cn(errors.title && 'border-red-500 dark:border-red-500')}
          disabled={isSubmitting}
        />
        {errors.title && (
          <div className="mt-2 flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{errors.title.message}</span>
          </div>
        )}
      </div>

      {/* Description Field */}
      <div>
        <Label htmlFor="description" className="font-semibold">
          Description <span className="text-gray-500 dark:text-gray-400 font-normal">(Optional)</span>
        </Label>
        <textarea
          id="description"
          placeholder="Add task details and notes here..."
          rows={4}
          {...register('description')}
          className={cn(`flex w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white
            placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-950 focus-visible:ring-offset-2
            disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-800 dark:bg-slate-950 dark:text-gray-100 dark:ring-offset-slate-950
            dark:placeholder:text-slate-400 dark:focus-visible:ring-slate-300`,
            `resize-vertical`,
            errors.description && 'border-red-500 dark:border-red-500'
          )}
          disabled={isSubmitting}
        />
        {errors.description && (
          <div className="mt-2 flex items-center gap-2 text-red-600 dark:text-red-400 text-sm">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{errors.description.message}</span>
          </div>
        )}
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
          {descriptionValue ? descriptionValue.length : 0}/2000 characters
        </p>
      </div>

      {/* Status Field */}
      <div>
        <Label htmlFor="status" className="font-semibold">
          Status
        </Label>
        <select
          id="status"
          {...register('status')}
          className={cn(`flex h-10 w-full items-center justify-between rounded-md border border-slate-200 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-800 dark:bg-slate-950 dark:text-gray-100 dark:ring-offset-slate-950 dark:placeholder:text-slate-400 dark:focus:ring-slate-300`,
              `cursor-pointer`
            )}
            disabled={isSubmitting}
          >
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
      </div>

      {/* Form Actions */}
      <div className="flex gap-3 justify-end pt-4 border-t border-gray-200 dark:border-gray-800">
        <Button
          type="button"
          variant="outline"
          onClick={handleCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting && (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
          )}
          {isSubmitting ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Task' : 'Create Task')}
        </Button>
      </div>
    </form>
  )
}
