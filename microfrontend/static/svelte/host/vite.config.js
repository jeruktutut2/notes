import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import tailwindcss from '@tailwindcss/vite'
import federation from "@originjs/vite-plugin-federation";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        svelte(),
        tailwindcss(),
        federation(
            {
                name: "host",
                remotes: {
                    remote: "http://localhost:3001/assets/remoteEntry.js",
                },
                // shared: {
                //     svelte: {
                //         singleton: true,
                //         // strictVersion: true,
                //         // requiredVersion: '^3.0.0'
                //     },
                //     tailwindcss: {
                //         singleton: true,
                //         // requiredVersion: '^3.0.0'
                //     },
                // },
                // shared: ['svelte'],
                // shared: {
                //     svelte: {
                //       singleton: true,
                //       requiredVersion: '^3.0.0'
                //     }
                // }
                // shared: ['svelte']
                shared: {
                    svelte: { singleton: true, requiredVersion: '^3.0.0' }
                }
            }
        ),
    ],
    build: {
        target: 'esnext',
        minify: false,
        // cssCodeSplit: false,
        // modulePreload: false,
    },
    server: {
        port: 3000,
    },
    preview: {
        port: 3000,
    }
})
