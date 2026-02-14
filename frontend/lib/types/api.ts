// Task T-239: TypeScript types for API responses and errors
// Reference: plan.md API contracts

/**
 * Standard API response wrapper
 */
export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

/**
 * Standard error response from backend
 * Follows FastAPI error format
 */
export interface ErrorResponse {
  detail: string;
  status_code?: number;
  message?: string;
}

/**
 * HTTP status codes used in the application
 */
export enum HttpStatus {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  INTERNAL_ERROR = 500,
}
