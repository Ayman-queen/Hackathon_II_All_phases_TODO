// Task T-229 + T-253: Login page with Better Auth integration
// Uses complete LoginForm component with full validation
// Responsive design: Mobile (320px) to Desktop (1920px)

import { LoginForm } from "@/components/auth/LoginForm"

export default function LoginPage() {
  return (
    <div className="w-full h-full">
      <LoginForm />
    </div>
  )
}
