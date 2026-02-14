// Task T-234: Custom useAuth hook for authentication state management
// Provides reactive authentication state with Better Auth client
// Used by components to check login status, access user info, and trigger auth actions

"use client"

import { useEffect, useState } from "react"
import { authClient } from "../auth-client"

export interface AuthUser {
  id: string
  email: string
  name?: string
}

export interface AuthSession {
  user: AuthUser
  token: string
  expiresAt?: number
}

export interface UseAuthReturn {
  // State
  user: AuthUser | null
  session: AuthSession | null
  isLoading: boolean
  error: string | null
  isAuthenticated: boolean

  // Methods
  signUp: (email: string, password: string) => Promise<void>
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  refreshSession: () => Promise<void>
}

/**
 * Task T-234: Custom useAuth hook
 * - Manages authentication state using Better Auth client
 * - Auto-fetches session on mount
 * - Provides sign up, sign in, sign out methods
 * - Handles loading and error states
 * - Integrates with API wrapper for JWT token management
 */
export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [session, setSession] = useState<AuthSession | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isAuthd, setIsAuthd] = useState(false)

  // Initial session fetch on mount
  useEffect(() => {
    refreshSession()
  }, [])

  /**
   * Task T-234: Refresh authentication session
   * Called on mount and after auth actions
   */
  const refreshSession = async () => {
    try {
      setIsLoading(true)
      setError(null)

      console.log("[useAuth] Refreshing session...")
      const { data: betterAuthSession, error: sessionError } = await authClient.getSession()

      if (sessionError) {
        throw new Error(sessionError.message || "Failed to load session")
      }

      if (betterAuthSession) {
        console.log("[useAuth] Session found, fetching token...")
        // Get JWT token for API requests
        const { data: tokenData } = await authClient.token()

        const token = tokenData?.token || ""

        setSession({
          user: betterAuthSession.user,
          token: token,
          expiresAt: betterAuthSession.session.expiresAt.getTime(),
        })
        setUser(betterAuthSession.user)
        setIsAuthd(true)
        console.log("[useAuth] ✓ Session authenticated:", {
          userId: betterAuthSession.user?.id,
          hasToken: !!token,
        })
      } else {
        console.log("[useAuth] ✗ No session found")
        setSession(null)
        setUser(null)
        setIsAuthd(false)
      }
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to load session"
      console.error("[useAuth] ✗ Session refresh error:", errorMessage)
      setError(errorMessage)
      setSession(null)
      setUser(null)
      setIsAuthd(false)
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Task T-234: Sign up new user
   * - Creates account with email/password
   * - Automatically fetches new session
   * - Throws error if signup fails
   */
  const handleSignUp = async (email: string, password: string, name: string = "") => {
    try {
      setIsLoading(true)
      setError(null)

      console.log("[useAuth] Signing up user:", email)
      const { error: signupError } = await authClient.signUp.email({
        name: name || email.split("@")[0],
        email: email,
        password: password,
      })

      if (signupError) {
        throw new Error(signupError.message || "Signup failed")
      }

      console.log("[useAuth] ✓ Signup successful, fetching session...")
      // Refresh session after signup
      await refreshSession()
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Signup failed"
      console.error("[useAuth] ✗ Signup error:", errorMessage)
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Task T-234: Sign in user
   * - Authenticates with email/password
   * - Automatically fetches new session
   * - Throws error if signin fails
   */
  const handleSignIn = async (email: string, password: string) => {
    try {
      setIsLoading(true)
      setError(null)

      console.log("[useAuth] Signing in user:", email)
      const { error: signinError } = await authClient.signIn.email({
        email: email,
        password: password,
      })

      if (signinError) {
        throw new Error(signinError.message || "Sign in failed")
      }

      console.log("[useAuth] ✓ Sign in successful, fetching session...")
      // Refresh session after signin
      await refreshSession()
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Sign in failed"
      console.error("[useAuth] ✗ Sign in error:", errorMessage)
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Task T-234: Sign out user
   * - Clears local session
   * - Resets authentication state
   */
  const handleSignOut = async () => {
    try {
      setIsLoading(true)
      setError(null)

      console.log("[useAuth] Signing out user...")
      const { error: signoutError } = await authClient.signOut()

      if (signoutError) {
        console.warn("[useAuth] Sign out returned error:", signoutError)
      }

      // Clear local state
      console.log("[useAuth] ✓ Signed out, clearing local state")
      setSession(null)
      setUser(null)
      setIsAuthd(false)
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Sign out failed"
      console.error("[useAuth] ✗ Sign out error:", errorMessage)
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  return {
    user,
    session,
    isLoading,
    error,
    isAuthenticated: isAuthd,
    signUp: handleSignUp,
    signIn: handleSignIn,
    signOut: handleSignOut,
    refreshSession,
  }
}
