import '@testing-library/jest-dom';

// jsdom does not implement ResizeObserver; polyfill it for component tests.
// Use globalThis (ES2020) instead of Node.js-specific `global`.
(globalThis as typeof globalThis & { ResizeObserver: unknown }).ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};
