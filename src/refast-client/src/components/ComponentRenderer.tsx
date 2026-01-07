import React, { useMemo } from 'react';
import { ComponentTree, CallbackRef } from '../types';
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

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return children.map((child: any, index: number) => (
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
