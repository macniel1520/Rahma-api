import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/panel-assets/",
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/panel-api": "http://localhost:8073",
      "/api/v1": "http://localhost:8073",
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
