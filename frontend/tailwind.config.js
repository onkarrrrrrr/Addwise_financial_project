/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-navy': {
          50: '#F0F4F9',      // Ekdum light ice-blue (Backgrounds ke liye best)
          100: '#D9E4F0',     // Soft light blue
          300: '#8AAED6',     // Light shaded blue
          DEFAULT: '#153769', // Main Navy Blue (Tumhara original)
          light: '#2B528A',   // Thoda bright navy (Hover effects ke liye)
          dark: '#0C2242',    // Deep dark navy (Footer ya dark sections ke liye)
        },
        'brand-yellow': {
          50: '#FEF8F2',      // Warm white/cream (Highlight sections ke liye)
          100: '#FCECDA',     // Soft light yellow
          300: '#F8C58C',     // Pastel yellow
          DEFAULT: '#F38D1E', // Main Chrome Yellow (Tumhara original)
          light: '#F6A851',   // Bright orange-yellow (Gradients ke liye)
          dark: '#C97112',    // Deep amber (Button hover states ke liye)
        },
        'brand-grey': {
          50: '#F7F7F8',      // Ultra light grey
          100: '#EAEBEF',     // Cards ke border ke liye
          300: '#A3A6AF',     // Disabled text ke liye
          DEFAULT: '#4C4C4C', // Main Stone Grey (Tumhara original)
          light: '#7A7A7A',   // Paragraphs aur subtitles ke liye
          dark: '#2B2B2B',    // Bold headings ke liye
        },
      },
      fontFamily: {
        sans: ['Montserrat', 'sans-serif'],
      }
    },
  },
  plugins: [],
}