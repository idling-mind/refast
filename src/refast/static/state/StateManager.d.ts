import { ComponentTree, UpdateMessage } from '../types';

/**
 * Hook for managing component tree and app state.
 */
export declare function useStateManager(initialTree?: ComponentTree): {
    componentTree: ComponentTree | null;
    appState: Record<string, unknown>;
    setComponentTree: (tree: ComponentTree) => void;
    updateComponent: (id: string, update: ComponentTree | null, operation?: string) => void;
    setAppState: (newState: Record<string, unknown>) => void;
    getAppState: <T = unknown>(key: string, defaultValue?: T) => T;
    handleUpdate: (message: UpdateMessage) => void;
};
/**
 * Find a component by ID in the tree.
 */
export declare function findComponent(tree: ComponentTree, id: string): ComponentTree | null;
/**
 * Get the path to a component in the tree.
 */
export declare function getComponentPath(tree: ComponentTree, id: string, path?: string[]): string[] | null;
