import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Merge class names with Tailwind CSS classes.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * Simple debounce implementation.
 */
export function debounce<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): T {
  let timeoutId: ReturnType<typeof setTimeout>;

  return ((...args: unknown[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  }) as T;
}

/**
 * Simple throttle implementation.
 */
export function throttle<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number
): T {
  let lastCall = 0;

  return ((...args: unknown[]) => {
    const now = Date.now();
    if (now - lastCall >= delay) {
      lastCall = now;
      fn(...args);
    }
  }) as T;
}

/**
 * Generate a unique ID.
 */
export function generateId(prefix: string = 'refast'): string {
  return `${prefix}-${Math.random().toString(36).substring(2, 11)}`;
}

/**
 * Check if a value is a plain object.
 */
export function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

/**
 * Deep merge two objects.
 */
export function deepMerge<
  T extends Record<string, unknown>,
  S extends Record<string, unknown>
>(
  target: T,
  source: S
): T & S {
  const result = { ...target } as T & S;

  for (const key in source) {
    const sourceValue = source[key];
    const targetValue = (target as Record<string, unknown>)[key];

    if (isPlainObject(sourceValue) && isPlainObject(targetValue)) {
      (result as Record<string, unknown>)[key] = deepMerge(
        targetValue as Record<string, unknown>,
        sourceValue as Record<string, unknown>
      );
    } else if (sourceValue !== undefined) {
      (result as Record<string, unknown>)[key] = sourceValue;
    }
  }

  return result;
}

/**
 * Compile-time exhaustiveness check for discriminated union switch / if-else
 * chains.
 *
 * Pass the "impossible" value in the default / else branch.  TypeScript will
 * flag any unhandled union member as a type error before the build completes.
 * At runtime it throws, turning silent no-ops into loud, traceable failures.
 *
 * @example
 * function handle(ref: AnyActionRef) {
 *   if (isCallbackRef(ref)) { ... }
 *   else if (isSavePropRef(ref)) { ... }
 *   // …all branches covered…
 *   else { assertNever(ref); }
 * }
 */
export function assertNever(x: never, message?: string): never {
  throw new Error(message ?? `[Refast] Unhandled case: ${JSON.stringify(x)}`);
}

export * from './sizes';

