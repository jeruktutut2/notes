import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		port: 3000,
		proxy: {
			'/file/upload': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/file\/upload/, '/file/upload'),
      		},
			'/file/merge': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/file\/merge/, '/file/merge'),
      		},
			'/file/check-file': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/file\/check-file/, '/file/check-file'),
      		},
			'/file/upload-merge': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/file\/upload-merge/, '/file/upload-merge'),
      		},
		}
	}
});
