import React from 'react';
import * as ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';
import { RefastApp } from './App';
import { componentRegistry } from './components/registry';

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
      /** Component registry for registering custom React components */
      componentRegistry: typeof componentRegistry;
      /** React library - use this instead of bundling your own */
      React: typeof React;
      /** ReactDOM library - use this instead of bundling your own */
      ReactDOM: typeof ReactDOM;
      /** Version of the Refast client */
      version: string;
    };
    /** React exposed globally for UMD extension bundles */
    React: typeof React;
    /** ReactDOM exposed globally for UMD extension bundles */
    ReactDOM: typeof ReactDOM;
  }
}

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

async function initializeRefast(): Promise<void> {
  const rootElement = document.getElementById('refast-root');
  if (rootElement) {
    componentRegistry.configureLazyFeatures(getConfiguredLazyFeatures());
    await warmupPreloadedFeatures();
    const root = createRoot(rootElement);
    root.render(React.createElement(RefastApp));
  }
}

export function bootstrapRefast(registerCallback: () => void, version: string = '0.1.0') {
  // 1. Expose globals for extensions
  window.RefastClient = {
    componentRegistry,
    React,
    ReactDOM,
    version,
  };
  window.React = React;
  window.ReactDOM = ReactDOM;

  // 2. Perform registry initialization
  registerCallback();

  // 3. Initialize on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      void initializeRefast();
    });
  } else {
    void initializeRefast();
  }

  // 4. Dispatch ready event
  window.dispatchEvent(new CustomEvent('refast:ready'));
}
