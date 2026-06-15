/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        poker: {
          red: '#EF4444',
          black: '#1F2937',
          green: '#10B981',
          gold: '#F59E0B',
          table: '#0D5D2E',
          felt: '#15803D'
        }
      }
    },
  },
  plugins: [],
}
