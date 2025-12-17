import { ClassValue } from 'clsx';

/**
 * Merge class names with Tailwind CSS classes.
 */
export declare function cn(...inputs: ClassValue[]): string;
/**
 * Simple debounce implementation.
 */
export declare function debounce<T extends (...args: unknown[]) => void>(fn: T, delay: number): T;
/**
 * Simple throttle implementation.
 */
export declare function throttle<T extends (...args: unknown[]) => void>(fn: T, delay: number): T;
/**
 * Generate a unique ID.
 */
export declare function generateId(prefix?: string): string;
/**
 * Check if a value is a plain object.
 */
export declare function isPlainObject(value: unknown): value is Record<string, unknown>;
/**
 * Deep merge two objects.
 */
export declare function deepMerge<T extends Record<string, unknown>, S extends Record<string, unknown>>(target: T, source: S): T & S;
