import { default as React } from 'react';

interface RowProps {
    id?: string;
    className?: string;
    justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
    align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
    gap?: number | string;
    wrap?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Row component - horizontal flex container.
 */
export declare function Row({ id, className, justify, align, gap, wrap, children, 'data-refast-id': dataRefastId, }: RowProps): React.ReactElement;
interface ColumnProps {
    id?: string;
    className?: string;
    justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
    align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
    gap?: number | string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Column component - vertical flex container.
 */
export declare function Column({ id, className, justify, align, gap, children, 'data-refast-id': dataRefastId, }: ColumnProps): React.ReactElement;
interface StackProps {
    id?: string;
    className?: string;
    spacing?: number | string;
    direction?: 'vertical' | 'horizontal';
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Stack component - flex container with spacing.
 */
export declare function Stack({ id, className, spacing, direction, children, 'data-refast-id': dataRefastId, }: StackProps): React.ReactElement;
interface GridProps {
    id?: string;
    className?: string;
    columns?: number | string;
    rows?: number | string;
    gap?: number | string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Grid component - CSS grid container.
 */
export declare function Grid({ id, className, columns, rows, gap, children, 'data-refast-id': dataRefastId, }: GridProps): React.ReactElement;
interface FlexProps extends RowProps {
    direction?: 'row' | 'column';
}
/**
 * Flex component - configurable flex container.
 */
export declare function Flex({ direction, ...rest }: FlexProps): React.ReactElement;
interface CenterProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Center component - centers content horizontally and vertically.
 */
export declare function Center({ id, className, children, 'data-refast-id': dataRefastId, }: CenterProps): React.ReactElement;
interface SpacerProps {
    size?: number | string;
    'data-refast-id'?: string;
}
/**
 * Spacer component - flexible space element.
 */
export declare function Spacer({ size, 'data-refast-id': dataRefastId, }: SpacerProps): React.ReactElement;
interface DividerProps {
    id?: string;
    orientation?: 'horizontal' | 'vertical';
    className?: string;
    'data-refast-id'?: string;
}
/**
 * Divider component - visual separator.
 */
export declare function Divider({ id, orientation, className, 'data-refast-id': dataRefastId, }: DividerProps): React.ReactElement;
export {};
