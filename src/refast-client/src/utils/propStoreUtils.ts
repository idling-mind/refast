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
 * Apply a store_prop directive to store event data in the prop store immediately.
 * Used by the action execution engine for StoreProp actions.
 * 
 * @param storeProp - String key or object mapping event keys to store keys
 * @param eventData - The extracted event data
 */
export function applyStoreProp(
  storeProp: string | Record<string, string>,
  eventData: Record<string, unknown>
): void {
  if (typeof storeProp === 'string') {
    propStore.set(storeProp, eventData.value);
  } else if (typeof storeProp === 'object') {
    for (const [eventKey, storeKey] of Object.entries(storeProp)) {
      if (eventKey in eventData) {
        propStore.set(storeKey, eventData[eventKey]);
      }
    }
  }
}
