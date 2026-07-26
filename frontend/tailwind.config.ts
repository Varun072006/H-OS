import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0f",
        card: "#12131c",
        border: "#1e202e",
        accent: "#3b82f6",
        cyan: "#06b6d4",
        emerald: "#10b981",
        amber: "#f59e0b",
        rose: "#f43f5e",
      },
    },
  },
  plugins: [],
};

export default config;
