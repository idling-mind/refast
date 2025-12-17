import { default as React } from 'react';

interface ContainerProps {
    id?: string;
    className?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Container component - basic div wrapper.
 */
export declare function Container({ id, className, style, children, 'data-refast-id': dataRefastId, }: ContainerProps): React.ReactElement;
interface TextProps {
    id?: string;
    className?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Text component - basic span wrapper.
 */
export declare function Text({ id, className, style, children, 'data-refast-id': dataRefastId, }: TextProps): React.ReactElement;
interface FragmentProps {
    children?: React.ReactNode;
}
/**
 * Fragment component - renders children without wrapper.
 */
export declare function Fragment({ children }: FragmentProps): React.ReactElement;
export {};
