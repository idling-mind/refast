import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';
import { resolve } from 'path';

export default defineConfig(({ mode }) => ({
  plugins: [
    react(),
    dts({ insertTypesEntry: true }),
  ],
  define: {
    // Replace process.env.NODE_ENV - use 'production' for builds, preserve mode for tests
    'process.env.NODE_ENV': JSON.stringify(mode === 'test' ? 'development' : 'production'),
  },
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.tsx'),
      name: 'RefastClient',
      // Use a function to control the output filename
      fileName: () => 'refast-client.js',
      // Use IIFE format for standalone browser use (bundles everything)
      formats: ['iife'],
    },
    rollupOptions: {
      // Don't externalize React - bundle it for standalone use
      output: {
        // Ensure all code is in a single file
        inlineDynamicImports: true,
        // Override the entry file name to not include format suffix
        entryFileNames: 'refast-client.js',
        // Output CSS with consistent name
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith('.css')) {
            return 'refast-client.css';
          }
          return assetInfo.name || 'asset-[hash][extname]';
        },
      },
    },
    // Use esbuild for minification (bundled with Vite)
    minify: 'esbuild',
    // Ensure CSS is extracted to a separate file
    cssCodeSplit: false,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
}));
