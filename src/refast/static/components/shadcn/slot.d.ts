import { default as React } from 'react';

interface SlotProps {
    id?: string;
    name?: string;
    fallback?: React.ReactNode;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Slot component - placeholder for dynamic content.
 */
export declare function Slot({ id, name, fallback, children, 'data-refast-id': dataRefastId, }: SlotProps): React.ReactElement;
export {};
