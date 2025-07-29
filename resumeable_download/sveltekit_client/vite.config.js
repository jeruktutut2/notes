import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		port: 3000,
		proxy: {
			'/file/stat': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/file\/stat/, '/file/stat'),
      		},
			'/file/download': {
        		target: 'http://localhost:8080',
        		changeOrigin: true,
        		rewrite: (path) => path.replace(/^\/file\/download/, '/file/download'),
      		},
		}
	}
});
