import React, { useEffect, useMemo, useCallback} from 'react';
import { ComponentRenderer } from './components/ComponentRenderer';
import { ToastManager } from './components/ToastManager';
import { EventManagerProvider, useEventManager } from './events/EventManager';
import { useWebSocket, buildWebSocketUrl } from './events/WebSocketClient';
import { useStateManager } from './state/StateManager';
import { persistentStateManager } from './state/PersistentStateManager';
import { ComponentTree, UpdateMessage } from './types';

// Extend Window interface for initial data
declare global {
  interface Window {
    __REFAST_INITIAL_DATA__?: ComponentTree;
    __REFAST_CONFIG__?: {
      wsUrl?: string;
      csrfToken?: string;
    };
  }
}

interface RefastAppProps {
  initialTree?: ComponentTree;
  wsUrl?: string;
  className?: string;
}

/**
 * Main Refast application component.
 */
export function RefastApp({ initialTree, wsUrl, className }: RefastAppProps): React.ReactElement {
  // Get initial data from window if not provided
  const tree = useMemo(() => {
    if (initialTree) return initialTree;

    const windowData = window.__REFAST_INITIAL_DATA__;
    return windowData || null;
  }, [initialTree]);

  // Get config from window
  const config = useMemo(() => {
    return window.__REFAST_CONFIG__ || {};
  }, []);

  // WebSocket connection
  const { socket, isConnected, isConnecting, reconnectAttempts } = useWebSocket({
    url: wsUrl || config.wsUrl || buildWebSocketUrl('/ws'),
    reconnect: true,
    maxReconnectAttempts: 10,
    onOpen: () => {},
    onClose: () => {},
  });

  // State management
  const { componentTree, setComponentTree, updateComponent, handleUpdate } =
    useStateManager(tree || undefined);

  // Initialize persistent state manager with WebSocket and listen for messages
  useEffect(() => {
    if (socket) {
      persistentStateManager.setWebSocket(socket);

      // Listen for messages directly (before EventManagerProvider is mounted)
      const handleMessage = (event: MessageEvent) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === 'store_ready') {
            persistentStateManager.handleStoreReady();
          }
          if (message.type === 'store_update' && message.updates) {
            persistentStateManager.handleUpdates(message.updates);
          }
          // Handle page render from WebSocket (after store_init)
          if (message.type === 'page_render' && message.component) {
            setComponentTree(message.component);
          }
        } catch {
          // Ignore parse errors
        }
      };

      socket.addEventListener('message', handleMessage);

      return () => {
        socket.removeEventListener('message', handleMessage);
        persistentStateManager.reset();
      };
    }
    return () => {
      persistentStateManager.reset();
    };
  }, [socket, setComponentTree]);

  // Fetch page data from server (used for refresh events)
  const fetchPage = useCallback(async () => {
    try {
      const path = window.location.pathname;
      const response = await fetch(`/api/page?path=${encodeURIComponent(path)}`);
      if (response.ok) {
        const data = await response.json();
        if (data.component) {
          setComponentTree(data.component);
        }
      }
    } catch (error) {
      console.error('[Refast] Failed to fetch page:', error);
    }
  }, [setComponentTree]);

  // Listen for browser back/forward navigation (popstate)
  useEffect(() => {
    const handlePopState = () => {
      if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(
          JSON.stringify({
            type: 'navigate',
            path: window.location.pathname,
          })
        );
      }
    };

    window.addEventListener('popstate', handlePopState);
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, [socket]);

  // Listen for refresh events
  useEffect(() => {
    const handleRefresh = () => {
      fetchPage();
    };

    window.addEventListener('refast:refresh', handleRefresh);
    return () => {
      window.removeEventListener('refast:refresh', handleRefresh);
    };
  }, [fetchPage]);

  // Show loading state until page is rendered
  if (!componentTree) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Wrapper to match the expected signature
  const handleComponentUpdate = useCallback(
    (id: string, component: ComponentTree | null, operation?: string) => {
      updateComponent(id, component, operation || 'replace');
    },
    [updateComponent]
  );

  return (
    <EventManagerProvider
      websocket={socket}
      onComponentUpdate={handleComponentUpdate}
    >
      <RefastAppContent
        tree={componentTree}
        isConnected={isConnected}
        isConnecting={isConnecting}
        reconnectAttempts={reconnectAttempts}
        onUpdate={handleUpdate}
        className={className}
      />
    </EventManagerProvider>
  );
}

interface RefastAppContentProps {
  tree: ComponentTree;
  isConnected: boolean;
  isConnecting: boolean;
  reconnectAttempts: number;
  onUpdate: (message: UpdateMessage) => void;
  className?: string;
}

function RefastAppContent({
  tree,
  isConnected,
  isConnecting,
  reconnectAttempts,
  onUpdate,
  className,
}: RefastAppContentProps): React.ReactElement {
  const { onUpdate: registerUpdateHandler } = useEventManager();

  // Register update handler
  useEffect(() => {
    return registerUpdateHandler(onUpdate);
  }, [registerUpdateHandler, onUpdate]);

  return (
    <div
      className={`refast-app ${className || ''}`}
      data-connected={isConnected}
      data-connecting={isConnecting}
      data-reconnect-attempts={reconnectAttempts}
    >
      <ComponentRenderer tree={tree} />
      <ToastManager />
    </div>
  );
}

// Export for standalone use
export default RefastApp;
