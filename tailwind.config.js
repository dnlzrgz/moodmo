/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/custom.js",
  ],
  theme: {
    extend: {
      colors: {
        // Palette
        "white": "#fff",
        "black": "#000",
        "cinnabar": "#e94f37",
        "navajo": "#ffe0b5",
        "periwinkle": "#a6b1e1",
        "zomp": "#66a182",
        "naples": "#f5d547",
        "naples": {
          50: "#fefbec",
          100: "#fdf6d8",
          200: "#fbeeb6",
          300: "#f9e690",
          400: "#f7de6e",
          500: "#f5d547",
          600: "#f2c80d",
          700: "#b3940a",
          800: "#796407",
          900: "#3a3003",
          950: "#1d1802"
        },
        "periwinkle": {
          50: "#f7f8fc",
          100: "#eceef9",
          200: "#dde1f3",
          300: "#cad0ed",
          400: "#b7bfe7",
          500: "#a6b1e1",
          600: "#6a7ccd",
          700: "#3b50af",
          800: "#283676",
          900: "#131a39",
          950: "#0a0e1f"
        },
        "primary": {
          50: "#f7f8fc",
          100: "#eceef9",
          200: "#dde1f3",
          300: "#cad0ed",
          400: "#b7bfe7",
          500: "#a6b1e1",
          600: "#6a7ccd",
          700: "#3b50af",
          800: "#283676",
          900: "#131a39",
          950: "#0a0e1f"
        },

        "cinnabar": {
          50: "#fdefed",
          100: "#fadbd6",
          200: "#f6bab1",
          300: "#f29688",
          400: "#ed715e",
          500: "#e94f37",
          600: "#cf2f17",
          700: "#9c2411",
          800: "#6a180c",
          900: "#330c06",
          950: "#1c0603"
        },
        "zomp": {
          50: "#eff5f2",
          100: "#dfece5",
          200: "#c3dace",
          300: "#a3c7b4",
          400: "#84b39a",
          500: "#66a182",
          600: "#508267",
          700: "#3c624e",
          800: "#294235",
          900: "#132019",
          950: "#0a100d"
        },
        "navajo": {
          50: "#fffbf5",
          100: "#fff4e5",
          200: "#ffeacc",
          300: "#ffe0b5",
          400: "#ffc675",
          500: "#ffac38",
          600: "#fa9200",
          700: "#bd6e00",
          800: "#7a4700",
          900: "#3d2400",
          950: "#1f1200"
        }
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
