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
                name: "remote",
                filename: "remoteEntry.js",
                exposes: {
                    "./Button": "./src/lib/Button.svelte",
                    "./Text": "./src/lib/Text.svelte",
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
                // shared: ['svelte', 'svelte/internal']
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
        // rollupOptions: {
        //     output: {
        //         format: 'iife',
        //         entryFileNames: 'assets/[name].js',
        //         chunkFileNames: 'assets/[name].js', // <<< ini juga penting!
        //         assetFileNames: 'assets/[name][extname]',
        //         inlineDynamicImports: true,
        //         manualChunks: undefined, // <<< penting
        //     },
        // },
    },
    server: {
        port: 3001,
    },
    preview: {
        port: 3001,
    }
})
