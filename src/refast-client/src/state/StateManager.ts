import { useState, useCallback } from 'react';
import { ComponentTree, UpdateMessage, StateManagerState } from '../types';
import { propStore } from './PropStore';

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
  // If IDs don't match, replace entirely
  if (oldTree.id !== newTree.id) {
    return { tree: newTree, changed: true };
  }
  
  // If types don't match, replace entirely
  if (oldTree.type !== newTree.type) {
    return { tree: newTree, changed: true };
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
                window.dispatchEvent(
                  new CustomEvent('refast:force-value-sync', {
                    detail: { targetId: message.targetId, value: message.props.value },
                  })
                );
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
            window.history.pushState({}, '', message.path);
            // Trigger a custom event for navigation
            window.dispatchEvent(new CustomEvent('refast:navigate', { detail: { path: message.path } }));
          }
          break;

        case 'toast':
          // Trigger a custom event for toast notifications
          // Forward all toast options from the server (snake_case)
          if (typeof window !== 'undefined') {
            window.dispatchEvent(
              new CustomEvent('refast:toast', {
                detail: {
                  message: message.message,
                  variant: message.variant,
                  duration: message.duration,
                  description: message.description,
                  position: message.position,
                  dismissible: message.dismissible,
                  close_button: message.close_button,
                  invert: message.invert,
                  icon: message.icon,
                  action: message.action,
                  cancel: message.cancel,
                  id: message.id,
                },
              })
            );
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
              window.dispatchEvent(new CustomEvent('refast:refresh'));
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
 * prop store so that any store_prop binding on that component's onChange
 * reflects the server-set value.  This prevents stale values from being
 * sent with the next callback invocation.
 *
 * Only applies when the component's onChange is a StorePropRef
 * (i.e. `{ storeProp: "<key>" }`).
 */
function syncPropStoreForComponent(
  tree: ComponentTree,
  newValue: unknown,
): void {
  // Look for a store_prop binding on onChange (or on_change in snake_case)
  const onChange = tree.props?.on_change ?? tree.props?.onChange;
  if (
    onChange &&
    typeof onChange === 'object' &&
    'storeProp' in (onChange as Record<string, unknown>)
  ) {
    const storeProp = (onChange as Record<string, unknown>).storeProp;
    if (typeof storeProp === 'string') {
      propStore.set(storeProp, newValue);
    } else if (typeof storeProp === 'object' && storeProp !== null) {
      // Dict mapping — the "value" event key maps to a store key
      const mapping = storeProp as Record<string, string>;
      if ('value' in mapping) {
        propStore.set(mapping.value, newValue);
      }
    }
  }
}

/**
 * Apply an update operation to a component tree.
 */
function applyUpdate(
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
        // store_prop binding, keep the prop store in sync so that the
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

  // Recursively search children (default to empty array if undefined)
  const newChildren = (tree.children || [])
    .map((child) => {
      if (typeof child === 'string') return child;

      // Handle remove operation
      if (operation === 'remove' && child.id === targetId) {
        return null;
      }

      return applyUpdate(child, targetId, update, operation);
    })
    .filter((child): child is ComponentTree | string => child !== null);

  return {
    ...tree,
    children: newChildren,
  };
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

  return null;
}
