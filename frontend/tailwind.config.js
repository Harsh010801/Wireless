/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        editorial: {
          bg: "#F3F4EF",
          surface: "#FFFFFF",
          lime: "#A8EB12",
          limeBright: "#B4F434",
          forest: "#134729",
          forestDark: "#0B2E1A",
          charcoal: "#151618",
          ink: "#111827",
          muted: "#6B7280",
        },
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '"Inter"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
};

