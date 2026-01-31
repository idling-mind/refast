import React, { useMemo } from 'react';
import { ComponentTree, CallbackRef, JsCallbackRef, BoundMethodCallbackRef } from '../types';
import { useEventManager } from '../events/EventManager';
import { componentRegistry } from './registry';
import { debounce, throttle } from '../utils';

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
  invokeCallback: (callbackId: string, data: Record<string, unknown>) => void;
}

/**
 * Create a handler function for a callback reference.
 */
function createCallbackHandler(
  ref: CallbackRef,
  eventManager: EventManagerInterface
): (...args: unknown[]) => void {
  const { callbackId, boundArgs, debounce: debounceMs, throttle: throttleMs } = ref;

  let handler = (...args: unknown[]) => {
    // Extract event data from args
    const eventData = extractEventData(args);

    eventManager.invokeCallback(callbackId, {
      ...boundArgs,
      ...eventData,
    });
  };

  // Apply debounce
  if (debounceMs && debounceMs > 0) {
    handler = debounce(handler, debounceMs);
  }

  // Apply throttle
  if (throttleMs && throttleMs > 0) {
    handler = throttle(handler, throttleMs);
  }

  return handler;
}

/**
 * Create a handler function for a JavaScript callback reference.
 * Executes the JavaScript code directly in the browser without server roundtrip.
 */
function createJsCallbackHandler(
  ref: JsCallbackRef
): (...args: unknown[]) => void {
  const { jsFunction, boundArgs } = ref;

  return (...args: unknown[]) => {
    try {
      // Extract event data from args
      const eventData = extractEventData(args);
      
      // Get the element that triggered the event (if available)
      let element: HTMLElement | null = null;
      if (args[0] && typeof args[0] === 'object' && 'target' in args[0]) {
        const event = args[0] as React.SyntheticEvent;
        element = event.target as HTMLElement;
      }

      // Create a function that has access to event, args, and element
      // eslint-disable-next-line no-new-func
      const fn = new Function('event', 'args', 'element', jsFunction);
      fn(eventData, boundArgs, element);
    } catch (error) {
      console.error('[Refast] Error executing JavaScript callback:', error);
      console.error('[Refast] Code:', jsFunction);
    }
  };
}

/**
 * Create a handler function for a bound method callback reference.
 * Calls a specific method on a component identified by its ID.
 */
function createBoundMethodCallbackHandler(
  ref: BoundMethodCallbackRef
): (...args: unknown[]) => void {
  const { boundMethod } = ref;
  const { targetId, methodName, args: positionalArgs = [], kwargs = {} } = boundMethod;

  return () => {
    try {
      const element = document.getElementById(targetId);
      if (element) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const method = (element as any)[methodName];
        if (typeof method === 'function') {
          // Combine positional args and kwargs
          // If there are kwargs, pass them as the last argument (as an object)
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

    return {
      value: target.value,
      checked: target.checked,
      name: target.name,
    };
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
