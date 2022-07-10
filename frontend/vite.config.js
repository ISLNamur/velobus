import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { quasar, transformAssetUrls } from "@quasar/vite-plugin";

export default defineConfig({
    plugins: [vue({
        template: { transformAssetUrls },
    })],
    publicDir: "../assets",
    build: {
        rollupOptions: {
            output: {
                dir: "../assets",
                assetFileNames: "[name][extname]",
                entryFileNames: "main.js",
            },
        },
    },
});
