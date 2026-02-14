// Task T-245: Complete SignupForm component with Better Auth integration
// Handles user registration with email/password validation
// Integrates with Better Auth client for JWT issuance

"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { AlertCircle, Loader2, Check } from "lucide-react"
import { authClient } from "@/lib/auth-client"
import { logAuthCookies } from "@/lib/utils"

export function SignupForm() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [serverError, setServerError] = useState("")
  const [passwordStrength, setPasswordStrength] = useState<"weak" | "medium" | "strong">("weak")

  // Task T-245: Email validation regex
  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  // Task T-245: Check password strength
  const checkPasswordStrength = (password: string) => {
    if (password.length < 8) {
      setPasswordStrength("weak")
      return
    }
    if (password.length < 12 || !/[^a-zA-Z0-9]/.test(password)) {
      setPasswordStrength("medium")
      return
    }
    setPasswordStrength("strong")
  }

  // Task T-245: Form validation
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = "Name is required"
    }

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

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = "Please confirm your password"
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Task T-245: Handle signup submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setServerError("")

    console.log("[SignupForm] ==================== SIGNUP ATTEMPT ====================");
    console.log("[SignupForm] Form submission started");
    console.log("[SignupForm] Name:", formData.name);
    console.log("[SignupForm] Email:", formData.email);

    if (!validateForm()) {
      console.log("[SignupForm] Form validation failed");
      return
    }

    setIsLoading(true)
    console.log("[SignupForm] Validation passed, calling authClient.signUp.email()");

    try {
      // Log cookies before signup
      logAuthCookies("SignupForm-Before");

      // Call Better Auth signUp function via client
      // This creates account and issues a JWT token
      console.log("[SignupForm] Sending signup request to Better Auth...");

      const response = await authClient.signUp.email({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      })

      console.log("[SignupForm] Signup response received:", {
        hasResponse: !!response,
        responseType: typeof response,
      });

      // Log cookies after successful signup
      logAuthCookies("SignupForm-After");

      if (response) {
        // Task T-245: Redirect to todos dashboard after successful signup
        // JWT token is automatically stored by Better Auth client
        console.log("[SignupForm] ✓ Signup successful, redirecting to /todos");
        console.log("[SignupForm] ===========================================================");
        router.push("/dashboard/todos")
      } else {
        console.warn("[SignupForm] No response from signup");
        logAuthCookies("SignupForm-NoResponse");
        setServerError("Signup failed. Please try again.")
      }
    } catch (err) {
      console.error("[SignupForm] ✗ Signup failed with error:", err);
      const errorMessage =
        err instanceof Error ? err.message : "Signup failed. Please try again."

      console.error("[SignupForm] Error message:", errorMessage);
      logAuthCookies("SignupForm-Error");

      // Task T-245: Handle specific error cases
      if (errorMessage.includes("already exists") || errorMessage.includes("409")) {
        setServerError(
          "Email already registered. Please log in instead or use a different email."
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
    }
  }

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Create Account
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Join us to manage your tasks efficiently
        </p>
      </div>

      {/* Task T-245: Server error display */}
      {serverError && (
        <div className="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-red-800 dark:text-red-200">
              Signup failed
            </p>
            <p className="text-sm text-red-700 dark:text-red-300 mt-1">
              {serverError}
            </p>
          </div>
        </div>
      )}

      {/* Task T-245: Signup form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Name field */}
        <div className="space-y-2">
          <Label htmlFor="name" className="text-gray-900 dark:text-gray-100">
            Full Name
          </Label>
          <Input
            id="name"
            type="text"
            placeholder="John Doe"
            value={formData.name}
            onChange={(e) => {
              setFormData({ ...formData, name: e.target.value })
              if (errors.name) {
                setErrors({ ...errors, name: "" })
              }
            }}
            disabled={isLoading}
            className={errors.name ? "border-red-500" : ""}
          />
          {errors.name && (
            <p className="text-sm text-red-600 dark:text-red-400">
              {errors.name}
            </p>
          )}
        </div>

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
              const password = e.target.value
              setFormData({ ...formData, password })
              checkPasswordStrength(password)
              if (errors.password) {
                setErrors({ ...errors, password: "" })
              }
            }}
            disabled={isLoading}
            className={errors.password ? "border-red-500" : ""}
            autoComplete="new-password"
          />

          {/* Task T-245: Password strength indicator */}
          {formData.password && (
            <div className="flex items-center gap-2 text-xs">
              <div className="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all ${
                    passwordStrength === "weak"
                      ? "w-1/3 bg-red-500"
                      : passwordStrength === "medium"
                      ? "w-2/3 bg-yellow-500"
                      : "w-full bg-green-500"
                  }`}
                />
              </div>
              <span
                className={
                  passwordStrength === "weak"
                    ? "text-red-600 dark:text-red-400"
                    : passwordStrength === "medium"
                    ? "text-yellow-600 dark:text-yellow-400"
                    : "text-green-600 dark:text-green-400"
                }
              >
                {passwordStrength === "weak"
                  ? "Weak"
                  : passwordStrength === "medium"
                  ? "Medium"
                  : "Strong"}
              </span>
            </div>
          )}

          {errors.password && (
            <p className="text-sm text-red-600 dark:text-red-400">
              {errors.password}
            </p>
          )}

          {/* Task T-245: Password requirements */}
          {formData.password && (
            <div className="space-y-1 mt-3 text-xs text-gray-600 dark:text-gray-400">
              <div className="flex items-center gap-2">
                {formData.password.length >= 8 ? (
                  <Check className="h-4 w-4 text-green-600 dark:text-green-400" />
                ) : (
                  <div className="h-4 w-4 rounded-full border border-gray-300 dark:border-gray-600" />
                )}
                <span>At least 8 characters</span>
              </div>
            </div>
          )}
        </div>

        {/* Confirm password field */}
        <div className="space-y-2">
          <Label
            htmlFor="confirmPassword"
            className="text-gray-900 dark:text-gray-100"
          >
            Confirm Password
          </Label>
          <Input
            id="confirmPassword"
            type="password"
            placeholder="••••••••"
            value={formData.confirmPassword}
            onChange={(e) => {
              setFormData({ ...formData, confirmPassword: e.target.value })
              if (errors.confirmPassword) {
                setErrors({ ...errors, confirmPassword: "" })
              }
            }}
            disabled={isLoading}
            className={errors.confirmPassword ? "border-red-500" : ""}
            autoComplete="new-password"
          />
          {errors.confirmPassword && (
            <p className="text-sm text-red-600 dark:text-red-400">
              {errors.confirmPassword}
            </p>
          )}
        </div>

        {/* Task T-245: Submit button with loading state */}
        <Button
          type="submit"
          className="w-full"
          disabled={isLoading}
          size="lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Creating account...
            </>
          ) : (
            "Create Account"
          )}
        </Button>
      </form>

      {/* Task T-245: Login link */}
      <p className="text-center text-sm text-gray-600 dark:text-gray-400 mt-6">
        Already have an account?{" "}
        <a
          href="/login"
          className="font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 underline-offset-2 hover:underline"
        >
          Log in here
        </a>
      </p>
    </div>
  )
}
