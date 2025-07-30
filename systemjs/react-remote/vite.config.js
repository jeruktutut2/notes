import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: './src/remote.js',
      name: 'ReactRemote',
      // fileName: 'react-remote',
      formats: ['umd'],
      fileName: (format) => {
        if (format === 'umd') return 'react-remote.umd.js';
        return `react-remote.${format}.js`;
      },
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
      }
    }
  }
})
