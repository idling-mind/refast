import React from 'react';
import * as ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';

// Import Tailwind CSS and shadcn styles
import './index.css';

// Main App
export { RefastApp } from './App';
import { RefastApp } from './App';

// Components
export { ComponentRenderer } from './components/ComponentRenderer';
export { componentRegistry } from './components/registry';
export type { FeatureChunk, LazyChunkLoader, ComponentType } from './components/registry';
import { componentRegistry } from './components/registry';

// Base components
export { Container, Text, Fragment } from './components/base';
import { Container, Text, Fragment } from './components/base';

// slot
export { Slot } from './components/shadcn/slot';
import { Slot } from './components/shadcn/slot';

export { ToastManager, toast, dismissToast, promiseToast } from './components/ToastManager';
import { Toaster } from './components/shadcn/toaster';

// Events
export {
  EventManagerProvider,
  useEventManager,
  useEvent,
  useChannel,
} from './events/EventManager';

export {
  useWebSocket,
  buildWebSocketUrl,
  WebSocketClient,
} from './events/WebSocketClient';

// State
export {
  useStateManager,
  findComponent,
  getComponentPath,
} from './state/StateManager';

// Utils
export { cn, debounce, throttle, generateId, isPlainObject, deepMerge } from './utils';

// Types
export type {
  ComponentTree,
  ComponentProps,
  CallbackRef,
  UpdateMessage,
  EventMessage,
  WebSocketState,
  WebSocketOptions,
  StateManagerState,
} from './types';

function getConfiguredPreloadedFeatures(): string[] {
  const globalValue = (window as Window & { __REFAST_PRELOADED_FEATURES__?: unknown })
    .__REFAST_PRELOADED_FEATURES__;
  if (!Array.isArray(globalValue)) {
    return [];
  }
  return globalValue.filter((v): v is string => typeof v === 'string');
}

function getConfiguredStartupFeatures(): string[] {
  const globalValue = (window as Window & { __REFAST_STARTUP_FEATURES__?: unknown })
    .__REFAST_STARTUP_FEATURES__;
  if (!Array.isArray(globalValue)) {
    return getConfiguredPreloadedFeatures();
  }
  return globalValue.filter((v): v is string => typeof v === 'string');
}

function getConfiguredLazyFeatures(): string[] {
  const globalValue = (window as Window & { __REFAST_LAZY_FEATURES__?: unknown })
    .__REFAST_LAZY_FEATURES__;
  if (!Array.isArray(globalValue)) {
    return componentRegistry.listChunks();
  }
  return globalValue.filter((v): v is string => typeof v === 'string');
}

async function warmupPreloadedFeatures(): Promise<void> {
  const configured = getConfiguredStartupFeatures();
  if (configured.length === 0) {
    return;
  }

  const available = new Set(componentRegistry.listChunks());
  const selected = configured.filter((name) => available.has(name));
  if (selected.length === 0) {
    return;
  }

  try {
    await componentRegistry.preloadChunks(selected);
  } catch (error) {
    console.error('Failed to preload configured feature chunks:', error);
  }
}

// Auto-initialize when script loads
async function initializeRefast(): Promise<void> {
  // Look for the refast-root element
  const rootElement = document.getElementById('refast-root');

  if (rootElement) {
    componentRegistry.configureLazyFeatures(getConfiguredLazyFeatures());
    await warmupPreloadedFeatures();
    const root = createRoot(rootElement);
    root.render(React.createElement(RefastApp));
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    void initializeRefast();
  });
} else {
  void initializeRefast();
}

// =============================================================================
// Extension Support: Expose RefastClient on window for third-party extensions
// =============================================================================

declare global {
  interface Window {
    __REFAST_PRELOADED_FEATURES__?: string[];
    __REFAST_STARTUP_FEATURES__?: string[];
    __REFAST_LAZY_FEATURES__?: string[];
    __REFAST_EXTENSIONS_READY__?: boolean;
    __REFAST_EXTENSION_SCRIPT_MAP__?: Record<string, string[]>;
    __REFAST_EXTENSION_COMPONENT_MAP__?: Record<string, string>;
    __REFAST_EXTENSION_LOADED__?: Record<string, boolean>;
    __REFAST_LOAD_EXTENSION__?: (name: string) => Promise<void>;
    RefastClient: {
      componentRegistry: typeof componentRegistry;
      React: typeof React;
      ReactDOM: typeof ReactDOM;
      version: string;
    };
    React: typeof React;
    ReactDOM: typeof ReactDOM;
  }
}

// Expose RefastClient globally for extensions
window.RefastClient = {
  componentRegistry,
  React,
  ReactDOM,
  version: '0.1.0',
};

// Also expose React and ReactDOM globally for UMD extension bundles
window.React = React;
window.ReactDOM = ReactDOM;

// Register ONLY core primitives in the componentRegistry
componentRegistry.register('Container', Container);
componentRegistry.register('Text', Text);
componentRegistry.register('Fragment', Fragment);
componentRegistry.register('Slot', Slot);
componentRegistry.register('Toast', Toaster);

// Dispatch a custom event so extension scripts (loaded after the core ESM
// module) know that RefastClient is ready.
window.dispatchEvent(new CustomEvent('refast:ready'));
