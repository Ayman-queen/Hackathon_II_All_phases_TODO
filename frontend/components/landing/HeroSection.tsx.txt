// Task T-245: HeroSection component for landing page
// Displays main headline, subheading, value proposition, and CTAs

import { Button } from "@/components/ui/button"
import { ArrowRight, CheckCircle2 } from "lucide-react"

export function HeroSection() {
  return (
    <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 lg:py-32">
      <div className="text-center">
        <h2 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-5xl lg:text-6xl">
          Master Your Tasks with{" "}
          <span className="text-blue-600 dark:text-blue-400">Evo-TODO</span>
        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600 dark:text-gray-300">
          A powerful, secure, and intuitive task management platform built for teams
          and individuals who want to get things done faster.
        </p>

        {/* Value Proposition */}
        <div className="mx-auto mt-8 max-w-2xl space-y-3 text-left sm:text-center">
          <div className="flex items-center gap-3 justify-center">
            <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
            <span className="text-gray-700 dark:text-gray-200">
              Secure authentication with JWT tokens
            </span>
          </div>
          <div className="flex items-center gap-3 justify-center">
            <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
            <span className="text-gray-700 dark:text-gray-200">
              Smart filtering and sorting for better productivity
            </span>
          </div>
          <div className="flex items-center gap-3 justify-center">
            <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
            <span className="text-gray-700 dark:text-gray-200">
              Beautiful dark mode and responsive design
            </span>
          </div>
        </div>

        {/* CTAs */}
        <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Button size="lg" asChild className="text-base">
            <a href="/signup">
              Get Started Free
              <ArrowRight className="ml-2 h-4 w-4" />
            </a>
          </Button>
          <Button size="lg" variant="outline" asChild className="text-base">
            <a href="/login">Sign In</a>
          </Button>
        </div>
      </div>
    </section>
  )
}
