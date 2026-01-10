import React from 'react';
import ReactDOM from 'react-dom';
import { createRoot } from 'react-dom/client';

// Import Tailwind CSS and shadcn styles
import './index.css';

// Main App
export { RefastApp } from './App';
import { RefastApp } from './App';

// Components
export { ComponentRenderer } from './components/ComponentRenderer';
export { componentRegistry } from './components/registry';
import { componentRegistry } from './components/registry';

// Base components
export { Container, Text, Fragment } from './components/base';

// shadcn components
export {
  Row,
  Column,
  Stack,
  Grid,
  Flex,
  Center,
  Spacer,
  Divider,
} from './components/shadcn/layout';

export { Button, IconButton } from './components/shadcn/button';

export {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  CardTitle,
  CardDescription,
} from './components/shadcn/card';

export {
  Input,
  Textarea,
  Select,
  SelectOption,
  Checkbox,
  Radio,
  RadioGroup,
} from './components/shadcn/input';

export { Slot } from './components/shadcn/slot';

export {
  Heading,
  Paragraph,
  Link,
  Code,
  BlockQuote,
  List,
  ListItem,
  Label,
} from './components/shadcn/typography';

export {
  Alert,
  AlertTitle,
  AlertDescription,
  Badge,
  Progress,
  Spinner,
  Toast,
  Skeleton,
} from './components/shadcn/feedback';

export { ToastManager, toast, dismissToast, promiseToast } from './components/ToastManager';

export {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  Avatar,
  Image,
  Tooltip,
} from './components/shadcn/data_display';

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

// Auto-initialize when script loads
function initializeRefast(): void {
  // Look for the refast-root element
  const rootElement = document.getElementById('refast-root');
  
  if (rootElement && window.__REFAST_INITIAL_DATA__) {
    const root = createRoot(rootElement);
    root.render(React.createElement(RefastApp));
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeRefast);
} else {
  initializeRefast();
}

// =============================================================================
// Extension Support: Expose RefastClient on window for third-party extensions
// =============================================================================

/**
 * RefastClient global object for extension development.
 * 
 * Extensions can use this to:
 * - Register custom React components
 * - Access React and ReactDOM (avoid bundling duplicates)
 * - Use utility functions
 * 
 * Example usage in an extension's UMD bundle:
 * ```javascript
 * (function() {
 *   const { componentRegistry, React } = window.RefastClient;
 *   
 *   const MyComponent = (props) => {
 *     return React.createElement('div', { className: props.className }, props.children);
 *   };
 *   
 *   componentRegistry.register('MyComponent', MyComponent);
 * })();
 * ```
 */
declare global {
  interface Window {
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
  }
}

// Expose RefastClient globally for extensions
window.RefastClient = {
  componentRegistry,
  React,
  ReactDOM,
  version: '0.1.0',
};
