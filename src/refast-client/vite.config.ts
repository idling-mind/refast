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
  charts: ['recharts'],
  markdown: ['react-markdown', 'remark-gfm', 'rehype-raw', 'react-syntax-highlighter'],
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
          // Normalise separators so matching works on both Windows and Unix.
          const normalId = id.replace(/\\/g, '/');

          // Keep Rollup virtual modules and CommonJS helper shims in the
          // neutral vendor chunk so feature chunks are not pulled into core.
          if (id.startsWith('\u0000') || normalId.includes('commonjsHelpers')) {
            return 'vendor';
          }

          for (const [chunkName, markers] of Object.entries(CHUNK_GROUPS)) {
            if (markers.some((m) => normalId.includes(m))) {
              // Only apply manual chunks for node_modules to avoid circular
              // static imports between app chunks where Rollup merges shared app code
              // into the explicitly named chunk.
              if (normalId.includes('node_modules')) {
                 return chunkName;
              }
            }
          }
          if (normalId.includes('node_modules')) {
            // Keep other third-party modules in a neutral shared vendor chunk
            // so feature chunks do not accidentally become dependencies of core runtime.
            return 'vendor';
          }
          // Let Vite handle everything else (goes into entry or shared)
          return undefined;
        },
      },
    },
    // Use esbuild for JS minification (bundled with Vite)
    minify: 'esbuild',
    // Use esbuild for CSS minification too — avoids SVGO crashing on
    // URL-encoded SVGs embedded in third-party CSS (e.g. react-day-picker).
    cssMinify: 'esbuild',
    // Single CSS file (no CSS code splitting)
    cssCodeSplit: false,
    // Generate a manifest so the Python side knows which chunks exist
    manifest: true,
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
    // Ensure every package that depends on React (e.g. recharts) resolves to
    // the exact same module file as the main app.  Without this, dynamic
    // chunks that bundle recharts can end up with a second copy of React,
    // triggering "Invalid hook call" (React error #310) at runtime.
    dedupe: ['react', 'react-dom', 'react-is', 'scheduler'],
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
  };
});
