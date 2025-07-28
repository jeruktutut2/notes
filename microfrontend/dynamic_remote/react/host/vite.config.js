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
              shared: ['react', 'react-dom']
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
