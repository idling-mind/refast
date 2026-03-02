import React, { useMemo, Suspense, Component } from 'react';
import { ComponentTree, CallbackRef, JsCallbackRef, BoundMethodCallbackRef, SavePropRef, ChainedActionRef, AnyActionRef } from '../types';
import { useEventManager } from '../events/EventManager';
import { componentRegistry } from './registry';
import {
  EventManagerInterface,
  isCallbackRef,
  isJsCallbackRef,
  isBoundMethodCallbackRef,
  isSavePropRef,
  isChainedActionRef,
  createSingleActionExecutor,
} from '../utils/actionExecutor';

/**
 * Error boundary that isolates render failures to a single component subtree.
 * Without this, a crash in any component (e.g. recharts hook errors) would
 * unmount the entire page.
 */
interface ErrorBoundaryState { hasError: boolean; errorMessage: string }
class ComponentErrorBoundary extends Component<
  { children: React.ReactNode; componentType: string },
  ErrorBoundaryState
> {
  constructor(props: { children: React.ReactNode; componentType: string }) {
    super(props);
    this.state = { hasError: false, errorMessage: '' };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, errorMessage: error.message };
  }

  componentDidCatch(error: Error) {
    console.error(`[Refast] Error rendering <${this.props.componentType}>:`, error);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          data-refast-error={this.props.componentType}
          title={this.state.errorMessage}
          style={{
            display: 'inline-block',
            border: '1px dashed #ef4444',
            borderRadius: 4,
            padding: '2px 6px',
            color: '#ef4444',
            fontSize: 11,
            fontFamily: 'monospace',
          }}
        >
          {`<${this.props.componentType}>`}
        </div>
      );
    }
    return this.props.children;
  }
}

/**
 * Default loading fallback for lazy-loaded components.
 * Shows a subtle shimmer animation that minimises layout shift.
 */
function LazyFallback() {
  return (
    <div
      className="animate-pulse rounded bg-muted/40"
      style={{ minHeight: 24, minWidth: 48 }}
    />
  );
}

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
  if (!tree) {
    return null;
  }

  // If it's a string, render as text immediately without hitting any object-specific hooks
  if (typeof tree === 'string') {
    return <>{tree}</>;
  }

  // Delegate object rendering to a sub-component to maintain hook rules
  return <ComponentObjectRenderer tree={tree} onUpdate={onUpdate} ref={ref} {...rest} />;
});
ComponentRenderer.displayName = 'ComponentRenderer';

const ComponentObjectRenderer = React.forwardRef<HTMLElement, ComponentRendererProps & { tree: Extract<ComponentTree, object> }>(({ tree, onUpdate, ...rest }, ref) => {
  const eventManager = useEventManager();

  if (!tree) {
    return null;
  }

  const { type, id, props, children } = tree;

  // Get the component from registry
  const Component = componentRegistry.get(type);

  // Process props - convert snake_case to camelCase, handle callbacks and formatters
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
      } else if (isSavePropRef(value)) {
        result[camelKey] = createSavePropHandler(value);
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
  const renderedChildren = useMemo(() => {
    if (!children || children.length === 0) {
      return null;
    }

    const isChartComponent = (compType: string) => componentRegistry.getChunkName(compType) === 'charts';
    const isChartParent = isChartComponent(type);

    // Define a recursive unwrap function for Recharts children (e.g. XAxis, Line, Cell, Label)
    const buildChartElement = (node: any, i: number): React.ReactNode => {
      if (typeof node === 'string') return node;
      const RComp = componentRegistry.get(node.type) as any;
      if (!RComp || !isChartComponent(node.type)) {
        // Fall back to normal renderer if it's NOT a charts component (e.g. Tooltip custom content)
        return <ComponentRenderer key={node.id || i} tree={node} onUpdate={onUpdate} />;
      }
      
      const nProps: any = { key: node.id || i };
      for (const [nk, nv] of Object.entries(node.props || {})) {
        if (isFormatterString(nk, nv)) {
          nProps[snakeToCamel(nk)] = createFormatterFunction(nv as string);
        } else if (typeof nv === 'object' && nv !== null && (nv as any).type) {
          nProps[snakeToCamel(nk)] = <ComponentRenderer tree={nv as any} onUpdate={onUpdate} />;
        } else {
          nProps[snakeToCamel(nk)] = nv;
        }
      }
      
      const nChildren = (node.children || [])
        .filter((c: any) => c != null && c !== 'None')
        .map((c: any, ci: number) => buildChartElement(c, ci));
        
      return React.createElement(RComp, removeNullValues(nProps), nChildren.length > 0 ? nChildren : undefined);
    };

    // Filter out null/undefined values and 'None' strings (defensive check)
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return children
      .filter((child: any) => child != null && child !== 'None')
      .map((child: any, index: number) => {
        if (typeof child === 'string') return child;

        // Recharts requires direct elements, not Wrapped by ComponentRenderer/Suspense
        // Unroll them if their parent is a Recharts parent.
        if (isChartParent && isChartComponent(child.type)) {
           return buildChartElement(child, index);
        }

        return (
          <ComponentRenderer
            key={typeof child === 'string' ? index : child.id || index}
            tree={child}
            onUpdate={onUpdate}
          />
        );
      });
  }, [children, onUpdate, type]);

  if (!Component) {
    console.warn(`Unknown component type: ${type}`);
    return <div data-unknown-type={type}>{JSON.stringify(tree)}</div>;
  }

  // Handle parentStyle for wrapper div
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { parentStyle, ...componentProps } = processedProps;

  // Determine if the component is lazy (needs Suspense boundary)
  const needsSuspense = componentRegistry.isLazy(type);

  // Only pass ref forward if this is actually a forwardRef capable component.
  // Many internal or customized wrappers don't like having ref forced upon them.
  const isChart = componentRegistry.getChunkName(type) === 'charts';
  const shouldPassRef = !isChart;

  const componentElement = shouldPassRef ? (
    <Component {...componentProps} {...rest} data-refast-id={id} ref={ref}>
      {renderedChildren}
    </Component>
  ) : (
    <Component {...componentProps} {...rest} data-refast-id={id}>
      {renderedChildren}
    </Component>
  );

  // Wrap in Suspense if this component was lazily resolved
  const wrappedElement = needsSuspense ? (
    <Suspense fallback={<LazyFallback />}>
      {componentElement}
    </Suspense>
  ) : componentElement;

  const bounded = (
    <ComponentErrorBoundary componentType={type}>
      {wrappedElement}
    </ComponentErrorBoundary>
  );

  if (parentStyle) {
    return (
      <div
        style={parentStyle as React.CSSProperties}
        className="refast-component-wrapper"
        data-wrapper-for={id}
      >
        {bounded}
      </div>
    );
  }

  return bounded;
});
ComponentObjectRenderer.displayName = 'ComponentObjectRenderer';

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
function createSavePropHandler(
  ref: SavePropRef,
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

  // Date object (e.g., Calendar onSelect in single mode)
  if (first instanceof Date) {
    return {
      value: first.toISOString(),
      date: first.toISOString(),
    };
  }

  // React event
  if (first && typeof first === 'object' && 'target' in first) {
    const event = first as React.SyntheticEvent<HTMLInputElement>;
    const target = event.target as HTMLInputElement;
    const data: Record<string, unknown> = {};

    // Only extract form-field properties from actual form elements.
    // Buttons and their children have empty/undefined value/name which
    // would pollute callback kwargs inconsistently.
    const tag = target.tagName?.toLowerCase();
    if (tag === 'input' || tag === 'select' || tag === 'textarea') {
      data.value = target.value;
      data.name = target.name;
      if (target.type === 'checkbox' || target.type === 'radio') {
        data.checked = target.checked;
      }
    }

    // Extract keyboard event properties (onKeyDown, onKeyUp, onKeyPress)
    if ('key' in event) {
      const ke = event as unknown as React.KeyboardEvent;
      data.key = ke.key;
      data.code = ke.code;
      if (ke.altKey) data.altKey = true;
      if (ke.ctrlKey) data.ctrlKey = true;
      if (ke.metaKey) data.metaKey = true;
      if (ke.shiftKey) data.shiftKey = true;
      if (ke.repeat) data.repeat = true;
    }

    return data;
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
