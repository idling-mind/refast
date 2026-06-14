import '@testing-library/jest-dom';
import React from 'react';
import { vi } from 'vitest';

// jsdom does not implement ResizeObserver; polyfill it for component tests.
(globalThis as typeof globalThis & { ResizeObserver: unknown }).ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock heavy markdown modules to prevent test timeouts and ESM import cascade
vi.mock('react-markdown', () => {
  return {
    default: ({ children, components }: { children: string; components?: Record<string, React.ComponentType<any>> }) => {
      // Basic mock rendering to support custom tags / images mapping in tests
      const imgMatch = /!\[([^\]]*)\]\(([^)]*)\)/.exec(children);
      if (imgMatch && components?.img) {
        const alt = imgMatch[1];
        const src = imgMatch[2];
        const ImgComp = components.img;
        return React.createElement('div', { 'data-testid': 'mocked-react-markdown' }, 
          React.createElement(ImgComp, { src, alt })
        );
      }
      return React.createElement('div', { 'data-testid': 'mocked-react-markdown' }, children);
    }
  };
});

vi.mock('remark-gfm', () => ({ default: {} }));
vi.mock('rehype-raw', () => ({ default: {} }));
