import { useState, useCallback } from 'react';
import { ComponentTree, UpdateMessage, StateManagerState } from '../types';
import { propStore } from './PropStore';
import { refastBus } from '../utils/eventBus';

/**
 * Deep equality check for component props.
 */
function propsEqual(
  props1: Record<string, unknown> | undefined,
  props2: Record<string, unknown> | undefined
): boolean {
  if (props1 === props2) return true;
  if (!props1 || !props2) return false;
  
  const keys1 = Object.keys(props1);
  const keys2 = Object.keys(props2);
  
  if (keys1.length !== keys2.length) return false;
  
  for (const key of keys1) {
    const val1 = props1[key];
    const val2 = props2[key];
    
    // Skip callback comparison (they have unique IDs each render)
    if (key === 'onClick' || key === 'onChange' || key === 'onSubmit' || key === 'onInput') {
      // Compare callback IDs if both are objects with callbackId
      if (typeof val1 === 'object' && val1 !== null && 'callbackId' in val1 &&
          typeof val2 === 'object' && val2 !== null && 'callbackId' in val2) {
        // Callbacks are considered equal if they exist (ID will differ)
        continue;
      }
    }
    
    if (typeof val1 === 'object' && typeof val2 === 'object') {
      if (JSON.stringify(val1) !== JSON.stringify(val2)) return false;
    } else if (val1 !== val2) {
      return false;
    }
  }
  
  return true;
}

/**
 * Check if two children arrays are equal.
 */
function childrenEqual(
  children1: (ComponentTree | string)[],
  children2: (ComponentTree | string)[]
): boolean {
  if (children1.length !== children2.length) return false;
  
  for (let i = 0; i < children1.length; i++) {
    const c1 = children1[i];
    const c2 = children2[i];
    
    if (typeof c1 === 'string' && typeof c2 === 'string') {
      if (c1 !== c2) return false;
    } else if (typeof c1 !== 'string' && typeof c2 !== 'string') {
      if (!componentsEqual(c1, c2)) return false;
    } else {
      return false;
    }
  }
  
  return true;
}

/**
 * Check if two components are structurally equal.
 */
function componentsEqual(comp1: ComponentTree, comp2: ComponentTree): boolean {
  if (comp1.type !== comp2.type) return false;
  if (comp1.id !== comp2.id) return false;
  if (!propsEqual(comp1.props, comp2.props)) return false;
  if (!childrenEqual(comp1.children || [], comp2.children || [])) return false;
  return true;
}

/**
 * Diff two component trees and apply minimal updates.
 * Returns the new tree with only changed parts replaced.
 */
function diffAndMerge(
  oldTree: ComponentTree,
  newTree: ComponentTree
): { tree: ComponentTree; changed: boolean } {
  // If types don't match, replace entirely regardless of ID
  if (oldTree.type !== newTree.type) {
    return { tree: newTree, changed: true };
  }

  // If IDs don't match but types match, the server re-rendered with a new auto-generated
  // ID (e.g. from uuid4() on every page render). Preserve the OLD id so React keeps the
  // same component instance alive (same key) and internal state (like upload progress) is
  // not lost. This mirrors React's own positional reconciliation when no explicit key is set.
  if (oldTree.id !== newTree.id) {
    return diffAndMerge(oldTree, { ...newTree, id: oldTree.id });
  }
  
  // Check if props changed
  const propsChanged = !propsEqual(oldTree.props, newTree.props);
  
  // Recursively diff children
  let childrenChanged = false;
  const newChildren: (ComponentTree | string)[] = [];
  
  // Handle different children lengths (default to empty array if undefined)
  const oldChildren = oldTree.children || [];
  const newChildrenArr = newTree.children || [];
  const maxLen = Math.max(oldChildren.length, newChildrenArr.length);
  
  for (let i = 0; i < maxLen; i++) {
    const oldChild = oldChildren[i];
    const newChild = newChildrenArr[i];
    
    if (newChild === undefined) {
      // Child was removed
      childrenChanged = true;
      continue;
    }
    
    if (oldChild === undefined) {
      // Child was added
      childrenChanged = true;
      newChildren.push(newChild);
      continue;
    }
    
    if (typeof newChild === 'string') {
      if (oldChild !== newChild) {
        childrenChanged = true;
      }
      newChildren.push(newChild);
    } else if (typeof oldChild === 'string') {
      // Type changed from string to component
      childrenChanged = true;
      newChildren.push(newChild);
    } else {
      // Both are components, recursively diff
      const result = diffAndMerge(oldChild, newChild);
      if (result.changed) {
        childrenChanged = true;
      }
      newChildren.push(result.tree);
    }
  }
  
  // If nothing changed, return the old tree (preserves reference)
  if (!propsChanged && !childrenChanged) {
    return { tree: oldTree, changed: false };
  }
  
  // Return merged tree
  return {
    tree: {
      ...newTree,
      // Keep old props reference if unchanged
      props: propsChanged ? newTree.props : oldTree.props,
      children: newChildren,
    },
    changed: true,
  };
}

/**
 * Hook for managing component tree and app state.
 */
export function useStateManager(initialTree?: ComponentTree) {
  const [state, setState] = useState<StateManagerState>({
    componentTree: initialTree || null,
    appState: {},
  });

  /**
   * Update the entire component tree.
   */
  const setComponentTree = useCallback((tree: ComponentTree) => {
    setState((s) => ({ ...s, componentTree: tree }));
  }, []);

  /**
   * Update a specific component by ID.
   */
  const updateComponent = useCallback(
    (id: string, update: ComponentTree | null, operation: string = 'replace') => {
      setState((s) => {
        if (!s.componentTree) return s;

        const newTree = applyUpdate(s.componentTree, id, update, operation);
        return { ...s, componentTree: newTree };
      });
    },
    []
  );

  /**
   * Update app state.
   */
  const setAppState = useCallback((newState: Record<string, unknown>) => {
    setState((s) => ({
      ...s,
      appState: { ...s.appState, ...newState },
    }));
  }, []);

  /**
   * Get a value from app state.
   */
  const getAppState = useCallback(
    <T = unknown>(key: string, defaultValue?: T): T => {
      return (state.appState[key] as T) ?? (defaultValue as T);
    },
    [state.appState]
  );

  /**
   * Handle an update message from the backend.
   */
  const handleUpdate = useCallback(
    (message: UpdateMessage) => {
      switch (message.type) {
        case 'update':
          if (message.targetId && message.operation) {
            // Build the update object based on operation type
            let updateObj: ComponentTree | null = message.component || null;
            
            // For update_children and update_props, the data comes in separate fields
            if (message.operation === 'update_children' && message.children) {
              updateObj = { type: '', id: '', props: {}, children: message.children } as ComponentTree;
            } else if (message.operation === 'update_props' && (message.props || message.children)) {
              updateObj = { type: '', id: '', props: message.props || {}, children: message.children || [] } as ComponentTree;
              // Flag whether children were explicitly provided in the message
              (updateObj as any).__hasChildren = 'children' in message;

              // Notify Input/Textarea/Select components to force-sync their
              // local value state.  This handles the edge case where the prop
              // value string hasn't changed (e.g. "" → "") but the local
              // value has drifted due to user typing.
              if (message.props && 'value' in message.props && message.targetId) {
                refastBus.emit('refast:force-value-sync', {
                  targetId: message.targetId,
                  value: message.props.value,
                });
              }
            } else if (message.operation === 'append_prop' && message.propName !== undefined) {
              // For append_prop, we pass propName and value via props
              updateObj = { type: '', id: '', props: { __propName: message.propName, __value: message.value }, children: [] } as ComponentTree;
            }
            
            updateComponent(
              message.targetId,
              updateObj,
              message.operation
            );
          }
          break;

        case 'state_update':
          if (message.state) {
            setAppState(message.state);
          }
          break;

        case 'navigate':
          if (message.path && typeof window !== 'undefined') {
            if (message.redirect) {
              if (message.target) {
                window.open(message.path, message.target);
              } else {
                window.location.href = message.path;
              }
            } else {
              window.history.pushState({}, '', message.path);
              // Trigger a typed event for navigation
              refastBus.emit('refast:navigate', { path: message.path });
              // Handle scroll after navigation
              if (message.scroll_to != null) {
                const behavior = (message.scroll_behavior as ScrollBehavior | undefined) ?? 'instant';
                if (message.scroll_to === 'top') {
                  window.scrollTo({ top: 0, behavior });
                } else {
                  document.getElementById(message.scroll_to)?.scrollIntoView({ behavior });
                }
              }
            }
          }
          break;

        case 'toast':
          // Dispatch a typed toast event consumed by ToastManager.
          if (typeof window !== 'undefined') {
            refastBus.emit('refast:toast', {
              message: message.message,
              variant: message.variant as 'default' | 'success' | 'error' | 'destructive' | 'warning' | 'info' | 'loading' | undefined,
              duration: message.duration,
              description: message.description,
              position: message.position as 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center' | undefined,
              dismissible: message.dismissible,
              close_button: message.close_button,
              invert: message.invert,
              icon: message.icon,
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              action: message.action as any,
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              cancel: message.cancel as any,
              id: message.id,
              component: message.component,
            });
          }
          break;

        case 'refresh':
          // Handle page refresh with optional component tree
          if (typeof window !== 'undefined') {
            if (message.component) {
              // Server sent the rendered component tree directly
              // Use diff-and-merge to only update changed parts
              setState((s) => {
                if (!s.componentTree) {
                  // No existing tree, just set the new one
                  return { ...s, componentTree: message.component! };
                }
                
                // Diff and merge to minimize re-renders
                const { tree, changed } = diffAndMerge(s.componentTree, message.component!);
                
                if (!changed) {
                  // Nothing changed, return same state to prevent re-render
                  return s;
                }
                
                return { ...s, componentTree: tree };
              });
            } else {
              // Fallback: trigger a page refresh via HTTP request
              refastBus.emit('refast:refresh', {});
            }
          }
          break;
      }
    },
    [updateComponent, setAppState]
  );

  return {
    componentTree: state.componentTree,
    appState: state.appState,
    setComponentTree,
    updateComponent,
    setAppState,
    getAppState,
    handleUpdate,
  };
}

/**
 * When the server updates a component's value via update_props, sync the
 * prop store so that any save_prop binding on that component's onChange
 * reflects the server-set value.  This prevents stale values from being
 * sent with the next callback invocation.
 *
 * Only applies when the component's onChange is a SavePropRef
 * (i.e. `{ saveProp: "<key>" }`).
 */
function syncPropStoreForComponent(
  tree: ComponentTree,
  newValue: unknown,
): void {
  // Look for a save_prop binding on onChange (or on_change in snake_case)
  const onChange = tree.props?.on_change ?? tree.props?.onChange;
  if (
    onChange &&
    typeof onChange === 'object' &&
    'saveProp' in (onChange as Record<string, unknown>)
  ) {
    const saveProp = (onChange as Record<string, unknown>).saveProp;
    if (typeof saveProp === 'string') {
      propStore.set(saveProp, newValue);
    } else if (typeof saveProp === 'object' && saveProp !== null) {
      // Dict mapping — the "value" event key maps to a store key
      const mapping = saveProp as Record<string, string>;
      if ('value' in mapping) {
        propStore.set(mapping.value, newValue);
      }
    }
  }
}

/**
 * Recursively apply an update to any ComponentTree objects found within a
 * prop value (plain object, array, or ComponentTree-shaped object).
 * Returns { value, changed } – `changed` is true only if a nested component
 * was actually found and updated, preserving reference equality otherwise.
 */
function applyUpdateInPropValue(
  val: unknown,
  targetId: string,
  update: ComponentTree | null,
  operation: string
): { value: unknown; changed: boolean } {
  if (val === null || val === undefined || typeof val !== 'object') {
    return { value: val, changed: false };
  }

  if (Array.isArray(val)) {
    let changed = false;
    const newArr: unknown[] = [];
    for (const item of val as unknown[]) {
      // Handle remove: skip the item that directly matches the target
      if (
        operation === 'remove' &&
        item !== null &&
        typeof item === 'object' &&
        !Array.isArray(item)
      ) {
        const obj = item as Record<string, unknown>;
        if (typeof obj.type === 'string' && obj.id === targetId) {
          changed = true;
          continue;
        }
      }
      const r = applyUpdateInPropValue(item, targetId, update, operation);
      if (r.changed) changed = true;
      newArr.push(r.value);
    }
    return { value: changed ? newArr : val, changed };
  }

  const obj = val as Record<string, unknown>;
  // If this looks like a ComponentTree (has `type` string + `id`), recurse via applyUpdate
  if (typeof obj.type === 'string' && 'id' in obj) {
    const updated = applyUpdate(obj as unknown as ComponentTree, targetId, update, operation);
    return { value: updated, changed: updated !== (obj as unknown) };
  }

  // Generic plain object: search its values
  let changed = false;
  const newObj: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(obj)) {
    const r = applyUpdateInPropValue(v, targetId, update, operation);
    if (r.changed) changed = true;
    newObj[k] = r.value;
  }
  return { value: changed ? newObj : val, changed };
}

/**
 * Apply an update operation to a component tree.
 */
export function applyUpdate(
  tree: ComponentTree,
  targetId: string,
  update: ComponentTree | null,
  operation: string
): ComponentTree {
  // Check if this is the target
  if (tree.id === targetId) {
    switch (operation) {
      case 'replace':
        return update || tree;

      case 'update_props': {
        // When the server updates the value of a component that has a
        // save_prop binding, keep the prop store in sync so that the
        // next callback invocation sees the server-set value instead of
        // a stale user-typed value.  This is one-way: server → store.
        const newProps = update?.props || {};
        if ('value' in newProps) {
          syncPropStoreForComponent(tree, newProps.value);
        }
        const result: ComponentTree = {
          ...tree,
          props: { ...tree.props, ...newProps },
        };
        // If the update explicitly includes children, replace them
        if ((update as any)?.__hasChildren) {
          result.children = update?.children || [];
        }
        return result;
      }

      case 'update_children':
        return {
          ...tree,
          children: update?.children || [],
        };

      case 'remove':
        // Can't remove self, handled by parent
        return tree;

      case 'append':
        if (update) {
          return {
            ...tree,
            children: [...(tree.children || []), update],
          };
        }
        return tree;

      case 'prepend':
        if (update) {
          return {
            ...tree,
            children: [update, ...(tree.children || [])],
          };
        }
        return tree;

      case 'append_prop': {
        // Append to a specific prop (string concatenation or array append)
        const propName = update?.props?.__propName as string;
        const value = update?.props?.__value;
        if (!propName) return tree;

        const currentValue = tree.props[propName];
        let newValue: unknown;

        if (typeof currentValue === 'string' && typeof value === 'string') {
          // String concatenation
          newValue = currentValue + value;
        } else if (Array.isArray(currentValue)) {
          // Array append - if value is array, extend; otherwise push
          if (Array.isArray(value)) {
            newValue = [...currentValue, ...value];
          } else {
            newValue = [...currentValue, value];
          }
        } else if (currentValue === undefined || currentValue === null) {
          // Prop doesn't exist yet - initialize it
          if (typeof value === 'string') {
            newValue = value;
          } else if (Array.isArray(value)) {
            newValue = value;
          } else {
            newValue = [value];
          }
        } else {
          // Fallback: try to concatenate or just replace
          newValue = value;
        }

        return {
          ...tree,
          props: { ...tree.props, [propName]: newValue },
        };
      }

      default:
        return tree;
    }
  }

  // Recursively search children (default to empty array if undefined).
  // Preserve references when no descendant changed so React can skip
  // re-rendering sibling subtrees.
  const currentChildren = tree.children || [];
  let hasChanges = false;
  const newChildren: (ComponentTree | string)[] = [];

  for (const child of currentChildren) {
    if (typeof child === 'string') {
      newChildren.push(child);
      continue;
    }

    // Handle remove operation for direct children
    if (operation === 'remove' && child.id === targetId) {
      hasChanges = true;
      continue;
    }

    const updatedChild = applyUpdate(child, targetId, update, operation);
    if (updatedChild !== child) {
      hasChanges = true;
    }
    newChildren.push(updatedChild);
  }

  if (hasChanges) {
    return {
      ...tree,
      children: newChildren,
    };
  }

  // Also search through props values for embedded ComponentTree objects
  // (e.g. component instances stored in DataTable's `data` prop).
  const currentProps = tree.props as Record<string, unknown> | undefined;
  if (currentProps) {
    let propsChanged = false;
    const newProps: Record<string, unknown> = {};
    for (const [key, val] of Object.entries(currentProps)) {
      const r = applyUpdateInPropValue(val, targetId, update, operation);
      if (r.changed) propsChanged = true;
      newProps[key] = r.value;
    }
    if (propsChanged) {
      return { ...tree, props: newProps as ComponentTree['props'] };
    }
  }

  return tree;
}

/**
 * Find a component by ID in the tree.
 */
export function findComponent(
  tree: ComponentTree,
  id: string
): ComponentTree | null {
  if (tree.id === id) {
    return tree;
  }

  for (const child of tree.children || []) {
    if (typeof child !== 'string') {
      const found = findComponent(child, id);
      if (found) {
        return found;
      }
    }
  }

  // Also search through props values for embedded ComponentTree objects
  for (const val of Object.values((tree.props as Record<string, unknown>) || {})) {
    const found = findComponentInPropValue(val, id);
    if (found) return found;
  }

  return null;
}

function findComponentInPropValue(val: unknown, id: string): ComponentTree | null {
  if (val === null || val === undefined || typeof val !== 'object') return null;
  if (Array.isArray(val)) {
    for (const item of val as unknown[]) {
      const found = findComponentInPropValue(item, id);
      if (found) return found;
    }
    return null;
  }
  const obj = val as Record<string, unknown>;
  if (typeof obj.type === 'string' && 'id' in obj) {
    return findComponent(obj as unknown as ComponentTree, id);
  }
  for (const v of Object.values(obj)) {
    const found = findComponentInPropValue(v, id);
    if (found) return found;
  }
  return null;
}

/**
 * Get the path to a component in the tree.
 */
export function getComponentPath(
  tree: ComponentTree,
  id: string,
  path: string[] = []
): string[] | null {
  if (tree.id === id) {
    return [...path, id];
  }

  for (const child of tree.children || []) {
    if (typeof child !== 'string') {
      const found = getComponentPath(child, id, [...path, tree.id]);
      if (found) {
        return found;
      }
    }
  }

  // Also search through props values for embedded ComponentTree objects
  for (const val of Object.values((tree.props as Record<string, unknown>) || {})) {
    const found = getComponentPathInPropValue(val, id, [...path, tree.id]);
    if (found) return found;
  }

  return null;
}

function getComponentPathInPropValue(
  val: unknown,
  id: string,
  path: string[]
): string[] | null {
  if (val === null || val === undefined || typeof val !== 'object') return null;
  if (Array.isArray(val)) {
    for (const item of val as unknown[]) {
      const found = getComponentPathInPropValue(item, id, path);
      if (found) return found;
    }
    return null;
  }
  const obj = val as Record<string, unknown>;
  if (typeof obj.type === 'string' && 'id' in obj) {
    return getComponentPath(obj as unknown as ComponentTree, id, path);
  }
  for (const v of Object.values(obj)) {
    const found = getComponentPathInPropValue(v, id, path);
    if (found) return found;
  }
  return null;
}
