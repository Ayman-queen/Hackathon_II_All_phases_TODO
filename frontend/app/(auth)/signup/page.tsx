// Task T-229 + T-245: Signup page with Better Auth integration
// Uses complete SignupForm component with full validation and password strength
// Responsive design: Mobile (320px) to Desktop (1920px)

import { SignupForm } from "@/components/auth/SignupForm"

export default function SignupPage() {
  return (
    <div className="w-full h-full">
      <SignupForm />
    </div>
  )
}
