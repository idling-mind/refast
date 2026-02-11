/**
 * PropStore - Frontend-only state for storing component prop values.
 *
 * This store allows values from component events (like input changes) to be
 * captured on the frontend and made available to subsequent callbacks without
 * requiring server roundtrips for each state update.
 *
 * Usage Pattern:
 * 1. Components use `ctx.store_prop("key")` to store event values on the frontend
 * 2. When a callback with `props=[...]` is invoked, matching prop store values
 *    are sent as keyword arguments to the Python callback
 *
 * Example (Python):
 * ```python
 * Input(
 *     name="email",
 *     on_change=ctx.store_prop("email"),  # Store-only, no server call
 * )
 *
 * Button(
 *     "Submit",
 *     on_click=ctx.callback(handle_submit, props=["email"]),  # email passed as kwarg
 * )
 * ```
 */
type PropStoreListener = (key: string, value: unknown) => void;
declare class PropStore {
    private store;
    private listeners;
    /**
     * Set a value in the prop store.
     */
    set(key: string, value: unknown): void;
    /**
     * Get a value from the prop store.
     */
    get(key: string): unknown;
    /**
     * Check if a key exists in the prop store.
     */
    has(key: string): boolean;
    /**
     * Delete a key from the prop store.
     */
    delete(key: string): void;
    /**
     * Clear all values from the prop store.
     */
    clear(): void;
    /**
     * Get all values as a plain object.
     * This is sent to the backend with callback invocations.
     */
    getAll(): Record<string, unknown>;
    /**
     * Get all keys in the prop store.
     * Used for regex pattern matching.
     */
    keys(): string[];
    /**
     * Subscribe to prop store changes.
     */
    subscribe(listener: PropStoreListener): () => void;
    private notifyListeners;
}
export declare const propStore: PropStore;
export type { PropStore };
