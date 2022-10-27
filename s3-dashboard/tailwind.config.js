/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "bg-dark": "#181a1b",
        "bg-dark-accent": "#313131",
      },
    },
  },
  plugins: [],
};
