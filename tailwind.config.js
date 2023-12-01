/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        'primary': {
          '50': '#f0fdfc',
          '100': '#ccfbf7',
          '200': '#99f6ee',
          '300': '#5eeade',
          '400': '#2dd4c5',
          '500': '#14b8a9',
          '600': '#0d9488',
          '700': '#0f766d',
          '800': '#115e57',
          '900': '#134e49',
          '950': '#042f2b',
        },
      },
    },
  },
  plugins: [],
};
