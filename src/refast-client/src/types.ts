import React from 'react';

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
  id?: string;
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
  type: 'update' | 'state_update' | 'navigate' | 'toast' | 'event' | 'refresh' | 'store_update' | 'store_ready' | 'page_render';
  operation?: 'replace' | 'append' | 'prepend' | 'remove' | 'update_props' | 'update_children';
  targetId?: string;
  component?: ComponentTree;
  props?: Record<string, unknown>;
  children?: (ComponentTree | string)[];
  state?: Record<string, unknown>;
  path?: string;
  message?: string;
  variant?: string;
  duration?: number;
  eventType?: string;
  data?: unknown;
  updates?: StoreUpdate[];
  // Toast-specific properties
  description?: string;
  position?: string;
  dismissible?: boolean;
  closeButton?: boolean;
  invert?: boolean;
  icon?: string;
  action?: { label: string; callback_id: string };
  cancel?: { label: string; callback_id: string };
  id?: string;  // toast_id
}

/**
 * Store update operation from backend.
 */
export interface StoreUpdate {
  storageType: 'local' | 'session';
  operation: 'set' | 'delete' | 'clear';
  key: string | null;
  value?: unknown;
  encrypt?: boolean;
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

/**
 * WebSocket connection state.
 */
export interface WebSocketState {
  socket: WebSocket | null;
  isConnected: boolean;
  isConnecting: boolean;
  reconnectAttempts: number;
}

/**
 * WebSocket connection options.
 */
export interface WebSocketOptions {
  url: string;
  reconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
}

/**
 * State manager state.
 */
export interface StateManagerState {
  componentTree: ComponentTree | null;
  appState: Record<string, unknown>;
}
