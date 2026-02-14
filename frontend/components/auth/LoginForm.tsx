// Task T-253: Complete LoginForm component with Better Auth integration
// Handles user login with email/password validation
// Integrates with Better Auth client for JWT issuance

"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AlertCircle, Loader2 } from "lucide-react"
import { authClient } from "@/lib/auth-client"
import { logAuthCookies } from "@/lib/utils"

export function LoginForm() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [serverError, setServerError] = useState("")

  // Task T-253: Email validation regex
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  // Task T-253: Form validation
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.email.trim()) {
      newErrors.email = "Email is required"
    } else if (!validateEmail(formData.email)) {
      newErrors.email = "Please enter a valid email address"
    }

    if (!formData.password) {
      newErrors.password = "Password is required"
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Task T-253: Handle login submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setServerError("")

    console.log("[LoginForm] ==================== LOGIN ATTEMPT ====================");
    console.log("[LoginForm] Form submission started");
    console.log("[LoginForm] Email:", formData.email);

    if (!validateForm()) {
      console.log("[LoginForm] Form validation failed");
      return
    }

    setIsLoading(true)
    console.log("[LoginForm] Validation passed, calling authClient.signIn.email()");

    try {
      // Log cookies before login
      logAuthCookies("LoginForm-Before");

      // Call Better Auth signIn function via client
      // This authenticates with the backend and issues a JWT token
      console.log("[LoginForm] Sending login request to Better Auth...");
      const response = await authClient.signIn.email({
        email: formData.email,
        password: formData.password,
      })

      console.log("[LoginForm] Login response received:", {
        hasResponse: !!response,
        responseType: typeof response,
      });

      // Log cookies after successful login
      logAuthCookies("LoginForm-After");

      if (response) {
        // Task T-253: Redirect to todos dashboard after successful login
        // JWT token is automatically stored by Better Auth client
        console.log("[LoginForm] ✓ Login successful, redirecting to /todos");
        console.log("[LoginForm] ===========================================================");
        router.push("/dashboard/todos")
      }
    } catch (err) {
      console.error("[LoginForm] ✗ Login failed with error:", err);
      const errorMessage =
        err instanceof Error ? err.message : "Login failed. Please try again."

      console.error("[LoginForm] Error message:", errorMessage);
      logAuthCookies("LoginForm-Error");

      // Task T-253: Handle specific error cases
      if (
        errorMessage.includes("Invalid") ||
        errorMessage.includes("not found") ||
        errorMessage.includes("401")
      ) {
        setServerError(
          "Invalid email or password. Please check and try again."
        )
      } else if (errorMessage.includes("network")) {
        setServerError(
          "Network error. Please check your connection and try again."
        )
      } else {
        setServerError(errorMessage)
      }
    } finally {
      setIsLoading(false)
      console.log("[LoginForm] Login attempt completed");
    }
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Welcome Back
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Sign in to access your tasks
        </p>
      </div>

      {/* Task T-253: Server error display */}
      {serverError && (
        <div className="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-red-800 dark:text-red-200">
              Login failed
            </p>
            <p className="text-sm text-red-700 dark:text-red-300 mt-1">
              {serverError}
            </p>
          </div>
        </div>
      )}

      {/* Task T-253: Login form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Email field */}
        <div className="space-y-2">
          <Label htmlFor="email" className="text-gray-900 dark:text-gray-100">
            Email Address
          </Label>
          <Input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={formData.email}
            onChange={(e) => {
              setFormData({ ...formData, email: e.target.value })
              if (errors.email) {
                setErrors({ ...errors, email: "" })
              }
            }}
            disabled={isLoading}
            className={errors.email ? "border-red-500" : ""}
            autoComplete="email"
          />
          {errors.email && (
            <p className="text-sm text-red-600 dark:text-red-400">
              {errors.email}
            </p>
          )}
        </div>

        {/* Password field */}
        <div className="space-y-2">
          <Label
            htmlFor="password"
            className="text-gray-900 dark:text-gray-100"
          >
            Password
          </Label>
          <Input
            id="password"
            type="password"
            placeholder="••••••••"
            value={formData.password}
            onChange={(e) => {
              setFormData({ ...formData, password: e.target.value })
              if (errors.password) {
                setErrors({ ...errors, password: "" })
              }
            }}
            disabled={isLoading}
            className={errors.password ? "border-red-500" : ""}
            autoComplete="current-password"
          />
          {errors.password && (
            <p className="text-sm text-red-600 dark:text-red-400">
              {errors.password}
            </p>
          )}
        </div>

        {/* Task T-253: Submit button with loading state */}
        <Button
          type="submit"
          className="w-full"
          disabled={isLoading}
          size="lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Signing in...
            </>
          ) : (
            "Sign In"
          )}
        </Button>
      </form>

      {/* Task T-253: Signup link */}
      <p className="text-center text-sm text-gray-600 dark:text-gray-400 mt-6">
        Don't have an account?{" "}
        <a
          href="/signup"
          className="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 underline-offset-2 hover:underline"
        >
          Create one here
        </a>
      </p>
    </div>
  )
}
