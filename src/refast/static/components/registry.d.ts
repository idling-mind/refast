import { default as React } from 'react';

type ComponentType = React.ComponentType<any>;
/**
 * Registry of all available components.
 */
declare class ComponentRegistry {
    private components;
    register(name: string, component: ComponentType): void;
    get(name: string): ComponentType | undefined;
    has(name: string): boolean;
    list(): string[];
    /**
     * Register multiple components at once.
     */
    registerAll(components: Record<string, ComponentType>): void;
}
export declare const componentRegistry: ComponentRegistry;
export {};
