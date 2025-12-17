import React, { useMemo } from 'react';
import { ComponentTree, CallbackRef } from '../types';
import { useEventManager } from '../events/EventManager';
import { componentRegistry } from './registry';
import { debounce, throttle } from '../utils';

interface ComponentRendererProps {
  tree: ComponentTree | string;
  onUpdate?: (id: string, component: ComponentTree) => void;
}

/**
 * Renders a component tree from Python backend.
 */
export function ComponentRenderer({ tree, onUpdate }: ComponentRendererProps): React.ReactElement | null {
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

  // Process props - convert callbacks to functions
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const processedProps = useMemo(() => {
    const result: Record<string, unknown> = { ...props, id };

    for (const [key, value] of Object.entries(props)) {
      if (isCallbackRef(value)) {
        result[key] = createCallbackHandler(value, eventManager);
      }
    }

    return result;
  }, [props, id, eventManager]);

  // Render children
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const renderedChildren = useMemo(() => {
    if (!children || children.length === 0) {
      return null;
    }

    return children.map((child, index) => (
      <ComponentRenderer
        key={typeof child === 'string' ? index : child.id || index}
        tree={child}
        onUpdate={onUpdate}
      />
    ));
  }, [children, onUpdate]);

  return (
    <Component {...processedProps} data-refast-id={id}>
      {renderedChildren}
    </Component>
  );
}

/**
 * Check if a value is a callback reference.
 */
function isCallbackRef(value: unknown): value is CallbackRef {
  return (
    typeof value === 'object' &&
    value !== null &&
    'callbackId' in value
  );
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
