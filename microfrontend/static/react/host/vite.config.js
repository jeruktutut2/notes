import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import federation from "@originjs/vite-plugin-federation";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        tailwindcss(),
        federation(
            {
                name: "host",  //app name
                remotes: {
                    remote: "http://localhost:3001/assets/remoteEntry.js",  //remote path containing the port configured on remote side, the build path, and the filename also configured on the remote side
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
                // ['vue'],
            }
        ),
    ],
    build: {
        target: 'esnext',
        minify: false,
        cssCodeSplit: false,
    },
    server: {
        port: 3000,
    },
    preview: {
        port: 3000,
    }
})
