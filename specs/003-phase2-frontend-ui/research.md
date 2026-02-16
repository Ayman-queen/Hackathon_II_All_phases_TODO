# Research: Phase II Frontend UI (Phase 0)

**Date**: 2025-12-30
**Feature**: 003-phase2-frontend-ui
**Purpose**: Resolve all technical unknowns and establish best practices for frontend implementation

---

## Better Auth Client Configuration & JWT Plugin

### Research Question
How to configure Better Auth on a Next.js frontend to enable JWT token retrieval and storage for automatic API request authentication?

### Decision
**Use Better Auth's `createAuthClient` from `better-auth/react` with the `jwtClient()` plugin**

### Rationale
- Better Auth provides official React integration via `/react` export specifically for Next.js
- `jwtClient()` plugin handles JWT issuance, storage, and retrieval automatically
- Native integration means no manual OAuth2 implementation
- Hooks-based API (`useSession()`) integrates naturally with React components
- Official MCP support ensures up-to-date guidance

### Implementation Pattern
```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3000",
  plugins: [jwtClient()],
});

// Hook usage in components
export function useSession() {
  return authClient.useSession();
}
```

### Alternatives Considered
1. **Custom OAuth2 Implementation**: Too complex, reinvents wheel, security risks
2. **Auth.js / NextAuth.js**: Different authentication framework, not compatible with Better Auth backend
3. **Manual JWT handling with fetch**: No session state management, error-prone token refresh

### Trade-offs
- **Pro**: Secure, maintained, official MCP support
- **Con**: Dependency on Better Auth service availability
- **Mitigation**: Better Auth is already deployed for backend; use official MCP for guidance

---

## JWT Token Retrieval & Storage Strategy

### Research Question
What is the best way to retrieve and store JWT tokens after login/signup, and make them available to all API calls?

### Decision
**Store JWT in localStorage with `TokenManager` utility that proactively checks expiration and refreshes tokens 5 minutes before expiry**

### Rationale
- **localStorage**: Persists across page reloads, accessible from any component, supports synchronous retrieval
- **Proactive Refresh**: Checking expiration before each API call prevents 401 errors mid-operation
- **5-min buffer**: Allows time for token refresh before actual expiry (tokens typically 15-60 min lifetime)
- **TokenManager singleton**: Centralized logic, avoids duplicate refresh calls

### Implementation Pattern
```typescript
// lib/token-manager.ts
export class TokenManager {
  private static REFRESH_THRESHOLD = 5 * 60 * 1000; // 5 minutes

  static getValidToken(): Promise<string | null> {
    const token = localStorage.getItem("better_auth_jwt");
    if (!token) return null;

    // Decode JWT and check expiration (without verification)
    const payload = JSON.parse(atob(token.split('.')[1]));
    const expiresAt = payload.exp * 1000;

    // If expiring soon, refresh
    if (expiresAt - Date.now() < this.REFRESH_THRESHOLD) {
      return this.refreshToken();
    }

    return Promise.resolve(token);
  }

  private static async refreshToken(): Promise<string | null> {
    const { data } = await authClient.token(); // Better Auth refresh endpoint
    if (data?.token) {
      localStorage.setItem("better_auth_jwt", data.token);
      return data.token;
    }
    return null;
  }

  static clearToken(): void {
    localStorage.removeItem("better_auth_jwt");
  }
}
```

### Alternatives Considered
1. **httpOnly Cookies**: More secure (no JS access), but can't be accessed from components, requires server-side management
2. **sessionStorage**: Lost when tab closes, not ideal for SPA with page refreshes
3. **Memory-only storage**: Lost on page reload, forces re-login every time
4. **Lazy refresh on 401**: Simpler code, but causes failed API calls and poor UX

### Trade-offs
- **Pro**: Persistent, accessible, no failed requests
- **Con**: Slightly lower security (JS-accessible)
- **Mitigation**: Refresh logic ensures tokens are fresh; combine with HTTPS-only transmission and CORS

---

## API Client Implementation for JWT Attachment

### Research Question
How to automatically attach JWT tokens to all API requests without repeating header logic in every component?

### Decision
**Create custom `api-client.ts` wrapper around fetch() that retrieves JWT from TokenManager and intercepts all requests/responses**

### Rationale
- **Centralization**: Single place to manage JWT attachment, error handling, retries
- **Separation of Concerns**: API logic separate from component logic
- **Consistency**: All API calls follow same error handling, validation, retry logic
- **Native fetch**: No additional dependencies (axios, got, etc.), built-in to browsers

### Implementation Pattern
```typescript
// lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // 1. Get fresh JWT token (with automatic refresh if needed)
  const token = await TokenManager.getValidToken();

  // 2. Build request with JWT in Authorization header
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  // 3. Handle errors
  if (response.status === 401) {
    TokenManager.clearToken();
    window.location.href = "/login"; // Redirect to login
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "API request failed");
  }

  // 4. Return response data
  return response.json();
}

// Export convenience methods
export const api = {
  getTodos: () => apiRequest<Todo[]>("/api/todos"),
  createTodo: (data) => apiRequest<Todo>("/api/todos", { method: "POST", body: JSON.stringify(data) }),
  // ... other methods
};
```

### Alternatives Considered
1. **Axios with interceptors**: More powerful, but adds dependency; fetch is sufficient
2. **React Query / SWR**: Better for data fetching with caching, but adds complexity; start with hooks
3. **Manual headers in each component**: Code duplication, error-prone, hard to maintain
4. **Context API for token distribution**: Introduces prop drilling, unnecessary complexity

### Trade-offs
- **Pro**: Minimal dependencies, full control, easy to debug
- **Con**: Manual fetch wrapper vs. established library
- **Mitigation**: Wrapper is ~100 lines of code, covers 95% of use cases; can upgrade to React Query later if needed

---

## Protected Routes Implementation

### Research Question
How to protect routes so unauthenticated users are redirected to login and can't access `/todo`, `/profile`, etc.?

### Decision
**Use Next.js middleware (`middleware.ts`) for early redirection + optional ProtectedRoute HOC component for granular control**

### Rationale
- **Middleware**: Runs at edge/server, catches unauthenticated requests before component loads (faster)
- **Two-layer approach**: Defense-in-depth; middleware is primary, component wrapper is secondary
- **App Router native**: No additional libraries needed, built into Next.js 16+
- **Granular control**: Can protect specific routes or all routes in `(protected)` group

### Implementation Pattern
```typescript
// middleware.ts (root of frontend/)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Check if user has valid JWT token
  const token = request.cookies.get("better_auth_jwt")?.value;

  // Redirect unauthenticated users to login
  if (!token && request.nextUrl.pathname.startsWith("/(protected)")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/(protected)/:path*"],
};
```

```typescript
// components/ProtectedRoute.tsx (optional component wrapper)
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isPending } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isPending, router]);

  if (isPending) return <LoadingSpinner />;
  if (!isAuthenticated) return null;

  return <>{children}</>;
}
```

### Alternatives Considered
1. **Middleware only**: Simpler, but can't show loading state or graceful redirect in component
2. **Component wrapper only**: More flexibility, but slower (component loads before redirecting)
3. **API route guards**: Only checks at API layer, allows HTML to load first (poor UX)
4. **Library solutions (next-auth guards)**: Adds dependencies, unnecessary for our use case

### Trade-offs
- **Pro**: Fast, secure, integrates with app router
- **Con**: Two-layer approach adds slight code duplication
- **Mitigation**: Duplication is minimal (~10 lines per layer); clear separation of concerns

---

## State Management for Todo CRUD Operations

### Research Question
How to manage todo list state, API calls, optimistic updates, and error recovery without Redux/Zustand?

### Decision
**Use custom React hooks (`useTodos`, `useAuthenticatedApi`) with local state (useState) and optimistic updates with rollback on error**

### Rationale
- **React hooks are native**: No external dependencies, simpler for small app
- **Optimistic updates**: Immediate UI feedback while API call completes in background
- **Error recovery**: Rollback state on API failure and show error message
- **Sufficient for todo app**: Single user, linear operations, no complex state trees

### Implementation Pattern
```typescript
// hooks/useTodos.ts
export function useTodos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filter, setFilter] = useState<'ALL' | 'PENDING' | 'COMPLETED'>('ALL');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { api } = useAuthenticatedApi();

  // Load todos from backend
  const loadTodos = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await api.getTodos();
      setTodos(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load todos");
    } finally {
      setIsLoading(false);
    }
  }, [api]);

  // Create todo with optimistic update
  const createTodo = useCallback(async (newTodo: Omit<Todo, 'id' | 'createdAt' | 'updatedAt'>) => {
    const tempId = crypto.randomUUID();
    const optimisticTodo = { ...newTodo, id: tempId, createdAt: new Date(), updatedAt: new Date() };

    // Optimistically update UI
    setTodos((prev) => [optimisticTodo, ...prev]);
    setError(null);

    try {
      // Call API
      const created = await api.createTodo(newTodo);

      // Replace optimistic todo with server response
      setTodos((prev) => prev.map((t) => (t.id === tempId ? created : t)));
      return created;
    } catch (err) {
      // Rollback on error
      setTodos((prev) => prev.filter((t) => t.id !== tempId));
      setError(err instanceof Error ? err.message : "Failed to create todo");
      throw err;
    }
  }, [api]);

  // Similarly for updateTodo, deleteTodo, etc.

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  return { todos, filter, setFilter, isLoading, error, createTodo, updateTodo, deleteTodo, loadTodos };
}
```

### Alternatives Considered
1. **React Query / SWR**: Powerful caching and sync, but adds dependency and complexity
2. **Redux**: Industry standard, but overkill for todo app; too much boilerplate
3. **Zustand**: Lightweight state manager, good middle ground, but unnecessary for this scope
4. **Context API**: Fine for state distribution, but not for cache management

### Trade-offs
- **Pro**: No dependencies, simple to understand, full control
- **Con**: Manual state management, no automatic cache invalidation
- **Mitigation**: Upgrade to React Query/SWR later if app grows; start simple

---

## Theming Architecture (Light/Dark Mode)

### Research Question
How to implement light/dark mode with persistence, system preference detection, and no flash of wrong theme (FOUC)?

### Decision
**Use `next-themes` library with localStorage persistence + CSS class-based switching**

### Rationale
- **next-themes solves FOUC**: Injects script to detect theme before React hydration
- **System detection**: Auto-detects OS theme preference if user hasn't set preference
- **localStorage persistence**: User preference saved and restored on return visits
- **Tailwind integration**: Works seamlessly with Tailwind's `dark:` utility classes
- **Zero dependencies needed for theme logic**: Library handles all complexity

### Implementation Pattern
```typescript
// app/layout.tsx (root layout)
import { ThemeProvider } from "next-themes";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}

// components/ThemeToggle.tsx
import { useTheme } from "next-themes";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="rounded-lg bg-gray-200 dark:bg-gray-800 p-2"
    >
      {theme === "dark" ? "🌙" : "☀️"}
    </button>
  );
}
```

### Alternatives Considered
1. **Manual localStorage + useEffect**: Works but causes FOUC (flash of wrong theme), poor UX
2. **CSS variables only**: Flexible but no persistence, loses user preference
3. **Context API**: Manual implementation, still causes FOUC
4. **Tailwind's dark mode with class**: Good, but doesn't persist or detect system preference

### Trade-offs
- **Pro**: Solves FOUC, system detection, minimal code
- **Con**: Additional dependency
- **Mitigation**: `next-themes` is lightweight (5KB), widely used, well-maintained

---

## Form Validation & Input Handling

### Research Question
How to handle form validation, submission, and error display for login, signup, and todo forms?

### Decision
**Use React Hook Form + Zod for type-safe, performant form handling with client-side validation**

### Rationale
- **React Hook Form**: Minimal re-renders (only on change, not per keystroke), hooks-based API
- **Zod**: Type-safe schema validation, TypeScript integration, human-readable error messages
- **Client + Server**: Validate on client (UX), re-validate on server (security)
- **Both already installed**: Dependencies already in package.json

### Implementation Pattern
```typescript
// lib/validation.ts
import { z } from "zod";

export const TodoSchema = z.object({
  title: z.string().min(1, "Title is required").max(255),
  description: z.string().optional(),
  priority: z.enum(["HIGH", "MEDIUM", "LOW"]).default("MEDIUM"),
  dueDate: z.date().optional(),
});

export const LoginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

// components/TodoForm.tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

export function TodoForm({ onSubmit }: { onSubmit: (data: z.infer<typeof TodoSchema>) => Promise<void> }) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(TodoSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("title")} placeholder="Todo title" />
      {errors.title && <span>{errors.title.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save"}
      </button>
    </form>
  );
}
```

### Alternatives Considered
1. **Formik**: More boilerplate, slower re-renders, less modern
2. **Native HTML validation**: No TypeScript support, poor error handling
3. **Form state in useState**: Manual validation, error-prone, verbose

### Trade-offs
- **Pro**: Type-safe, performant, minimal code
- **Con**: Two dependencies (already installed)

---

## Summary: Technology Choices Validated

| Decision | Chosen | Validated | Confidence |
|----------|--------|-----------|-----------|
| Better Auth client | `createAuthClient` + `jwtClient()` | ✅ Official React integration | High |
| JWT storage | localStorage with proactive refresh | ✅ Solves persistence + refresh | High |
| API client | Custom fetch wrapper | ✅ Centralized, minimal overhead | High |
| Protected routes | Middleware + component wrapper | ✅ Defense-in-depth, fast | High |
| State management | React hooks (useState) + optimistic updates | ✅ Sufficient for todo app | Medium-High |
| Theming | next-themes library | ✅ Solves FOUC + system detection | High |
| Forms | React Hook Form + Zod | ✅ Type-safe, performant | High |
| API contracts | REST with JWT Bearer token | ✅ Standard, compatible with FastAPI | High |

---

## Next Steps (Phase 1)

1. **Create data-model.md**: Detailed TypeScript interfaces for User, Todo, Session, Error types
2. **Create contracts/**: API contract specifications (endpoints, request/response schemas)
3. **Create quickstart.md**: Development setup instructions, running the app, API testing
4. **Generate Phase 2 tasks.md**: Break research into actionable implementation tasks mapped to spec requirements
