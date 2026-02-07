import React, { createContext, useContext, useCallback, useMemo, useRef, useEffect } from 'react';
import { EventMessage, UpdateMessage, ComponentTree, ThemePayload } from '../types';
import { persistentStateManager } from '../state/PersistentStateManager';

/**
 * CSS variable names that may be set as inline styles by a previous
 * (buggy) version of this function. We clean them up on the first call.
 */
let _inlineStylesCleaned = false;

/**
 * Apply a runtime theme update using stylesheet rules (not inline styles).
 *
 * We write both `:root { … }` (light) and `.dark { … }` (dark) blocks into
 * a single `<style data-refast-theme-runtime>` element appended at the end of
 * `<head>`.  Because it appears **after** the client CSS bundle and after the
 * server-rendered `<style data-refast-theme>` block, it wins in the cascade
 * for every variable it declares — while leaving un-declared variables to
 * fall through to the CSS bundle defaults.
 *
 * We also blank out the server-rendered `<style data-refast-theme>` so that
 * stale overrides from the initial theme don't bleed through.
 */
function applyThemeUpdate(theme: ThemePayload): void {
  const root = document.documentElement;

  // --- Housekeeping: remove any inline style overrides left from an
  //     earlier (incorrect) implementation that used root.style.setProperty.
  if (!_inlineStylesCleaned) {
    // Remove every custom property that was set as an inline style
    const inlineStyle = root.style;
    const toRemove: string[] = [];
    for (let i = 0; i < inlineStyle.length; i++) {
      const prop = inlineStyle[i];
      if (prop.startsWith('--')) {
        toRemove.push(prop);
      }
    }
    toRemove.forEach((p) => inlineStyle.removeProperty(p));
    _inlineStylesCleaned = true;
  }

  // --- Blank the server-rendered theme block so stale values don't persist.
  const serverBlock = document.querySelector('style[data-refast-theme]');
  if (serverBlock) {
    (serverBlock as HTMLStyleElement).textContent = '';
  }

  // --- Build the runtime stylesheet with both :root and .dark blocks.
  let sheet = document.querySelector('style[data-refast-theme-runtime]') as HTMLStyleElement | null;
  if (!sheet) {
    sheet = document.createElement('style');
    sheet.setAttribute('data-refast-theme-runtime', '');
    document.head.appendChild(sheet);
  }

  const lightEntries = Object.entries(theme.light);
  const darkEntries = Object.entries(theme.dark);

  // Include radius in the light block (it's mode-independent)
  if (theme.radius) {
    lightEntries.push(['--radius', theme.radius]);
  }

  const lightLines = lightEntries.map(([k, v]) => `  ${k}: ${v};`).join('\n');
  const darkLines = darkEntries.map(([k, v]) => `  ${k}: ${v};`).join('\n');

  let css = '';
  if (lightLines) css += `:root {\n${lightLines}\n}\n`;
  if (darkLines) css += `.dark {\n${darkLines}\n}`;

  sheet.textContent = css;

  // --- Font family (applied via body.style since it's not a CSS variable)
  if (theme.fontFamily) {
    document.body.style.fontFamily = theme.fontFamily;
  } else {
    document.body.style.removeProperty('font-family');
  }
}

interface EventManagerContextValue {
  invokeCallback: (callbackId: string, data: Record<string, unknown>, eventData?: Record<string, unknown>) => void;
  emitEvent: (eventType: string, data: unknown) => void;
  subscribe: (channel: string) => void;
  unsubscribe: (channel: string) => void;
  onUpdate: (handler: (message: UpdateMessage) => void) => () => void;
}

const EventManagerContext = createContext<EventManagerContextValue | null>(null);

interface EventManagerProviderProps {
  children: React.ReactNode;
  websocket: WebSocket | null;
  onComponentUpdate?: (id: string, component: ComponentTree | null, operation?: string) => void;
}

/**
 * Provides event management to the component tree.
 */
export function EventManagerProvider({
  children,
  websocket,
  onComponentUpdate,
}: EventManagerProviderProps): React.ReactElement {
  const updateHandlers = useRef<Set<(message: UpdateMessage) => void>>(new Set());
  const websocketRef = useRef<WebSocket | null>(websocket);
  
  // Keep websocket ref updated
  useEffect(() => {
    websocketRef.current = websocket;
  }, [websocket]);

  // Listen for custom refast:callback events from components
  useEffect(() => {
    const handleCallbackEvent = (event: Event) => {
      const customEvent = event as CustomEvent<{
        callbackId: string;
        data: Record<string, unknown>;
      }>;
      
      const { callbackId, data } = customEvent.detail;
      
      if (websocketRef.current && websocketRef.current.readyState === WebSocket.OPEN) {
        // Note: requested props should already be merged into data
        const message = {
          type: 'callback',
          callbackId,
          data,
        };
        websocketRef.current.send(JSON.stringify(message));
      } else {
        console.warn('WebSocket not connected, cannot invoke callback');
      }
    };

    window.addEventListener('refast:callback', handleCallbackEvent);
    return () => {
      window.removeEventListener('refast:callback', handleCallbackEvent);
    };
  }, []);

  // Handle incoming messages
  useEffect(() => {
    if (!websocket) return;

    const handleMessage = (event: MessageEvent) => {
      try {
        const message: UpdateMessage = JSON.parse(event.data);

        // Notify all handlers
        updateHandlers.current.forEach((handler) => handler(message));

        // Handle store updates
        if (message.type === 'store_update' && message.updates) {
          persistentStateManager.handleUpdates(message.updates);
        }

        // Handle store ready (after store_init is acknowledged)
        if (message.type === 'store_ready') {
          persistentStateManager.handleStoreReady();
        }

        // Note: Component updates (message.type === 'update') are handled by the 
        // registered update handlers via handleUpdate in StateManager.
        // We don't call onComponentUpdate here to avoid processing updates twice.

        // Handle JavaScript execution from backend
        if (message.type === 'js_exec' && message.code) {
          try {
            // eslint-disable-next-line no-new-func
            const fn = new Function('args', message.code);
            fn(message.args || {});
          } catch (error) {
            console.error('[Refast] Error executing JavaScript from server:', error);
            console.error('[Refast] Code:', message.code);
          }
        }

        // Handle bound method calls from backend
        if (message.type === 'bound_method_call' && message.targetId && message.methodName) {
          try {
            const element = document.getElementById(message.targetId);
            if (element) {
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              const method = (element as any)[message.methodName];
              if (typeof method === 'function') {
                // Call the method with the provided arguments
                // For bound_method_call, args is always an array
                const positionalArgs = (Array.isArray(message.args) ? message.args : []) as unknown[];
                const kwargs = message.kwargs || {};
                
                // Combine positional args and kwargs
                // If there are kwargs, pass them as the last argument (as an object)
                const hasKwargs = Object.keys(kwargs).length > 0;
                const allArgs = hasKwargs ? [...positionalArgs, kwargs] : positionalArgs;
                
                if (allArgs.length === 0) {
                  method.call(element);
                } else if (allArgs.length === 1) {
                  method.call(element, allArgs[0]);
                } else {
                  method.apply(element, allArgs);
                }
              } else {
                console.warn(`[Refast] Method '${message.methodName}' not found on element '${message.targetId}'`);
              }
            } else {
              console.warn(`[Refast] Element with id '${message.targetId}' not found`);
            }
          } catch (error) {
            console.error('[Refast] Error calling bound method:', error);
            console.error('[Refast] Target:', message.targetId, 'Method:', message.methodName);
          }
        }

        // Handle resync_store request from backend
        if (message.type === 'resync_store') {
          persistentStateManager.resyncStore();
        }

        // Handle runtime theme updates from backend
        if (message.type === 'theme_update' && message.theme) {
          applyThemeUpdate(message.theme);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    websocket.addEventListener('message', handleMessage);
    return () => websocket.removeEventListener('message', handleMessage);
  }, [websocket, onComponentUpdate]);

  const invokeCallback = useCallback(
    (callbackId: string, data: Record<string, unknown>, eventData?: Record<string, unknown>) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        console.warn('WebSocket not connected');
        return;
      }

      // Send bound args + props as 'data' (becomes **kwargs on the backend)
      // Send DOM event data separately as 'eventData' (accessible via ctx.event_data)
      const message: EventMessage = {
        type: 'callback',
        callbackId,
        data,
        ...(eventData && Object.keys(eventData).length > 0 ? { eventData } : {}),
      };

      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );

  const emitEvent = useCallback(
    (eventType: string, data: unknown) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) {
        console.warn('WebSocket not connected');
        return;
      }

      const message: EventMessage = {
        type: 'event',
        eventType,
        data: data as Record<string, unknown>,
      };

      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );

  const subscribe = useCallback(
    (channel: string) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) return;

      const message: EventMessage = {
        type: 'subscribe',
        eventType: channel,
      };

      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );

  const unsubscribe = useCallback(
    (channel: string) => {
      if (!websocket || websocket.readyState !== WebSocket.OPEN) return;

      const message: EventMessage = {
        type: 'unsubscribe',
        eventType: channel,
      };

      websocket.send(JSON.stringify(message));
    },
    [websocket]
  );

  const onUpdate = useCallback(
    (handler: (message: UpdateMessage) => void) => {
      updateHandlers.current.add(handler);
      return () => {
        updateHandlers.current.delete(handler);
      };
    },
    []
  );

  const value = useMemo(
    () => ({
      invokeCallback,
      emitEvent,
      subscribe,
      unsubscribe,
      onUpdate,
    }),
    [invokeCallback, emitEvent, subscribe, unsubscribe, onUpdate]
  );

  return (
    <EventManagerContext.Provider value={value}>
      {children}
    </EventManagerContext.Provider>
  );
}

/**
 * Hook to access the event manager.
 */
export function useEventManager(): EventManagerContextValue {
  const context = useContext(EventManagerContext);

  if (!context) {
    throw new Error('useEventManager must be used within EventManagerProvider');
  }

  return context;
}

/**
 * Hook to listen for specific event types.
 */
export function useEvent(
  eventType: string,
  handler: (data: unknown) => void
): void {
  const { onUpdate } = useEventManager();

  useEffect(() => {
    return onUpdate((message) => {
      if (message.type === 'event' && message.eventType === eventType) {
        handler(message.data);
      }
    });
  }, [eventType, handler, onUpdate]);
}

/**
 * Hook to subscribe to a channel on mount.
 */
export function useChannel(channel: string): void {
  const { subscribe, unsubscribe } = useEventManager();

  useEffect(() => {
    subscribe(channel);
    return () => unsubscribe(channel);
  }, [channel, subscribe, unsubscribe]);
}
