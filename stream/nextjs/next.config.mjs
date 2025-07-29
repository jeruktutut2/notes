/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
        return [
               {
                     source: '/stream/:path*',
                     destination: `http://localhost:8080/stream/:path*`,
               },
               
        ]
    },
};

export default nextConfig;
