# Stage 6: React Frontend Client

## Progress

- [x] Task 6.1: Project setup
- [x] Task 6.2: Component renderer
- [x] Task 6.3: Event manager
- [x] Task 6.4: WebSocket client
- [x] Task 6.5: State manager
- [x] Task 6.6: shadcn components
- [x] Task 6.7: Build and bundle

## Objectives

Build the React frontend that:
- Renders component trees from Python definitions
- Handles events and callbacks
- Manages WebSocket connection
- Applies updates from backend
- Provides shadcn-based components

## Prerequisites

- Stage 2 complete (component definitions)
- Stage 3 complete (event types)
- Node.js 18+
- React 18+

---

## Task 6.1: Project Setup

### Description
Set up the React/TypeScript project with Vite.

### Files to Create

**src/refast-client/package.json**
```json
{
  "name": "refast-client",
  "version": "0.1.0",
  "type": "module",
  "main": "dist/refast-client.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist"
  ],
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext ts,tsx",
    "test": "vitest",
    "test:ui": "vitest --ui"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@radix-ui/react-slot": "^1.0.2",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vite-plugin-dts": "^3.6.0",
    "vitest": "^1.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.54.0",
    "@typescript-eslint/eslint-plugin": "^6.12.0",
    "@typescript-eslint/parser": "^6.12.0"
  }
}
```

**src/refast-client/tsconfig.json**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "declaration": true,
    "declarationDir": "dist",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**src/refast-client/vite.config.ts**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';
import { resolve } from 'path';

export default defineConfig({
  plugins: [
    react(),
    dts({ insertTypesEntry: true }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.tsx'),
      name: 'RefastClient',
      fileName: 'refast-client',
      formats: ['es', 'umd'],
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
});
```

**src/refast-client/tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### Acceptance Criteria

- [ ] npm install works
- [ ] npm run build works
- [ ] TypeScript compiles

---

## Task 6.2: Component Renderer

### Description
Create the dynamic component renderer.

### Files to Create

**src/refast-client/src/index.tsx**
```typescript
export { RefastApp } from './App';
export { ComponentRenderer } from './components/ComponentRenderer';
export { EventManager } from './events/EventManager';
export { WebSocketClient } from './events/WebSocketClient';
export { StateManager } from './state/StateManager';

// Re-export component types
export type { ComponentTree, ComponentProps } from './types';
```

**src/refast-client/src/types.ts**
```typescript
/**
 * Component tree structure from Python backend.
 */
export interface ComponentTree {
  type: string;
  id: string;
  props: Record<string, unknown>;
  children: (ComponentTree | string)[];
}

/**
 * Props passed to rendered components.
 */
export interface ComponentProps {
  id: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  [key: string]: unknown;
}

/**
 * Callback reference from backend.
 */
export interface CallbackRef {
  callbackId: string;
  boundArgs: Record<string, unknown>;
  debounce?: number;
  throttle?: number;
}

/**
 * Update message from backend.
 */
export interface UpdateMessage {
  type: 'update' | 'state_update' | 'navigate' | 'toast' | 'event';
  operation?: 'replace' | 'append' | 'prepend' | 'remove' | 'update_props';
  targetId?: string;
  component?: ComponentTree;
  props?: Record<string, unknown>;
  state?: Record<string, unknown>;
  path?: string;
  message?: string;
  variant?: string;
  eventType?: string;
  data?: unknown;
}

/**
 * Event message to backend.
 */
export interface EventMessage {
  type: 'callback' | 'event' | 'subscribe' | 'unsubscribe';
  callbackId?: string;
  eventType?: string;
  data?: Record<string, unknown>;
  boundArgs?: Record<string, unknown>;
}
```

**src/refast-client/src/components/ComponentRenderer.tsx**
```typescript
import React, { useMemo, useCallback } from 'react';
import { ComponentTree, CallbackRef } from '../types';
import { useEventManager } from '../events/EventManager';
import { componentRegistry } from './registry';

interface ComponentRendererProps {
  tree: ComponentTree | string;
  onUpdate?: (id: string, component: ComponentTree) => void;
}

/**
 * Renders a component tree from Python backend.
 */
export function ComponentRenderer({ tree, onUpdate }: ComponentRendererProps) {
  const eventManager = useEventManager();
  
  // If it's a string, render as text
  if (typeof tree === 'string') {
    return <>{tree}</>;
  }
  
  const { type, id, props, children } = tree;
  
  // Get the component from registry
  const Component = componentRegistry.get(type);
  
  if (!Component) {
    console.warn(`Unknown component type: ${type}`);
    return <div data-unknown-type={type}>{JSON.stringify(tree)}</div>;
  }
  
  // Process props - convert callbacks to functions
  const processedProps = useMemo(() => {
    const result: Record<string, unknown> = { ...props, id };
    
    for (const [key, value] of Object.entries(props)) {
      if (isCallbackRef(value)) {
        result[key] = createCallbackHandler(value, eventManager);
      }
    }
    
    return result;
  }, [props, id, eventManager]);
  
  // Render children
  const renderedChildren = useMemo(() => {
    if (!children || children.length === 0) {
      return null;
    }
    
    return children.map((child, index) => (
      <ComponentRenderer
        key={typeof child === 'string' ? index : child.id || index}
        tree={child}
        onUpdate={onUpdate}
      />
    ));
  }, [children, onUpdate]);
  
  return (
    <Component {...processedProps} data-refast-id={id}>
      {renderedChildren}
    </Component>
  );
}

/**
 * Check if a value is a callback reference.
 */
function isCallbackRef(value: unknown): value is CallbackRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'callbackId' in value
  );
}

/**
 * Create a handler function for a callback reference.
 */
function createCallbackHandler(
  ref: CallbackRef,
  eventManager: ReturnType<typeof useEventManager>
) {
  const { callbackId, boundArgs, debounce, throttle } = ref;
  
  let handler = (...args: unknown[]) => {
    // Extract event data from args
    const eventData = extractEventData(args);
    
    eventManager.invokeCallback(callbackId, {
      ...boundArgs,
      ...eventData,
    });
  };
  
  // Apply debounce
  if (debounce && debounce > 0) {
    handler = debounceFunction(handler, debounce);
  }
  
  // Apply throttle
  if (throttle && throttle > 0) {
    handler = throttleFunction(handler, throttle);
  }
  
  return handler;
}

/**
 * Extract relevant data from event arguments.
 */
function extractEventData(args: unknown[]): Record<string, unknown> {
  if (args.length === 0) return {};
  
  const first = args[0];
  
  // React event
  if (first && typeof first === 'object' && 'target' in first) {
    const event = first as React.SyntheticEvent<HTMLInputElement>;
    const target = event.target as HTMLInputElement;
    
    return {
      value: target.value,
      checked: target.checked,
      name: target.name,
    };
  }
  
  // Plain value
  if (typeof first === 'string' || typeof first === 'number' || typeof first === 'boolean') {
    return { value: first };
  }
  
  // Object
  if (typeof first === 'object') {
    return first as Record<string, unknown>;
  }
  
  return {};
}

/**
 * Simple debounce implementation.
 */
function debounceFunction<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): T {
  let timeoutId: ReturnType<typeof setTimeout>;
  
  return ((...args: unknown[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  }) as T;
}

/**
 * Simple throttle implementation.
 */
function throttleFunction<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): T {
  let lastCall = 0;
  
  return ((...args: unknown[]) => {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      fn(...args);
    }
  }) as T;
}
```

**src/refast-client/src/components/registry.ts**
```typescript
import React from 'react';

// Import shadcn components
import { Container, Text, Fragment } from './base';
import { Row, Column, Stack, Grid, Flex, Center, Spacer, Divider } from './shadcn/layout';
import { Button, IconButton } from './shadcn/button';
import { Card, CardHeader, CardContent, CardFooter } from './shadcn/card';
import { Input, Textarea, Select, Checkbox, Radio } from './shadcn/input';
import { Slot } from './shadcn/slot';

type ComponentType = React.ComponentType<any>;

/**
 * Registry of all available components.
 */
class ComponentRegistry {
  private components: Map<string, ComponentType> = new Map();
  
  register(name: string, component: ComponentType): void {
    this.components.set(name, component);
  }
  
  get(name: string): ComponentType | undefined {
    return this.components.get(name);
  }
  
  has(name: string): boolean {
    return this.components.has(name);
  }
  
  list(): string[] {
    return Array.from(this.components.keys());
  }
}

export const componentRegistry = new ComponentRegistry();

// Register base components
componentRegistry.register('Container', Container);
componentRegistry.register('Text', Text);
componentRegistry.register('Fragment', Fragment);
componentRegistry.register('Slot', Slot);

// Register layout components
componentRegistry.register('Row', Row);
componentRegistry.register('Column', Column);
componentRegistry.register('Stack', Stack);
componentRegistry.register('Grid', Grid);
componentRegistry.register('Flex', Flex);
componentRegistry.register('Center', Center);
componentRegistry.register('Spacer', Spacer);
componentRegistry.register('Divider', Divider);

// Register button components
componentRegistry.register('Button', Button);
componentRegistry.register('IconButton', IconButton);

// Register card components
componentRegistry.register('Card', Card);
componentRegistry.register('CardHeader', CardHeader);
componentRegistry.register('CardContent', CardContent);
componentRegistry.register('CardFooter', CardFooter);

// Register input components
componentRegistry.register('Input', Input);
componentRegistry.register('Textarea', Textarea);
componentRegistry.register('Select', Select);
componentRegistry.register('Checkbox', Checkbox);
componentRegistry.register('Radio', Radio);
```

### Tests to Write

**src/refast-client/src/components/__tests__/ComponentRenderer.test.tsx**
```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ComponentRenderer } from '../ComponentRenderer';

describe('ComponentRenderer', () => {
  it('renders text content', () => {
    render(<ComponentRenderer tree="Hello World" />);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });
  
  it('renders a simple component', () => {
    const tree = {
      type: 'Container',
      id: 'test-1',
      props: { className: 'test-class' },
      children: ['Test content'],
    };
    
    render(<ComponentRenderer tree={tree} />);
    expect(screen.getByText('Test content')).toBeInTheDocument();
  });
  
  it('renders nested components', () => {
    const tree = {
      type: 'Container',
      id: 'parent',
      props: {},
      children: [
        {
          type: 'Text',
          id: 'child',
          props: {},
          children: ['Nested text'],
        },
      ],
    };
    
    render(<ComponentRenderer tree={tree} />);
    expect(screen.getByText('Nested text')).toBeInTheDocument();
  });
});
```

### Acceptance Criteria

- [ ] Renders component trees
- [ ] Handles nested components
- [ ] Converts callbacks to handlers
- [ ] Debounce/throttle work

---

## Task 6.3: Event Manager

### Description
Create the event manager for handling callbacks and events.

### Files to Create

**src/refast-client/src/events/EventManager.ts**
```typescript
import React, { createContext, useContext, useCallback, useMemo } from 'react';
import { EventMessage, UpdateMessage, ComponentTree } from '../types';

interface EventManagerContextValue {
  invokeCallback: (callbackId: string, data: Record<string, unknown>) => void;
  emitEvent: (eventType: string, data: unknown) => void;
  subscribe: (channel: string) => void;
  unsubscribe: (channel: string) => void;
  onUpdate: (handler: (message: UpdateMessage) => void) => () => void;
}

const EventManagerContext = createContext<EventManagerContextValue | null>(null);

interface EventManagerProviderProps {
  children: React.ReactNode;
  websocket: WebSocket | null;
  onComponentUpdate?: (id: string, component: ComponentTree | null) => void;
}

/**
 * Provides event management to the component tree.
 */
export function EventManagerProvider({
  children,
  websocket,
  onComponentUpdate,
}: EventManagerProviderProps) {
  const updateHandlers = React.useRef<Set<(message: UpdateMessage) => void>>(new Set());
  
  // Handle incoming messages
  React.useEffect(() => {
    if (!websocket) return;
    
    const handleMessage = (event: MessageEvent) => {
      try {
        const message: UpdateMessage = JSON.parse(event.data);
        
        // Notify all handlers
        updateHandlers.current.forEach((handler) => handler(message));
        
        // Handle component updates
        if (message.type === 'update' && onComponentUpdate) {
          const { operation, targetId, component } = message;
          
          if (targetId) {
            if (operation === 'remove') {
              onComponentUpdate(targetId, null);
            } else if (component) {
              onComponentUpdate(targetId, component);
            }
          }
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
    
    websocket.addEventListener('message', handleMessage);
    return () => websocket.removeEventListener('message', handleMessage);
  }, [websocket, onComponentUpdate]);
  
  const invokeCallback = useCallback(
    (callbackId: string, data: Record<string, unknown>) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        console.warn('WebSocket not connected');
        return;
      }
      
      const message: EventMessage = {
        type: 'callback',
        callbackId,
        data,
      };
      
      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );
  
  const emitEvent = useCallback(
    (eventType: string, data: unknown) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        console.warn('WebSocket not connected');
        return;
      }
      
      const message: EventMessage = {
        type: 'event',
        eventType,
        data: data as Record<string, unknown>,
      };
      
      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );
  
  const subscribe = useCallback(
    (channel: string) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) return;
      
      const message: EventMessage = {
        type: 'subscribe',
        eventType: channel,
      };
      
      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );
  
  const unsubscribe = useCallback(
    (channel: string) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) return;
      
      const message: EventMessage = {
        type: 'unsubscribe',
        eventType: channel,
      };
      
      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );
  
  const onUpdate = useCallback(
    (handler: (message: UpdateMessage) => void) => {
      updateHandlers.current.add(handler);
      return () => updateHandlers.current.delete(handler);
    },
    []
  );
  
  const value = useMemo(
    () => ({
      invokeCallback,
      emitEvent,
      subscribe,
      unsubscribe,
      onUpdate,
    }),
    [invokeCallback, emitEvent, subscribe, unsubscribe, onUpdate]
  );
  
  return (
    <EventManagerContext.Provider value={value}>
      {children}
    </EventManagerContext.Provider>
  );
}

/**
 * Hook to access the event manager.
 */
export function useEventManager(): EventManagerContextValue {
  const context = useContext(EventManagerContext);
  
  if (!context) {
    throw new Error('useEventManager must be used within EventManagerProvider');
  }
  
  return context;
}

/**
 * Hook to listen for specific event types.
 */
export function useEvent(
  eventType: string,
  handler: (data: unknown) => void
): void {
  const { onUpdate } = useEventManager();
  
  React.useEffect(() => {
    return onUpdate((message) => {
      if (message.type === 'event' && message.eventType === eventType) {
        handler(message.data);
      }
    });
  }, [eventType, handler, onUpdate]);
}
```

### Acceptance Criteria

- [ ] Callback invocation works
- [ ] Event emission works
- [ ] Subscription management works
- [ ] Update handlers work

---

## Task 6.4: WebSocket Client

### Description
Create the WebSocket connection manager.

### Files to Create

**src/refast-client/src/events/WebSocketClient.ts**
```typescript
import { useEffect, useState, useRef, useCallback } from 'react';

interface WebSocketOptions {
  url: string;
  reconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
}

interface WebSocketState {
  socket: WebSocket | null;
  isConnected: boolean;
  isConnecting: boolean;
  reconnectAttempts: number;
}

/**
 * WebSocket connection manager hook.
 */
export function useWebSocket(options: WebSocketOptions) {
  const {
    url,
    reconnect = true,
    reconnectInterval = 3000,
    maxReconnectAttempts = 10,
    onOpen,
    onClose,
    onError,
  } = options;
  
  const [state, setState] = useState<WebSocketState>({
    socket: null,
    isConnected: false,
    isConnecting: false,
    reconnectAttempts: 0,
  });
  
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout>>();
  const socketRef = useRef<WebSocket | null>(null);
  
  const connect = useCallback(() => {
    // Clean up existing connection
    if (socketRef.current) {
      socketRef.current.close();
    }
    
    setState((s) => ({ ...s, isConnecting: true }));
    
    const socket = new WebSocket(url);
    socketRef.current = socket;
    
    socket.onopen = () => {
      setState({
        socket,
        isConnected: true,
        isConnecting: false,
        reconnectAttempts: 0,
      });
      onOpen?.();
    };
    
    socket.onclose = () => {
      setState((s) => ({
        ...s,
        socket: null,
        isConnected: false,
        isConnecting: false,
      }));
      onClose?.();
      
      // Attempt reconnection
      if (reconnect && state.reconnectAttempts < maxReconnectAttempts) {
        reconnectTimeoutRef.current = setTimeout(() => {
          setState((s) => ({
            ...s,
            reconnectAttempts: s.reconnectAttempts + 1,
          }));
          connect();
        }, reconnectInterval);
      }
    };
    
    socket.onerror = (error) => {
      onError?.(error);
    };
  }, [url, reconnect, reconnectInterval, maxReconnectAttempts, onOpen, onClose, onError]);
  
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
    
    setState({
      socket: null,
      isConnected: false,
      isConnecting: false,
      reconnectAttempts: 0,
    });
  }, []);
  
  const send = useCallback((data: unknown) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(data));
      return true;
    }
    return false;
  }, []);
  
  // Connect on mount
  useEffect(() => {
    connect();
    return disconnect;
  }, [connect, disconnect]);
  
  return {
    socket: state.socket,
    isConnected: state.isConnected,
    isConnecting: state.isConnecting,
    reconnectAttempts: state.reconnectAttempts,
    connect,
    disconnect,
    send,
  };
}

/**
 * Build WebSocket URL from current location.
 */
export function buildWebSocketUrl(path: string = '/ws'): string {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}${path}`;
}
```

### Acceptance Criteria

- [ ] WebSocket connects
- [ ] Reconnection works
- [ ] Send/receive works
- [ ] Cleanup on unmount

---

## Task 6.5: State Manager

### Description
Create the state manager for component tree updates.

### Files to Create

**src/refast-client/src/state/StateManager.ts**
```typescript
import { useState, useCallback, useMemo } from 'react';
import { ComponentTree, UpdateMessage } from '../types';

interface StateManagerState {
  componentTree: ComponentTree | null;
  appState: Record<string, unknown>;
}

/**
 * Hook for managing component tree and app state.
 */
export function useStateManager(initialTree?: ComponentTree) {
  const [state, setState] = useState<StateManagerState>({
    componentTree: initialTree || null,
    appState: {},
  });
  
  /**
   * Update the entire component tree.
   */
  const setComponentTree = useCallback((tree: ComponentTree) => {
    setState((s) => ({ ...s, componentTree: tree }));
  }, []);
  
  /**
   * Update a specific component by ID.
   */
  const updateComponent = useCallback(
    (id: string, update: ComponentTree | null, operation: string = 'replace') => {
      setState((s) => {
        if (!s.componentTree) return s;
        
        const newTree = applyUpdate(s.componentTree, id, update, operation);
        return { ...s, componentTree: newTree };
      });
    },
    []
  );
  
  /**
   * Update app state.
   */
  const setAppState = useCallback((newState: Record<string, unknown>) => {
    setState((s) => ({
      ...s,
      appState: { ...s.appState, ...newState },
    }));
  }, []);
  
  /**
   * Handle an update message from the backend.
   */
  const handleUpdate = useCallback((message: UpdateMessage) => {
    switch (message.type) {
      case 'update':
        if (message.targetId && message.operation) {
          updateComponent(
            message.targetId,
            message.component || null,
            message.operation
          );
        }
        break;
      
      case 'state_update':
        if (message.state) {
          setAppState(message.state);
        }
        break;
    }
  }, [updateComponent, setAppState]);
  
  return {
    componentTree: state.componentTree,
    appState: state.appState,
    setComponentTree,
    updateComponent,
    setAppState,
    handleUpdate,
  };
}

/**
 * Apply an update operation to a component tree.
 */
function applyUpdate(
  tree: ComponentTree,
  targetId: string,
  update: ComponentTree | null,
  operation: string
): ComponentTree {
  // Check if this is the target
  if (tree.id === targetId) {
    switch (operation) {
      case 'replace':
        return update || tree;
      
      case 'update_props':
        return {
          ...tree,
          props: { ...tree.props, ...(update?.props || {}) },
        };
      
      case 'remove':
        // Can't remove self, handled by parent
        return tree;
      
      case 'append':
        if (update) {
          return {
            ...tree,
            children: [...tree.children, update],
          };
        }
        return tree;
      
      case 'prepend':
        if (update) {
          return {
            ...tree,
            children: [update, ...tree.children],
          };
        }
        return tree;
      
      default:
        return tree;
    }
  }
  
  // Recursively search children
  const newChildren = tree.children.map((child) => {
    if (typeof child === 'string') return child;
    
    // Handle remove operation
    if (operation === 'remove' && child.id === targetId) {
      return null;
    }
    
    return applyUpdate(child, targetId, update, operation);
  }).filter((child): child is ComponentTree | string => child !== null);
  
  return {
    ...tree,
    children: newChildren,
  };
}
```

### Acceptance Criteria

- [ ] Tree updates work
- [ ] Replace operation works
- [ ] Append/prepend work
- [ ] Remove works
- [ ] State updates work

---

## Task 6.6: shadcn Components

### Description
Create the React implementations of shadcn components.

### Files to Create

**src/refast-client/src/components/base.tsx**
```typescript
import React from 'react';
import { cn } from '../utils';

interface ContainerProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}

export function Container({ id, className, style, children }: ContainerProps) {
  return (
    <div id={id} className={cn('', className)} style={style}>
      {children}
    </div>
  );
}

interface TextProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
}

export function Text({ id, className, style, children }: TextProps) {
  return (
    <span id={id} className={cn('', className)} style={style}>
      {children}
    </span>
  );
}

interface FragmentProps {
  children?: React.ReactNode;
}

export function Fragment({ children }: FragmentProps) {
  return <>{children}</>;
}
```

**src/refast-client/src/components/shadcn/layout.tsx**
```typescript
import React from 'react';
import { cn } from '../../utils';

interface RowProps {
  id?: string;
  className?: string;
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
  align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
  gap?: number | string;
  wrap?: boolean;
  children?: React.ReactNode;
}

export function Row({
  id,
  className,
  justify = 'start',
  align = 'start',
  gap = 0,
  wrap = false,
  children,
}: RowProps) {
  const justifyClass = {
    start: 'justify-start',
    end: 'justify-end',
    center: 'justify-center',
    between: 'justify-between',
    around: 'justify-around',
    evenly: 'justify-evenly',
  }[justify];
  
  const alignClass = {
    start: 'items-start',
    end: 'items-end',
    center: 'items-center',
    stretch: 'items-stretch',
    baseline: 'items-baseline',
  }[align];
  
  return (
    <div
      id={id}
      className={cn(
        'flex flex-row',
        justifyClass,
        alignClass,
        wrap && 'flex-wrap',
        className
      )}
      style={{ gap: typeof gap === 'number' ? `${gap * 0.25}rem` : gap }}
    >
      {children}
    </div>
  );
}

interface ColumnProps {
  id?: string;
  className?: string;
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
  align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
  gap?: number | string;
  children?: React.ReactNode;
}

export function Column({
  id,
  className,
  justify = 'start',
  align = 'stretch',
  gap = 0,
  children,
}: ColumnProps) {
  const justifyClass = {
    start: 'justify-start',
    end: 'justify-end',
    center: 'justify-center',
    between: 'justify-between',
    around: 'justify-around',
    evenly: 'justify-evenly',
  }[justify];
  
  const alignClass = {
    start: 'items-start',
    end: 'items-end',
    center: 'items-center',
    stretch: 'items-stretch',
    baseline: 'items-baseline',
  }[align];
  
  return (
    <div
      id={id}
      className={cn('flex flex-col', justifyClass, alignClass, className)}
      style={{ gap: typeof gap === 'number' ? `${gap * 0.25}rem` : gap }}
    >
      {children}
    </div>
  );
}

interface StackProps {
  id?: string;
  className?: string;
  spacing?: number | string;
  direction?: 'vertical' | 'horizontal';
  children?: React.ReactNode;
}

export function Stack({
  id,
  className,
  spacing = 4,
  direction = 'vertical',
  children,
}: StackProps) {
  return (
    <div
      id={id}
      className={cn(
        'flex',
        direction === 'vertical' ? 'flex-col' : 'flex-row',
        className
      )}
      style={{
        gap: typeof spacing === 'number' ? `${spacing * 0.25}rem` : spacing,
      }}
    >
      {children}
    </div>
  );
}

interface GridProps {
  id?: string;
  className?: string;
  columns?: number | string;
  rows?: number | string;
  gap?: number | string;
  children?: React.ReactNode;
}

export function Grid({
  id,
  className,
  columns = 1,
  rows,
  gap = 0,
  children,
}: GridProps) {
  return (
    <div
      id={id}
      className={cn('grid', className)}
      style={{
        gridTemplateColumns:
          typeof columns === 'number' ? `repeat(${columns}, 1fr)` : columns,
        gridTemplateRows: rows
          ? typeof rows === 'number'
            ? `repeat(${rows}, 1fr)`
            : rows
          : undefined,
        gap: typeof gap === 'number' ? `${gap * 0.25}rem` : gap,
      }}
    >
      {children}
    </div>
  );
}

export function Flex(props: RowProps & { direction?: 'row' | 'column' }) {
  const { direction = 'row', ...rest } = props;
  return direction === 'row' ? <Row {...rest} /> : <Column {...rest} />;
}

export function Center({ id, className, children }: ContainerProps) {
  return (
    <div
      id={id}
      className={cn('flex items-center justify-center', className)}
    >
      {children}
    </div>
  );
}

interface SpacerProps {
  size?: number | string;
}

export function Spacer({ size }: SpacerProps) {
  return (
    <div
      className="flex-grow"
      style={size ? { flexGrow: 0, flexBasis: size } : undefined}
    />
  );
}

interface DividerProps {
  orientation?: 'horizontal' | 'vertical';
  className?: string;
}

export function Divider({ orientation = 'horizontal', className }: DividerProps) {
  return (
    <div
      className={cn(
        'bg-border',
        orientation === 'horizontal' ? 'h-px w-full' : 'w-px h-full',
        className
      )}
    />
  );
}

interface ContainerProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
}
```

**src/refast-client/src/components/shadcn/button.tsx**
```typescript
import React from 'react';
import { cn } from '../../utils';

interface ButtonProps {
  id?: string;
  className?: string;
  variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  children?: React.ReactNode;
}

export function Button({
  id,
  className,
  variant = 'default',
  size = 'md',
  disabled = false,
  loading = false,
  type = 'button',
  onClick,
  children,
}: ButtonProps) {
  const variantClasses = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
    link: 'text-primary underline-offset-4 hover:underline',
  };
  
  const sizeClasses = {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-11 px-8 text-lg',
    icon: 'h-10 w-10',
  };
  
  return (
    <button
      id={id}
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
        'disabled:pointer-events-none disabled:opacity-50',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
    >
      {loading && (
        <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  );
}

interface IconButtonProps {
  id?: string;
  className?: string;
  icon: string;
  variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  ariaLabel?: string;
}

export function IconButton({
  id,
  className,
  icon,
  variant = 'ghost',
  size = 'md',
  disabled = false,
  onClick,
  ariaLabel,
}: IconButtonProps) {
  // Icon rendering would use lucide-react or similar
  return (
    <Button
      id={id}
      className={className}
      variant={variant}
      size="icon"
      disabled={disabled}
      onClick={onClick}
    >
      <span className="sr-only">{ariaLabel || icon}</span>
      {/* Icon component would go here */}
      <span>{icon}</span>
    </Button>
  );
}
```

Continue with more components (card.tsx, input.tsx, slot.tsx, etc.) following the same pattern.

**src/refast-client/src/utils/index.ts**
```typescript
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge class names with Tailwind CSS classes.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### Acceptance Criteria

- [ ] Base components work
- [ ] Layout components work
- [ ] Button components work
- [ ] Input components work
- [ ] All match Python definitions

---

## Task 6.7: Main App Component

### Description
Create the main Refast App component.

### Files to Create

**src/refast-client/src/App.tsx**
```typescript
import React, { useEffect, useMemo } from 'react';
import { ComponentRenderer } from './components/ComponentRenderer';
import { EventManagerProvider, useEventManager } from './events/EventManager';
import { useWebSocket, buildWebSocketUrl } from './events/WebSocketClient';
import { useStateManager } from './state/StateManager';
import { ComponentTree } from './types';

interface RefastAppProps {
  initialTree?: ComponentTree;
  wsUrl?: string;
}

/**
 * Main Refast application component.
 */
export function RefastApp({ initialTree, wsUrl }: RefastAppProps) {
  // Get initial data from window if not provided
  const tree = useMemo(() => {
    if (initialTree) return initialTree;
    
    const windowData = (window as any).__REFAST_INITIAL_DATA__;
    return windowData || null;
  }, [initialTree]);
  
  // WebSocket connection
  const { socket, isConnected } = useWebSocket({
    url: wsUrl || buildWebSocketUrl('/ws'),
    reconnect: true,
  });
  
  // State management
  const { componentTree, setComponentTree, updateComponent, handleUpdate } =
    useStateManager(tree);
  
  // Initialize with server data
  useEffect(() => {
    if (tree && !componentTree) {
      setComponentTree(tree);
    }
  }, [tree, componentTree, setComponentTree]);
  
  if (!componentTree) {
    return <div>Loading...</div>;
  }
  
  return (
    <EventManagerProvider
      websocket={socket}
      onComponentUpdate={updateComponent}
    >
      <RefastAppContent
        tree={componentTree}
        isConnected={isConnected}
        onUpdate={handleUpdate}
      />
    </EventManagerProvider>
  );
}

interface RefastAppContentProps {
  tree: ComponentTree;
  isConnected: boolean;
  onUpdate: (message: any) => void;
}

function RefastAppContent({ tree, isConnected, onUpdate }: RefastAppContentProps) {
  const { onUpdate: registerUpdateHandler } = useEventManager();
  
  // Register update handler
  useEffect(() => {
    return registerUpdateHandler(onUpdate);
  }, [registerUpdateHandler, onUpdate]);
  
  return (
    <div className="refast-app" data-connected={isConnected}>
      <ComponentRenderer tree={tree} />
    </div>
  );
}

// Export for standalone use
export default RefastApp;
```

### Acceptance Criteria

- [ ] App mounts and renders
- [ ] WebSocket connects
- [ ] Updates applied
- [ ] Initial data loaded

---

## Final Checklist for Stage 6

- [ ] Project setup complete
- [ ] Component renderer works
- [ ] Event manager works
- [ ] WebSocket client works
- [ ] State manager works
- [ ] All shadcn components implemented
- [ ] Build produces bundle
- [ ] Tests pass
- [ ] Update `.github/copilot-instructions.md` status to 🟢
