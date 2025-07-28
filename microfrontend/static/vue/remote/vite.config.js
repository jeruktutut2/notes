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
            name: "remote", //name of remote you want to use on host side
            filename: "remoteEntry.js", //filename after the build
            exposes: {
                "./Button": "./src/components/Button.vue",  //target component you want to serve as remote side. In our case is the entire application
                "./Text": "./src/components/Text.vue",
            },
            shared: {
                vue: {
                    singleton: true,
                    // requiredVersion: '^3.4.0',
                    // strictVersion: true
                },
                tailwindcss: {
                    singleton: true,
                    // requiredVersion: '^3.0.0'
                },
            }
        //   ["vue"],  //we don't want to build our remote with a library the host side already have. So here we sinalize "hey, use this host side package"
        }),
    ],
    build: {
        target: 'esnext',
        minify: false,
        cssCodeSplit: false,
        // rollupOptions: {
        //     output: {
        //         // 🛑 ini penting supaya remoteEntry.js di ROOT, bukan di /assets
        //         entryFileNames: `[name].js`,
        //         chunkFileNames: `[name].js`,
        //         assetFileNames: `[name].[ext]`
        //     }
        // },
    },
    server: {
        port: 3001
    },
    preview: {
        port: 3001, //port you want to serve this remote
    },
})
