import { useEffect, useState, useRef } from 'react';

/**
 * Get or create a unique tab-scoped connection ID.
 * Stored in sessionStorage so that multiple tabs do not share state.
 */
function getOrCreateConnectionId(): string {
  if (typeof window === 'undefined') {
    return '';
  }
  let id = sessionStorage.getItem('refast:connection_id');
  if (!id) {
    try {
      if (typeof crypto !== 'undefined' && crypto.randomUUID) {
        id = crypto.randomUUID();
      } else {
        id = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          const r = (Math.random() * 16) | 0;
          const v = c === 'x' ? r : (r & 0x3) | 0x8;
          return v.toString(16);
        });
      }
    } catch {
      id = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }
    sessionStorage.setItem('refast:connection_id', id);
  }
  return id;
}

export interface SSEOptions {
  url: string;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: any) => void;
}

/**
 * SSEClient wraps EventSource and fetch to mimic a WebSocket interface.
 * This keeps other parts of the client (StateManager, persistentStateManager)
 * clean without rewrite.
 */
export class SSEClient {
  private eventSource: EventSource | null = null;
  private messageListeners: Set<(event: MessageEvent) => void> = new Set();
  private openListeners: Set<() => void> = new Set();
  private closeListeners: Set<() => void> = new Set();
  private errorListeners: Set<(error: any) => void> = new Set();

  public connectionId: string;
  public readyState: number; // 0 = CONNECTING, 1 = OPEN, 2 = CLOSING, 3 = CLOSED
  private url: string;

  constructor(url: string, connectionId: string) {
    this.url = url;
    this.connectionId = connectionId;
    this.readyState = 3; // CLOSED
  }

  public connect() {
    if (this.eventSource) {
      this.eventSource.close();
    }

    this.readyState = 0; // CONNECTING

    const separator = this.url.includes('?') ? '&' : '?';
    const sseUrl = `${this.url}${separator}connection_id=${this.connectionId}`;

    this.eventSource = new EventSource(sseUrl);

    this.eventSource.onopen = () => {
      this.readyState = 1; // OPEN
      this.openListeners.forEach((l) => l());
    };

    this.eventSource.onmessage = (event) => {
      this.messageListeners.forEach((l) => l(event));
    };

    this.eventSource.onerror = (error) => {
      // EventSource reconnects automatically, but readyState toggles back to connecting
      this.readyState = 0; // CONNECTING
      this.errorListeners.forEach((l) => l(error));
    };
  }

  public disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
    this.readyState = 3; // CLOSED
    this.closeListeners.forEach((l) => l());
  }

  public addEventListener(type: string, listener: any, _options?: any) {
    if (type === 'message') this.messageListeners.add(listener);
    if (type === 'open') {
      this.openListeners.add(listener);
      if (this.readyState === 1) {
        listener();
      }
    }
    if (type === 'close') this.closeListeners.add(listener);
    if (type === 'error') this.errorListeners.add(listener);
  }

  public removeEventListener(type: string, listener: any) {
    if (type === 'message') this.messageListeners.delete(listener);
    if (type === 'open') this.openListeners.delete(listener);
    if (type === 'close') this.closeListeners.delete(listener);
    if (type === 'error') this.errorListeners.delete(listener);
  }

  public async send(data: string): Promise<boolean> {
    try {
      const payload = JSON.parse(data);
      payload.connection_id = this.connectionId;

      const response = await fetch('/api/event', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        console.error('[Refast SSE] Failed to post event to server:', response.statusText);
        return false;
      }
      return true;
    } catch (e) {
      console.error('[Refast SSE] Error posting event to server:', e);
      return false;
    }
  }
}

/**
 * useSSE React hook replacing useWebSocket hook.
 */
export function useSSE(options: SSEOptions) {
  const { url, onOpen, onClose, onError } = options;
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);

  const [socket, setSocket] = useState<SSEClient | null>(null);

  const onOpenRef = useRef(onOpen);
  const onCloseRef = useRef(onClose);
  const onErrorRef = useRef(onError);

  useEffect(() => {
    onOpenRef.current = onOpen;
    onCloseRef.current = onClose;
    onErrorRef.current = onError;
  }, [onOpen, onClose, onError]);

  useEffect(() => {
    const connectionId = getOrCreateConnectionId();
    // Resolve absolute path or match host relative path
    let sseUrl = url;
    if (url.startsWith('ws://') || url.startsWith('wss://')) {
      // Convert ws protocols to http for SSE
      const httpProtocol = window.location.protocol;
      const host = window.location.host;
      sseUrl = `${httpProtocol}//${host}/api/events`;
    }

    const client = new SSEClient(sseUrl, connectionId);
    setSocket(client);
    setIsConnecting(true);

    const handleOpen = () => {
      setIsConnected(true);
      setIsConnecting(false);
      setReconnectAttempts(0);
      onOpenRef.current?.();
    };

    const handleClose = () => {
      setIsConnected(false);
      setIsConnecting(false);
      onCloseRef.current?.();
    };

    const handleError = (err: any) => {
      setIsConnected(false);
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        setIsConnecting(false);
      } else {
        setIsConnecting(true);
        setReconnectAttempts((prev) => prev + 1);
      }
      onErrorRef.current?.(err);
    };

    const handleOffline = () => {
      setIsConnected(false);
      setIsConnecting(false);
      onCloseRef.current?.();
    };

    const handleOnline = () => {
      setIsConnecting(true);
      client.connect();
    };

    client.addEventListener('open', handleOpen);
    client.addEventListener('close', handleClose);
    client.addEventListener('error', handleError);

    if (typeof window !== 'undefined') {
      window.addEventListener('offline', handleOffline);
      window.addEventListener('online', handleOnline);
      
      // If we are currently offline, adjust state immediately
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        setIsConnected(false);
        setIsConnecting(false);
      }
    }

    client.connect();

    return () => {
      client.removeEventListener('open', handleOpen);
      client.removeEventListener('close', handleClose);
      client.removeEventListener('error', handleError);
      if (typeof window !== 'undefined') {
        window.removeEventListener('offline', handleOffline);
        window.removeEventListener('online', handleOnline);
      }
      client.disconnect();
    };
  }, [url]);

  return {
    socket,
    isConnected,
    isConnecting,
    reconnectAttempts,
  };
}
