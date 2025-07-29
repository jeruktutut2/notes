import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/request-id/:path*',
        destination: 'http://localhost:8080/request-id/:path*', // domain tujuan
      },
    ]
  },
};

export default nextConfig;
