import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: '/file/stat',
        destination: 'http://localhost:8080/file/stat',
      },
      {
        source: '/file/download',
        destination: 'http://localhost:8080/file/download',
      },
    ]
  }
};

export default nextConfig;
