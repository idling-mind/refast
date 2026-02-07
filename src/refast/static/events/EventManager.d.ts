import { default as React } from 'react';
import { UpdateMessage, ComponentTree } from '../types';

interface EventManagerContextValue {
    invokeCallback: (callbackId: string, data: Record<string, unknown>, eventData?: Record<string, unknown>) => void;
    emitEvent: (eventType: string, data: unknown) => void;
    subscribe: (channel: string) => void;
    unsubscribe: (channel: string) => void;
    onUpdate: (handler: (message: UpdateMessage) => void) => () => void;
}
interface EventManagerProviderProps {
    children: React.ReactNode;
    websocket: WebSocket | null;
    onComponentUpdate?: (id: string, component: ComponentTree | null, operation?: string) => void;
}
/**
 * Provides event management to the component tree.
 */
export declare function EventManagerProvider({ children, websocket, onComponentUpdate, }: EventManagerProviderProps): React.ReactElement;
/**
 * Hook to access the event manager.
 */
export declare function useEventManager(): EventManagerContextValue;
/**
 * Hook to listen for specific event types.
 */
export declare function useEvent(eventType: string, handler: (data: unknown) => void): void;
/**
 * Hook to subscribe to a channel on mount.
 */
export declare function useChannel(channel: string): void;
export {};
