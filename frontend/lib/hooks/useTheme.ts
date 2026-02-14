// Task T-236: Custom useTheme hook for theme management
// Provides reactive theme state with next-themes integration
// Handles dark/light mode toggle with localStorage persistence and system preference detection

"use client"

import { useEffect, useState } from "react"
import { useTheme as useNextTheme } from "next-themes"

export type Theme = "light" | "dark" | "system"

export interface UseThemeReturn {
  // State
  theme: Theme | undefined
  isDark: boolean
  mounted: boolean

  // Methods
  setTheme: (theme: Theme) => void
  toggleTheme: () => void
}

/**
 * Task T-236: Custom useTheme hook
 * - Wraps next-themes useTheme hook
 * - Provides simplified API for theme switching
 * - Handles hydration with mounted flag
 * - Provides isDark boolean for conditional rendering
 * - Persists theme preference to localStorage
 * - Respects system OS preference
 */
export function useTheme(): UseThemeReturn {
  const { theme: nextTheme, setTheme: setNextTheme } = useNextTheme()
  const [mounted, setMounted] = useState(false)

  // Mark as mounted to avoid hydration mismatch
  useEffect(() => {
    setMounted(true)
  }, [])

  /**
   * Task T-236: Determine if current theme is dark
   * Considers: explicit theme setting, system preference
   */
  const isDark = mounted
    ? nextTheme === "dark" ||
      (nextTheme === "system" &&
        typeof window !== "undefined" &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    : false

  /**
   * Task T-236: Set theme and persist to localStorage
   * - "light": Force light mode
   * - "dark": Force dark mode
   * - "system": Use OS preference
   */
  const setTheme = (theme: Theme) => {
    setNextTheme(theme)
  }

  /**
   * Task T-236: Toggle between light and dark mode
   * Respects current setting
   */
  const toggleTheme = () => {
    if (nextTheme === "dark") {
      setTheme("light")
    } else if (nextTheme === "light") {
      setTheme("dark")
    } else {
      // If system, toggle to opposite of current
      setTheme(isDark ? "light" : "dark")
    }
  }

  return {
    theme: nextTheme as Theme | undefined,
    isDark,
    mounted,
    setTheme,
    toggleTheme,
  }
}
