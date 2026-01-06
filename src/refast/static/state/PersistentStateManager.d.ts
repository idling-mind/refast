/**
 * Persistent state manager for browser storage (localStorage and sessionStorage).
 *
 * Handles syncing between Python backend and browser storage, providing
 * persistent state that survives page refreshes and browser restarts.
 */
/**
 * Store update operation from the backend.
 */
export interface StoreUpdate {
    storageType: 'local' | 'session';
    operation: 'set' | 'delete' | 'clear';
    key: string | null;
    value?: unknown;
    encrypt?: boolean;
}
/**
 * Store data structure sent to backend on init.
 */
export interface StoreData {
    local: Record<string, string>;
    session: Record<string, string>;
}
/**
 * PersistentStateManager handles syncing browser storage with the backend.
 */
export declare class PersistentStateManager {
    private websocket;
    private initialized;
    private onReadyCallback;
    /**
     * Set the WebSocket connection to use for communication.
     */
    setWebSocket(ws: WebSocket | null): void;
    /**
     * Register a callback to be called when store is ready (after init is acknowledged).
     */
    onReady(callback: () => void): void;
    /**
     * Called when backend acknowledges store_init.
     */
    handleStoreReady(): void;
    /**
     * Check if store has been initialized with backend.
     */
    isInitialized(): boolean;
    /**
     * Send the current browser storage state to the backend.
     */
    sendInitialState(): void;
    /**
     * Handle store updates from the backend.
     */
    handleUpdates(updates: StoreUpdate[]): void;
    /**
     * Apply a single store update.
     */
    private applyUpdate;
    /**
     * Read a value from browser storage directly.
     * Useful for getting initial values before backend sync.
     */
    get(storageType: 'local' | 'session', key: string): string | null;
    /**
     * Get all values from a storage type.
     */
    getAll(storageType: 'local' | 'session'): Record<string, string>;
    /**
     * Reset the initialized state (used on reconnect).
     */
    reset(): void;
}
export declare const persistentStateManager: PersistentStateManager;
