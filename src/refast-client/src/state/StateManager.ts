import { useState, useCallback } from 'react';
import { ComponentTree, UpdateMessage, StateManagerState } from '../types';

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
            updateComponent(
              message.targetId,
              message.component || null,
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
          if (typeof window !== 'undefined') {
            window.dispatchEvent(
              new CustomEvent('refast:toast', {
                detail: {
                  message: message.message,
                  variant: message.variant,
                },
              })
            );
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

      case 'update_props':
        return {
          ...tree,
          props: { ...tree.props, ...(update?.props || {}) },
        };

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
            children: [...tree.children, update],
          };
        }
        return tree;

      case 'prepend':
        if (update) {
          return {
            ...tree,
            children: [update, ...tree.children],
          };
        }
        return tree;

      default:
        return tree;
    }
  }

  // Recursively search children
  const newChildren = tree.children
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

  for (const child of tree.children) {
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

  for (const child of tree.children) {
    if (typeof child !== 'string') {
      const found = getComponentPath(child, id, [...path, tree.id]);
      if (found) {
        return found;
      }
    }
  }

  return null;
}
