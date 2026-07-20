/**
 * Typed internal event bus.
 *
 * Replaces scattered window.dispatchEvent / window.addEventListener calls
 * for refast: prefixed events. Using a typed bus means:
 *   - Typos in event names become compile errors.
 *   - Payload types are enforced at every emit() and on() call.
 *   - All internal event names are inventoried in one place.
 *
 * The bus still dispatches via window so browser extensions and external
 * consumers that already listen on window continue to work unchanged.
 */

import type { AnyActionRef, ComponentTree } from '../types';

// ---------------------------------------------------------------------------
// Payload types
// ---------------------------------------------------------------------------

/**
 * Payload for toast notifications (mirrors the data sent from StateManager
 * to ToastManager, sourced from the Python backend toast() call).
 */
export interface ToastEventDetail {
  message?: string;
  component?: ComponentTree;
  variant?: 'default' | 'success' | 'error' | 'destructive' | 'warning' | 'info' | 'loading';
  description?: string;
  duration?: number;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
  dismissible?: boolean;
  close_button?: boolean;
  invert?: boolean;
  icon?: string;
  action?: { label: string; callback: AnyActionRef };
  cancel?: { label: string; callback: AnyActionRef };
  id?: string;
}

// ---------------------------------------------------------------------------
// Event map
// ---------------------------------------------------------------------------

/**
 * Map of every internal refast event to its payload type.
 * Add a new entry here whenever a new refast: event is introduced.
 */
export interface RefastEventMap {
  /** Invoke a Python callback via WebSocket (emitted by refastJsHelper + ConnectionStatus). */
  'refast:callback': { callbackId: string; data: Record<string, unknown> };
  /** Emit a custom event to the server (emitted by refast.emit). */
  'refast:custom-event': { eventType: string; data: Record<string, unknown> };
  /** Show a toast notification (emitted by StateManager, consumed by ToastManager). */
  'refast:toast': ToastEventDetail;
  /** Client-side navigation event (emitted by StateManager). */
  'refast:navigate': { path: string };
  /** Trigger a page refresh via HTTP (emitted by StateManager fallback). */
  'refast:refresh': Record<string, never>;
  /** Force input/select components to sync their local value state with a new server value. */
  'refast:force-value-sync': { targetId: string; value: unknown };
  /** Signals that all extensions have finished loading and registering components. */
  'refast:extensions-ready': Record<string, never>;
  /** Signals that a single extension chunk has loaded and registered its components. */
  'refast:extension-loaded': { name?: string };
  /** Log a WebSocket message (emitted by interceptor under debug mode). */
  'refast:debug-message': { direction: 'in' | 'out'; message: any; timestamp: number };
  /** Log a debug error (emitted by error boundary, JS client or python backend). */
  'refast:debug-error': { type: string; message: string; timestamp: number; details?: any };
}

// ---------------------------------------------------------------------------
// Bus implementation
// ---------------------------------------------------------------------------

type EventBusListener<T> = (payload: T) => void;

class RefastEventBus {
  /**
   * Dispatch a typed refast event on the window.
   */
  emit<K extends keyof RefastEventMap>(type: K, payload: RefastEventMap[K]): void {
    window.dispatchEvent(new CustomEvent(type, { detail: payload }));
  }

  /**
   * Subscribe to a typed refast event.
   * Returns an unsubscribe function suitable for use as a useEffect cleanup.
   */
  on<K extends keyof RefastEventMap>(
    type: K,
    handler: EventBusListener<RefastEventMap[K]>,
  ): () => void {
    const wrapper = (e: Event) =>
      handler((e as CustomEvent<RefastEventMap[K]>).detail);
    window.addEventListener(type, wrapper);
    return () => window.removeEventListener(type, wrapper);
  }
}

/** Singleton typed event bus for all internal refast events. */
export const refastBus = new RefastEventBus();
