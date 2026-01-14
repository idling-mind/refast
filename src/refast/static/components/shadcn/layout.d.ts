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
    wrap?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Column component - vertical flex container.
 */
export declare function Column({ id, className, justify, align, gap, wrap, children, 'data-refast-id': dataRefastId, }: ColumnProps): React.ReactElement;
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
export {};
