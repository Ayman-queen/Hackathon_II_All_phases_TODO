# Quickstart: JWT Authentication Implementation

**Feature**: JWT Authentication Integration (Phase 2.2)
**Last Updated**: 2026-01-01

## Overview

This guide provides step-by-step instructions for implementing JWT authentication with Better Auth (frontend) and FastAPI (backend). At the end of this quickstart, you will have:

1. Better Auth configured with JWT plugin
2. Frontend API client that automatically attaches JWT tokens
3. FastAPI middleware that verifies JWT tokens
4. All 6 API endpoints protected with user isolation

**Time to complete**: ~2-3 hours (excluding testing)

---

## Prerequisites

### Frontend (Next.js)
- Node.js 18+ installed
- Next.js 16+ project with Better Auth already configured
- Package: `better-auth` with plugins support
- Package: `jose` or similar for JWT utilities (optional, for debugging)

### Backend (FastAPI)
- Python 3.10+ installed
- FastAPI project scaffolded
- Package: `fastapi` 0.100+
- Package: `python-jose[cryptography]` for JWT verification
- Package: `pydantic` for request/response validation
- Package: `httpx` for async HTTP calls (for JWKS fetching)

### Shared
- PostgreSQL database (via Neon or local)
- Better Auth instance running on `http://localhost:3000`
- FastAPI instance running on `http://localhost:8000`

---

## Phase 1: Frontend - Better Auth JWT Configuration

### Step 1: Add JWT Plugin to Better Auth

**File**: `src/auth.ts` (or equivalent)

```typescript
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: {
    type: "postgres",
    url: process.env.DATABASE_URL,
  },
  plugins: [
    jwt({
      jwks: {
        keyPairConfig: {
          alg: "EdDSA",
          crv: "Ed25519"
        }
      },
      jwt: {
        // Configure JWT payload to include user ID and email
        definePayload: ({ user }) => {
          return {
            sub: user.id,
            email: user.email,
          }
        },
        expirationTime: "7d", // Default to 7 days
      }
    })
  ],
  trustedOrigins: [
    process.env.FRONTEND_URL || "http://localhost:3000"
  ],
})
```

### Step 2: Run Better Auth Migration

Run the migration to add JWT tables to your database:

```bash
npx @better-auth/cli migrate
```

This creates the `jwks` table for storing signing keys.

### Step 3: Add JWT Client Plugin

**File**: `src/auth-client.ts` (or equivalent)

```typescript
import { createAuthClient } from "better-auth/react"
import { jwtClient } from "better-auth/client/plugins"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3000",
  plugins: [
    jwtClient()
  ]
})
```

### Step 4: Create API Client with Token Attachment

**File**: `src/lib/api-client.ts`

```typescript
export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api") {
    this.baseUrl = baseUrl
  }

  private getToken(): string {
    // Retrieve token from localStorage
    if (typeof window !== "undefined") {
      return localStorage.getItem("jwt_token") || ""
    }
    return ""
  }

  private async ensureValidToken(): Promise<void> {
    // Check if token exists, if not fetch new one
    if (!this.getToken()) {
      const { data } = await authClient.token()
      if (data?.token) {
        localStorage.setItem("jwt_token", data.token)
      }
    }
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    await this.ensureValidToken()

    const token = this.getToken()
    if (!token) {
      // No token available, redirect to login
      if (typeof window !== "undefined") {
        window.dispatchEvent(new Event("auth:unauthorized"))
      }
      throw new Error("No authentication token available")
    }

    const url = `${this.baseUrl}${endpoint}`
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("jwt_token")
      if (typeof window !== "undefined") {
        window.dispatchEvent(new Event("auth:unauthorized"))
      }
      throw new Error("Authentication required")
    }

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "API request failed")
    }

    return response.json()
  }

  // Task endpoints
  async listTasks(userId: string): Promise<any[]> {
    const response = await this.request(`/${userId}/tasks`)
    return response.data || []
  }

  async createTask(userId: string, title: string, description?: string): Promise<any> {
    return this.request(`/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify({ title, description }),
    })
  }

  async getTask(userId: string, taskId: string): Promise<any> {
    return this.request(`/${userId}/tasks/${taskId}`)
  }

  async updateTask(userId: string, taskId: string, updates: any): Promise<any> {
    return this.request(`/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    })
  }

  async deleteTask(userId: string, taskId: string): Promise<void> {
    await this.request(`/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    })
  }

  async toggleTaskCompletion(userId: string, taskId: string): Promise<any> {
    return this.request(`/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    })
  }
}

export const apiClient = new ApiClient()
```

### Step 5: Store Token After Login

**File**: `src/components/login-form.tsx` (or equivalent)

```typescript
import { authClient } from "@/lib/auth-client"
import { useRouter } from "next/navigation"

export function LoginForm() {
  const router = useRouter()

  async function handleLogin(email: string, password: string) {
    try {
      const response = await authClient.signIn.email({
        email,
        password,
      })

      if (response.data) {
        // Fetch JWT token after successful login
        const { data: tokenData } = await authClient.token()
        if (tokenData?.token) {
          localStorage.setItem("jwt_token", tokenData.token)
        }

        // Redirect to dashboard
        router.push("/dashboard")
      }
    } catch (error) {
      console.error("Login failed:", error)
    }
  }

  return (
    // ... form JSX
  )
}
```

### Step 6: Handle Token Expiration

Listen for auth errors and prompt re-authentication:

```typescript
import { useEffect } from "react"
import { useRouter } from "next/navigation"

export function useAuthErrorHandler() {
  const router = useRouter()

  useEffect(() => {
    function handleAuthError() {
      localStorage.removeItem("jwt_token")
      router.push("/login?expired=true")
    }

    window.addEventListener("auth:unauthorized", handleAuthError)
    return () => window.removeEventListener("auth:unauthorized", handleAuthError)
  }, [router])
}
```

---

## Phase 2: Backend - FastAPI JWT Verification

### Step 1: Install Dependencies

```bash
pip install fastapi python-jose[cryptography] httpx pydantic
```

### Step 2: Configure JWT Verification

**File**: `src/auth/jwt.py`

```python
from typing import Optional
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import jwt, JWTError
import httpx
import json
from functools import lru_cache

# Configuration
BETTER_AUTH_BASE_URL = "http://localhost:3000"
JWKS_URL = f"{BETTER_AUTH_BASE_URL}/api/auth/jwks"
ALGORITHM = "EdDSA"

security = HTTPBearer()

# Cache JWKS to reduce HTTP calls
@lru_cache(maxsize=1)
async def get_jwks():
    """Fetch JWKS from Better Auth"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(JWKS_URL)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch JWKS"
        )

async def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """
    Verify JWT token and extract user ID
    Returns the user ID from the token
    """
    token = credentials.credentials

    try:
        # Decode without verification first to get the kid
        unverified_header = jwt.get_unverified_header(token)

        # Fetch JWKS
        jwks = await get_jwks()

        # Find the matching key
        key = None
        for jwk in jwks.get("keys", []):
            if jwk.get("kid") == unverified_header.get("kid"):
                key = jwk
                break

        if not key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key"
            )

        # Verify and decode token
        payload = jwt.decode(
            token,
            json.dumps(key),  # Convert key to JSON for jose
            algorithms=[ALGORITHM],
            options={"verify_signature": True}
        )

        # Extract user ID from token
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims"
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_user_ownership(path_user_id: str, token_user_id: str) -> None:
    """
    Verify that the user ID in the URL matches the authenticated user
    Raises 403 Forbidden if they don't match
    """
    if path_user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
```

### Step 3: Create Pydantic Models

**File**: `src/models/task.py`

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    completed: Optional[bool] = None

class Task(TaskBase):
    id: str
    user_id: str
    completed: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Step 4: Create API Routes

**File**: `src/routes/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from src.auth.jwt import verify_token, verify_user_ownership
from src.models.task import Task, TaskCreate, TaskUpdate
from src.database import get_db

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

# Helper to get task by ID and verify ownership
async def get_user_task(
    user_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
) -> Task:
    verify_user_ownership(user_id, current_user_id)

    stmt = select(Task).where(
        (Task.id == task_id) & (Task.user_id == current_user_id)
    )
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.get("")
async def list_tasks(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
):
    """List all tasks for the authenticated user"""
    verify_user_ownership(user_id, current_user_id)

    stmt = select(Task).where(Task.user_id == current_user_id)
    result = await db.execute(stmt)
    tasks = result.scalars().all()

    return {"data": tasks, "count": len(tasks)}

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
):
    """Create a new task"""
    verify_user_ownership(user_id, current_user_id)

    db_task = Task(
        id=str(uuid.uuid4()),
        user_id=current_user_id,
        title=task.title,
        description=task.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)

    return db_task

@router.get("/{task_id}")
async def get_task(
    user_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
):
    """Get a specific task"""
    task = await get_user_task(user_id, task_id, db, current_user_id)
    return task

@router.put("/{task_id}")
async def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
):
    """Update a task"""
    task = await get_user_task(user_id, task_id, db, current_user_id)

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
):
    """Delete a task"""
    task = await get_user_task(user_id, task_id, db, current_user_id)

    await db.delete(task)
    await db.commit()

    return None

@router.patch("/{task_id}/complete")
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token),
):
    """Toggle task completion status"""
    task = await get_user_task(user_id, task_id, db, current_user_id)

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return task
```

### Step 5: Register Routes in FastAPI App

**File**: `src/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import tasks

app = FastAPI(
    title="Evo-TODO API",
    version="2.2.0",
    description="JWT-authenticated task management API"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://evo-todo.com",   # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include task routes
app.include_router(tasks.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

---

## Phase 3: Testing the Integration

### Test 1: Frontend Login

```bash
# In browser console
const response = await fetch("http://localhost:3000/api/auth/signin", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email: "test@example.com", password: "password" })
})
const data = await response.json()
console.log(data)
```

### Test 2: Fetch JWT Token

```typescript
const { data } = await authClient.token()
console.log("JWT Token:", data.token)
localStorage.setItem("jwt_token", data.token)
```

### Test 3: API Request with Token

```typescript
const apiClient = new ApiClient()
const tasks = await apiClient.listTasks("user-id-from-jwt")
console.log("Tasks:", tasks)
```

### Test 4: Invalid Token Handling

```typescript
localStorage.setItem("jwt_token", "invalid.token.here")
try {
  await apiClient.listTasks("user-id")
} catch (error) {
  console.log("Expected 401 error:", error)
}
```

---

## Environment Variables

### Frontend (.env.local)

```
NEXT_PUBLIC_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend (.env)

```
DATABASE_URL=postgresql://user:password@localhost/evo_todo
BETTER_AUTH_BASE_URL=http://localhost:3000
```

---

## Checklist

- [ ] Better Auth JWT plugin configured and migrated
- [ ] JWT client plugin added to auth-client
- [ ] API client created with token attachment
- [ ] Token stored in localStorage after login
- [ ] Token expiration handling implemented
- [ ] FastAPI JWT verification middleware created
- [ ] All 6 API endpoints protected with user ownership check
- [ ] CORS configured for frontend origin
- [ ] End-to-end test: login → create task → fetch tasks → update task → delete task
- [ ] Error handling: test 401 and 403 responses
- [ ] Token refresh: test expired token handling

---

## Troubleshooting

### Token Not Being Attached to Requests
- Verify token is stored in localStorage: `console.log(localStorage.getItem("jwt_token"))`
- Check Authorization header in network tab: should show `Bearer <token>`
- Ensure fetch wrapper in ApiClient is being called

### 401 Unauthorized from Backend
- Verify JWKS is accessible: `curl http://localhost:3000/api/auth/jwks`
- Check token expiration: decode JWT and check `exp` claim
- Verify algorithm matches: should be EdDSA for Better Auth JWT plugin

### 403 Forbidden
- Confirm user_id in URL matches JWT token's `sub` claim
- Verify task belongs to authenticated user in database

### CORS Errors
- Add frontend URL to `trustedOrigins` in Better Auth config
- Check CORS headers in response: should include `Access-Control-Allow-Origin`

---

## Next Steps

1. Implement token refresh strategy (refresh tokens)
2. Add token revocation/blacklist for logout
3. Set up audit logging for authentication events
4. Implement rate limiting on login attempts
5. Add 2FA (two-factor authentication) support

---

## Related Documentation

- Better Auth JWT Plugin: https://better-auth.com/docs/plugins/jwt
- Better Auth Client: https://better-auth.com/docs/client
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- python-jose: https://python-jose.readthedocs.io/
- OpenAPI Contract: See `contracts/api-contract.openapi.json`
