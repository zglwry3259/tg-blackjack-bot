/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: {
    extend: {
      colors: {
        poker: { green: '#0D6E4B', dark: '#0A4D35', gold: '#FFD700', red: '#E53E3E' }
      }
    },
  },
  plugins: [],
}
