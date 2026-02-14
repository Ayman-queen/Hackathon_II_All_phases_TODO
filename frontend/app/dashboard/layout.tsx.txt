import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { DashboardUI } from '@/components/dashboard/DashboardUI'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  try {
    const session = await auth.api.getSession({
      headers: await headers(),
    })

    if (!session) {
      console.warn('[Dashboard Layout] No valid session found, redirecting to login')
      redirect('/login')
    }

    console.log('[Dashboard Layout] ✓ Session validated:', {
      userId: session.user.id,
      userEmail: session.user.email,
      sessionExpiresAt: session.session.expiresAt,
    })
  } catch (error) {
    console.error('[Dashboard Layout] Session validation error:', error)
    redirect('/login')
  }

  return <DashboardUI>{children}</DashboardUI>
}
