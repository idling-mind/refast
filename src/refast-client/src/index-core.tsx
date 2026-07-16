

// Import Tailwind CSS and shadcn styles
import './index.css';

// Main App
export { RefastApp } from './App';


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

import { bootstrapRefast } from './bootstrap';

bootstrapRefast(() => {
  // Register ONLY core primitives in the componentRegistry
  componentRegistry.register('Container', Container);
  componentRegistry.register('Text', Text);
  componentRegistry.register('Fragment', Fragment);
  componentRegistry.register('Slot', Slot);
  componentRegistry.register('Toast', Toaster);
});
