import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { sveltePreprocess } from "svelte-preprocess/dist/autoProcess";

export default defineConfig({
  resolve: {
    alias: {
      "~bootstrap": "../node_modules/bootstrap",
    },
  },
  plugins: [svelte({ preprocess: sveltePreprocess() })],
});
