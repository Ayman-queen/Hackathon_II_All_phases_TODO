// Task T-239: TypeScript types for todo entities
// Reference: plan.md data model, backend API contract

/**
 * Priority levels for todos
 */
export type Priority = 'HIGH' | 'MEDIUM' | 'LOW';

/**
 * Completion status of a todo
 */
export type TodoStatus = 'pending' | 'completed';

/**
 * Todo entity from backend API
 * Represents a single task in the system
 */
export interface Todo {
  id: string;
  userId: string;
  title: string;
  description?: string;
  priority: Priority;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Request payload for creating a new todo
 * Backend automatically assigns user_id and timestamps
 */
export interface CreateTodoRequest {
  title: string;
  description?: string;
}

/**
 * Request payload for updating an existing todo
 */
export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  priority?: Priority;
  is_complete?: boolean;
}

/**
 * Response from /api/todos endpoint (list todos)
 */
export interface TodoListResponse {
  todos: Todo[];
  total: number;
}

/**
 * Todo filter type
 */
export type TodoFilter = 'all' | 'pending' | 'completed';

/**
 * Todo sort type
 */
export type TodoSort = 'priority' | 'dueDate' | 'title';

/**
 * Local state for todo management
 */
export interface TodoListState {
  todos: Todo[];
  filter: TodoFilter;
  sort: TodoSort;
  isLoading: boolean;
  error: string | null;
}
