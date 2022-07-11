import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { quasar, transformAssetUrls } from "@quasar/vite-plugin";

export default defineConfig({
    plugins: [vue({
        template: { transformAssetUrls },
    })],
    publicDir: "../assets",
    build: {
        lib: {
            entry: "src/main.js",
            name: "mylib",
            fileName: () => "main.js"
        },
        rollupOptions: {
            external: ["vue"],
            output: {
                dir: "../assets",
                assetFileNames: "[name][extname]",
                entryFileNames: "main.js",
                globals: {
                    vue: "Vue"
                },
            },
        },
    },
});
