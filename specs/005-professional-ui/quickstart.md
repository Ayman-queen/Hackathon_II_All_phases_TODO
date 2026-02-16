# Quick Start Guide: Professional UI & Advanced CRUD

**Feature**: 005-professional-ui
**Branch**: `005-professional-ui`
**Last Updated**: 2026-01-02

## 5-Minute Overview

Build a task management dashboard with:
- Professional UI using Shadcn/UI components
- Immediate feedback with Next.js `useOptimistic` hook
- Light/dark theme support with `next-themes`
- Bulk operations (delete, mark complete)
- Toast notifications for all actions
- Better Auth integration for user sessions

---

## Architecture at a Glance

```
Frontend (Next.js 16 App Router)
  ↓
  Components:
    - Dashboard Layout (Navbar + Sidebar)
    - Task List with checkboxes
    - Task Form (add/edit modal)
    - Delete Confirmation Dialog
    - Priority Selector Popover
  ↓
  State Management:
    - useOptimistic() → immediate UI updates
    - useState(Set<string>) → bulk selection
    - next-themes → theme persistence
  ↓
  API Layer:
    - Fetch client with JWT headers
    - Promise.all for batch operations

Backend (FastAPI - existing)
  ↓
  Endpoints:
    - GET /api/tasks (list)
    - POST /api/tasks (create)
    - PUT /api/tasks/{id} (update)
    - DELETE /api/tasks/{id} (delete)
    - POST /api/tasks/bulk-delete (batch)
    - POST /api/tasks/bulk-complete (batch)
```

---

## Key Implementation Patterns

### 1. Immediate UI Updates with useOptimistic

**When user creates a task:**

```typescript
const [optimisticTasks, updateOptimisticTasks] = useOptimistic(
  initialTasks,
  (state, action) => {
    // Handle add/update/delete actions
    switch (action.type) {
      case 'add': return [...state, action.task]
      // ...
    }
  }
)

const handleCreateTask = async (formData) => {
  // 1. Update UI immediately (optimistic)
  updateOptimisticTasks({
    type: 'add',
    task: { id: `temp-${Date.now()}`, ...formData }
  })

  // 2. Call server action
  const result = await createTaskServerAction(formData)

  // 3. React handles rollback if it fails
  if (!result.success) {
    showErrorToast(result.error)
  }
}
```

**Result**: User sees task appear instantly, no 500ms wait.

### 2. Bulk Operations with Set + Promise.all

**User selects multiple tasks:**

```typescript
const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())

const toggleSelection = (id: string) => {
  const newSet = new Set(selectedIds)
  newSet.has(id) ? newSet.delete(id) : newSet.add(id)
  setSelectedIds(newSet)
}

// Bulk delete
const handleBulkDelete = async () => {
  // Confirm first
  setDeleteDialogOpen(true)
}

const confirmBulkDelete = async () => {
  // Option A: If backend has batch endpoint
  const response = await fetch('/api/tasks/bulk-delete', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({ task_ids: Array.from(selectedIds) })
  })

  // Option B: Client-side batching (if backend doesn't have batch)
  // await Promise.all(
  //   Array.from(selectedIds).map(id => deleteTask(id))
  // )

  setSelectedIds(new Set())
  showSuccessToast(`Deleted ${selectedIds.size} tasks`)
}
```

**Result**: 100 tasks deleted in ~3 seconds with parallelization.

### 3. Theme Toggle with next-themes

**Setup in root layout:**

```typescript
// app/layout.tsx
import { ThemeProvider } from 'next-themes'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

**Use in component:**

```typescript
import { useTheme } from 'next-themes'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  return (
    <Button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      {theme === 'dark' ? '🌙' : '☀️'}
    </Button>
  )
}
```

**Result**: Theme persists across sessions via localStorage.

### 4. Modal Dialogs with Shadcn

**Delete confirmation:**

```typescript
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog'

const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)

<Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Delete Task?</DialogTitle>
    </DialogHeader>
    <p>This action cannot be undone.</p>
    <DialogFooter>
      <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
      <Button variant="destructive" onClick={handleDelete}>Delete</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

**Result**: Accessible modal with focus management, keyboard navigation (Escape key).

### 5. Inline Selections with Popover

**Priority selector:**

```typescript
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

const [popoverOpen, setPopoverOpen] = useState(false)
const [priority, setPriority] = useState('Medium')

<Popover open={popoverOpen} onOpenChange={setPopoverOpen}>
  <PopoverTrigger asChild>
    <Button variant="outline">{priority}</Button>
  </PopoverTrigger>
  <PopoverContent>
    {['High', 'Medium', 'Low'].map(p => (
      <Button
        key={p}
        onClick={() => {
          setPriority(p)
          setPopoverOpen(false)
        }}
      >
        {p}
      </Button>
    ))}
  </PopoverContent>
</Popover>
```

**Result**: Non-modal selection menu, closes after choice.

### 6. Toast Notifications with Sonner

**Show success/error:**

```typescript
import { toast } from 'sonner'

const handleCreateTask = async (formData) => {
  try {
    await createTask(formData)
    toast.success('Task created successfully')
  } catch (error) {
    toast.error(`Failed: ${error.message}`)
  }
}
```

**Result**: Stacked, auto-dismissing notifications.

---

## Development Workflow

### Phase 1: Setup (1-2 hours)

- [ ] Create Next.js App Router structure
- [ ] Install dependencies: Shadcn/UI, next-themes, Sonner, Zod, React Hook Form
- [ ] Setup ThemeProvider in root layout
- [ ] Setup Better Auth session check middleware
- [ ] Create basic Navbar, Sidebar, Layout components

### Phase 2: Task CRUD (2-3 hours)

- [ ] Create TaskList component with checkboxes
- [ ] Create TaskForm modal (add/edit)
- [ ] Create TaskItem component with edit/delete buttons
- [ ] Implement useOptimistic hook for immediate feedback
- [ ] Setup fetch API client with JWT headers
- [ ] Integrate with backend endpoints

### Phase 3: Bulk & Advanced (1-2 hours)

- [ ] Create BulkActions component (bulk delete/complete buttons)
- [ ] Implement Set-based selection state
- [ ] Create BulkDeleteDialog (confirmation with count)
- [ ] Setup batch operations (Promise.all or backend endpoints)
- [ ] Add bulk operation success/error notifications

### Phase 4: Polish & Testing (1-2 hours)

- [ ] Accessibility audit (keyboard nav, WCAG 2.1 AA)
- [ ] Performance testing (load time <2s, operations <500ms)
- [ ] Component tests (Jest + RTL)
- [ ] E2E test scenarios
- [ ] Responsive design testing (mobile/tablet/desktop)

---

## File Structure to Create

```
frontend/src/
├── app/
│   ├── layout.tsx                      # Root layout + theme provider
│   ├── dashboard/
│   │   ├── layout.tsx                  # Dashboard layout
│   │   ├── page.tsx                    # Dashboard page
│   │   └── tasks/
│   │       └── page.tsx                # Task list page
├── components/
│   ├── dashboard/
│   │   ├── Navbar.tsx                  # User profile + logout + theme toggle
│   │   ├── Sidebar.tsx                 # Navigation
│   │   └── TaskDashboard.tsx           # Main container
│   ├── tasks/
│   │   ├── TaskList.tsx                # Task list with selection
│   │   ├── TaskItem.tsx                # Single task
│   │   ├── TaskForm.tsx                # Add/edit modal
│   │   ├── DeleteConfirmDialog.tsx     # Single delete
│   │   ├── BulkDeleteDialog.tsx        # Bulk delete
│   │   ├── PriorityPopover.tsx         # Priority selector
│   │   └── TaskNotification.tsx        # Sonner toast integration
│   └── common/
│       ├── ThemeToggle.tsx             # Theme switcher
│       └── LoadingSpinner.tsx          # Loading state
├── services/
│   ├── api.ts                          # Fetch client with JWT
│   ├── tasks.ts                        # Task API methods
│   └── auth.ts                         # Better Auth hooks
├── hooks/
│   ├── useTaskActions.ts               # useOptimistic wrapper
│   ├── useBulkSelection.ts             # Selection state
│   └── useTheme.ts                     # next-themes integration
└── types/
    └── tasks.ts                        # TypeScript interfaces
```

---

## Testing Checklist

### Functional Tests
- [ ] Create task appears immediately (optimistic)
- [ ] Edit task updates immediately
- [ ] Delete task requires confirmation dialog
- [ ] Bulk delete works for 5+ tasks
- [ ] Bulk complete marks tasks as done
- [ ] All operations show success/error toast

### Accessibility Tests
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Dialog focus management (focus inside on open)
- [ ] Screen reader announces dialog titles
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] Touch targets >= 44x44px on mobile

### Performance Tests
- [ ] Dashboard page loads in <2 seconds
- [ ] Single task CRUD completes in <500ms
- [ ] Bulk operations on 100 tasks in <3 seconds
- [ ] Theme toggle is instant
- [ ] No layout shift on theme change

### Responsive Design Tests
- [ ] Mobile (320px): Hamburger menu, single column
- [ ] Tablet (640px): Sidebar visible, task grid layout
- [ ] Desktop (1024px+): Full layout with all features

---

## Common Pitfalls to Avoid

1. **Forgetting JWT header**: All API calls must include `Authorization: Bearer {token}`
2. **Not filtering by user_id**: Backend must validate user_id from JWT, not trust client
3. **Missing accessibility attributes**: Use Shadcn components (built on Radix UI)
4. **Slow bulk operations**: Use Promise.all, not sequential loops
5. **Theme flash on load**: Use next-themes to prevent FOUC
6. **Orphaned optimistic updates**: Always handle error rollback
7. **No confirmation before delete**: Always show Shadcn Dialog

---

## Links & References

- **Specification**: specs/005-professional-ui/spec.md
- **Research**: specs/005-professional-ui/research.md
- **Data Model**: specs/005-professional-ui/data-model.md
- **API Contracts**: specs/005-professional-ui/contracts/task-api.openapi.yaml
- **Tasks**: specs/005-professional-ui/tasks.md (generated by `/sp.tasks`)

- **External Docs**:
  - Next.js 16: https://nextjs.org/docs
  - React 19 useOptimistic: https://react.dev/reference/react/useOptimistic
  - Shadcn/UI: https://ui.shadcn.com
  - next-themes: https://github.com/pacocoursey/next-themes
  - Sonner: https://sonner.emilkowal.ski/
  - WCAG 2.1 AA: https://www.w3.org/WAI/WCAG21/quickref/

---

## Questions?

Refer to the appropriate document:
- **"What should this look like?"** → spec.md (user stories, acceptance scenarios)
- **"Why this technology choice?"** → research.md (decisions & rationale)
- **"What's the database schema?"** → data-model.md (entities, relationships)
- **"What endpoints do I need?"** → contracts/task-api.openapi.yaml (API spec)
- **"How do I build this?"** → tasks.md (step-by-step implementation tasks)

Good luck! 🚀
