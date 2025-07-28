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
                shared: ['vue']
            }
        )
    ],
    build: {
        target: 'esnext',
        // minify: false,
        cssCodeSplit: true,
    },
    server: {
        port: 3000,
        proxy: {
            '/cookie/set-remote1': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/cookie\/set-remote1/, '/cookie/set-remote1'),
      		},
            '/cookie/set-remote2': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/cookie\/set-remote2/, '/cookie/set-remote2'),
      		},
            '/assets/remoteEntry.js': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/assets\/remoteEntry.js/, '/assets/remoteEntry.js'),
      		},
            '/assets/remote': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/assets\/remote/, '/assets/remote'),
      		},
            '/remote/remoteEntry.js': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/remote\/remoteEntry.js/, '/remote/remoteEntry.js'),
      		},
            '/remote': {
                target: 'http://localhost:8080',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/remote/, '/remote'),
            },
            '/remote/': {
                target: 'http://localhost:8080',
                changeOrigin: true,
                // Tidak perlu rewrite karena path `/remote/abc.js` akan langsung diteruskan ke target
                // Jika kamu ingin menghapus "/remote" dari path saat diteruskan ke backend, baru gunakan rewrite
                // rewrite: (path) => path.replace(/^\/remote/, '')
            },
        }
    },
    preview: {
        port: 3000,
    },
})
