/**
 * Apply a store_prop directive to store event data in the prop store immediately.
 * Used by the action execution engine for StoreProp actions.
 *
 * @param storeProp - String key or object mapping event keys to store keys
 * @param eventData - The extracted event data
 */
export declare function applyStoreProp(storeProp: string | Record<string, string>, eventData: Record<string, unknown>): void;
