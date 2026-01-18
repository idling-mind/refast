import { default as React } from 'react';

import * as TooltipPrimitive from '@radix-ui/react-tooltip';
interface AccordionProps {
    id?: string;
    className?: string;
    type?: 'single' | 'multiple';
    collapsible?: boolean;
    defaultValue?: string | string[];
    value?: string | string[];
    onValueChange?: (value: string | string[]) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Accordion component - expandable/collapsible sections.
 */
export declare function Accordion({ id, className, type, collapsible, defaultValue, value, onValueChange, children, 'data-refast-id': dataRefastId, }: AccordionProps): React.ReactElement;
interface AccordionItemProps {
    id?: string;
    className?: string;
    value: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * AccordionItem component - individual accordion section.
 */
export declare function AccordionItem({ id, className, value, children, 'data-refast-id': dataRefastId, }: AccordionItemProps): React.ReactElement;
interface AccordionTriggerProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * AccordionTrigger component - clickable header to toggle section.
 */
export declare const AccordionTrigger: React.ForwardRefExoticComponent<AccordionTriggerProps & React.RefAttributes<HTMLButtonElement>>;
interface AccordionContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * AccordionContent component - content revealed when section is open.
 */
export declare const AccordionContent: React.ForwardRefExoticComponent<AccordionContentProps & React.RefAttributes<HTMLDivElement>>;
interface TableProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Table component - shadcn-styled table.
 */
export declare function Table({ id, className, children, 'data-refast-id': dataRefastId, }: TableProps): React.ReactElement;
interface TableHeaderProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * TableHeader component - table header section.
 */
export declare function TableHeader({ id, className, children, 'data-refast-id': dataRefastId, }: TableHeaderProps): React.ReactElement;
interface TableBodyProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * TableBody component - table body section.
 */
export declare function TableBody({ id, className, children, 'data-refast-id': dataRefastId, }: TableBodyProps): React.ReactElement;
interface TableRowProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * TableRow component - table row.
 */
export declare function TableRow({ id, className, children, 'data-refast-id': dataRefastId, }: TableRowProps): React.ReactElement;
interface TableHeadProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * TableHead component - table header cell.
 */
export declare function TableHead({ id, className, children, 'data-refast-id': dataRefastId, }: TableHeadProps): React.ReactElement;
interface TableCellProps {
    id?: string;
    className?: string;
    colSpan?: number;
    rowSpan?: number;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * TableCell component - table data cell.
 */
export declare function TableCell({ id, className, colSpan, rowSpan, children, 'data-refast-id': dataRefastId, }: TableCellProps): React.ReactElement;
interface AvatarProps {
    id?: string;
    className?: string;
    src?: string;
    alt?: string;
    fallback?: string;
    size?: 'sm' | 'md' | 'lg';
    'data-refast-id'?: string;
}
/**
 * Avatar component - user avatar.
 */
export declare function Avatar({ id, className, src, alt, fallback, size, 'data-refast-id': dataRefastId, }: AvatarProps): React.ReactElement;
interface ImageProps {
    id?: string;
    className?: string;
    src: string;
    alt?: string;
    width?: number | string;
    height?: number | string;
    objectFit?: 'contain' | 'cover' | 'fill' | 'none' | 'scale-down';
    loading?: boolean;
    fallbackSrc?: string;
    fallback?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Image component - responsive image with loading state and fallback support.
 */
export declare function Image({ id, className, src, alt, width, height, objectFit, loading, fallbackSrc, fallback, 'data-refast-id': dataRefastId, }: ImageProps): React.ReactElement;
interface TooltipProps {
    id?: string;
    className?: string;
    content: string;
    side?: 'top' | 'right' | 'bottom' | 'left';
    sideOffset?: number;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Tooltip component - hover tooltip.
 */
export declare function Tooltip({ id, className, content, side, sideOffset, children, 'data-refast-id': dataRefastId, }: TooltipProps): React.ReactElement;
export declare const TooltipTrigger: React.ForwardRefExoticComponent<TooltipPrimitive.TooltipTriggerProps & React.RefAttributes<HTMLButtonElement>>;
export declare const TooltipContent: React.ForwardRefExoticComponent<TooltipPrimitive.TooltipContentProps & React.RefAttributes<HTMLDivElement>>;
export declare const TooltipProvider: React.FC<TooltipPrimitive.TooltipProviderProps>;
interface TabsProps {
    id?: string;
    className?: string;
    defaultValue?: string;
    value?: string;
    onValueChange?: (value: string) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Tabs component - tab container.
 * Children should be TabItem components that will be rendered in a tabbed interface.
 */
export declare function Tabs({ id, className, defaultValue, value, onValueChange, children, 'data-refast-id': dataRefastId, }: TabsProps): React.ReactElement;
interface TabItemProps {
    id?: string;
    className?: string;
    value: string;
    label: string;
    disabled?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * TabItem component - individual tab panel.
 * The visibility is controlled by the parent Tabs component.
 */
export declare function TabItem({ id, className, value, label, disabled, children, 'data-refast-id': dataRefastId, }: TabItemProps): React.ReactElement;
export {};
