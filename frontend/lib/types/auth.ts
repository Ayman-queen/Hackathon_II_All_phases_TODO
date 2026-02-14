// Task T-239: TypeScript types for authentication entities
// Reference: plan.md data model

/**
 * User entity from Better Auth
 * Represents an authenticated user in the system
 */
export interface User {
  id: string;
  email: string;
  name?: string;
  emailVerified: boolean;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Authentication session state
 * Represents the current user's authentication status
 */
export interface AuthSession {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: Error | null;
}

/**
 * Authentication error response from Better Auth
 */
export interface AuthError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

/**
 * Sign up/Sign in request payload
 */
export interface AuthCredentials {
  email: string;
  password: string;
  name?: string;
}

/**
 * Authentication response from Better Auth endpoints
 */
export interface AuthResponse {
  user: User;
  token: string;
}
