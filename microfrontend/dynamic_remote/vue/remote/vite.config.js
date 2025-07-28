import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import federation from "@originjs/vite-plugin-federation";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        tailwindcss(),
        federation({
            name: "remote",
            filename: "remoteEntry.js",
            exposes: {
                "./Button": "./src/components/Button.vue",
                "./Text": "./src/components/Text.vue",
                "./AppView": "./src/views/AppView.vue",
                "./AboutView": "./src/views/AboutView.vue",
                "./ProfileView": "./src/views/ProfileView.vue",
            },
            // shared: {
            //     vue: {
            //         singleton: true,
            //         requiredVersion: '^3.4.0',
            //         strictVersion: true
            //     },
            //     tailwindcss: {
            //         singleton: true,
            //         requiredVersion: '^3.0.0'
            //     },
            // }
            shared: ['vue']
        }),
    ],
    build: {
        target: 'esnext',
        // minify: false,
        cssCodeSplit: true,
        // rollupOptions: {
        //     output: {
        //       format: 'esm'
        //     }
        // }
    },
    server: {
        port: 3001
    },
    preview: {
        port: 3001,
    },
})
