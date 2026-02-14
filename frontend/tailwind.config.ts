import type { Config } from 'tailwindcss'

// Task T-243: Tailwind CSS configuration with dark mode and custom theme
const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      // Task T-243: Custom color scheme for light/dark mode
      colors: {
        // Brand colors
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          900: '#0c2d6b',
        },
      },
      // Task T-243: Custom animations for UI feedback
      animation: {
        'fade-in': 'fadeIn 200ms ease-in',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
    },
  },
  // Task T-243: Dark mode strategy - class-based (compatible with next-themes)
  darkMode: 'class',
  plugins: [],
}
export default config
