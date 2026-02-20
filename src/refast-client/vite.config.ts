import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// Conditional imports for build-time plugins
// vite-plugin-compression generates .gz and .br pre-compressed files
// rollup-plugin-visualizer produces an HTML bundle size report
let compressionPlugin: (() => Plugin) | undefined;
let visualizerPlugin: ((opts: Record<string, unknown>) => Plugin) | undefined;
try {
  compressionPlugin = (await import('vite-plugin-compression')).default;
} catch { /* not installed or dev-only */ }
try {
  visualizerPlugin = (await import('rollup-plugin-visualizer')).visualizer;
} catch { /* not installed or dev-only */ }

/**
 * Component chunk groups for code-splitting.
 *
 * Each key is a chunk name and the value lists the module-path markers
 * that should be routed into that chunk.  The first match wins.
 */
const CHUNK_GROUPS: Record<string, string[]> = {
  // Heavy third-party libraries get their own chunks
  charts: ['recharts', '/charts/'],
  markdown: ['react-markdown', 'remark-gfm', 'react-syntax-highlighter'],
  icons: ['lucide-react'],
  // Component group chunks
  navigation: ['/shadcn/navigation'],
  overlay: ['/shadcn/overlay'],
  controls: ['/shadcn/controls'],
};

export default defineConfig(({ mode }) => {
  const plugins: Plugin[] = [react()];

  // Pre-compress assets for production builds
  if (mode !== 'test' && compressionPlugin) {
    // gzip compression
    plugins.push(compressionPlugin({ algorithm: 'gzip', ext: '.gz' }) as unknown as Plugin);
    // brotli compression
    plugins.push(compressionPlugin({ algorithm: 'brotliCompress', ext: '.br' }) as unknown as Plugin);
  }

  // Bundle analysis — run with ANALYZE=true npm run build
  if (process.env.ANALYZE === 'true' && visualizerPlugin) {
    plugins.push(
      visualizerPlugin({
        filename: 'dist/bundle-report.html',
        open: true,
        gzipSize: true,
        brotliSize: true,
      }) as unknown as Plugin,
    );
  }

  return {
    plugins,
  define: {
    // Replace process.env.NODE_ENV - use 'production' for builds, preserve mode for tests
    'process.env.NODE_ENV': JSON.stringify(mode === 'test' ? 'development' : 'production'),
  },
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.tsx'),
      // ESM format to enable code splitting via dynamic import()
      formats: ['es'],
    },
    rollupOptions: {
      output: {
        // Entry chunk keeps a stable name for the HTML shell
        entryFileNames: 'refast-client.js',
        // Feature chunks get content-hashed names for cache-busting
        chunkFileNames: 'refast-[name]-[hash].js',
        // CSS keeps a stable name
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith('.css')) {
            return 'refast-client.css';
          }
          return 'refast-[name]-[hash][extname]';
        },
        // Split heavy feature groups into separate chunks
        manualChunks(id) {
          for (const [chunkName, markers] of Object.entries(CHUNK_GROUPS)) {
            if (markers.some((m) => id.includes(m))) {
              return chunkName;
            }
          }
          // Let Vite handle everything else (goes into entry or shared)
          return undefined;
        },
      },
    },
    // Use esbuild for minification (bundled with Vite)
    minify: 'esbuild',
    // Single CSS file (no CSS code splitting)
    cssCodeSplit: false,
    // Generate a manifest so the Python side knows which chunks exist
    manifest: true,
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
  };
});
