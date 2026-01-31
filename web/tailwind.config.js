/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#0D0D0D',
          secondary: '#1A1A1A',
          tertiary: '#252525',
          hover: '#2D2D2D',
        },
        accent: {
          DEFAULT: '#00D9A5',
          hover: '#00F5BA',
          dim: '#00A87D',
        },
        text: {
          primary: '#E8E8E8',
          secondary: '#888888',
          muted: '#555555',
        },
        border: {
          DEFAULT: '#333333',
          light: '#444444',
        },
        status: {
          warning: '#FF6B35',
          error: '#FF4757',
          success: '#00D9A5',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'sans-serif'],
        heading: ['Outfit', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
