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
export declare function applyStoreAs(storeAs: string | Record<string, string>, eventData: Record<string, unknown>): void;
