/**
 * Shared utilities for prop store operations used by both
 * ComponentRenderer and individual components (e.g. Input, Textarea).
 * 
 * Separated to avoid circular imports:
 *   ComponentRenderer → registry → input → ComponentRenderer (circular!)
 *   ComponentRenderer → propStoreUtils (ok)
 *   input → propStoreUtils (ok)
 */
import { propStore } from '../state/PropStore';

/**
 * Type for callback handlers that carry storeAs metadata.
 * Components with their own debounce (e.g. Input) can check this
 * to call propStore.set() immediately on every event.
 */
export interface CallbackHandlerWithStoreAs {
  (...args: unknown[]): void;
  __storeAs?: string | Record<string, string>;
}

/**
 * Apply a store_as directive to store event data in the prop store immediately.
 * Used by ComponentRenderer for normal flow, and by Input/Textarea when
 * they have their own debounce that would otherwise delay the store write.
 */
export function applyStoreAs(
  storeAs: string | Record<string, string>,
  eventData: Record<string, unknown>
): void {
  if (typeof storeAs === 'string') {
    propStore.set(storeAs, eventData.value);
  } else if (typeof storeAs === 'object') {
    for (const [eventKey, storeKey] of Object.entries(storeAs)) {
      if (eventKey in eventData) {
        propStore.set(storeKey, eventData[eventKey]);
      }
    }
  }
}
