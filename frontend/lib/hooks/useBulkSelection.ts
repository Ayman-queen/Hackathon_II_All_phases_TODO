// Task T017: Bulk selection hook
// Manages selection state for bulk operations using Set<string> for O(1) add/remove operations
// Provides checkbox selection state for multiple items with "select all" functionality

'use client'

import { useState, useCallback } from 'react'

/**
 * Return type for useBulkSelection hook
 */
export interface UseBulkSelectionReturn {
  // State
  selectedIds: Set<string>
  selectedCount: number
  isAllSelected: boolean

  // Actions
  toggleSelection: (id: string) => void
  selectAll: (ids: string[]) => void
  clearSelection: () => void
  isSelected: (id: string) => boolean

  // Helpers
  getSelectedArray: () => string[]
}

/**
 * Task T017: Custom hook for managing bulk selection of items
 *
 * Features:
 * - Efficient Set-based tracking (O(1) operations)
 * - Single item toggle
 * - Select/deselect all functionality
 * - Count of selected items
 * - Array conversion for API calls
 * - Membership checking
 *
 * Usage:
 * ```tsx
 * const {
 *   selectedIds,
 *   selectedCount,
 *   toggleSelection,
 *   selectAll,
 *   clearSelection,
 *   isSelected,
 *   getSelectedArray,
 * } = useBulkSelection()
 *
 * // Toggle single item
 * toggleSelection('todo-1')
 *
 * // Select all visible items
 * selectAll(visibleTodoIds)
 *
 * // Use for API call
 * await bulkDeleteTodos(getSelectedArray())
 * ```
 */
export function useBulkSelection(): UseBulkSelectionReturn {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())

  /**
   * Toggle selection of a single item
   * Adds to set if not selected, removes if already selected
   */
  const toggleSelection = useCallback((id: string) => {
    setSelectedIds((prevIds) => {
      const newIds = new Set(prevIds)
      if (newIds.has(id)) {
        newIds.delete(id)
      } else {
        newIds.add(id)
      }
      return newIds
    })
  }, [])

  /**
   * Select all items from provided array
   * Replaces current selection with all provided IDs
   */
  const selectAll = useCallback((ids: string[]) => {
    setSelectedIds(new Set(ids))
  }, [])

  /**
   * Clear all selections
   */
  const clearSelection = useCallback(() => {
    setSelectedIds(new Set())
  }, [])

  /**
   * Check if an item is selected
   * O(1) operation with Set
   */
  const isSelected = useCallback(
    (id: string) => {
      return selectedIds.has(id)
    },
    [selectedIds]
  )

  /**
   * Get selected IDs as array for API calls
   * Useful for passing to bulk operation endpoints
   */
  const getSelectedArray = useCallback(() => {
    return Array.from(selectedIds)
  }, [selectedIds])

  return {
    selectedIds,
    selectedCount: selectedIds.size,
    isAllSelected: selectedIds.size > 0,
    toggleSelection,
    selectAll,
    clearSelection,
    isSelected,
    getSelectedArray,
  }
}
