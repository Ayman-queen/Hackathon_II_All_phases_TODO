// Task T-248: CallToActionSection component
// Final CTA section encouraging signup

import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"

export function CallToActionSection() {
  return (
    <section className="border-t border-gray-200 bg-blue-50 py-20 dark:border-gray-800 dark:bg-blue-950/20 sm:py-32">
      <div className="mx-auto max-w-2xl px-4 text-center sm:px-6 lg:px-8">
        <h3 className="text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
          Ready to get started?
        </h3>

        <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
          Join thousands of users who are already using Evo-TODO to manage their
          tasks efficiently.
        </p>

        <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Button size="lg" asChild className="text-base">
            <a href="/signup">
              Create Free Account
              <ArrowRight className="ml-2 h-4 w-4" />
            </a>
          </Button>
          <Button size="lg" variant="outline" asChild className="text-base">
            <a href="/login">Sign In to Your Account</a>
          </Button>
        </div>
      </div>
    </section>
  )
}
