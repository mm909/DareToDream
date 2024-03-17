/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        matblue: '#2464a8',
        matwhite: '#F6F6F6'
      },
    },
  },
  plugins: [],
}
