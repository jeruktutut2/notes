import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: './src/remote.js',
      name: 'VueRemote',
      // fileName: 'vue-remote',
      formats: ['umd'], // agar bisa dipakai SystemJS
      fileName: (format) => {
        if (format === 'umd') return 'vue-remote.umd.js';
        return `vue-remote.${format}.js`;
      },
    },
    rollupOptions: {
      external: ['vue'], // agar host yang punya Vue
      output: {
        globals: {
          vue: 'Vue'
        }
      }
    }
  }
})
