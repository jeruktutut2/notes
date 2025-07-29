import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/file/upload',
        destination: 'http://localhost:8080/file/upload',
      },
      {
        source: '/file/merge',
        destination: 'http://localhost:8080/file/merge',
      },
      {
        source: '/file/check-file/:path*',
        destination: 'http://localhost:8080/file/check-file/:path*',
      },
      {
        source: '/file/upload-merge',
        destination: 'http://localhost:8080/file/upload-merge',
      },
    ]
  },
};

export default nextConfig;
