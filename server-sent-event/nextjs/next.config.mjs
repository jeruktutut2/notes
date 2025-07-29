/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
               {
                     source: '/sse/:path*',
                     destination: `http://localhost:8080/sse/:path*`,
               },
               
        ]
    },
};

export default nextConfig;
