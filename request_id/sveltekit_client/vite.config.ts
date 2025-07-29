import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		port: 3000,
		proxy: {
			'/request-id': {
			  	target: 'http://localhost:8080/request-id',
			  	changeOrigin: true,
				  rewrite: path => path.replace(/^\/request-id/, ''),
			}
		}
	}
});
