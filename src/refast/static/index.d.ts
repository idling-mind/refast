import { default as React } from 'react';
import { default as ReactDOM } from 'react-dom';
import { componentRegistry } from './components/registry';

export { RefastApp } from './App';
export { ComponentRenderer } from './components/ComponentRenderer';
export { componentRegistry } from './components/registry';
export { Container, Text, Fragment } from './components/base';
export { Row, Column, Grid, Flex, Center, } from './components/shadcn/layout';
export { Button, IconButton } from './components/shadcn/button';
export { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription, } from './components/shadcn/card';
export { Input, Textarea, Select, SelectOption, Checkbox, Radio, RadioGroup, } from './components/shadcn/input';
export { Slot } from './components/shadcn/slot';
export { Heading, Paragraph, Link, Code, BlockQuote, List, ListItem, Label, } from './components/shadcn/typography';
export { Alert, AlertTitle, AlertDescription, Badge, Progress, Spinner, Skeleton, } from './components/shadcn/feedback';
export { ToastManager, toast, dismissToast, promiseToast } from './components/ToastManager';
export { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, Avatar, Image, Tooltip, } from './components/shadcn/data_display';
export { EventManagerProvider, useEventManager, useEvent, useChannel, } from './events/EventManager';
export { useWebSocket, buildWebSocketUrl, WebSocketClient, } from './events/WebSocketClient';
export { useStateManager, findComponent, getComponentPath, } from './state/StateManager';
export { cn, debounce, throttle, generateId, isPlainObject, deepMerge } from './utils';
export type { ComponentTree, ComponentProps, CallbackRef, UpdateMessage, EventMessage, WebSocketState, WebSocketOptions, StateManagerState, } from './types';
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
        /** React exposed globally for UMD extension bundles */
        React: typeof React;
        /** ReactDOM exposed globally for UMD extension bundles */
        ReactDOM: typeof ReactDOM;
    }
}
