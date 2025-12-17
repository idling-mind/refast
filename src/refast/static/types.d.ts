import { default as React } from 'react';

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
    type: 'update' | 'state_update' | 'navigate' | 'toast' | 'event';
    operation?: 'replace' | 'append' | 'prepend' | 'remove' | 'update_props' | 'update_children';
    targetId?: string;
    component?: ComponentTree;
    props?: Record<string, unknown>;
    children?: (ComponentTree | string)[];
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
