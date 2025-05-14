import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { NodeGlobalsPolyfillPlugin } from '@esbuild-plugins/node-globals-polyfill';

export default defineConfig({
  base: '/',

  plugins: [
    react(),
    NodeGlobalsPolyfillPlugin({
      process: true,
      buffer: true
    })
  ],
  optimizeDeps: {
    include: ['simple-peer']
  },
  define: {
    'global': 'window'
  }
});