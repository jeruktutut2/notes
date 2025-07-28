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
                name: 'host',
                remotes: {
                    dummy: {
                        external: '',
                        format: 'var'
                    }
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
            }
        )
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
        port: 3000
    },
    preview: {
        port: 3000,
    },
})
