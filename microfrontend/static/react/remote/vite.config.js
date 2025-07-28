import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import federation from "@originjs/vite-plugin-federation";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        tailwindcss(),
        federation({
            name: "remote",
            filename: "remoteEntry.js",
            exposes: {
                "./Button": "./src/components/Button.jsx",
                "./Text": "./src/components/Text.jsx",
            },
            shared: {
                react: {
                    singleton: true,
                    // requiredVersion: '^18.2.0',
                    // strictVersion: true
                },
                'react-dom': {
                    singleton: true,
                    // requiredVersion: '^18.2.0',
                    // strictVersion: true
                },
                tailwindcss: {
                    singleton: true,
                    // requiredVersion: '^3.0.0'
                },
            }
        }),
    ],
    build: {
        target: 'esnext',
        minify: false,
        cssCodeSplit: false,
    },
    server: {
        port: 3001,
    },
    preview: {
        port: 3001,
    }
})
