'use client'

import { useState, useEffect } from 'react'
import { useTodos, Todo, TodoStatus } from '@/lib/hooks/useTodos'
import { useBulkSelection } from '@/lib/hooks/useBulkSelection'
import { TaskForm } from './TaskForm'
import { TaskList } from './TaskList'
import { BulkActions } from './BulkActions'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'

interface TasksContainerProps {
  showCreateForm?: boolean
}

/**
 * Task T032: TasksContainer Component
 *
 * Orchestrator component that:
 * 1. Manages tasks state with useTodos hook
 * 2. Handles bulk selection with useBulkSelection hook
 * 3. Integrates TaskForm, TaskList, and BulkActions
 * 4. Manages create/edit modal state
 * 5. Refreshes tasks on CRUD operations
 */
export function TasksContainer({ showCreateForm = true }: TasksContainerProps) {
  const { todos, isLoading, refreshTodos, createTodo, updateTodoFields, updateTodo } = useTodos()
  const { selectedIds } = useBulkSelection()
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<Todo | null>(null)

  // Load tasks on mount
  useEffect(() => {
    refreshTodos()
  }, [])

  const handleFormSuccess = async (data: { title: string; description?: string; status: string }) => {
    try {
      if (editingTask) {
        // Update existing task
        // First, update title/description with PUT
        await updateTodoFields(editingTask.id, {
          title: data.title,
          description: data.description,
        })

        // Then, update status separately with PATCH if different from current
        if (editingTask.status !== data.status) {
          await updateTodo(editingTask.id, {
            status: data.status as TodoStatus,
          })
        }

        toast.success('Task updated successfully')
      } else {
        // Create new task with POST
        await createTodo({
          title: data.title,
          description: data.description,
          status: 'pending',
        })
        toast.success('Task created successfully')
      }

      setShowForm(false)
      setEditingTask(null)
      refreshTodos()
    } catch (error) {
      console.error('Form submission error:', error)
      toast.error(editingTask ? 'Failed to update task' : 'Failed to create task')
      throw error // Let's form handle error state
    }
  }

  const handleEdit = (task: Todo) => {
    setEditingTask(task)
    setShowForm(true)
  }

  const handleCloseForm = () => {
    setShowForm(false)
    setEditingTask(null)
  }

  return (
    <div className="space-y-6 min-h-screen">
      {/* Header with Create Button */}
      {showCreateForm && !showForm && (
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Your Tasks
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              {todos.length} task{todos.length === 1 ? '' : 's'} total
            </p>
          </div>
          <Button
            onClick={() => setShowForm(true)}
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            New Task
          </Button>
        </div>
      )}

      {/* Create/Edit Form */}
      {showForm && (
        <div className="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              {editingTask ? 'Edit Task' : 'Create New Task'}
            </h3>
            <button
              onClick={handleCloseForm}
              className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              aria-label="Close form"
            >
              ✕
            </button>
          </div>
          <TaskForm
            onSuccess={handleFormSuccess}
            initialData={editingTask || undefined}
            isEditing={!!editingTask}
          />
        </div>
      )}

      {/* Tasks List */}
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <TaskList
          tasks={todos}
          onEdit={handleEdit}
          onTaskUpdate={refreshTodos}
        />
      )}

      {/* Bulk Actions Bar */}
      <BulkActions
        selectedCount={selectedIds.size}
        onActionsComplete={refreshTodos}
      />
    </div>
  )
}
