/**
 * Shared prop transformation utilities.
 *
 * Extracts the prop normalization pipeline that was previously duplicated
 * between the main ComponentRenderer path and the chart child element
 * fast-path (buildChartElement). Both paths need:
 *   - snake_case → camelCase key normalisation
 *   - Formatter string → function conversion
 *   - null removal (Recharts expects undefined for absent optional props)
 *
 * Action-ref → handler resolution and component-tree → React element
 * resolution are injected via callbacks so this module stays free of React
 * and EventManager dependencies.
 */

import type { AnyActionRef } from '../types';
import {
  isCallbackRef,
  isJsCallbackRef,
  isBoundMethodCallbackRef,
  isSavePropRef,
  isChainedActionRef,
} from './actionExecutor';

// ---------------------------------------------------------------------------
// Primitive transforms (exported so callers that need them individually can use them)
// ---------------------------------------------------------------------------

/**
 * Convert snake_case to camelCase.
 */
export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

/**
 * Check if a prop key/value pair is a formatter string that should be
 * converted to a function. Checks for both camelCase and snake_case names.
 */
export function isFormatterString(key: string, value: unknown): boolean {
  const formatterProps = [
    'tickFormatter',
    'tick_formatter',
    'labelFormatter',
    'label_formatter',
    'formatter',
  ];
  return formatterProps.includes(key) && typeof value === 'string';
}

/**
 * Remove null values from a props object.
 * Recharts expects undefined (not null) for absent optional props.
 */
export function removeNullValues(
  obj: Record<string, unknown>,
): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (value !== null) {
      result[key] = value;
    }
  }
  return result;
}

/**
 * Check if a value is a field-getter sentinel: `{ "$field_getter": "keyName" }`.
 * Python components can emit this to turn any prop into `(entry) => entry[key]`
 * without component-specific frontend logic.
 */
export function isFieldGetterRef(value: unknown): value is { $field_getter: string } {
  return (
    typeof value === 'object' &&
    value !== null &&
    '$field_getter' in value &&
    typeof (value as Record<string, unknown>).$field_getter === 'string'
  );
}

/**
 * Create a field-getter function from a sentinel.
 * Returns `(entry) => entry[key]` as a string (falls back to empty string).
 */
export function createFieldGetterFunction(
  key: string,
): (entry: Record<string, unknown>) => string {
  return (entry: Record<string, unknown>): string => {
    const v = entry[key];
    return v !== null && v !== undefined ? String(v) : '';
  };
}

/**
 * Create a formatter function from a string expression.
 * The expression may reference `value` and `index` variables.
 */
export function createFormatterFunction(
  expression: string,
): (value: unknown, index?: number) => string {
  return (value: unknown, index?: number): string => {
    try {
      if (value === null || value === undefined) return '';
      // eslint-disable-next-line no-new-func
      const fn = new Function('value', 'index', `return ${expression}`);
      return fn(value, index);
    } catch {
      return String(value);
    }
  };
}

// ---------------------------------------------------------------------------
// Detection helpers (private)
// ---------------------------------------------------------------------------

function isAnyActionRef(value: unknown): value is AnyActionRef {
  return (
    isCallbackRef(value) ||
    isJsCallbackRef(value) ||
    isBoundMethodCallbackRef(value) ||
    isSavePropRef(value) ||
    isChainedActionRef(value)
  );
}

function isComponentTree(value: unknown): boolean {
  return (
    typeof value === 'object' &&
    value !== null &&
    'type' in value &&
    typeof (value as Record<string, unknown>).type === 'string'
  );
}

// ---------------------------------------------------------------------------
// Main transform
// ---------------------------------------------------------------------------

export interface PropTransformOptions {
  /**
   * Component id to inject as the `id` prop. Passed through as-is (no
   * snake_case conversion). When omitted no `id` prop is injected.
   */
  id?: string;
  /**
   * Called for every value that is an action ref (CallbackRef, JsCallbackRef,
   * SavePropRef, BoundMethodCallbackRef, ChainedActionRef). Return the value
   * the prop should have — typically a React event-handler function.
   * When omitted, action refs are passed through unchanged.
   */
  resolveAction?: (value: AnyActionRef, camelKey: string) => unknown;
  /**
   * Called for every value that looks like a nested ComponentTree (an object
   * with a `type: string` field). Return the replacement value — typically a
   * React element.
   * When omitted, component-tree values are passed through unchanged.
   */
  resolveComponentTree?: (value: unknown, camelKey: string) => unknown;
}

/**
 * Normalize a raw props object received from the Python backend.
 *
 * Applies, in order:
 *  1. snake_case → camelCase key conversion
 *  2. Action ref → handler (via `resolveAction`)
 *  3. Formatter string → function
 *  4. Nested component tree → React element (via `resolveComponentTree`)
 *  5. null removal
 */
export function transformProps(
  rawProps: Record<string, unknown>,
  options: PropTransformOptions = {},
): Record<string, unknown> {
  const { id, resolveAction, resolveComponentTree } = options;
  const result: Record<string, unknown> = {};

  if (id !== undefined) result['id'] = id;

  for (const [key, value] of Object.entries(rawProps)) {
    const camelKey = snakeToCamel(key);

    if (resolveAction && isAnyActionRef(value)) {
      result[camelKey] = resolveAction(value, camelKey);
    } else if (isFieldGetterRef(value)) {
      result[camelKey] = createFieldGetterFunction(value.$field_getter);
    } else if (isFormatterString(key, value)) {
      result[camelKey] = createFormatterFunction(value as string);
    } else if (resolveComponentTree && isComponentTree(value)) {
      result[camelKey] = resolveComponentTree(value, camelKey);
    } else {
      result[camelKey] = value;
    }
  }

  return removeNullValues(result);
}
