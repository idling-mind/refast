

// Import Tailwind CSS and shadcn styles
import './index.css';

// Main App
export { RefastApp } from './App';


// Components
export { ComponentRenderer } from './components/ComponentRenderer';
export { componentRegistry } from './components/registry';
export type { FeatureChunk, LazyChunkLoader, ComponentType } from './components/registry';

import './components/register-full';


// Base components
export { Container, Text, Fragment } from './components/base';

// shadcn components
export {
  Row,
  Column,
  Grid,
  Flex,
  Center,
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

import { bootstrapRefast } from './bootstrap';

bootstrapRefast(() => {});
