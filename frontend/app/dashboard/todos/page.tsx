import { TasksContainer } from '@/components/todos/TasksContainer'

/**
 * Task T026: Dashboard Todos Page
 *
 * Full task management interface accessed from dashboard navigation
 * Displays comprehensive task list with create/edit/delete/bulk operations
 */
export default function DashboardTodosPage() {
  return (
    <div className="space-y-6">
      <section>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Task Management
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Create, edit, and manage all your tasks in one place
        </p>
      </section>

      <TasksContainer showCreateForm={true} />
    </div>
  )
}
