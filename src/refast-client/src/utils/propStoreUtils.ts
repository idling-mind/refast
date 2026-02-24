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
 * Apply a save_prop directive to store event data in the prop store immediately.
 * Used by the action execution engine for SaveProp actions.
 * 
 * @param saveProp - String key or object mapping event keys to store keys
 * @param eventData - The extracted event data
 */
export function applySaveProp(
  saveProp: string | Record<string, string>,
  eventData: Record<string, unknown>
): void {
  if (typeof saveProp === 'string') {
    propStore.set(saveProp, eventData.value);
  } else if (typeof saveProp === 'object') {
    for (const [eventKey, storeKey] of Object.entries(saveProp)) {
      if (eventKey in eventData) {
        propStore.set(storeKey, eventData[eventKey]);
      }
    }
  }
}
