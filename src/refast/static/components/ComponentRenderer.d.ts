import { default as React } from 'react';
import { ComponentTree } from '../types';

interface ComponentRendererProps {
    tree: ComponentTree | string;
    onUpdate?: (id: string, component: ComponentTree) => void;
}
/**
 * Renders a component tree from Python backend.
 */
export declare function ComponentRenderer({ tree, onUpdate }: ComponentRendererProps): React.ReactElement | null;
export {};
