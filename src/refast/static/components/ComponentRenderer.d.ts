import { default as React } from 'react';
import { ComponentTree } from '../types';

interface ComponentRendererProps {
    tree: ComponentTree | string;
    onUpdate?: (id: string, component: ComponentTree) => void;
    [key: string]: any;
}
/**
 * Renders a component tree from Python backend.
 */
export declare const ComponentRenderer: React.ForwardRefExoticComponent<Omit<ComponentRendererProps, "ref"> & React.RefAttributes<HTMLElement>>;
export {};
