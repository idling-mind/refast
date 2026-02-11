/**
 * PropStore - Frontend-only state for storing component prop values.
 * 
 * This store allows values from component events (like input changes) to be
 * captured on the frontend and made available to subsequent callbacks without
 * requiring server roundtrips for each state update.
 * 
 * Usage Pattern:
 * 1. Components use `store_as` in their callbacks to store event values
 * 2. When a callback with `props=[...]` is invoked, matching prop store values
 *    are sent as keyword arguments to the Python callback
 * 
 * Example (Python):
 * ```python
 * Input(
 *     name="email",
 *     on_change=ctx.callback(store_as="email"),  # Store-only, no server call
 * )
 * 
 * Button(
 *     "Submit",
 *     on_click=ctx.callback(handle_submit, props=["email"]),  # email passed as kwarg
 * )
 * ```
 */

type PropStoreListener = (key: string, value: unknown) => void;

class PropStore {
  private store: Map<string, unknown> = new Map();
  private listeners: Set<PropStoreListener> = new Set();

  /**
   * Set a value in the prop store.
   */
  set(key: string, value: unknown): void {
    this.store.set(key, value);
    this.notifyListeners(key, value);
  }

  /**
   * Get a value from the prop store.
   */
  get(key: string): unknown {
    const value = this.store.get(key);
    return value;
  }

  /**
   * Check if a key exists in the prop store.
   */
  has(key: string): boolean {
    return this.store.has(key);
  }

  /**
   * Delete a key from the prop store.
   */
  delete(key: string): void {
    this.store.delete(key);
    this.notifyListeners(key, undefined);
  }

  /**
   * Clear all values from the prop store.
   */
  clear(): void {
    this.store.clear();
  }

  /**
   * Get all values as a plain object.
   * This is sent to the backend with callback invocations.
   */
  getAll(): Record<string, unknown> {
    const result: Record<string, unknown> = {};
    this.store.forEach((value, key) => {
      result[key] = value;
    });
    return result;
  }

  /**
   * Get all keys in the prop store.
   * Used for regex pattern matching.
   */
  keys(): string[] {
    return Array.from(this.store.keys());
  }

  /**
   * Subscribe to prop store changes.
   */
  subscribe(listener: PropStoreListener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notifyListeners(key: string, value: unknown): void {
    this.listeners.forEach(listener => listener(key, value));
  }
}

// Global singleton instance
export const propStore = new PropStore();

// Export the class for typing purposes
export type { PropStore };
