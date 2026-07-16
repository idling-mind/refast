import React from 'react';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type ComponentType = React.ComponentType<any>;

/**
 * A lazy component loader: a function that returns a promise resolving to
 * a record of component names → React components.
 */
export type LazyChunkLoader = () => Promise<Record<string, ComponentType>>;

/**
 * Describes a feature chunk that can be lazily loaded.
 */
export interface FeatureChunk {
  /** Human-readable chunk name (e.g., "charts", "navigation") */
  name: string;
  /** Component names that belong to this chunk */
  componentNames: string[];
  /** Loader function that dynamically imports the chunk */
  loader: LazyChunkLoader;
}

/**
 * Registry of all available components.
 *
 * Supports two registration modes:
 * - **Eager**: component reference stored directly (core components)
 * - **Lazy**: a chunk loader is stored; the component is resolved on first
 *   access via `React.lazy()` + `<Suspense>`.
 *
 * Extensions continue to use `register()` / `registerAll()` exactly as before.
 */
class ComponentRegistry {
  private components: Map<string, ComponentType> = new Map();
  /** Maps component name → the chunk it belongs to (for lazy resolution) */
  private lazyMap: Map<string, string> = new Map();
  /** Registered chunk loaders */
  private chunkLoaders: Map<string, LazyChunkLoader> = new Map();
  /** Cache of resolved lazy components (wrapped in React.lazy) */
  private lazyCache: Map<string, ComponentType> = new Map();
  /** Chunk load promises (so we don't trigger the same import twice) */
  private chunkPromises: Map<string, Promise<Record<string, ComponentType>>> = new Map();
  /** Which chunks have been fully resolved */
  private resolvedChunks: Set<string> = new Set();
  /** Which feature chunks are allowed to load lazily */
  private lazyFeatureSet: Set<string> | null = null;

  // ── Eager registration (unchanged API) ─────────────────────────────

  register(name: string, component: ComponentType): void {
    this.components.set(name, component);
  }

  registerAll(components: Record<string, ComponentType>): void {
    for (const [name, component] of Object.entries(components)) {
      this.register(name, component);
    }
  }

  // ── Lazy registration ──────────────────────────────────────────────

  /**
   * Register a feature chunk whose components will be lazily loaded.
   */
  registerLazyChunk(chunk: FeatureChunk): void {
    this.chunkLoaders.set(chunk.name, chunk.loader);
    for (const name of chunk.componentNames) {
      this.lazyMap.set(name, chunk.name);
    }
  }

  // ── Component resolution ───────────────────────────────────────────

  /**
   * Get a component by name.
   *
   * 1. If eagerly registered → return immediately.
   * 2. If the component belongs to a lazy chunk → return a `React.lazy()`
   *    wrapper that will trigger the chunk import on first render.
   * 3. Otherwise → return `undefined`.
   */
  get(name: string): ComponentType | undefined {
    // 1. Eager
    const eager = this.components.get(name);
    if (eager) return eager;

    // 2. Lazy
    const chunkName = this.lazyMap.get(name);
    if (!chunkName) return undefined;

    // If the chunk has already been fully resolved, check the eager map
    // (resolved components are promoted to eager after loading)
    if (this.resolvedChunks.has(chunkName)) {
      return this.components.get(name);
    }

    // Return a cached React.lazy wrapper (create one if it doesn't exist)
    let lazy = this.lazyCache.get(name);
    if (!lazy) {
      lazy = React.lazy(() => this._loadComponent(name, chunkName));
      this.lazyCache.set(name, lazy);
    }
    return lazy;
  }

  has(name: string): boolean {
    return this.components.has(name) || this.lazyMap.has(name);
  }

  /**
   * Get the chunk name a component belongs to (if any).
   */
  getChunkName(name: string): string | undefined {
    return this.lazyMap.get(name);
  }

  /**
   * Check whether a component name is registered as part of a lazy chunk
   * that hasn't been loaded yet.
   */
  isLazy(name: string): boolean {
    if (this.components.has(name)) return false;
    const chunkName = this.lazyMap.get(name);
    if (!chunkName) return false;
    return !this.resolvedChunks.has(chunkName);
  }

  list(): string[] {
    const all = new Set([...this.components.keys(), ...this.lazyMap.keys()]);
    return Array.from(all);
  }

  /**
   * List all registered feature-chunk names.
   */
  listChunks(): string[] {
    return Array.from(this.chunkLoaders.keys());
  }

  /**
   * Configure which feature chunks are allowed to load lazily.
   */
  configureLazyFeatures(featureNames: string[]): void {
    this.lazyFeatureSet = new Set(featureNames);
  }

  private _isLazyAllowed(chunkName: string): boolean {
    if (this.lazyFeatureSet === null) {
      return true;
    }
    return this.lazyFeatureSet.has(chunkName);
  }

  /**
   * Eagerly load a lazy feature chunk.
   *
   * This resolves and promotes all chunk components to eager registrations
   * before the first render that uses them.
   */
  async preloadChunk(chunkName: string): Promise<void> {
    if (this.resolvedChunks.has(chunkName)) {
      return;
    }

    let promise = this.chunkPromises.get(chunkName);
    if (!promise) {
      const loader = this.chunkLoaders.get(chunkName);
      if (!loader) {
        throw new Error(`No loader for chunk "${chunkName}"`);
      }
      promise = loader();
      this.chunkPromises.set(chunkName, promise);
    }

    const exports = await promise;
    for (const [name, component] of Object.entries(exports)) {
      this.components.set(name, component);
    }
    this.resolvedChunks.add(chunkName);
  }

  /**
   * Eagerly load multiple lazy feature chunks.
   */
  async preloadChunks(chunkNames: string[]): Promise<void> {
    await Promise.all(chunkNames.map((chunkName) => this.preloadChunk(chunkName)));
  }

  // ── Internal ───────────────────────────────────────────────────────

  /**
   * Load a single component from its chunk.  Returns in the shape
   * `{ default: Component }` which `React.lazy()` requires.
   */
  private async _loadComponent(
    name: string,
    chunkName: string,
  ): Promise<{ default: ComponentType }> {
    if (!this._isLazyAllowed(chunkName) && !this.resolvedChunks.has(chunkName)) {
      throw new Error(
        `Chunk "${chunkName}" is configured as non-lazy and must be preloaded at startup.`,
      );
    }

    // De-duplicate chunk loading
    let promise = this.chunkPromises.get(chunkName);
    if (!promise) {
      const loader = this.chunkLoaders.get(chunkName);
      if (!loader) throw new Error(`No loader for chunk "${chunkName}"`);
      promise = loader();
      this.chunkPromises.set(chunkName, promise);
    }

    const exports = await promise;

    // Promote all resolved components to eager so subsequent `get()` calls
    // skip the lazy path entirely.
    for (const [n, comp] of Object.entries(exports)) {
      this.components.set(n, comp);
    }
    this.resolvedChunks.add(chunkName);

    const component = exports[name];
    if (!component) {
      throw new Error(
        `Component "${name}" not found in chunk "${chunkName}". ` +
        `Available: ${Object.keys(exports).join(', ')}`,
      );
    }
    return { default: component };
  }
}

export const componentRegistry = new ComponentRegistry();


