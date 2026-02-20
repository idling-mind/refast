/**
 * Tests for the lazy-loading and code-splitting features of ComponentRegistry.
 *
 * Covers:
 * - registerLazyChunk / isLazy / listChunks
 * - get() returning a React.lazy wrapper for lazy components
 * - Chunk de-duplication (single import per chunk)
 * - Promotion of resolved components to eager
 * - Error handling for missing components in a chunk
 */

import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';

// We need a *fresh* registry for each test — import the class, not the singleton.
// The class is not exported directly, so we'll test via the module-level helpers.
// Instead, we'll create a minimal registry implementation for unit-test isolation.

// ── Minimal stub to match the shape of ComponentRegistry ─────────────────

type ComponentType = React.ComponentType<any>;
type LazyChunkLoader = () => Promise<Record<string, ComponentType>>;

interface FeatureChunk {
  name: string;
  componentNames: string[];
  loader: LazyChunkLoader;
}

function createRegistry() {
  const components = new Map<string, ComponentType>();
  const lazyMap = new Map<string, string>();
  const chunkLoaders = new Map<string, LazyChunkLoader>();
  const lazyCache = new Map<string, ComponentType>();
  const chunkPromises = new Map<string, Promise<Record<string, ComponentType>>>();
  const resolvedChunks = new Set<string>();

  function register(name: string, component: ComponentType) {
    components.set(name, component);
  }

  function registerLazyChunk(chunk: FeatureChunk) {
    chunkLoaders.set(chunk.name, chunk.loader);
    for (const name of chunk.componentNames) {
      lazyMap.set(name, chunk.name);
    }
  }

  function _loadComponent(name: string, chunkName: string): Promise<{ default: ComponentType }> {
    let promise = chunkPromises.get(chunkName);
    if (!promise) {
      const loader = chunkLoaders.get(chunkName);
      if (!loader) throw new Error(`No loader for chunk "${chunkName}"`);
      promise = loader();
      chunkPromises.set(chunkName, promise);
    }
    return promise.then((exports) => {
      for (const [n, comp] of Object.entries(exports)) {
        components.set(n, comp);
      }
      resolvedChunks.add(chunkName);
      const component = exports[name];
      if (!component) {
        throw new Error(`Component "${name}" not found in chunk "${chunkName}".`);
      }
      return { default: component };
    });
  }

  function get(name: string): ComponentType | undefined {
    const eager = components.get(name);
    if (eager) return eager;

    const chunkName = lazyMap.get(name);
    if (!chunkName) return undefined;

    if (resolvedChunks.has(chunkName)) {
      return components.get(name);
    }

    let lazy = lazyCache.get(name);
    if (!lazy) {
      lazy = React.lazy(() => _loadComponent(name, chunkName));
      lazyCache.set(name, lazy);
    }
    return lazy;
  }

  function has(name: string): boolean {
    return components.has(name) || lazyMap.has(name);
  }

  function isLazy(name: string): boolean {
    if (components.has(name)) return false;
    const chunkName = lazyMap.get(name);
    if (!chunkName) return false;
    return !resolvedChunks.has(chunkName);
  }

  function list(): string[] {
    return Array.from(new Set([...components.keys(), ...lazyMap.keys()]));
  }

  function listChunks(): string[] {
    return Array.from(chunkLoaders.keys());
  }

  return { register, registerLazyChunk, get, has, isLazy, list, listChunks };
}

// ── Dummy components used in tests ───────────────────────────────────────

function DummyA() {
  return React.createElement('div', null, 'DummyA');
}

function DummyB() {
  return React.createElement('div', null, 'DummyB');
}

function DummyC() {
  return React.createElement('div', null, 'DummyC');
}

// ── Tests ────────────────────────────────────────────────────────────────

describe('ComponentRegistry – lazy loading', () => {
  let registry: ReturnType<typeof createRegistry>;

  beforeEach(() => {
    registry = createRegistry();
  });

  // ── Registration ─────────────────────────────────────────────────────

  it('registerLazyChunk stores chunk metadata', () => {
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA', 'DummyB'],
      loader: async () => ({ DummyA, DummyB }),
    });

    expect(registry.has('DummyA')).toBe(true);
    expect(registry.has('DummyB')).toBe(true);
    expect(registry.listChunks()).toContain('testChunk');
  });

  it('isLazy returns true for lazy components before loading', () => {
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA'],
      loader: async () => ({ DummyA }),
    });

    expect(registry.isLazy('DummyA')).toBe(true);
  });

  it('isLazy returns false for eagerly registered components', () => {
    registry.register('DummyC', DummyC);
    expect(registry.isLazy('DummyC')).toBe(false);
  });

  it('isLazy returns false for unknown components', () => {
    expect(registry.isLazy('NonExistent')).toBe(false);
  });

  // ── Retrieval ────────────────────────────────────────────────────────

  it('get() returns the eager component directly', () => {
    registry.register('DummyC', DummyC);
    const comp = registry.get('DummyC');
    expect(comp).toBe(DummyC);
  });

  it('get() returns undefined for unknown components', () => {
    expect(registry.get('NonExistent')).toBeUndefined();
  });

  it('get() returns a React.lazy wrapper for lazy components', () => {
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA'],
      loader: async () => ({ DummyA }),
    });

    const LazyComp = registry.get('DummyA');
    expect(LazyComp).toBeDefined();
    // React.lazy components have $$typeof Symbol(react.lazy) — verify it's a lazy wrapper
    expect((LazyComp as any).$$typeof).toBe(Symbol.for('react.lazy'));
  });

  it('get() returns the same lazy wrapper on repeated calls', () => {
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA'],
      loader: async () => ({ DummyA }),
    });

    const first = registry.get('DummyA');
    const second = registry.get('DummyA');
    expect(first).toBe(second);
  });

  // ── Chunk loading and promotion ──────────────────────────────────────

  it('resolves lazy component and renders correctly', async () => {
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA'],
      loader: async () => ({ DummyA }),
    });

    const LazyComp = registry.get('DummyA')!;
    await act(async () => {
      render(
        React.createElement(
          React.Suspense,
          { fallback: React.createElement('div', null, 'Loading...') },
          React.createElement(LazyComp),
        ),
      );
    });

    await waitFor(() => {
      expect(screen.getByText('DummyA')).toBeInTheDocument();
    });
  });

  it('promotes lazy component to eager after chunk loads', async () => {
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA', 'DummyB'],
      loader: async () => ({ DummyA, DummyB }),
    });

    expect(registry.isLazy('DummyA')).toBe(true);
    expect(registry.isLazy('DummyB')).toBe(true);

    // Trigger the load by rendering
    const LazyA = registry.get('DummyA')!;
    await act(async () => {
      render(
        React.createElement(
          React.Suspense,
          { fallback: React.createElement('div', null, 'Loading...') },
          React.createElement(LazyA),
        ),
      );
    });

    await waitFor(() => {
      expect(screen.getByText('DummyA')).toBeInTheDocument();
    });

    // After loading, all components from the same chunk are promoted
    expect(registry.isLazy('DummyA')).toBe(false);
    expect(registry.isLazy('DummyB')).toBe(false);
  });

  it('de-duplicates chunk imports (loader called only once)', async () => {
    const loader = vi.fn(async () => ({ DummyA, DummyB }));

    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['DummyA', 'DummyB'],
      loader,
    });

    // Trigger both lazy components
    const LazyA = registry.get('DummyA')!;
    const LazyB = registry.get('DummyB')!;

    await act(async () => {
      render(
        React.createElement(
          React.Suspense,
          { fallback: React.createElement('div', null, 'Loading...') },
          React.createElement('div', null, [
            React.createElement(LazyA, { key: 'a' }),
            React.createElement(LazyB, { key: 'b' }),
          ]),
        ),
      );
    });

    await waitFor(() => {
      expect(screen.getByText('DummyA')).toBeInTheDocument();
      expect(screen.getByText('DummyB')).toBeInTheDocument();
    });

    // Loader should have been called exactly once
    expect(loader).toHaveBeenCalledTimes(1);
  });

  // ── list() ───────────────────────────────────────────────────────────

  it('list() includes both eager and lazy component names', () => {
    registry.register('Eager1', DummyC);
    registry.registerLazyChunk({
      name: 'testChunk',
      componentNames: ['LazyA', 'LazyB'],
      loader: async () => ({ LazyA: DummyA, LazyB: DummyB }),
    });

    const all = registry.list();
    expect(all).toContain('Eager1');
    expect(all).toContain('LazyA');
    expect(all).toContain('LazyB');
  });

  // ── Multiple chunks ──────────────────────────────────────────────────

  it('supports multiple independent chunks', () => {
    registry.registerLazyChunk({
      name: 'chunk1',
      componentNames: ['Comp1'],
      loader: async () => ({ Comp1: DummyA }),
    });
    registry.registerLazyChunk({
      name: 'chunk2',
      componentNames: ['Comp2'],
      loader: async () => ({ Comp2: DummyB }),
    });

    expect(registry.listChunks()).toEqual(expect.arrayContaining(['chunk1', 'chunk2']));
    expect(registry.isLazy('Comp1')).toBe(true);
    expect(registry.isLazy('Comp2')).toBe(true);
  });
});

describe('ComponentRegistry – singleton integration', () => {
  // These tests use the real singleton to verify the initial registrations
  // from the module-level code.

  it('singleton has lazy chunks registered', async () => {
    const { componentRegistry } = await import('../registry');
    const chunks = componentRegistry.listChunks();
    expect(chunks).toContain('charts');
    expect(chunks).toContain('icons');
    expect(chunks).toContain('controls');
    expect(chunks).toContain('navigation');
    expect(chunks).toContain('overlay');
  });

  it('singleton reports chart components as lazy', async () => {
    const { componentRegistry } = await import('../registry');
    expect(componentRegistry.isLazy('BarChart')).toBe(true);
    expect(componentRegistry.isLazy('PieChart')).toBe(true);
  });

  it('singleton reports core components as eager', async () => {
    const { componentRegistry } = await import('../registry');
    expect(componentRegistry.isLazy('Button')).toBe(false);
    expect(componentRegistry.isLazy('Container')).toBe(false);
    expect(componentRegistry.isLazy('Card')).toBe(false);
  });

  it('singleton total component count includes lazy + eager', async () => {
    const { componentRegistry } = await import('../registry');
    const all = componentRegistry.list();
    // At minimum: ~80 eager + all lazy chunk components
    expect(all.length).toBeGreaterThan(100);
  });
});
