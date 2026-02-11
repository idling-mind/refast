import React, { useMemo } from 'react';
import { ComponentTree, CallbackRef, JsCallbackRef, BoundMethodCallbackRef, StorePropRef, ChainedActionRef, AnyActionRef } from '../types';
import { useEventManager } from '../events/EventManager';
import { componentRegistry } from './registry';
import { debounce, throttle } from '../utils';
import { propStore } from '../state/PropStore';
import { applyStoreProp } from '../utils/propStoreUtils';

interface ComponentRendererProps {
  tree: ComponentTree | string;
  onUpdate?: (id: string, component: ComponentTree) => void;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any;
}

/**
 * Renders a component tree from Python backend.
 */
export const ComponentRenderer = React.forwardRef<HTMLElement, ComponentRendererProps>(({ tree, onUpdate, ...rest }, ref) => {
  const eventManager = useEventManager();

  // If it's a string, render as text
  if (typeof tree === 'string') {
    return <>{tree}</>;
  }

  const { type, id, props, children } = tree;

  // Get the component from registry
  const Component = componentRegistry.get(type);

  if (!Component) {
    console.warn(`Unknown component type: ${type}`);
    return <div data-unknown-type={type}>{JSON.stringify(tree)}</div>;
  }

  // Process props - convert snake_case to camelCase, handle callbacks and formatters
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const processedProps = useMemo(() => {
    const result: Record<string, unknown> = { id };

    for (const [key, value] of Object.entries(props)) {
      // Convert snake_case keys to camelCase for React/DOM compatibility
      const camelKey = snakeToCamel(key);
      
      if (isCallbackRef(value)) {
        result[camelKey] = createCallbackHandler(value, eventManager);
      } else if (isJsCallbackRef(value)) {
        result[camelKey] = createJsCallbackHandler(value);
      } else if (isBoundMethodCallbackRef(value)) {
        result[camelKey] = createBoundMethodCallbackHandler(value);
      } else if (isStorePropRef(value)) {
        result[camelKey] = createStorePropHandler(value);
      } else if (isChainedActionRef(value)) {
        result[camelKey] = createChainedActionHandler(value, eventManager);
      } else if (isFormatterString(key, value)) {
        // Convert formatter strings to functions (e.g., tickFormatter)
        result[camelKey] = createFormatterFunction(value as string);
      } else {
        result[camelKey] = value;
      }
    }

    // Remove null values - Recharts expects undefined, not null
    // for optional props like 'data' to use defaults properly
    return removeNullValues(result);
  }, [props, id, eventManager]);

  // Render children
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const renderedChildren = useMemo(() => {
    if (!children || children.length === 0) {
      return null;
    }

    // Filter out null/undefined values and 'None' strings (defensive check)
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return children
      .filter((child: any) => child != null && child !== 'None')
      .map((child: any, index: number) => (
        <ComponentRenderer
          key={typeof child === 'string' ? index : child.id || index}
          tree={child}
          onUpdate={onUpdate}
        />
      ));
  }, [children, onUpdate]);

  // Handle parentStyle for wrapper div
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { parentStyle, ...componentProps } = processedProps;

  const componentElement = (
    <Component {...componentProps} {...rest} data-refast-id={id} ref={ref}>
      {renderedChildren}
    </Component>
  );

  if (parentStyle) {
    return (
      <div
        style={parentStyle as React.CSSProperties}
        className="refast-component-wrapper"
        data-wrapper-for={id}
      >
        {componentElement}
      </div>
    );
  }

  return componentElement;
});
ComponentRenderer.displayName = 'ComponentRenderer';

/**
 * Check if a value is a callback reference (Python callback).
 */
function isCallbackRef(value: unknown): value is CallbackRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'callbackId' in value
  );
}

/**
 * Check if a value is a JavaScript callback reference (client-side execution).
 */
function isJsCallbackRef(value: unknown): value is JsCallbackRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'jsFunction' in value
  );
}

/**
 * Check if a value is a bound method callback reference (calls a method on a component).
 */
function isBoundMethodCallbackRef(value: unknown): value is BoundMethodCallbackRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'boundMethod' in value &&
    typeof (value as BoundMethodCallbackRef).boundMethod === 'object' &&
    'targetId' in (value as BoundMethodCallbackRef).boundMethod &&
    'methodName' in (value as BoundMethodCallbackRef).boundMethod
  );
}

/**
 * Check if a value is a store prop reference (frontend prop store write).
 */
function isStorePropRef(value: unknown): value is StorePropRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'storeProp' in value
  );
}

/**
 * Check if a value is a chained action reference (multiple actions).
 */
function isChainedActionRef(value: unknown): value is ChainedActionRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'chain' in value &&
    Array.isArray((value as ChainedActionRef).chain)
  );
}

/**
 * Check if a prop key/value pair is a formatter string that needs conversion.
 * Checks for both camelCase and snake_case versions.
 */
function isFormatterString(key: string, value: unknown): boolean {
  const formatterProps = [
    'tickFormatter', 'tick_formatter',
    'labelFormatter', 'label_formatter', 
    'formatter'
  ];
  return formatterProps.includes(key) && typeof value === 'string';
}

/**
 * Convert snake_case to camelCase.
 */
function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

/**
 * Remove null values from props object.
 * Recharts expects undefined (prop not present) rather than null
 * for optional props to properly use their default values.
 */
function removeNullValues(obj: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== null) {
      result[key] = value;
    }
  }
  return result;
}

/**
 * Create a formatter function from a string expression.
 * The expression can use 'value' and 'index' variables.
 * For safety, wraps in try-catch to handle null/undefined values.
 */
function createFormatterFunction(expression: string): (value: unknown, index?: number) => string {
  return (value: unknown, index?: number): string => {
    try {
      // Handle null/undefined values gracefully
      if (value === null || value === undefined) {
        return '';
      }
      // Create a function that evaluates the expression
      // eslint-disable-next-line no-new-func
      const fn = new Function('value', 'index', `return ${expression}`);
      return fn(value, index);
    } catch {
      // If expression evaluation fails, return value as string
      return String(value);
    }
  };
}

/**
 * Event manager interface for callback handling.
 */
interface EventManagerInterface {
  invokeCallback: (callbackId: string, data: Record<string, unknown>, eventData?: Record<string, unknown>) => void;
}

/**
 * Resolve prop store values for a callback's `props` list.
 * Supports exact key matches and regex patterns.
 */
function resolveProps(props: string[]): Record<string, unknown> {
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
function applyTimingControls<T extends (...args: any[]) => any>(
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

/**
 * Create a handler for a single action ref that takes pre-extracted event data.
 * Returns an async function for uniform chain execution.
 */
function createSingleActionExecutor(
  ref: AnyActionRef,
  eventManager: EventManagerInterface,
): (eventData: Record<string, unknown>, rawArgs: unknown[]) => Promise<void> {
  if (isChainedActionRef(ref)) {
    return createChainedActionExecutor(ref, eventManager);
  }

  if (isStorePropRef(ref)) {
    const { storeProp, debounce: d, throttle: t } = ref;
    let exec = (eventData: Record<string, unknown>) => {
      applyStoreProp(storeProp, eventData);
    };
    exec = applyTimingControls(exec, d, t) as typeof exec;
    return async (eventData) => { exec(eventData); };
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
    return async (eventData) => { invoke(eventData); };
  }

  if (isJsCallbackRef(ref)) {
    const { jsFunction, boundArgs, debounce: d, throttle: t } = ref;
    let exec = (eventData: Record<string, unknown>, rawArgs: unknown[]) => {
      try {
        let element: HTMLElement | null = null;
        if (rawArgs[0] && typeof rawArgs[0] === 'object' && 'target' in rawArgs[0]) {
          element = (rawArgs[0] as React.SyntheticEvent).target as HTMLElement;
        }
        // eslint-disable-next-line no-new-func
        const fn = new Function('event', 'args', 'element', jsFunction);
        fn(eventData, boundArgs, element);
      } catch (error) {
        console.error('[Refast] Error executing JavaScript callback:', error);
        console.error('[Refast] Code:', jsFunction);
      }
    };
    exec = applyTimingControls(exec, d, t) as typeof exec;
    return async (eventData, rawArgs) => { exec(eventData, rawArgs); };
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
    return async () => { exec(); };
  }

  // Unknown action type — no-op
  return async () => {};
}

/**
 * Create an executor for a chained action (serial or parallel).
 */
function createChainedActionExecutor(
  ref: ChainedActionRef,
  eventManager: EventManagerInterface,
): (eventData: Record<string, unknown>, rawArgs: unknown[]) => Promise<void> {
  const executors = ref.chain.map(action => createSingleActionExecutor(action, eventManager));
  const mode = ref.mode || 'serial';

  return async (eventData, rawArgs) => {
    if (mode === 'parallel') {
      await Promise.all(executors.map(exec => exec(eventData, rawArgs)));
    } else {
      for (const exec of executors) {
        await exec(eventData, rawArgs);
      }
    }
  };
}

/**
 * Create the top-level event handler for any action ref.
 * This is the function that React event props (onClick, onChange, etc.) call.
 */
function createActionHandler(
  ref: AnyActionRef,
  eventManager: EventManagerInterface,
): (...args: unknown[]) => void {
  const executor = createSingleActionExecutor(ref, eventManager);

  return (...args: unknown[]) => {
    const eventData = extractEventData(args);
    // Fire-and-forget — we don't await because React event handlers are sync
    executor(eventData, args);
  };
}

/**
 * Create a handler function for a callback reference (Python callback).
 */
function createCallbackHandler(
  ref: CallbackRef,
  eventManager: EventManagerInterface,
): (...args: unknown[]) => void {
  return createActionHandler(ref, eventManager);
}

/**
 * Create a handler function for a JavaScript callback reference.
 */
function createJsCallbackHandler(
  ref: JsCallbackRef,
): (...args: unknown[]) => void {
  // JsCallback doesn't need eventManager; pass a dummy
  return createActionHandler(ref, { invokeCallback: () => {} });
}

/**
 * Create a handler function for a bound method callback reference.
 */
function createBoundMethodCallbackHandler(
  ref: BoundMethodCallbackRef,
): (...args: unknown[]) => void {
  return createActionHandler(ref, { invokeCallback: () => {} });
}

/**
 * Create a handler function for a store prop reference.
 */
function createStorePropHandler(
  ref: StorePropRef,
): (...args: unknown[]) => void {
  return createActionHandler(ref, { invokeCallback: () => {} });
}

/**
 * Create a handler function for a chained action reference.
 */
function createChainedActionHandler(
  ref: ChainedActionRef,
  eventManager: EventManagerInterface,
): (...args: unknown[]) => void {
  return createActionHandler(ref, eventManager);
}

/**
 * Extract relevant data from event arguments.
 */
function extractEventData(args: unknown[]): Record<string, unknown> {
  if (args.length === 0) return {};

  const first = args[0];

  // React event
  if (first && typeof first === 'object' && 'target' in first) {
    const event = first as React.SyntheticEvent<HTMLInputElement>;
    const target = event.target as HTMLInputElement;

    // Only extract form-field properties from actual form elements.
    // Buttons and their children have empty/undefined value/name which
    // would pollute callback kwargs inconsistently.
    const tag = target.tagName?.toLowerCase();
    if (tag === 'input' || tag === 'select' || tag === 'textarea') {
      const data: Record<string, unknown> = {
        value: target.value,
        name: target.name,
      };
      if (target.type === 'checkbox' || target.type === 'radio') {
        data.checked = target.checked;
      }
      return data;
    }

    return {};
  }

  // Plain value
  if (typeof first === 'string' || typeof first === 'number' || typeof first === 'boolean') {
    return { value: first };
  }

  // Object
  if (typeof first === 'object') {
    return first as Record<string, unknown>;
  }

  return {};
}
