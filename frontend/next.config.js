/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: false, // Disable strict mode to prevent double effect invocation in dev
  // This was causing authClient.signOut() to be called twice, triggering auto-logout
  experimental: {
		optimizePackageImports: ['better-auth']
	},
  serverExternalPackages: ['pg'],
  turbopack: { // Moved here
    root: '../', // Set monorepo root for Turbopack
  },
}

module.exports = nextConfig
