# Frontend Architecture Documentation

## Overview

The Evo-TODO frontend is a Next.js 16+ application with TypeScript, providing a modern, responsive UI for task management and a real-time chat interface to interact with an AI agent. It uses Better Auth for authentication.

**Tech Stack:**
- **Framework**: Next.js 16+ (App Router, Server Components)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS 3.4+
- **UI Components**: Shadcn UI (Radix UI + Tailwind)
- **Theme**: next-themes 0.4+ (dark/light mode)
- **Auth**: Better Auth 1.4+ (JWT + JWKS)
- **Forms**: React Hook Form 7.50+
- **Icons**: Lucide React 0.562+
- **State Management**: React Hooks (useState, useEffect, custom hooks)
- **Notifications**: Sonner 2.0+

## New Features in Phase 3

- **Real-time Chat Interface**: A new page under the dashboard for real-time chat with an AI agent.
- **`useChat` Hook**: A custom hook to manage the state of the chat, including messages and user input.
- **Scrollable Chat Area**: A new UI component for a scrollable chat window.

## Project Structure

```
frontend/
├── app/
│   ├── (auth)/                    # Authentication route group
│   │   ├── layout.tsx           # Auth layout
│   │   ├── login/              # Login page
│   │   │   └── page.tsx
│   │   └── signup/             # Signup page
│   │       └── page.tsx
│   ├── dashboard/                # Dashboard route group (protected)
│   │   ├── layout.tsx           # Dashboard layout with sidebar/navbar
│   │   ├── page.tsx            # Dashboard home (placeholder)
│   │   ├── todos/             # Tasks page
│   │   │   └── page.tsx
│   │   └── chat/              # Chat page
│   │       └── page.tsx
│   ├── (protected)/             # Protected route group (redirect)
│   │   ├── layout.tsx           # Protected layout
│   │   └── page.tsx            # Redirect to /dashboard/todos
│   ├── api/
│   │   ├── auth/[...all]/route.ts  # Better Auth server handler
│   │   └── chat/[userId]/route.ts # Chat API route
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                # Landing page
│   └── globals.css              # Global styles
├── components/
│   ├── auth/                    # Authentication components
│   │   ├── LoginForm.tsx
│   │   └── SignupForm.tsx
│   ├── common/                  # Common UI components
│   │   ├── EmptyState.tsx
│   │   └── LoadingSpinner.tsx
│   ├── dashboard/               # Dashboard-specific components
│   │   ├── DashboardUI.tsx       # Dashboard layout wrapper
│   │   ├── Navbar.tsx
│   │   └── Sidebar.tsx
│   ├── landing/                 # Landing page components
│   │   ├── CallToActionSection.tsx
│   │   ├── FeatureHighlights.tsx
│   │   ├── Footer.tsx
│   │   ├── HeroSection.tsx
│   │   ├── LandingNavBar.tsx
│   │   └── SocialProof.tsx
│   ├── todos/                   # Task management components
│   │   ├── BulkActions.tsx
│   │   ├── TaskForm.tsx
│   │   ├── TaskItem.tsx
│   │   ├── TaskList.tsx
│   │   └── TasksContainer.tsx
│   └── ui/                      # Shadcn UI base components
│       ├── alert.tsx
│       ├── button.tsx
│       ├── input.tsx
│       ├── label.tsx
│       └── scroll-area.tsx
├── lib/
│   ├── api.ts                   # API client with JWT injection
│   ├── auth-client.ts            # Better Auth client configuration
│   ├── auth.ts                  # Auth utilities
│   ├── hooks/                   # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useBulkSelection.ts
│   │   ├── useTheme.ts
│   │   ├── useTodos.ts          # Main todo state management hook
│   │   └── useChat.ts           # Chat state management hook
│   ├── types/                   # TypeScript types
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── todo.ts
│   └── utils.ts                 # Utility functions
├── middleware.ts                  # Route protection middleware
├── next.config.js                 # Next.js configuration
├── tailwind.config.ts             # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Dependencies
```

## Configuration

### Environment Variables (.env)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth URL
NEXT_PUBLIC_AUTH_URL=http://localhost:3000

# Node environment
NODE_ENV=development
```

### Next.js Configuration

- **App Router**: Modern file-based routing
- **Server Components**: Default (opt-in client with "use client")
- **Edge Runtime**: Middleware runs on Edge
- **API Routes**: Server-side API endpoints (Better Auth handler)

## Authentication Flow

### Better Auth Integration

1. **Server Handler** (`app/api/auth/[...all]/route.ts`)
   - Better Auth instance running on `/api/auth`
   - Handles: signup, signin, signout, session, token

2. **Client** (`lib/auth-client.ts`)
   - `createAuthClient()` with jwtClient plugin
   - Methods: `signIn.email()`, `signUp.email()`, `signOut()`
   - JWT token retrieval via `authClient.token()`

3. **Middleware Protection** (`middleware.ts`)
   - Protected routes: `/dashboard` and subroutes
   - Checks for session cookie
   - Redirects unauthenticated to `/login`
   - Matcher: `/dashboard/:path*`

4. **API Integration** (`lib/api.ts`)
   - Automatic JWT token injection
   - Session cookie via `credentials: "include"`
   - Error handling: 401 → redirect to login

### Auth Flow Diagram

```
User enters credentials
    ↓
LoginForm/SignupForm
    ↓
authClient.signIn.email() / authClient.signUp.email()
    ↓
Better Auth Server (/api/auth)
    ↓
JWT Token Generated (EdDSA/Ed25519)
    ↓
Token Stored (Cookie + Client State)
    ↓
Redirect to /dashboard/todos
    ↓
API Requests (Authorization: Bearer <token>)
    ↓
Backend validates JWT via JWKS
    ↓
Session active, user can access todos
```

## Routing Structure

### Public Routes

| Route | Component | Auth Required |
|-------|-----------|---------------|
| `/` | Landing page | No |
| `/login` | LoginForm | No |
| `/signup` | SignupForm | No |

### Protected Routes

| Route | Component | Layout | Description |
|-------|-----------|--------|-------------|
| `/dashboard` | DashboardPage | DashboardUI | Placeholder page |
| `/dashboard/todos` | DashboardTodosPage | DashboardUI | Main tasks page |
| `/dashboard/chat` | ChatPage | DashboardUI | Real-time chat with AI agent |

### Route Groups

**`(auth)` Group** (`app/(auth)/`)
- Layout for authentication pages
- Routes: `/login`, `/signup`
- No authentication required

**`(protected)` Group** (`app/(protected)/`)
- Protected root page
- **Auto-redirects to `/dashboard/todos`
- Acts as fallback for authenticated users

**`dashboard` Group** (`app/dashboard/`)
- Layout: DashboardUI (Sidebar + Navbar)
- Routes: `/`, `/todos`, `/chat`
- Requires authentication (validated in layout)

## Components Architecture

### Auth Components

#### LoginForm (`components/auth/LoginForm.tsx`)
- Email/password form
- Client-side validation
- Error display
- Loading state
- Redirects to `/dashboard/todos` on success

#### SignupForm (`components/auth/SignupForm.tsx`)
- Name/email/password/confirm form
- Password strength indicator
- Email validation regex
- Password requirements checklist
- Redirects to `/dashboard/todos` on success

### Dashboard Components

#### DashboardUI (`components/dashboard/DashboardUI.tsx`)
- Sidebar (collapsible)
- Navbar (mobile menu toggle)
- Responsive design
- Theme-aware styling

#### Navbar (`components/dashboard/Navbar.tsx`)
- Mobile menu toggle
- User info display
- Logout button

#### Sidebar (`components/dashboard/Sidebar.tsx`)
- Navigation links
- Active route highlighting
- Mobile close handler

### Todo Components

#### TasksContainer (`components/todos/TasksContainer.tsx`)
- Orchestrates task management
- Manages create/edit modal
- Integrates TaskForm, TaskList, BulkActions
- Refreshes tasks on CRUD operations

#### TaskForm (`components/todos/TaskForm.tsx`)
- Create/edit form
- Title and description fields
- Validation
- Submit handler

#### TaskList (`components/todos/TaskList.tsx`)
- Displays filtered/sorted tasks
- Empty state handling
- Task items with edit/delete

#### TaskItem (`components/todos/TaskItem.tsx`)
- Single task display
- Checkbox for completion
- Edit/delete actions
- Status styling

#### BulkActions (`components/todos/BulkActions.tsx`)
- Bulk delete/select all
- Selection count display
- Action buttons

### Chat Components

#### ChatPage (`app/dashboard/chat/page.tsx`)
- Main component for the chat interface.
- Uses the `useChat` hook to manage state.
- Renders the chat history and input form.

### Landing Components

All landing page components use gradient backgrounds and consistent styling:
- **HeroSection**: Value proposition
- **FeatureHighlights**: Feature cards
- **SocialProof**: Testimonials/stats
- **CallToActionSection**: CTA buttons
- **LandingNavBar**: Public navbar
- **Footer**: Site footer

## State Management

### useTodos Hook (`lib/hooks/useTodos.ts`)

**Purpose**: Centralized todo state management

**Returns**:
```typescript
{
  // State
  todos: Todo[]                    // All todos
  filteredTodos: Todo[]           // Filtered and sorted
  isLoading: boolean                // Loading state
  error: string | null             // Error message

  // Filter & Sort
  currentFilter: TodoFilter          // "all" | "pending" | "completed"
  currentSort: TodoSort             // "title" | "priority" | "dueDate" | "createdAt"
  setFilter: (filter) => void
  setSort: (sort) => void

  // CRUD Operations
  createTodo: (data) => Promise<Todo>
  getTodoById: (id) => Promise<Todo>
  updateTodo: (id, data) => Promise<Todo>  // Status toggle (PATCH)
  updateTodoFields: (id, data) => Promise<Todo>  // Fields update (PUT)
  deleteTodo: (id) => Promise<void>
  refreshTodos: () => Promise<void>
}
```

**Features**:
- Fetches todos on mount
- Filters by status (all/pending/completed)
- Sorts by multiple fields
- Transforms backend snake_case to frontend camelCase
- Updates `is_complete` → `status` mapping

### useChat Hook (`lib/hooks/useChat.ts`)

**Purpose**: Manages the state of the real-time chat.

**Returns**:
```typescript
{
  messages: ChatMessage[];
  input: string;
  handleInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
}
```

### useTheme Hook (`lib/hooks/useTheme.ts`)

**Purpose**: Theme management with system preference

**Returns**:
```typescript
{
  theme: "light" | "dark" | "system" | undefined
  isDark: boolean
  mounted: boolean
  setTheme: (theme) => void
  toggleTheme: () => void
}
```

**Features**:
- Wraps next-themes `useTheme()`
- Handles hydration (mounted flag)
- Determines `isDark` from theme + system preference
- Persists to localStorage

### useAuth Hook (`lib/hooks/useAuth.ts`)

**Purpose**: Authentication state management

**Features**:
- Session validation
- Login/logout handlers
- User info access

### useBulkSelection Hook (`lib/hooks/useBulkSelection.ts`)

**Purpose**: Bulk task selection management

**Returns**:
```typescript
{
  selectedIds: Set<string>
  toggleSelection: (id) => void
  clearSelection: () => void
  selectAll: (ids) => void
  deselectAll: () => void
}
```

## API Integration

### API Client (`lib/api.ts`)

**Base URL**: `NEXT_PUBLIC_API_URL` (default: `http://localhost:8000`)

**Features**:
- Automatic JWT token injection
- Session cookie inclusion (`credentials: "include"`)
- Request timeout (10 seconds)
- Error handling (401, 403, 404, 500)
- Response transformation

**Methods**:
```typescript
apiGet<T>(endpoint: string): Promise<ApiResponse<T>>
apiPost<T>(endpoint: string, body: any): Promise<ApiResponse<T>>
apiPut<T>(endpoint: string, body: any): Promise<ApiResponse<T>>
apiPatch<T>(endpoint: string, body: any): Promise<ApiResponse<T>>
apiDelete<T>(endpoint: string): Promise<ApiResponse<T>>
apiGetPublic<T>(endpoint: string): Promise<ApiResponse<T>>
verifyApiConnectivity(): Promise<{connected, tokenIncluded, error?}>
```

**JWT Token Flow**:
1. `authClient.token()` fetches JWT from Better Auth
2. Token injected as `Authorization: Bearer <token>` header
3. Session cookie included automatically
4. 401 errors trigger redirect to `/login`

**Error Handling**:
| Status | Action |
|--------|--------|
| 401 | Redirect to `/login`, call `authClient.signOut()` |
| 403 | Show "insufficient permissions" error |
| 404 | Show "not found" error |
| 500 | Show "server error" message |
| Timeout | Show "request timeout" message |

## Theme System

### Dark/Light Mode

**Library**: next-themes 0.4+

**Configuration** (`app/layout.tsx`):
```tsx
<ThemeProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
  enableColorScheme={false}
  disableTransitionOnChange
>
```

**Attribute Strategy**: Class-based (adds `dark` class to `<html>`)

**Theme Switching**:
- `light`: Force light mode
- `dark`: Force dark mode
- `system`: Use OS preference

**CSS Classes**:
```css
/* Light mode (default) */
bg-white text-gray-900

/* Dark mode (applied by ThemeProvider) */
dark:bg-gray-950 dark:text-gray-50
```

**Hydration Handling**:
- `mounted` flag in `useTheme()` hook
- Prevents mismatch between server and client

## Data Types

### Todo Types (`lib/types/todo.ts`)

```typescript
export interface Todo {
  id: string
  userId: string
  title: string
  description?: string
  status: "pending" | "completed"
  priority: "low" | "medium" | "high"
  dueDate?: string
  createdAt: string
  updatedAt: string
}

export type TodoFilter = "all" | "pending" | "completed"
export type TodoSort = "title" | "priority" | "dueDate" | "createdAt"
```

### Backend to Frontend Transformation

**Backend Format** (snake_case):
```json
{
  "id": "...",
  "user_id": "...",
  "title": "...",
  "description": "...",
  "is_complete": false,
  "priority": "...",
  "due_date": "...",
  "created_at": "...",
  "updated_at": "..."
}
```

**Frontend Format** (camelCase):
```typescript
{
  id: "...",
  userId: "...",
  title: "...",
  description: "...",
  status: "pending" | "completed",  // is_complete → status
  priority: "low" | "medium" | "high",
  dueDate: "...",                   // due_date → dueDate
  createdAt: "...",                 // created_at → createdAt
  updatedAt: "..."                  // updated_at → updatedAt
}
```

## UI Components (Shadcn)

### Installed Components

- **Button**: Customizable button with variants
- **Input**: Text, email, password inputs
- **Label**: Form labels
- **Alert**: Alert display component
- **ScrollArea**: For scrollable content areas.

### Styling Approach

**Tailwind CSS**:
- Utility-first approach
- Responsive design (mobile-first)
- Dark mode with `dark:` prefix
- Consistent color scales (gray, blue, red, green)

**Color Palette**:
- **Primary**: Blue (`blue-600` light, `blue-400` dark)
- **Success**: Green (`green-600` light, `green-400` dark)
- **Error**: Red (`red-600` light, `red-400` dark)
- **Background**: White/Gray (`white` light, `gray-950` dark)
- **Text**: Gray (`gray-900` light, `gray-50` dark)

## Middleware

### Auth Middleware (`middleware.ts`)

**Purpose**: Protect dashboard routes

**Protected Routes**:
- `/dashboard`
- All subroutes under `/dashboard`

**Flow**:
1. Check if route is protected
2. If protected, check for session cookie
3. No cookie → Redirect to `/login?from={pathname}`
4. Has cookie → Allow access (full validation in layout)

**Matcher**:
```typescript
export const config = {
  matcher: ['/dashboard/:path*'],
}
```

**Important**: Middleware runs on Edge Runtime, cannot make DB calls. Only checks for cookie presence.

## Better Auth Integration

### Server Handler (`app/api/auth/[...all]/route.ts`)

**Purpose**: Provide Better Auth endpoints on frontend

**Endpoints**:
- `/api/auth/sign-up` - Email/password signup
- `/api/auth/sign-in` - Email/password signin
- `/api/auth/sign-out` - Logout
- `/api/auth/session` - Get current session
- `/api/auth/token` - Get JWT token (via jwtClient plugin)

**Configuration**:
- Base URL: `NEXT_PUBLIC_AUTH_URL` (default: `http://localhost:3000`)
- JWT Plugin enabled: `jwtClient()`
- Cookie handling: Automatically managed

### Client (`lib/auth-client.ts`)

```typescript
const authClient = createAuthClient({
  baseURL: NEXT_PUBLIC_AUTH_URL,
  plugins: [jwtClient()]
})

export const useSession = () => authClient.useSession()
export const signIn = authClient.signIn
export const signUp = authClient.signUp
export const signOut = authClient.signOut
```

## Routing Issues Found

### Issues During Review

1. **Dashboard Root Redirect** (`app/(protected)/page.tsx`)
   - **File**: `app/(protected)/page.tsx`
   - **Issue**: Automatically redirects to `/dashboard/todos` on mount
   - **Impact**: Users accessing `/dashboard` or `/` after login get redirected
   - **Recommendation**: Keep redirect but improve UX or redirect to `/dashboard` instead

2. **Unused Dashboard Page** (`app/dashboard/page.tsx`)
   - **File**: `app/dashboard/page.tsx`
   - **Issue**: Contains placeholder content, not used
   - **Recommendation**: Either make it a proper dashboard overview or redirect to `/dashboard/todos`

3. **Route Confusion**:
   - `/dashboard` → placeholder page
   - `/dashboard/todos` → actual tasks page
   - `/` (protected) → redirects to `/dashboard/todos`
   - This creates multiple paths to the same destination

## Performance Optimizations

1. **Client Components**: Only where necessary (forms, interactive)
2. **Server Components**: Default (pages, layouts)
3. **Suspense**: Loading states for dynamic content
4. **Code Splitting**: Automatic with App Router
5. **Image Optimization**: Next.js automatic optimization
6. **Font Optimization**: Next.js automatic optimization

## Testing

**Framework**: Jest 30+

**Configuration**: `jest.config.js`

**Test Files**:
- Component tests (not present in current structure)
- Hook tests (not present)
- Integration tests (not present)

**Status**: Test suite needs to be created

## Deployment

### Development

```bash
npm run dev
# Runs on http://localhost:3000
```

### Build

```bash
npm run build
# Creates .next/ production build
```

### Production Start

```bash
npm start
# Runs production server
```

### Docker

```bash
docker build -t evo-todo-frontend .
docker run -p 3000:3000 evo-todo-frontend
```

## Dependencies (package.json)

### Core Dependencies

- `next@^16.0.0` - React framework
- `react@^18.3.1` - UI library
- `react-dom@^18.3.1` - DOM rendering
- `better-auth@^1.4.10` - Authentication
- `next-themes@^0.4.6` - Theme management
- `@radix-ui/*` - Headless UI components
- `shadcn-ui@^0.9.5` - UI component library
- `lucide-react@^0.562.0` - Icons

### Form & State

- `react-hook-form@^7.50.1` - Form handling
- `@hookform/resolvers@^3.3.4` - Form resolvers
- `nanostores@^0.10.3` - Lightweight state management

### Utilities

- `zod@^3.22.4` - Schema validation
- `clsx@^2.0.0` - Class name utility
- `class-variance-authority@^0.7.0` - Variant management
- `tailwind-merge@^2.2.0` - Tailwind merging

### Notifications

- `sonner@^2.0.7` - Toast notifications

### Database

- `pg@^8.16.3` - PostgreSQL client (for direct DB access if needed)

## Important Notes

1. **Authentication Flow**:
   - Better Auth handles signup/signin/logout
   - JWT tokens issued via Better Auth server
   - Tokens injected in API requests automatically
   - Session cookies used for middleware protection

2. **Route Protection**:
   - Middleware checks for session cookie
   - Dashboard layout validates actual session
   - 401 errors trigger redirect to login

3. **Data Transformation**:
   - Backend uses snake_case (`is_complete`, `created_at`)
   - Frontend uses camelCase (`status`, `createdAt`)
   - Transformation in `useTodos()` hook

4. **Theme Support**:
   - Class-based approach (no CSS variables)
   - Dark mode: `dark:` prefix in Tailwind
   - System preference supported

5. **Development Only**:
   - Extensive console.log statements for debugging
   - Should be removed for production

6. **Unused Code**:
   - `app/(protected)/page.tsx` redirects immediately
   - `app/dashboard/page.tsx` is placeholder
   - Consider consolidating routing structure
