import React, { useEffect, useMemo, useCallback } from 'react';
import { ComponentRenderer } from './components/ComponentRenderer';
import { ToastManager } from './components/ToastManager';
import { EventManagerProvider, useEventManager } from './events/EventManager';
import { useWebSocket, buildWebSocketUrl } from './events/WebSocketClient';
import { useStateManager } from './state/StateManager';
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

  // Fetch page data from server
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

  // Initialize with server data
  useEffect(() => {
    if (tree && !componentTree) {
      setComponentTree(tree);
    }
  }, [tree, componentTree, setComponentTree]);

  // Show loading state
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
