import { useEffect, useState, useRef, useCallback } from 'react';
import { WebSocketOptions, WebSocketState } from '../types';

/**
 * WebSocket connection manager hook.
 */
export function useWebSocket(options: WebSocketOptions) {
  const {
    url,
    reconnect = true,
    reconnectInterval = 3000,
    maxReconnectAttempts = 5,
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
  const reconnectAttemptsRef = useRef(0);
  const mountedRef = useRef(false);
  const connectingRef = useRef(false);
  
  // Use refs for callbacks to avoid re-creating connect function
  const onOpenRef = useRef(onOpen);
  const onCloseRef = useRef(onClose);
  const onErrorRef = useRef(onError);
  
  // Update refs when callbacks change
  useEffect(() => {
    onOpenRef.current = onOpen;
    onCloseRef.current = onClose;
    onErrorRef.current = onError;
  }, [onOpen, onClose, onError]);

  const connect = useCallback(() => {
    // Don't connect if unmounted or already connecting/connected
    if (!mountedRef.current) return;
    if (connectingRef.current) return;
    if (socketRef.current?.readyState === WebSocket.OPEN) return;
    if (socketRef.current?.readyState === WebSocket.CONNECTING) return;
    
    // Clean up existing connection
    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }

    connectingRef.current = true;
    setState((s) => ({ ...s, isConnecting: true }));

    try {
      const socket = new WebSocket(url);
      socketRef.current = socket;

      socket.onopen = () => {
        connectingRef.current = false;
        if (!mountedRef.current) {
          socket.close();
          return;
        }
        reconnectAttemptsRef.current = 0;
        setState({
          socket,
          isConnected: true,
          isConnecting: false,
          reconnectAttempts: 0,
        });
        onOpenRef.current?.();
      };

      socket.onclose = () => {
        connectingRef.current = false;
        if (!mountedRef.current) return;
        
        setState((s) => ({
          ...s,
          socket: null,
          isConnected: false,
          isConnecting: false,
        }));
        onCloseRef.current?.();

        // Attempt reconnection with exponential backoff
        if (reconnect && reconnectAttemptsRef.current < maxReconnectAttempts && mountedRef.current) {
          const backoff = Math.min(reconnectInterval * Math.pow(2, reconnectAttemptsRef.current), 30000);
          reconnectTimeoutRef.current = setTimeout(() => {
            if (!mountedRef.current) return;
            reconnectAttemptsRef.current += 1;
            setState((s) => ({
              ...s,
              reconnectAttempts: reconnectAttemptsRef.current,
            }));
            connect();
          }, backoff);
        }
      };

      socket.onerror = (error) => {
        onErrorRef.current?.(error);
      };
    } catch (error) {
      connectingRef.current = false;
      setState((s) => ({
        ...s,
        isConnecting: false,
      }));
      console.error('WebSocket connection error:', error);
    }
  }, [url, reconnect, reconnectInterval, maxReconnectAttempts]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = undefined;
    }

    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }

    connectingRef.current = false;
    reconnectAttemptsRef.current = 0;
    setState({
      socket: null,
      isConnected: false,
      isConnecting: false,
      reconnectAttempts: 0,
    });
  }, []);

  const send = useCallback((data: unknown): boolean => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(data));
      return true;
    }
    return false;
  }, []);

  // Connect on mount - only run once
  useEffect(() => {
    mountedRef.current = true;
    
    // Small delay to handle React StrictMode double-mounting
    const timeoutId = setTimeout(() => {
      if (mountedRef.current) {
        connect();
      }
    }, 100);
    
    return () => {
      mountedRef.current = false;
      clearTimeout(timeoutId);
      disconnect();
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [url]); // Only reconnect if URL changes

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
  if (typeof window === 'undefined') {
    return `ws://localhost${path}`;
  }

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}${path}`;
}

/**
 * Simple WebSocket client class for non-hook usage.
 */
export class WebSocketClient {
  private socket: WebSocket | null = null;
  private url: string;
  private reconnect: boolean;
  private reconnectInterval: number;
  private maxReconnectAttempts: number;
  private reconnectAttempts: number = 0;
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  private messageHandlers: Set<(data: unknown) => void> = new Set();
  private connectionHandlers: Set<(connected: boolean) => void> = new Set();

  constructor(options: WebSocketOptions) {
    this.url = options.url;
    this.reconnect = options.reconnect ?? true;
    this.reconnectInterval = options.reconnectInterval ?? 3000;
    this.maxReconnectAttempts = options.maxReconnectAttempts ?? 10;
  }

  connect(): void {
    if (this.socket) {
      this.socket.close();
    }

    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      this.reconnectAttempts = 0;
      this.notifyConnectionChange(true);
    };

    this.socket.onclose = () => {
      this.notifyConnectionChange(false);

      if (this.reconnect && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectTimeout = setTimeout(() => {
          this.reconnectAttempts++;
          this.connect();
        }, this.reconnectInterval);
      }
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.messageHandlers.forEach((handler) => handler(data));
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  }

  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }

    this.reconnectAttempts = 0;
  }

  send(data: unknown): boolean {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
      return true;
    }
    return false;
  }

  onMessage(handler: (data: unknown) => void): () => void {
    this.messageHandlers.add(handler);
    return () => this.messageHandlers.delete(handler);
  }

  onConnectionChange(handler: (connected: boolean) => void): () => void {
    this.connectionHandlers.add(handler);
    return () => this.connectionHandlers.delete(handler);
  }

  private notifyConnectionChange(connected: boolean): void {
    this.connectionHandlers.forEach((handler) => handler(connected));
  }

  get isConnected(): boolean {
    return this.socket?.readyState === WebSocket.OPEN;
  }
}
