/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Noto Sans', 'system-ui', '-apple-system', 'sans-serif'],
      },
      colors: {
        // Modern, warm color palette for name pronunciation
        brand: {
          primary: '#4F46E5', // Indigo - academic, trustworthy
          accent: '#F59E0B', // Amber - celebration, warmth
        },
        vercel: {
          black: '#1C1917', // Near-black, softer on eyes
          white: '#FFFFFF',
          gray: {
            50: '#FAFAF9', // Warm white
            100: '#F5F5F4',
            200: '#E7E5E4',
            300: '#D6D3D1',
            400: '#A8A29E',
            500: '#78716C',
            600: '#57534E',
            700: '#44403C',
            800: '#292524',
            900: '#1C1917',
          },
        },
        indigo: {
          50: '#EEF2FF',
          100: '#E0E7FF',
          600: '#4F46E5',
        },
        purple: {
          50: '#FAF5FF',
        },
        amber: {
          50: '#FFFBEB',
          100: '#FEF3C7',
        },
        orange: {
          50: '#FFF7ED',
        },
        emerald: {
          50: '#ECFDF5',
          100: '#D1FAE5',
          500: '#10B981',
        },
        teal: {
          50: '#F0FDFA',
        },
        rose: {
          50: '#FFF1F2',
          200: '#FECDD3',
          500: '#F43F5E',
          800: '#9F1239',
        },
      },
    },
  },
  plugins: [],
}
