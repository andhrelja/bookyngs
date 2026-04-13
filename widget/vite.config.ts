import { defineConfig } from "vite";

export default defineConfig({
  build: {
    lib: {
      entry: "src/index.ts",
      name: "BookyngsWidget",
      fileName: "widget",
      formats: ["iife"],
    },
    outDir: "dist",
    emptyOutDir: true,
  },
});
