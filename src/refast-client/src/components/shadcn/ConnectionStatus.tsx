import React, { useEffect, useRef, useState } from 'react';
import { Wifi, WifiOff, Loader2 } from 'lucide-react';
import { cn } from '../../utils';
import { ComponentRenderer } from '../ComponentRenderer';
import { ComponentTree } from '../../types';
import { refastBus } from '../../utils/eventBus';

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

// Global state to track connection transitions across unmounts/remounts
let globalIsConnected = true;
let lastReconnectTime = 0;

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
}: ConnectionStatusProps): React.ReactElement<any> | null {
  const [isConnected, setIsConnected] = useState(true);
  const [isConnecting, setIsConnecting] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const [showConnected, setShowConnected] = useState(false);
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const showConnectedTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
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

      // Fire Python callback via typed event bus
      if (onDisconnect?.callbackId) {
        refastBus.emit('refast:callback', {
          callbackId: onDisconnect.callbackId,
          data: { ...(onDisconnect.boundArgs || {}), event_type: 'disconnect' },
        });
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

      // Fire Python callback via typed event bus
      if (onReconnect?.callbackId) {
        refastBus.emit('refast:callback', {
          callbackId: onReconnect.callbackId,
          data: { ...(onReconnect.boundArgs || {}), event_type: 'reconnect' },
        });
      }
    };

    const updateState = () => {
      const connected = refastApp.getAttribute('data-connected') === 'true';
      const connecting = refastApp.getAttribute('data-connecting') === 'true';
      const attempts = parseInt(refastApp.getAttribute('data-reconnect-attempts') || '0', 10);

      setIsConnected(connected);
      setIsConnecting(connecting);
      setReconnectAttempts(attempts);

      // Track connection transitions globally across possible unmounts/remounts
      if (globalIsConnected === false && connected === true) {
        lastReconnectTime = Date.now();
      }
      globalIsConnected = connected;

      // Determine if we should show the temporary "Connected" toast
      const timeSinceReconnect = Date.now() - lastReconnectTime;
      if (connected && lastReconnectTime > 0 && timeSinceReconnect < 3000) {
        setShowConnected(true);
        if (showConnectedTimeoutRef.current) {
          clearTimeout(showConnectedTimeoutRef.current);
        }
        showConnectedTimeoutRef.current = setTimeout(() => {
          setShowConnected(false);
        }, 3000 - timeSinceReconnect);
      } else {
        setShowConnected(false);
        if (showConnectedTimeoutRef.current) {
          clearTimeout(showConnectedTimeoutRef.current);
          showConnectedTimeoutRef.current = null;
        }
      }

      // Fire callbacks on state change (debounced)
      if (lastStateRef.current !== null && lastStateRef.current !== connected) {
        if (debounceTimerRef.current) {
          clearTimeout(debounceTimerRef.current);
        }

        debounceTimerRef.current = setTimeout(() => {
          if (connected) {
            fireReconnectCallbacks();
          } else {
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
      if (showConnectedTimeoutRef.current) {
        clearTimeout(showConnectedTimeoutRef.current);
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

  // If no children to show, render nothing (unless disconnected/temporarily connected with no custom children - show default)
  if (!hasActiveChildren) {
    const shouldShowDefaultDisconnected = !isConnected && childrenDisconnected.length === 0;
    const shouldShowDefaultConnected = showConnected && childrenConnected.length === 0;

    if (shouldShowDefaultDisconnected || shouldShowDefaultConnected) {
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
              'flex items-center gap-2 rounded-full px-4 py-2 shadow-lg border text-sm font-medium transition-all duration-300 ease-in-out',
              showConnected
                ? 'bg-success text-success-foreground border-success/30 animate-in fade-in zoom-in-95 duration-200'
                : isConnecting
                ? 'bg-warning text-warning-foreground border-warning/30 animate-in fade-in zoom-in-95 duration-200'
                : 'bg-destructive text-destructive-foreground border-destructive/30 animate-in fade-in zoom-in-95 duration-200'
            )}
          >
            {showConnected ? (
              <>
                <Wifi className="h-4 w-4 shrink-0" />
                <span>Connected</span>
              </>
            ) : isConnecting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin shrink-0" />
                <span>Reconnecting</span>
                <span className="ml-1 px-1.5 py-0.5 text-xs font-semibold rounded-full bg-warning-foreground/20 text-warning-foreground shrink-0">
                  {reconnectAttempts}
                </span>
              </>
            ) : (
              <>
                <WifiOff className="h-4 w-4 shrink-0" />
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

