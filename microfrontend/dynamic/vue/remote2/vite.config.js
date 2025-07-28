import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import federation from "@originjs/vite-plugin-federation";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        tailwindcss(),
        federation(
            {
                name: "remote",
                filename: "remoteEntry.js",
                exposes: {
                    "./Button": "./src/components/Button.vue",
                    "./Text": "./src/components/Text.vue",
                    "./AppView": "./src/views/AppView.vue",
                    "./AboutView": "./src/views/AboutView.vue",
                    "./ProfileView": "./src/views/ProfileView.vue",
                },
                shared: ['vue']
            }
        ),
    ],
    base: '/remote/',
    build: {
        target: 'esnext',
        minify: false,
        cssCodeSplit: true,
        assetsDir: '', // 👈 hilangkan subfolder 'assets'
    },
    server: {
        port: 3002
    },
    preview: {
        port: 3002,
    },
})
