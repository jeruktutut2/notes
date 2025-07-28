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
            name: "host",  //app name
            remotes: {
                remote: "http://localhost:3001/assets/remoteEntry.js",  //remote path containing the port configured on remote side, the build path, and the filename also configured on the remote side
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
            // ['vue'],
        }
      ),
  ],
  build: {
      target: 'esnext',
      minify: false,
      cssCodeSplit: false,
    //   rollupOptions: {
    //       output: {
    //           // 🛑 ini penting supaya remoteEntry.js di ROOT, bukan di /assets
    //           entryFileNames: `[name].js`,
    //           chunkFileNames: `[name].js`,
    //           assetFileNames: `[name].[ext]`
    //       }
    //   },
  },
  server: {
      port: 3000
  },
  preview: {
    port: 3000, //port you want to serve this remote
  },
})
