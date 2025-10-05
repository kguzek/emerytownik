import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  rewrites: async () => [{ source: "/", destination: "/zus.html" }],
};

export default nextConfig;
