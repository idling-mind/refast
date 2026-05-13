/**
 * KeyboardShortcut component
 *
 * An invisible component that captures keyboard shortcuts and fires server
 * callbacks.  Multiple instances may coexist on the same page; a global
 * registry handles priority-based dispatch and optional event bubbling.
 */

import { useEffect, useRef } from 'react';
import { useEventManager } from '../../events/EventManager';
import { CallbackProp } from './types';
import { isCallbackRef } from '../../utils/actionExecutor';

// ---------------------------------------------------------------------------
// Global shortcut registry
// ---------------------------------------------------------------------------

interface ShortcutEntry {
  componentId: string;
  priority: number;
  bubble: boolean;
  preventDefault: boolean;
  handler: () => void;
}

/** normalised combo string → sorted (descending priority) list of entries */
const registry = new Map<string, ShortcutEntry[]>();

/** Insert or update a single entry in the registry, keeping entries sorted. */
function registerEntry(combo: string, entry: ShortcutEntry): void {
  if (!registry.has(combo)) {
    registry.set(combo, []);
  }
  const list = registry.get(combo)!;
  // Remove any previous entry for the same component + combo
  const idx = list.findIndex((e) => e.componentId === entry.componentId);
  if (idx !== -1) list.splice(idx, 1);
  list.push(entry);
  // Sort descending so index 0 is highest priority
  list.sort((a, b) => b.priority - a.priority);
}

function unregisterComponent(componentId: string): void {
  for (const [combo, list] of registry.entries()) {
    const filtered = list.filter((e) => e.componentId !== componentId);
    if (filtered.length === 0) {
      registry.delete(combo);
    } else {
      registry.set(combo, filtered);
    }
  }
}

// ---------------------------------------------------------------------------
// Key combo normalisation
// ---------------------------------------------------------------------------

/** Normalise a key combo string to a canonical form. */
function normaliseCombo(raw: string): string {
  const parts = raw
    .toLowerCase()
    .split('+')
    .map((p) => p.trim())
    .filter(Boolean);

  const modifiers = new Set<string>();
  const keys: string[] = [];

  for (const part of parts) {
    if (part === 'ctrl' || part === 'control') {
      modifiers.add('ctrl');
    } else if (part === 'shift') {
      modifiers.add('shift');
    } else if (part === 'alt') {
      modifiers.add('alt');
    } else if (part === 'meta' || part === 'cmd' || part === 'command' || part === 'win') {
      modifiers.add('meta');
    } else {
      keys.push(part);
    }
  }

  const modOrder = ['ctrl', 'shift', 'alt', 'meta'].filter((m) => modifiers.has(m));
  return [...modOrder, ...keys].join('+');
}

/** Build a normalised combo string from a keyboard event. */
function comboFromEvent(e: KeyboardEvent): string {
  const modifiers: string[] = [];
  if (e.ctrlKey) modifiers.push('ctrl');
  if (e.shiftKey) modifiers.push('shift');
  if (e.altKey) modifiers.push('alt');
  if (e.metaKey) modifiers.push('meta');

  // Normalise the key: use e.key, lowercased, with spaces replaced
  const key = e.key.toLowerCase().replace(' ', 'space');
  return [...modifiers, key].join('+');
}

// ---------------------------------------------------------------------------
// Document-level listener (single, shared)
// ---------------------------------------------------------------------------

let listenerActive = false;

function ensureListener(): void {
  if (listenerActive) return;
  listenerActive = true;

  document.addEventListener(
    'keydown',
    (e: KeyboardEvent) => {
      // Ignore events from input/textarea/contenteditable elements unless the
      // shortcut uses Ctrl, Alt, or Meta – those are intentional global bindings.
      const target = e.target as HTMLElement | null;
      const isEditable =
        target instanceof HTMLInputElement ||
        target instanceof HTMLTextAreaElement ||
        target?.isContentEditable;

      const hasGlobalModifier = e.ctrlKey || e.altKey || e.metaKey;

      if (isEditable && !hasGlobalModifier) return;

      const combo = comboFromEvent(e);
      const entries = registry.get(combo);
      if (!entries || entries.length === 0) return;

      let defaultPrevented = false;

      for (const entry of entries) {
        if (entry.preventDefault && !defaultPrevented) {
          e.preventDefault();
          defaultPrevented = true;
        }

        entry.handler();

        if (!entry.bubble) break; // stop propagating after this handler
      }
    },
    true, // capture phase so we run before any React synthetic events
  );
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export interface ShortcutDefinition {
  [combo: string]: CallbackProp | null | undefined;
}

export interface KeyboardShortcutProps {
  id?: string;
  shortcuts: ShortcutDefinition;
  priority?: number;
  bubble?: boolean;
  preventDefault?: boolean;
  enabled?: boolean;
}

/**
 * Invisible component that registers keyboard shortcuts and fires server
 * callbacks.  Renders nothing to the DOM.
 */
export function KeyboardShortcut({
  id,
  shortcuts,
  priority = 0,
  bubble = false,
  preventDefault = true,
  enabled = true,
}: KeyboardShortcutProps): null {
  const eventManager = useEventManager();
  // Stable ref so the keydown handler always uses the latest props
  const propsRef = useRef({ shortcuts, priority, bubble, preventDefault, enabled, id });
  propsRef.current = { shortcuts, priority, bubble, preventDefault, enabled, id };

  useEffect(() => {
    ensureListener();

    const componentId = id ?? crypto.randomUUID();

    if (!enabled) {
      unregisterComponent(componentId);
      return;
    }

    // Register all combos for this component
    for (const [rawCombo, cbRef] of Object.entries(shortcuts)) {
      if (!cbRef || !isCallbackRef(cbRef)) continue;

      const combo = normaliseCombo(rawCombo);
      const callbackId = cbRef.callbackId;
      const boundArgs = cbRef.boundArgs ?? {};

      registerEntry(combo, {
        componentId,
        priority,
        bubble,
        preventDefault: preventDefault,
        handler: () => {
          eventManager.invokeCallback(callbackId, boundArgs, {
            shortcut: rawCombo,
            combo,
          });
        },
      });
    }

    return () => {
      unregisterComponent(componentId);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, enabled, priority, bubble, preventDefault, JSON.stringify(shortcuts)]);

  return null;
}
