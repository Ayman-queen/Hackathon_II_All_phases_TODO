// Task T-235: Custom useTodos hook for todo CRUD operations
// Provides state management for todo items with filtering, sorting, and API integration
// Handles all todo operations: fetch, create, update, delete, filter

"use client"

import { useEffect, useState } from "react"
import { apiGet, apiPost, apiPut, apiPatch, apiDelete } from "../api"

export type TodoStatus = "pending" | "completed"
// Note: Priority is not supported by backend in Phase II
// Kept for future potential use
export type TodoPriority = "low" | "medium" | "high"

export interface Todo {
  id: string
  userId: string
  title: string
  description?: string
  status: TodoStatus
  createdAt: string
  updatedAt: string
}

export type TodoFilter = "all" | "pending" | "completed"
export type TodoSort = "title" | "createdAt"

/**
 * Task T008: Request schema for creating a todo (POST /api/todos)
 * Matches backend TodoCreate schema
 */
export interface TodoCreateRequest {
  title: string
  description?: string
}

/**
 * Task T008: Request schema for updating todo status (PATCH /api/todos/{id})
 * Matches backend TodoToggle schema - ONLY for status toggling
 */
export interface TodoStatusUpdateRequest {
  is_complete: boolean
}

/**
 * Task T008: Request schema for updating todo fields (PUT /api/todos/{id})
 * Matches backend TodoUpdate schema
 */
export interface TodoFieldsUpdateRequest {
  title?: string
  description?: string
  is_complete?: boolean
}

/**
 * Task T008: Response schema for single todo (GET /api/todos/{id}, POST/PATCH/PUT responses)
 * Backend returns snake_case, transformed to camelCase by transformTodoResponse()
 */
export interface TodoResponse {
  id: string
  user_id: string
  title: string
  description?: string
  is_complete: boolean
  priority: string
  due_date?: string
  created_at: string
  updated_at: string
}

/**
 * Task T008: Response schema for todo list (GET /api/todos)
 * Backend returns paginated todos with total count
 */
export interface TodoListResponse {
  todos: TodoResponse[]
  total: number
}

export interface UseTodosReturn {
  // State
  todos: Todo[]
  filteredTodos: Todo[]
  isLoading: boolean
  error: string | null

  // Filter & Sort
  currentFilter: TodoFilter
  currentSort: TodoSort
  setFilter: (filter: TodoFilter) => void
  setSort: (sort: TodoSort) => void

  // CRUD Operations
  createTodo: (data: Omit<Todo, "id" | "userId" | "createdAt" | "updatedAt">) => Promise<Todo>
  getTodoById: (id: string) => Promise<Todo>
  updateTodo: (id: string, data: Partial<Todo>) => Promise<Todo>
  updateTodoFields: (id: string, data: Partial<Todo>) => Promise<Todo>
  deleteTodo: (id: string) => Promise<void>
  refreshTodos: () => Promise<void>
}

/**
 * Task T-235: Custom useTodos hook
 * - Fetches todos from /api/todos endpoint
 * - Manages filtering by status (all/pending/completed)
 * - Supports sorting by multiple fields
 * - Provides create, update, delete methods
 * - Maintains loading and error states
 * 
 * FIX (2026-01-01): Handle backend response format
 * Backend returns: { todos: [...], total: number }
 * Frontend expects: Todo[] array
 * Also converts snake_case fields to camelCase
 */
export function useTodos(): UseTodosReturn {
  const [todos, setTodos] = useState<Todo[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentFilter, setFilter] = useState<TodoFilter>("all")
  const [currentSort, setSort] = useState<TodoSort>("createdAt")

  // Initial fetch on mount
  useEffect(() => {
    refreshTodos()
  }, [])

  /**
   * Task T-235: Apply filtering based on status
   * Converts backend is_complete field to frontend status field
   */
  const getFilteredTodos = (): Todo[] => {
    let filtered = todos

    // Apply status filter
    if (currentFilter === "pending") {
      filtered = filtered.filter((todo) => todo.status === "pending")
    } else if (currentFilter === "completed") {
      filtered = filtered.filter((todo) => todo.status === "completed")
    }

    // Apply sorting (note: priority and dueDate not supported by backend)
    const sorted = [...filtered].sort((a, b) => {
      switch (currentSort) {
        case "title":
          return a.title.localeCompare(b.title)
        case "createdAt":
        default:
          return (
            new Date(b.createdAt).getTime() -
            new Date(a.createdAt).getTime()
          )
      }
    })

    return sorted
  }

  /**
   * Convert backend todo response to frontend format
   * Backend returns snake_case, frontend uses camelCase
   * Note: Priority and dueDate are NOT supported by backend in Phase II
   *
   * @param {TodoResponse} backendTodo - Backend response in snake_case format
   * @returns {Todo} Frontend format in camelCase
   */
  const transformTodoResponse = (backendTodo: TodoResponse): Todo => {
    return {
      id: backendTodo.id,
      userId: backendTodo.user_id,
      title: backendTodo.title,
      description: backendTodo.description,
      status: backendTodo.is_complete ? "completed" : "pending",
      createdAt: backendTodo.created_at,
      updatedAt: backendTodo.updated_at,
    }
  }

  const filteredTodos = getFilteredTodos()

  /**
   * Task T007: Fetch all todos from backend
   * Endpoint: GET /api/todos
   *
   * @async
   * @returns {Promise<void>} Updates state with fetched todos
   * @throws Logs error to state.error but doesn't throw (allows graceful degradation)
   *
   * Features:
   * - Fetches paginated list of todos with total count
   * - Automatically includes JWT token in Authorization header
   * - Transforms backend snake_case to frontend camelCase
   * - Converts is_complete boolean to status string ("pending"/"completed")
   * - Sets loading state during fetch, clears on completion
   * - Sets error state on failure
   *
   * Query Parameters (optional):
   * - skip: Offset for pagination (default 0)
   * - limit: Number of items to return (default 100, max 1000)
   * - is_complete: Filter by status (true/false/null for all)
   *
   * Example:
   *   const { refreshTodos } = useTodos()
   *   await refreshTodos()  // Fetch todos
   */
  const refreshTodos = async () => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await apiGet<TodoListResponse>("/api/todos")

      if (response.ok && response.data?.todos) {
        // Transform backend todos to frontend format
        const transformedTodos = response.data.todos.map(transformTodoResponse)
        setTodos(transformedTodos)
      } else {
        setError(response.error || "Failed to load todos")
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to load todos"
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Task T001 + T007: Fetch single todo by ID
   * Endpoint: GET /api/todos/{id}
   *
   * @async
   * @param {string} id - UUID of the todo to fetch
   * @returns {Promise<Todo>} The requested todo object
   * @throws {Error} If todo not found (404) or API error occurs
   *
   * Features:
   * - Fetches single todo by UUID
   * - Automatically includes JWT token in Authorization header
   * - Transforms backend response to frontend format
   * - Returns 404 if todo doesn't exist OR if user doesn't own it
   * - Prevents information leakage (attacker can't distinguish)
   * - Clears any previous error state
   * - Does NOT update internal todos state (read-only fetch)
   *
   * Errors:
   * - 401: Missing or invalid authentication token
   * - 403: User does not own this todo (forbidden)
   * - 404: Todo with this ID does not exist
   *
   * Example:
   *   const { getTodoById } = useTodos()
   *   const todo = await getTodoById('550e8400-e29b-41d4-a716-446655440000')
   */
  const getTodoById = async (id: string): Promise<Todo> => {
    try {
      setError(null)

      const response = await apiGet<TodoResponse>(`/api/todos/${id}`)

      if (response.ok && response.data) {
        // Transform single todo response to frontend format
        const transformedTodo = transformTodoResponse(response.data)
        return transformedTodo
      } else {
        throw new Error(response.error || "Failed to fetch todo")
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to fetch todo"
      setError(errorMessage)
      throw err
    }
  }

  /**
   * Task T007: Create new todo
   * Endpoint: POST /api/todos
   *
   * @async
   * @param {Omit<Todo, "id" | "userId" | "createdAt" | "updatedAt">} data - Todo creation data
   * @param {string} data.title - Todo title (1-500 chars, required)
   * @param {string} [data.description] - Optional description (0-2000 chars)
   * @param {TodoStatus} data.status - Initial status ("pending" or "completed")
   * @param {TodoPriority} data.priority - Priority level ("low", "medium", "high")
   * @param {string} [data.dueDate] - Optional ISO 8601 due date
   * @returns {Promise<Todo>} Created todo with id, userId, and timestamps
   * @throws {Error} If validation fails or API error occurs
   *
   * Features:
   * - Creates new todo for authenticated user
   * - Validates title (1-500 characters, required)
   * - Validates description (max 2000 characters, optional)
   * - Automatically sets user_id from JWT token
   * - Status "completed" -> backend is_complete=true
   * - Adds new todo to internal todos state
   * - Sets error state on failure
   * - Clears previous error state on success
   *
   * Backend Validation:
   * - title: Required, 1-500 characters, cannot be all whitespace
   * - description: Optional, max 2000 characters
   * - user_id: Automatically set from JWT token (not from request)
   *
   * Errors:
   * - 400: Title validation failed
   * - 401: Missing or invalid authentication token
   * - 422: Validation error from Pydantic
   *
   * Example:
   *   const { createTodo } = useTodos()
   *   const newTodo = await createTodo({
   *     title: 'Buy groceries',
   *     description: 'Milk, eggs, bread',
   *     status: 'pending',
   *     priority: 'high',
   *     dueDate: '2026-01-15'
   *   })
   */
  const createTodo = async (
    data: Omit<Todo, "id" | "userId" | "createdAt" | "updatedAt">
  ): Promise<Todo> => {
    try {
      setError(null)

      // Convert frontend format to backend format
      const backendData: TodoCreateRequest = {
        title: data.title,
        description: data.description,
      }

      const response = await apiPost<TodoResponse>("/api/todos", backendData)

      if (response.ok && response.data) {
        // Transform and add new todo to state
        const transformedTodo = transformTodoResponse(response.data)
        await refreshTodos()
        return transformedTodo
      } else {
        throw new Error(response.error || "Failed to create todo")
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to create todo"
      setError(errorMessage)
      throw err
    }
  }

  /**
   * Task T003 + T007: Update todo status via PATCH
   * Endpoint: PATCH /api/todos/{id}
   *
   * @async
   * @param {string} id - UUID of the todo to update
   * @param {Partial<Todo>} data - Update data (only status field supported)
   * @param {TodoStatus} [data.status] - New status ("pending" or "completed")
   * @returns {Promise<Todo>} Updated todo object
   * @throws {Error} If validation fails, todo not found, or user doesn't own it
   *
   * Features:
   * - Updates ONLY the is_complete status field
   * - Status "completed" -> backend is_complete=true
   * - Status "pending" -> backend is_complete=false
   * - For updating title/description, use updateTodoFields() instead
   * - Updates todo in internal todos state
   * - Sets error state on failure
   * - Clears previous error state on success
   *
   * Endpoint Behavior:
   * - PATCH only sends { is_complete: boolean }
   * - Returns error if other fields are included in request
   * - Requires status field in data parameter
   *
   * Errors:
   * - 401: Missing or invalid authentication token
   * - 403: User does not own this todo
   * - 404: Todo with this ID does not exist
   *
   * Example:
   *   const { updateTodo } = useTodos()
   *   await updateTodo('550e8400-e29b-41d4-a716-446655440000', {
   *     status: 'completed'
   *   })
   */
  const updateTodo = async (
    id: string,
    data: Partial<Todo>
  ): Promise<Todo> => {
    try {
      setError(null)

      // T003: PATCH only sends is_complete status
      // For other fields, use updateTodoFields() instead
      if (data.status === undefined) {
        throw new Error("PATCH endpoint requires status field. Use updateTodoFields() for other fields.")
      }

      const backendData: TodoStatusUpdateRequest = {
        is_complete: data.status === "completed"
      }

      const response = await apiPatch<TodoResponse>(`/api/todos/${id}`, backendData)

      if (response.ok && response.data) {
        // Transform and update todo in state
        const transformedTodo = transformTodoResponse(response.data)
        await refreshTodos()
        return transformedTodo
      } else {
        throw new Error(response.error || "Failed to update todo status")
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to update todo status"
      setError(errorMessage)
      throw err
    }
  }

  /**
   * Task T004 + T007: Update todo fields via PUT
   * Endpoint: PUT /api/todos/{id}
   *
   * @async
   * @param {string} id - UUID of the todo to update
   * @param {Partial<Todo>} data - Update data for title/description
   * @param {string} [data.title] - New title (1-500 chars, optional)
   * @param {string} [data.description] - New description (0-2000 chars, optional)
   * @returns {Promise<Todo>} Updated todo object
   * @throws {Error} If validation fails, no fields provided, or user doesn't own todo
   *
   * Features:
   * - Updates title and/or description via PUT endpoint
   * - For updating status, use updateTodo() instead
   * - Validates title (1-500 characters if provided)
   * - Validates description (max 2000 characters if provided)
   * - Requires at least one field to be provided
   * - Updates todo in internal todos state
   * - Sets error state on failure
   * - Clears previous error state on success
   *
   * Endpoint Behavior:
   * - PUT only sends { title?, description? }
   * - At least one field must be provided (no-op rejected)
   * - Other fields are ignored by backend
   * - Updated timestamp is set automatically
   *
   * Field Support:
   * - title: 1-500 characters, cannot be all whitespace
   * - description: 0-2000 characters, optional
   * - Note: priority and dueDate not supported by backend PUT endpoint
   *
   * Errors:
   * - 400: Title/description validation failed
   * - 401: Missing or invalid authentication token
   * - 403: User does not own this todo
   * - 404: Todo with this ID does not exist
   *
   * Example:
   *   const { updateTodoFields } = useTodos()
   *   await updateTodoFields('550e8400-e29b-41d4-a716-446655440000', {
   *     title: 'Updated title',
   *     description: 'Updated description'
   *   })
   */
  const updateTodoFields = async (
    id: string,
    data: Partial<Todo>
  ): Promise<Todo> => {
    try {
      setError(null)

      // T004: PUT endpoint for updating title/description
      const backendData: TodoFieldsUpdateRequest = {}
      if (data.title !== undefined) backendData.title = data.title
      if (data.description !== undefined) backendData.description = data.description
      if (data.status !== undefined) backendData.is_complete = data.status === 'completed'
      // Note: priority and dueDate not supported by backend PUT endpoint

      // Only proceed if at least one field is being updated
      if (Object.keys(backendData).length === 0) {
        throw new Error("At least one field (title or description) must be provided")
      }

      const response = await apiPut<TodoResponse>(`/api/todos/${id}`, backendData)

      if (response.ok && response.data) {
        // Transform and update todo in state
        const transformedTodo = transformTodoResponse(response.data)
        await refreshTodos()
        return transformedTodo
      } else {
        throw new Error(response.error || "Failed to update todo fields")
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to update todo fields"
      setError(errorMessage)
      throw err
    }
  }

  /**
   * Task T007: Delete todo permanently
   * Endpoint: DELETE /api/todos/{id}
   *
   * @async
   * @param {string} id - UUID of the todo to delete
   * @returns {Promise<void>} Void - deletion has no response body
   * @throws {Error} If todo not found, user doesn't own it, or API error
   *
   * Features:
   * - Permanently deletes a todo from the database
   * - User must be the owner to delete
   * - Removes todo from internal todos state
   * - Sets error state on failure
   * - Clears previous error state on success
   * - Returns 204 No Content on success
   *
   * Destructive:
   * - This operation CANNOT be undone
   * - Todo is permanently removed from database
   * - No recovery possible
   *
   * Errors:
   * - 401: Missing or invalid authentication token
   * - 403: User does not own this todo
   * - 404: Todo with this ID does not exist
   *
   * Example:
   *   const { deleteTodo } = useTodos()
   *   await deleteTodo('550e8400-e29b-41d4-a716-446655440000')
   */
  const deleteTodo = async (id: string): Promise<void> => {
    try {
      setError(null)

      const response = await apiDelete(`/api/todos/${id}`)

      if (response.ok) {
        // Remove todo from state
        await refreshTodos()
      } else {
        throw new Error(response.error || "Failed to delete todo")
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to delete todo"
      setError(errorMessage)
      throw err
    }
  }

  return {
    todos,
    filteredTodos,
    isLoading,
    error,
    currentFilter,
    currentSort,
    setFilter,
    setSort,
    createTodo,
    getTodoById,
    updateTodo,
    updateTodoFields,
    deleteTodo,
    refreshTodos,
  }
}
