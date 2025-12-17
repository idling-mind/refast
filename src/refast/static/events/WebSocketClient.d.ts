import { WebSocketOptions } from '../types';

/**
 * WebSocket connection manager hook.
 */
export declare function useWebSocket(options: WebSocketOptions): {
    socket: WebSocket | null;
    isConnected: boolean;
    isConnecting: boolean;
    reconnectAttempts: number;
    connect: () => void;
    disconnect: () => void;
    send: (data: unknown) => boolean;
};
/**
 * Build WebSocket URL from current location.
 */
export declare function buildWebSocketUrl(path?: string): string;
/**
 * Simple WebSocket client class for non-hook usage.
 */
export declare class WebSocketClient {
    private socket;
    private url;
    private reconnect;
    private reconnectInterval;
    private maxReconnectAttempts;
    private reconnectAttempts;
    private reconnectTimeout;
    private messageHandlers;
    private connectionHandlers;
    constructor(options: WebSocketOptions);
    connect(): void;
    disconnect(): void;
    send(data: unknown): boolean;
    onMessage(handler: (data: unknown) => void): () => void;
    onConnectionChange(handler: (connected: boolean) => void): () => void;
    private notifyConnectionChange;
    get isConnected(): boolean;
}
