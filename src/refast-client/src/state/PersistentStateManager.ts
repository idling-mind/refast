/**
 * Persistent state manager for browser storage (localStorage and sessionStorage).
 *
 * Handles syncing between Python backend and browser storage, providing
 * persistent state that survives page refreshes and browser restarts.
 */

const STORAGE_PREFIX = 'refast:';
const LOCAL_PREFIX = `${STORAGE_PREFIX}local:`;
const SESSION_PREFIX = `${STORAGE_PREFIX}session:`;

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
 * Get all Refast-prefixed keys from a storage.
 */
function getRefastKeys(storage: Storage, prefix: string): string[] {
  const keys: string[] = [];
  for (let i = 0; i < storage.length; i++) {
    const key = storage.key(i);
    if (key && key.startsWith(prefix)) {
      keys.push(key);
    }
  }
  return keys;
}

/**
 * Read all Refast data from a storage.
 */
function readStorage(storage: Storage, prefix: string): Record<string, string> {
  const data: Record<string, string> = {};
  const keys = getRefastKeys(storage, prefix);

  for (const fullKey of keys) {
    const key = fullKey.substring(prefix.length);
    const value = storage.getItem(fullKey);
    if (value !== null) {
      data[key] = value;
    }
  }

  return data;
}

/**
 * Get the storage object and prefix for a storage type.
 */
function getStorageInfo(storageType: 'local' | 'session'): { storage: Storage; prefix: string } {
  if (storageType === 'local') {
    return { storage: localStorage, prefix: LOCAL_PREFIX };
  } else {
    return { storage: sessionStorage, prefix: SESSION_PREFIX };
  }
}

/**
 * PersistentStateManager handles syncing browser storage with the backend.
 */
export class PersistentStateManager {
  private websocket: WebSocket | null = null;
  private initialized = false;
  private onReadyCallback: (() => void) | null = null;

  /**
   * Set the WebSocket connection to use for communication.
   */
  setWebSocket(ws: WebSocket | null): void {
    this.websocket = ws;

    if (ws && ws.readyState === WebSocket.OPEN) {
      this.sendInitialState();
    } else if (ws) {
      // Wait for connection to open
      ws.addEventListener('open', () => {
        this.sendInitialState();
      }, { once: true });
    }
  }

  /**
   * Register a callback to be called when store is ready (after init is acknowledged).
   */
  onReady(callback: () => void): void {
    this.onReadyCallback = callback;
  }

  /**
   * Called when backend acknowledges store_init.
   */
  handleStoreReady(): void {
    if (this.onReadyCallback) {
      this.onReadyCallback();
    }
  }

  /**
   * Check if store has been initialized with backend.
   */
  isInitialized(): boolean {
    return this.initialized;
  }

  /**
   * Resync the store state with the backend.
   * This sends the current browser storage state as a store_sync message.
   */
  resyncStore(): void {
    if (!this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
      console.warn('[Refast] Cannot resync store: WebSocket not connected');
      return;
    }

    const data: StoreData = {
      local: readStorage(localStorage, LOCAL_PREFIX),
      session: readStorage(sessionStorage, SESSION_PREFIX),
    };

    this.websocket.send(JSON.stringify({
      type: 'store_sync',
      data,
    }));
  }

  /**
   * Send the current browser storage state to the backend.
   */
  sendInitialState(): void {
    if (!this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
      return;
    }

    if (this.initialized) {
      return;
    }

    const data: StoreData = {
      local: readStorage(localStorage, LOCAL_PREFIX),
      session: readStorage(sessionStorage, SESSION_PREFIX),
    };

    // Include current path so backend can render the correct page
    this.websocket.send(JSON.stringify({
      type: 'store_init',
      data,
      path: window.location.pathname,
    }));

    this.initialized = true;
  }

  /**
   * Handle store updates from the backend.
   */
  handleUpdates(updates: StoreUpdate[]): void {
    for (const update of updates) {
      this.applyUpdate(update);
    }
  }

  /**
   * Apply a single store update.
   */
  private applyUpdate(update: StoreUpdate): void {
    const { storage, prefix } = getStorageInfo(update.storageType);

    switch (update.operation) {
      case 'set':
        if (update.key !== null && update.value !== undefined) {
          // Serialize the value for storage
          // Primitives are stored as-is, objects/arrays as JSON
          const value = update.value;
          if (typeof value === 'string') {
            storage.setItem(`${prefix}${update.key}`, value);
          } else {
            storage.setItem(`${prefix}${update.key}`, JSON.stringify(value));
          }
        }
        break;

      case 'delete':
        if (update.key !== null) {
          storage.removeItem(`${prefix}${update.key}`);
        }
        break;

      case 'clear':
        // Only clear Refast-prefixed keys
        const keys = getRefastKeys(storage, prefix);
        for (const key of keys) {
          storage.removeItem(key);
        }
        break;
    }
  }

  /**
   * Read a value from browser storage directly.
   * Useful for getting initial values before backend sync.
   */
  get(storageType: 'local' | 'session', key: string): string | null {
    const { storage, prefix } = getStorageInfo(storageType);
    return storage.getItem(`${prefix}${key}`);
  }

  /**
   * Get all values from a storage type.
   */
  getAll(storageType: 'local' | 'session'): Record<string, string> {
    const { storage, prefix } = getStorageInfo(storageType);
    return readStorage(storage, prefix);
  }

  /**
   * Reset the initialized state (used on reconnect).
   */
  reset(): void {
    this.initialized = false;
  }
}

// Singleton instance
export const persistentStateManager = new PersistentStateManager();
