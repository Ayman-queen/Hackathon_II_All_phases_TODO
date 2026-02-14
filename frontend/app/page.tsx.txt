// Task T-201 + T-245-T-252: Landing page for Phase II - User Story 0
// Route: /
// Unauthenticated users see this onboarding page, then redirected to /login or /signup
// Features: Hero section, value proposition, feature highlights, CTAs, responsive design, dark mode

import { LandingNavBar } from "@/components/landing/LandingNavBar"
import { HeroSection } from "@/components/landing/HeroSection"
import { FeatureHighlights } from "@/components/landing/FeatureHighlights"
import { SocialProof } from "@/components/landing/SocialProof"
import { CallToActionSection } from "@/components/landing/CallToActionSection"
import { Footer } from "@/components/landing/Footer"

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-gray-950 dark:to-slate-900">
      <LandingNavBar />
      <HeroSection />
      <FeatureHighlights />
      <SocialProof />
      <CallToActionSection />
      <Footer />
    </main>
  )
}
