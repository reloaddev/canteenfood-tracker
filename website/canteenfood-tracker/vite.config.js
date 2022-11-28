import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
  resolve: {
    alias: {
      "~bootstrap": "../node_modules/bootstrap",
    },
  },
  plugins: [svelte()],
});
