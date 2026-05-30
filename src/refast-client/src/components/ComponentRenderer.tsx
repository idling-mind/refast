import React, { useMemo, Suspense, Component, useEffect, useState } from 'react';
import { ComponentTree, AnyActionRef } from '../types';
import { useEventManager } from '../events/EventManager';
import { componentRegistry } from './registry';
import { EventManagerInterface, createSingleActionExecutor } from '../utils/actionExecutor';
import { transformProps } from '../utils/propTransformer';
import { refastBus } from '../utils/eventBus';

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
  ref?: React.Ref<HTMLElement>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any;
}

/**
 * Renders a component tree from Python backend.
 */
export function ComponentRenderer({ tree, onUpdate, ref, ...rest }: ComponentRendererProps) {
  if (!tree) {
    return null;
  }

  // If it's a string, render as text immediately without hitting any object-specific hooks
  if (typeof tree === 'string') {
    return <>{tree}</>;
  }

  // Delegate object rendering to a sub-component to maintain hook rules
  return <ComponentObjectRenderer tree={tree} onUpdate={onUpdate} ref={ref} {...rest} />;
}
ComponentRenderer.displayName = 'ComponentRenderer';

function ComponentObjectRenderer({ tree, onUpdate, ref, ...rest }: ComponentRendererProps & { tree: Extract<ComponentTree, object> }) {
  const eventManager = useEventManager();
  const [extensionsReady, setExtensionsReady] = useState<boolean>(
    (window as Window & { __REFAST_EXTENSIONS_READY__?: boolean }).__REFAST_EXTENSIONS_READY__ ?? true,
  );
  const [extensionPending, setExtensionPending] = useState<boolean>(false);
  const [extensionEpoch, setExtensionEpoch] = useState<number>(0);

  useEffect(() => {
    const win = window as Window & { __REFAST_EXTENSIONS_READY__?: boolean };
    if (win.__REFAST_EXTENSIONS_READY__ === true) {
      setExtensionsReady(true);
      return;
    }
    return refastBus.on('refast:extensions-ready', () => setExtensionsReady(true));
  }, []);

  if (!tree) {
    return null;
  }

  const { type, id, props, children } = tree;

  const extensionWindow = window as Window & {
    __REFAST_EXTENSION_COMPONENT_MAP__?: Record<string, string>;
    __REFAST_EXTENSION_LOADED__?: Record<string, boolean>;
    __REFAST_LOAD_EXTENSION__?: (name: string) => Promise<void>;
  };
  const mappedExtension = extensionWindow.__REFAST_EXTENSION_COMPONENT_MAP__?.[type];
  const mappedExtensionLoaded = mappedExtension
    ? Boolean(extensionWindow.__REFAST_EXTENSION_LOADED__?.[mappedExtension])
    : false;

  // Re-resolve registry component after extension load events.
  const Component = useMemo(() => componentRegistry.get(type), [type, extensionEpoch]);

  useEffect(() => {
    return refastBus.on('refast:extension-loaded', () => setExtensionEpoch((v) => v + 1));
  }, []);

  useEffect(() => {
    if (Component) {
      setExtensionPending(false);
      return;
    }

    if (!mappedExtension) {
      return;
    }

    if (mappedExtensionLoaded) {
      return;
    }

    const load = extensionWindow.__REFAST_LOAD_EXTENSION__;
    if (!load) {
      return;
    }

    let cancelled = false;
    setExtensionPending(true);
    load(mappedExtension).finally(() => {
      if (!cancelled) {
        setExtensionPending(false);
        setExtensionEpoch((value) => value + 1);
      }
    });

    return () => {
      cancelled = true;
    };
  }, [Component, mappedExtension, mappedExtensionLoaded, extensionWindow.__REFAST_LOAD_EXTENSION__]);

  // Normalize props: snake_case → camelCase, resolve action refs → handlers,
  // convert formatter strings → functions, strip nulls.
  const processedProps = useMemo(() => {
    return transformProps(props, {
      id,
      resolveAction: (value) => createActionHandler(value, eventManager),
    });
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

        const nProps: Record<string, unknown> = {
          key: node.id || i,
          ...transformProps(node.props || {}, {
            resolveComponentTree: (value) => (
              <ComponentRenderer tree={value as ComponentTree} onUpdate={onUpdate} />
            ),
          }),
        };

        const nChildren = (node.children || [])
          .filter((c: any) => c != null && c !== 'None')
          .map((c: any, ci: number) => buildChartElement(c, ci));

        return React.createElement(RComp, nProps, nChildren.length > 0 ? nChildren : undefined);
    };

    return children
      .filter((child: any) => child != null && child !== 'None')
      .map((child: any, index: number) => {
        if (typeof child === 'string') return child;

        // Recharts requires direct elements, not wrapped by ComponentRenderer/Suspense
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
    // If this type is known to come from an extension, keep waiting until the
    // extension script is confirmed loaded and registration has a chance to apply.
    if (!extensionsReady || extensionPending || Boolean(mappedExtension && !mappedExtensionLoaded)) {
      return <LazyFallback />;
    }
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
}
ComponentObjectRenderer.displayName = 'ComponentObjectRenderer';

/**
 * Create the top-level React event handler for any action ref.
 * Called via `resolveAction` in transformProps for every action ref value.
 */
function createActionHandler(
  ref: AnyActionRef,
  eventManager: EventManagerInterface,
): (...args: unknown[]) => void {
  const executor = createSingleActionExecutor(ref, eventManager);

  return (...args: unknown[]) => {
    const eventData = extractEventData(args);
    // Fire-and-forget — React event handlers are synchronous
    executor(eventData, args);
  };
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

  // Array payloads (e.g., Slider onValueChange) should be available as
  // event.value for save_prop("key"), while keeping index access ("0", "1").
  if (Array.isArray(first)) {
    return {
      ...first,
      value: first,
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
