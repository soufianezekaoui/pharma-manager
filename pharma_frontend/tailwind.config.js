/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', './src/**/*.{js,jsx}'],
    theme: {
      extend: {
        fontFamily: {
          sans: ['DM Sans', 'sans-serif'],
          display: ['Syne', 'sans-serif'],
          mono: ['JetBrains Mono', 'monospace'],
        },
        colors: {
          teal: {
            50:  '#effcfa',
            100: '#c7f5ef',
            200: '#90eade',
            300: '#52d6c8',
            400: '#22bbb0',
            500: '#0d9e96',
            600: '#0a817b',
            700: '#0d6763',
            800: '#0f5250',
            900: '#114442',
            950: '#042a2a',
          },
          sage: {
            50:  '#f4f9f4',
            100: '#e4f2e4',
            200: '#cae4cb',
            300: '#a2cea5',
            400: '#72b077',
            500: '#4e9254',
            600: '#3b7540',
            700: '#305d35',
            800: '#294b2d',
            900: '#233e27',
          },
        },
        backgroundImage: {
          'grid-teal': "url(\"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40' fill='%230d9e96' fill-opacity='0.03'/%3E%3C/g%3E%3C/svg%3E\")",
        },
        boxShadow: {
          'card': '0 2px 12px rgba(13,158,150,0.08), 0 1px 3px rgba(0,0,0,0.06)',
          'card-hover': '0 8px 28px rgba(13,158,150,0.14), 0 2px 8px rgba(0,0,0,0.08)',
          'glow': '0 0 20px rgba(13,158,150,0.25)',
        },
        animation: {
          'fade-in': 'fadeIn 0.4s ease-out',
          'slide-up': 'slideUp 0.4s ease-out',
          'slide-in-right': 'slideInRight 0.35s ease-out',
          'pulse-slow': 'pulse 3s infinite',
        },
        keyframes: {
          fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
          slideUp: { from: { opacity: 0, transform: 'translateY(16px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
          slideInRight: { from: { opacity: 0, transform: 'translateX(20px)' }, to: { opacity: 1, transform: 'translateX(0)' } },
        },
      },
    },
    plugins: [],
}
