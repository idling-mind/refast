import { default as React } from 'react';

interface AlertProps {
    id?: string;
    className?: string;
    variant?: 'default' | 'destructive' | 'success' | 'warning' | 'info';
    title?: string;
    message?: string;
    children?: React.ReactNode;
    dismissible?: boolean;
    onDismiss?: () => void;
    'data-refast-id'?: string;
}
/**
 * Alert component - shadcn-styled alert.
 */
export declare function Alert({ id, className, variant, title, message, children, dismissible, onDismiss, 'data-refast-id': dataRefastId, }: AlertProps): React.ReactElement | null;
interface AlertTitleProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * AlertTitle component - alert title text.
 */
export declare function AlertTitle({ id, className, children, 'data-refast-id': dataRefastId, }: AlertTitleProps): React.ReactElement;
interface AlertDescriptionProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * AlertDescription component - alert description text.
 */
export declare function AlertDescription({ id, className, children, 'data-refast-id': dataRefastId, }: AlertDescriptionProps): React.ReactElement;
interface BadgeProps {
    id?: string;
    className?: string;
    variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'success' | 'warning';
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Badge component - shadcn-styled badge.
 */
export declare function Badge({ id, className, variant, children, 'data-refast-id': dataRefastId, }: BadgeProps): React.ReactElement;
interface ProgressProps {
    id?: string;
    className?: string;
    value?: number;
    max?: number;
    showValue?: boolean;
    foregroundColor?: string;
    trackColor?: string;
    striped?: 'static' | 'animated' | null;
    'data-refast-id'?: string;
}
/**
 * Progress component - progress bar.
 */
export declare function Progress({ id, className, value, max, showValue, foregroundColor, trackColor, striped, 'data-refast-id': dataRefastId, }: ProgressProps): React.ReactElement;
interface SpinnerProps {
    id?: string;
    className?: string;
    size?: 'sm' | 'md' | 'lg';
    'data-refast-id'?: string;
}
/**
 * Spinner component - loading spinner.
 */
export declare function Spinner({ id, className, size, 'data-refast-id': dataRefastId, }: SpinnerProps): React.ReactElement;
interface ToastProps {
    id?: string;
    className?: string;
    variant?: 'default' | 'destructive' | 'success';
    title?: string;
    description?: string;
    onClose?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Toast component - notification toast.
 */
export declare function Toast({ id, className, variant, title, description, onClose, children, 'data-refast-id': dataRefastId, }: ToastProps): React.ReactElement;
interface SkeletonProps {
    id?: string;
    className?: string;
    width?: string | number;
    height?: string | number;
    circle?: boolean;
    'data-refast-id'?: string;
}
/**
 * Skeleton component - loading placeholder.
 */
export declare function Skeleton({ id, className, width, height, circle, 'data-refast-id': dataRefastId, }: SkeletonProps): React.ReactElement;
export {};
