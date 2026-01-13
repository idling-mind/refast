import React, { useEffect, useRef, useState } from 'react';
import { cn } from '../../utils';
import { ComponentRenderer } from '../ComponentRenderer';
import { ComponentTree } from '../../types';

interface ConnectionStatusProps {
  id?: string;
  className?: string;
  childrenConnected?: ComponentTree[];
  childrenDisconnected?: ComponentTree[];
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'inline';
  onDisconnect?: { callbackId: string; boundArgs?: Record<string, unknown> };
  onReconnect?: { callbackId: string; boundArgs?: Record<string, unknown> };
  jsOnDisconnect?: { jsFunction: string; boundArgs?: Record<string, unknown> };
  jsOnReconnect?: { jsFunction: string; boundArgs?: Record<string, unknown> };
  debounceMs?: number;
  'data-refast-id'?: string;
}

/**
 * ConnectionStatus component - conditionally shows content based on WebSocket connection state.
 *
 * Reads connection state from the parent .refast-app element's data attributes
 * and fires callbacks when connection state changes.
 */
export function ConnectionStatus({
  id,
  className,
  childrenConnected = [],
  childrenDisconnected = [],
  position = 'bottom-right',
  onDisconnect,
  onReconnect,
  jsOnDisconnect,
  jsOnReconnect,
  debounceMs = 500,
  'data-refast-id': dataRefastId,
}: ConnectionStatusProps): React.ReactElement | null {
  const [isConnected, setIsConnected] = useState(true);
  const [isConnecting, setIsConnecting] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const lastStateRef = useRef<boolean | null>(null);

  // Observe the .refast-app element for connection state changes
  useEffect(() => {
    const refastApp = document.querySelector('.refast-app');
    if (!refastApp) return;

    const fireDisconnectCallbacks = () => {
      // Fire JS callback
      if (jsOnDisconnect?.jsFunction) {
        try {
          // eslint-disable-next-line no-new-func
          const fn = new Function('args', 'event', jsOnDisconnect.jsFunction);
          fn(jsOnDisconnect.boundArgs || {}, { type: 'disconnect' });
        } catch (error) {
          console.error('[ConnectionStatus] Error executing jsOnDisconnect:', error);
        }
      }

      // Fire Python callback via custom event
      if (onDisconnect?.callbackId) {
        window.dispatchEvent(
          new CustomEvent('refast:callback', {
            detail: {
              callbackId: onDisconnect.callbackId,
              data: { ...(onDisconnect.boundArgs || {}), event_type: 'disconnect' },
            },
          })
        );
      }
    };

    const fireReconnectCallbacks = () => {
      // Fire JS callback
      if (jsOnReconnect?.jsFunction) {
        try {
          // eslint-disable-next-line no-new-func
          const fn = new Function('args', 'event', jsOnReconnect.jsFunction);
          fn(jsOnReconnect.boundArgs || {}, { type: 'reconnect' });
        } catch (error) {
          console.error('[ConnectionStatus] Error executing jsOnReconnect:', error);
        }
      }

      // Fire Python callback via custom event
      if (onReconnect?.callbackId) {
        window.dispatchEvent(
          new CustomEvent('refast:callback', {
            detail: {
              callbackId: onReconnect.callbackId,
              data: { ...(onReconnect.boundArgs || {}), event_type: 'reconnect' },
            },
          })
        );
      }
    };

    const updateState = () => {
      const connected = refastApp.getAttribute('data-connected') === 'true';
      const connecting = refastApp.getAttribute('data-connecting') === 'true';
      const attempts = parseInt(refastApp.getAttribute('data-reconnect-attempts') || '0', 10);

      setIsConnected(connected);
      setIsConnecting(connecting);
      setReconnectAttempts(attempts);

      // Fire callbacks on state change (debounced)
      if (lastStateRef.current !== null && lastStateRef.current !== connected) {
        if (debounceTimerRef.current) {
          clearTimeout(debounceTimerRef.current);
        }

        debounceTimerRef.current = setTimeout(() => {
          if (connected) {
            // Connection restored
            fireReconnectCallbacks();
          } else {
            // Connection lost
            fireDisconnectCallbacks();
          }
        }, debounceMs);
      }

      lastStateRef.current = connected;
    };

    // Initial state
    updateState();

    // Use MutationObserver to watch for attribute changes
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (
          mutation.type === 'attributes' &&
          (mutation.attributeName === 'data-connected' ||
            mutation.attributeName === 'data-connecting' ||
            mutation.attributeName === 'data-reconnect-attempts')
        ) {
          updateState();
          break;
        }
      }
    });

    observer.observe(refastApp, { attributes: true });

    return () => {
      observer.disconnect();
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [debounceMs, jsOnDisconnect, jsOnReconnect, onDisconnect, onReconnect]);

  // Determine which children to show
  const activeChildren = isConnected ? childrenConnected : childrenDisconnected;
  const hasActiveChildren = activeChildren && activeChildren.length > 0;

  // Position classes
  const positionClasses: Record<string, string> = {
    'top-left': 'fixed top-4 left-4 z-50',
    'top-right': 'fixed top-4 right-4 z-50',
    'bottom-left': 'fixed bottom-4 left-4 z-50',
    'bottom-right': 'fixed bottom-4 right-4 z-50',
    inline: '',
  };

  // If no children to show, render nothing (unless disconnected with no disconnected children - show default)
  if (!hasActiveChildren) {
    // Show default disconnection indicator only when disconnected and no custom children provided
    if (!isConnected && childrenDisconnected.length === 0) {
      return (
        <div
          id={id}
          className={cn(positionClasses[position], className)}
          data-refast-id={dataRefastId}
          data-connected={isConnected}
          data-connecting={isConnecting}
          data-reconnect-attempts={reconnectAttempts}
        >
          <div
            className={cn(
              'flex items-center gap-2 rounded-lg px-3 py-2 shadow-lg',
              isConnecting ? 'bg-yellow-500 text-white' : 'bg-destructive text-destructive-foreground'
            )}
          >
            {isConnecting ? (
              <>
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                <span>Reconnecting... ({reconnectAttempts})</span>
              </>
            ) : (
              <>
                <div className="h-2 w-2 rounded-full bg-white animate-pulse" />
                <span>Connection lost</span>
              </>
            )}
          </div>
        </div>
      );
    }
    return null;
  }

  return (
    <div
      id={id}
      className={cn(positionClasses[position], className)}
      data-refast-id={dataRefastId}
      data-connected={isConnected}
      data-connecting={isConnecting}
      data-reconnect-attempts={reconnectAttempts}
    >
      {activeChildren.map((child, index) => (
        <ComponentRenderer key={child.id || index} tree={child} />
      ))}
    </div>
  );
}

export default ConnectionStatus;
