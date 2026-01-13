import { default as React } from 'react';
import { ComponentTree } from '../../types';

interface ConnectionStatusProps {
    id?: string;
    className?: string;
    childrenConnected?: ComponentTree[];
    childrenDisconnected?: ComponentTree[];
    position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'inline';
    onDisconnect?: {
        callbackId: string;
        boundArgs?: Record<string, unknown>;
    };
    onReconnect?: {
        callbackId: string;
        boundArgs?: Record<string, unknown>;
    };
    jsOnDisconnect?: {
        jsFunction: string;
        boundArgs?: Record<string, unknown>;
    };
    jsOnReconnect?: {
        jsFunction: string;
        boundArgs?: Record<string, unknown>;
    };
    debounceMs?: number;
    'data-refast-id'?: string;
}
/**
 * ConnectionStatus component - conditionally shows content based on WebSocket connection state.
 *
 * Reads connection state from the parent .refast-app element's data attributes
 * and fires callbacks when connection state changes.
 */
export declare function ConnectionStatus({ id, className, childrenConnected, childrenDisconnected, position, onDisconnect, onReconnect, jsOnDisconnect, jsOnReconnect, debounceMs, 'data-refast-id': dataRefastId, }: ConnectionStatusProps): React.ReactElement | null;
export default ConnectionStatus;
