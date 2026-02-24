/**
 * Shared action executor utilities.
 *
 * These are extracted from ComponentRenderer so they can also be used by
 * ToastManager (and any future consumer) without duplicating logic.
 */

import {
  AnyActionRef,
  CallbackRef,
  JsCallbackRef,
  BoundMethodCallbackRef,
  SavePropRef,
  ChainedActionRef,
} from '../types';
import { debounce, throttle } from '../utils';
import { propStore } from '../state/PropStore';
import { applySaveProp } from './propStoreUtils';
import { refastJsHelper } from './refastJsHelper';

// ---------------------------------------------------------------------------
// Event manager interface
// ---------------------------------------------------------------------------

export interface EventManagerInterface {
  invokeCallback: (
    callbackId: string,
    data: Record<string, unknown>,
    eventData?: Record<string, unknown>,
  ) => void;
}

// ---------------------------------------------------------------------------
// Type guards
// ---------------------------------------------------------------------------

export function isCallbackRef(value: unknown): value is CallbackRef {
  return typeof value === 'object' && value !== null && 'callbackId' in value;
}

export function isJsCallbackRef(value: unknown): value is JsCallbackRef {
  return typeof value === 'object' && value !== null && 'jsFunction' in value;
}

export function isBoundMethodCallbackRef(value: unknown): value is BoundMethodCallbackRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'boundMethod' in value &&
    typeof (value as BoundMethodCallbackRef).boundMethod === 'object' &&
    'targetId' in (value as BoundMethodCallbackRef).boundMethod &&
    'methodName' in (value as BoundMethodCallbackRef).boundMethod
  );
}

export function isSavePropRef(value: unknown): value is SavePropRef {
  return typeof value === 'object' && value !== null && 'saveProp' in value;
}

export function isChainedActionRef(value: unknown): value is ChainedActionRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'chain' in value &&
    Array.isArray((value as ChainedActionRef).chain)
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Resolve prop store values for a callback's `props` list.
 * Supports exact key matches and regex patterns.
 */
export function resolveProps(props: string[]): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  const allStoreKeys = propStore.keys();

  for (const pattern of props) {
    const isRegex = /[\\^$.*+?()[\]{}|]/.test(pattern);
    if (isRegex) {
      try {
        const regex = new RegExp(`^${pattern}$`);
        for (const key of allStoreKeys) {
          if (regex.test(key)) {
            const value = propStore.get(key);
            if (value !== undefined) {
              result[key] = value;
            }
          }
        }
      } catch {
        console.warn(`[Refast] Invalid regex pattern in props: ${pattern}`);
        const value = propStore.get(pattern);
        if (value !== undefined) {
          result[pattern] = value;
        }
      }
    } else {
      const value = propStore.get(pattern);
      if (value !== undefined) {
        result[pattern] = value;
      }
    }
  }
  return result;
}

/**
 * Wrap a function with debounce/throttle if configured.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function applyTimingControls<T extends (...args: any[]) => any>(
  fn: T,
  debounceMs?: number,
  throttleMs?: number,
): T {
  let result: (...args: unknown[]) => unknown = fn;
  if (debounceMs && debounceMs > 0) {
    result = debounce(result, debounceMs);
  }
  if (throttleMs && throttleMs > 0) {
    result = throttle(result, throttleMs);
  }
  return result as T;
}

// ---------------------------------------------------------------------------
// Executors
// ---------------------------------------------------------------------------

/**
 * Create an executor for a single action ref.
 * Returns an async function that receives pre-extracted eventData and raw args.
 */
export function createSingleActionExecutor(
  ref: AnyActionRef,
  eventManager: EventManagerInterface,
): (eventData: Record<string, unknown>, rawArgs: unknown[]) => Promise<void> {
  if (isChainedActionRef(ref)) {
    return createChainedActionExecutor(ref, eventManager);
  }

  if (isSavePropRef(ref)) {
    const { saveProp, debounce: d, throttle: t } = ref;
    let exec = (eventData: Record<string, unknown>) => {
      applySaveProp(saveProp, eventData);
    };
    exec = applyTimingControls(exec, d, t) as typeof exec;
    return async (eventData) => {
      exec(eventData);
    };
  }

  if (isCallbackRef(ref)) {
    const { callbackId, boundArgs, props, debounce: d, throttle: t } = ref;
    let invoke = (eventData: Record<string, unknown>) => {
      let propsData: Record<string, unknown> = {};
      if (props && props.length > 0) {
        propsData = resolveProps(props);
      }
      eventManager.invokeCallback(callbackId, { ...propsData, ...boundArgs }, eventData);
    };
    invoke = applyTimingControls(invoke, d, t) as typeof invoke;
    return async (eventData) => {
      invoke(eventData);
    };
  }

  if (isJsCallbackRef(ref)) {
    const { jsFunction, boundArgs, debounce: d, throttle: t } = ref;
    let exec = (eventData: Record<string, unknown>, rawArgs: unknown[]) => {
      try {
        let element: HTMLElement | null = null;
        if (rawArgs[0] && typeof rawArgs[0] === 'object' && 'target' in rawArgs[0]) {
          element = (rawArgs[0] as { target: HTMLElement }).target;
        }
        // eslint-disable-next-line no-new-func
        const fn = new Function('event', 'args', 'element', 'refast', jsFunction);
        fn(eventData, boundArgs, element, refastJsHelper);
      } catch (error) {
        console.error('[Refast] Error executing JavaScript callback:', error);
        console.error('[Refast] Code:', jsFunction);
      }
    };
    exec = applyTimingControls(exec, d, t) as typeof exec;
    return async (eventData, rawArgs) => {
      exec(eventData, rawArgs);
    };
  }

  if (isBoundMethodCallbackRef(ref)) {
    const { boundMethod, debounce: d, throttle: t } = ref;
    const { targetId, methodName, args: positionalArgs = [], kwargs = {} } = boundMethod;
    let exec = () => {
      try {
        const element = document.getElementById(targetId);
        if (element) {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          const method = (element as any)[methodName];
          if (typeof method === 'function') {
            const hasKwargs = Object.keys(kwargs).length > 0;
            const allArgs = hasKwargs ? [...positionalArgs, kwargs] : positionalArgs;
            if (allArgs.length === 0) {
              method.call(element);
            } else if (allArgs.length === 1) {
              method.call(element, allArgs[0]);
            } else {
              method.apply(element, allArgs);
            }
          } else {
            console.warn(`[Refast] Method '${methodName}' not found on element '${targetId}'`);
          }
        } else {
          console.warn(`[Refast] Element with id '${targetId}' not found`);
        }
      } catch (error) {
        console.error('[Refast] Error calling bound method:', error);
        console.error('[Refast] Target:', targetId, 'Method:', methodName);
      }
    };
    exec = applyTimingControls(exec, d, t) as typeof exec;
    return async () => {
      exec();
    };
  }

  // Unknown action type — no-op
  return async () => {};
}

/**
 * Create an executor for a chained action (serial or parallel).
 */
export function createChainedActionExecutor(
  ref: ChainedActionRef,
  eventManager: EventManagerInterface,
): (eventData: Record<string, unknown>, rawArgs: unknown[]) => Promise<void> {
  const executors = ref.chain.map((action) => createSingleActionExecutor(action, eventManager));
  const mode = ref.mode || 'serial';

  return async (eventData, rawArgs) => {
    if (mode === 'parallel') {
      await Promise.all(executors.map((exec) => exec(eventData, rawArgs)));
    } else {
      for (const exec of executors) {
        await exec(eventData, rawArgs);
      }
    }
  };
}
