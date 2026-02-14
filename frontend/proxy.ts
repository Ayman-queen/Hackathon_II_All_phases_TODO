// Task T008: Better Auth session middleware
// Validates authentication before route access to prevent unauthenticated content flashing
// Uses cookie-based checks for optimistic redirects (recommended for Next.js 15 with edge runtime)
// Ensures all protected routes require valid session cookie

import { NextRequest, NextResponse } from 'next/server'
import { getSessionCookie } from 'better-auth/cookies'

/**
 * Protected routes that require authentication
 * Routes not in this list are publicly accessible
 */
const PROTECTED_ROUTES = [
  '/dashboard',
]

/**
 * Task T008: Middleware for session validation using cookie checks
 *
 * IMPORTANT: This middleware runs on the Edge Runtime (default for Next.js 15)
 * and CANNOT make database calls. We use getSessionCookie() for optimistic
 * redirects only. Full session validation happens in each page/route via
 * server components or server actions.
 *
 * Better Auth Session Cookie:
 * - Cookie name: `better-auth.session_token` (default, prefixed with `better-auth.`)
 * - Signed with BETTER_AUTH_SECRET
 * - Set by Better Auth nextCookies plugin
 *
 * Flow:
 * 1. Check if route is protected
 * 2. If protected, check for session cookie (optimistic check only)
 * 3. If no cookie, redirect to /login (prevent FOUC)
 * 4. If cookie exists, allow access (full validation done server-side)
 *
 * Security Note:
 * - This is NOT a security boundary (checking for cookie presence only)
 * - Always validate session on the server for protected actions
 * - Full session validation must happen in pages/routes using auth.api.getSession()
 */
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Check if route is protected
  const isProtectedRoute = PROTECTED_ROUTES.some(route =>
    pathname.startsWith(route)
  )

  // Skip middleware for public routes
  if (!isProtectedRoute) {
    return NextResponse.next()
  }

  // For protected routes: check for session cookie
  // This is an optimistic check - the actual validation happens server-side
  try {
    const sessionCookie = getSessionCookie(request)

    if (!sessionCookie) {
      // No session cookie found - redirect to login
      // Preserve the original URL for post-login redirect
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('from', pathname)
      return NextResponse.redirect(loginUrl)
    }

    // Session cookie exists - allow access
    // The actual session validation will happen in the page using auth.api.getSession()
    return NextResponse.next()
  } catch (error) {
    // Error checking cookie - this shouldn't happen, but be safe
    console.error('[Middleware] Error checking session cookie:', error)
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('from', pathname)
    return NextResponse.redirect(loginUrl)
  }
}

/**
 * Configure which routes the middleware applies to
 * Apply to dashboard and its subroutes
 */
export const config = {
  matcher: [
    /*
     * Match protected routes:
     * - /dashboard and all subroutes
     *
     * Exclude:
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico
     * - public assets
     * - /api/auth (auth API routes are always public)
     * - /login, /signup (auth pages are public)
     */
    '/dashboard/:path*',
  ],
}
