import { describe, it, expect } from 'vitest';
import { cn, debounce, throttle, generateId, isPlainObject, deepMerge } from '../../utils';

describe('cn', () => {
  it('merges class names', () => {
    expect(cn('foo', 'bar')).toBe('foo bar');
  });

  it('handles conditional classes', () => {
    expect(cn('foo', false && 'bar', 'baz')).toBe('foo baz');
  });

  it('deduplicates tailwind classes', () => {
    expect(cn('p-4', 'p-2')).toBe('p-2');
  });

  it('handles empty input', () => {
    expect(cn()).toBe('');
  });
});

describe('debounce', () => {
  it('debounces function calls', async () => {
    let count = 0;
    const fn = debounce(() => count++, 50);

    fn();
    fn();
    fn();

    expect(count).toBe(0);

    await new Promise((resolve) => setTimeout(resolve, 100));
    expect(count).toBe(1);
  });
});

describe('throttle', () => {
  it('throttles function calls', () => {
    let count = 0;
    const fn = throttle(() => count++, 50);

    fn();
    fn();
    fn();

    expect(count).toBe(1);
  });
});

describe('generateId', () => {
  it('generates unique IDs', () => {
    const id1 = generateId();
    const id2 = generateId();

    expect(id1).not.toBe(id2);
    expect(id1).toMatch(/^refast-[a-z0-9]+$/);
  });

  it('uses custom prefix', () => {
    const id = generateId('custom');
    expect(id).toMatch(/^custom-[a-z0-9]+$/);
  });
});

describe('isPlainObject', () => {
  it('returns true for plain objects', () => {
    expect(isPlainObject({})).toBe(true);
    expect(isPlainObject({ a: 1 })).toBe(true);
  });

  it('returns false for non-objects', () => {
    expect(isPlainObject(null)).toBe(false);
    expect(isPlainObject(undefined)).toBe(false);
    expect(isPlainObject('string')).toBe(false);
    expect(isPlainObject(123)).toBe(false);
    expect(isPlainObject([])).toBe(false);
  });
});

describe('deepMerge', () => {
  it('merges simple objects', () => {
    const result = deepMerge({ a: 1 }, { b: 2 });
    expect(result).toEqual({ a: 1, b: 2 });
  });

  it('merges nested objects', () => {
    const result = deepMerge(
      { a: { b: 1, c: 2 } },
      { a: { c: 3, d: 4 } }
    );
    expect(result).toEqual({ a: { b: 1, c: 3, d: 4 } });
  });

  it('does not mutate original objects', () => {
    const original = { a: { b: 1 } };
    deepMerge(original, { a: { c: 2 } });
    expect(original).toEqual({ a: { b: 1 } });
  });
});
