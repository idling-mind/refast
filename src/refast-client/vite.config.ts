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
 *
 * Path-based markers (containing '/node_modules/') are used for packages
 * whose names are substrings of other packages (e.g. 'react' vs 'react-dom').
 */
const CHUNK_GROUPS: Record<string, string[]> = {
  // NOTE: React, ReactDOM, and scheduler are intentionally NOT given their own
  // chunk.  When they lived in a separate 'react-core' chunk they formed a
  // circular ESM dependency with 'vendor':
  //
  //   vendor    → react-core  (React's CJS proxy in vendor imports react-core)
  //   react-core → vendor     (react-dom CJS code imports commonjsHelpers from vendor)
  //
  // ESM cycle = TDZ crash: whichever chunk evaluates first sees the other's
  // exports as `undefined`, producing:
  //   "Cannot read properties of undefined (reading 'useLayoutEffect')"
  //
  // Keeping React in the vendor catch-all breaks the cycle: everything that
  // needs React (proxies, helpers, consumers) lives in the same chunk and
  // evaluates together with no ordering hazard.

  // ── Radix UI primitives ────────────────────────────────────────────────────
  // All @radix-ui packages share a release cadence; one cached chunk for all.
  radix: ['@radix-ui/'],

  // ── Heavy feature libraries (each in its own cached chunk) ─────────────────
  //
  // Chunk dependency rules (must form a DAG — no cycles):
  //
  //   vendor  ← react-core, radix, prism, d3-shared, es-toolkit-shared,
  //              markdown, katex, charts, mermaid
  //
  // PRISM chunk: only the tokenizer packages + their direct hast dependencies.
  // 'prism' must be listed BEFORE 'markdown' so the first-match rule routes
  // these packages here, not to markdown.
  //
  // Packages included here are ALL of refractor's transitive runtime deps.
  // None of them depend on unified/vfile, so the prism chunk imports from
  // vendor only — no back-link to markdown.
  //   prismjs                   — CJS tokenizer
  //   refractor                 — CJS, builds hast from prism token stream
  //   hastscript                — refractor's hast-node builder
  //   hast-util-parse-selector  — hastscript internals  (no unified dep)
  //   parse-entities            — refractor entity decoder  (no unified dep)
  //   property-information, space-separated, comma-separated
  //                             — hastscript utility deps
  //
  // DO NOT add hast-util-raw, hast-util-from-parse5, or parse5 here —
  // hast-util-raw imports unified/vfile (markdown chunk) which would recreate
  // a prism ↔ markdown circular dep.
  prism: ['prismjs', 'refractor', 'hastscript', 'hast-util-parse-selector',
          'parse-entities', 'property-information',
          'space-separated', 'comma-separated'],

  // D3 SHARED chunk: all d3 packages used by BOTH recharts (charts chunk) AND
  // mermaid.  Placing them in a single shared lazy chunk breaks the
  // charts ↔ mermaid circular import that would otherwise arise when recharts
  // imports d3-shape/d3-scale (mermaid chunk) and mermaid re-imports recharts
  // deps (charts chunk).
  //
  // d3 packages import only from each other, so this chunk imports vendor only.
  'd3-shared': ['d3', '/node_modules/d3-'],

  // ES-TOOLKIT SHARED chunk: es-toolkit utility functions used by both recharts
  // and mermaid's dagre-d3-es.  Without isolation, charts exports es-toolkit
  // symbols that mermaid imports, creating a charts ↔ mermaid cycle.
  'es-toolkit-shared': ['es-toolkit'],

  charts: [
    'recharts',
    // Recharts' own transitive deps — explicitly kept in the lazy charts chunk
    // rather than the eager vendor catch-all.
    '@reduxjs/toolkit', '/immer/', 'react-redux', 'reselect',
    'victory-vendor', 'decimal.js-light', 'eventemitter3',
    // NOTE: 'es-toolkit' and 'd3-*' intentionally omitted here — they live in
    // their own shared chunks to avoid charts ↔ mermaid circular imports.
  ],

  // KATEX must be listed BEFORE markdown so that 'micromark-extension-math'
  // and 'mdast-util-math' match katex's specific markers before the broader
  // 'micromark' and 'mdast-util' markers in markdown catch them.
  //
  // If both end up in markdown while remark-math/rehype-katex are in katex,
  // Rollup creates a katex ↔ markdown circular import.
  katex: ['katex', 'remark-math', 'rehype-katex', 'micromark-extension-math', 'mdast-util-math'],

  // unified.js ecosystem + hast/parse5 utilities: only used for markdown
  // rendering, so keep lazy.
  //
  // hast-util-* and parse5 live here (not in the prism chunk) because
  // hast-util-raw imports unified/vfile.  Keeping them in markdown avoids a
  // prism → markdown back-reference.
  //
  // remark-stringify, remark-rehype, lowlight, highlight.js are placed here so
  // they do not land in the vendor catch-all, which would cause vendor →
  // markdown imports (and force markdown to be eagerly loaded).
  //   remark-rehype — converts mdast→hast; calls mdast-util-to-hast which is
  //                   matched by the 'mdast-util' marker here.  Without an
  //                   explicit marker it falls to vendor and creates a
  //                   vendor → markdown circular import.
  //   parse-entities  — refractor dep; 'prism' chunk is listed earlier so it
  //                   wins the first-match, but keep the marker here as a
  //                   safety net for non-refractor callers.
  markdown: [
    'react-markdown', 'remark-gfm', 'rehype-raw', 'react-syntax-highlighter',
    'remark-rehype',
    'micromark', 'mdast-util', 'remark-parse', 'remark-stringify', 'unified', 'vfile',
    'parse-entities', 'parse5',
    'hast-util', 'lowlight', 'highlight.js',
    'decode-named-character-reference', 'character-entities', 'trim-lines',
    'ccount', 'zwitch', 'longest-streak', 'stringify-entities',
  ],
  mermaid: [
    'mermaid',
    // Mermaid's transitive deps — all lazy (only loaded when a Mermaid diagram renders).
    // Without explicit routing, these fall to the catch-all vendor chunk and get
    // loaded eagerly on every page, which wastes ~400 KB of initial download.
    //
    // NOTE: 'd3' and 'd3-sankey' intentionally omitted — they live in the shared
    // 'd3-shared' chunk to avoid a mermaid ↔ charts circular import via d3-*.
    'cytoscape', 'dagre', 'dagre-d3-es',
    '@braintree/sanitize-url', '@iconify/utils', '@mermaid-js/parser', '@upsetjs/venn.js',
    'cytoscape-cose-bilkent', 'cytoscape-fcose',
    'khroma', 'marked', 'roughjs', 'stylis', 'ts-dedent',
    'dompurify',
  ],
  icons: ['lucide-react'],

  // ── UI utility libraries (eagerly loaded, but separately cacheable) ─────────
  sonner: ['sonner'],
  carousel: ['embla-carousel'],
  panels: ['react-resizable-panels'],

  // ── Lazy-only libraries ────────────────────────────────────────────────────
  // These are ONLY referenced by lazy feature chunks (controls / navigation).
  // By naming them here they escape the vendor catch-all and become lazy chunks,
  // eliminating ~1300 KB (≈330 KB gzip) from the initial download.
  cmdk: ['cmdk'],
  'day-picker': ['react-day-picker', 'date-fns'],

  // ── Component group chunks (app code, not node_modules) ────────────────────
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

          // Keep all Rollup virtual modules (CommonJS proxies, helpers, etc.) in
          // vendor by default, with one targeted exception:
          //
          // CJS proxy virtual modules (\u0000 prefix) for packages in LAZY feature
          // chunks (prism, markdown, mermaid, charts, …) must be co-located in
          // those same lazy chunks.  If a proxy lands in vendor instead, Rollup
          // emits a side-effect import:
          //     import "./refast-prism.js"   ← inside vendor
          // which forces that lazy chunk to load eagerly on every page.
          //
          // IMPORTANT — only route proxies to LAZY chunks, never to EAGER ones
          // (radix, sonner, …).  Eager chunks share a commonjsHelpers dependency
          // with vendor; co-locating their CJS proxies in a separate eager chunk
          // would recreate the same vendor ↔ <chunk> circular ESM init hazard
          // that caused the 'useLayoutEffect' TDZ crash with the old react-core
          // chunk.  React itself lives in vendor for the same reason.
          if (id.startsWith('\u0000') || normalId.includes('commonjsHelpers')) {
            if (!normalId.includes('commonjsHelpers') && id.startsWith('\u0000')) {
              const realPath = normalId
                .replace(/^\u0000/, '')
                .replace(/\?commonjs[^?]*$/, '');
              if (realPath.includes('node_modules')) {
                // Only route to lazy feature chunks — skip eager ones.
                const LAZY_CHUNKS = [
                  'prism', 'markdown', 'katex', 'mermaid', 'charts',
                  'd3-shared', 'es-toolkit-shared', 'day-picker', 'cmdk',
                ] as const;
                for (const chunk of LAZY_CHUNKS) {
                  const markers = CHUNK_GROUPS[chunk];
                  if (markers?.some((m) => realPath.includes(m))) {
                    return chunk;
                  }
                }
              }
            }
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
            // Catch-all: any unmatched third-party package goes to vendor.
            //
            // This is intentional for correctness rather than optimal size:
            // it keeps CJS modules with complex init semantics (e.g. colour
            // utilities, unified.js AST helpers, etc.) in a separate file from
            // the feature chunks that import them.  Separate files guarantee
            // a deterministic ESM-import evaluation order — the vendor file
            // runs to completion before the feature chunk starts — which
            // prevents the CJS circular-initialisation crashes that occur when
            // these modules are inlined into the same chunk as their consumers.
            //
            // Packages that are genuinely lazy-only are handled by explicit
            // CHUNK_GROUPS entries above (prism, recharts deps, cmdk, …) so
            // they never fall through to this catch-all.
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
