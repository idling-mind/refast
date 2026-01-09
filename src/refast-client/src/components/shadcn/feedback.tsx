import React from 'react';
import { cn } from '../../utils';

interface AlertProps {
  id?: string;
  className?: string;
  variant?: 'default' | 'destructive' | 'success' | 'warning' | 'info';
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Alert component - shadcn-styled alert.
 */
export function Alert({
  id,
  className,
  variant = 'default',
  children,
  'data-refast-id': dataRefastId,
}: AlertProps): React.ReactElement {
  const variantClasses = {
    default: 'bg-background text-foreground',
    destructive: 'border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive',
    success: 'border-green-500/50 text-green-700 dark:text-green-400 [&>svg]:text-green-500',
    warning: 'border-yellow-500/50 text-yellow-700 dark:text-yellow-400 [&>svg]:text-yellow-500',
    info: 'border-blue-500/50 text-blue-700 dark:text-blue-400 [&>svg]:text-blue-500',
  };

  return (
    <div
      id={id}
      role="alert"
      className={cn(
        'relative w-full rounded-lg border p-4',
        '[&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px]',
        '[&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground',
        variantClasses[variant],
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface AlertTitleProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * AlertTitle component - alert title text.
 */
export function AlertTitle({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: AlertTitleProps): React.ReactElement {
  return (
    <h5
      id={id}
      className={cn('mb-1 font-medium leading-none tracking-tight', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </h5>
  );
}

interface AlertDescriptionProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * AlertDescription component - alert description text.
 */
export function AlertDescription({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: AlertDescriptionProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('text-sm [&_p]:leading-relaxed', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

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
export function Badge({
  id,
  className,
  variant = 'default',
  children,
  'data-refast-id': dataRefastId,
}: BadgeProps): React.ReactElement {
  const variantClasses = {
    default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
    secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
    outline: 'text-foreground',
    success: 'border-transparent bg-green-500 text-white hover:bg-green-600',
    warning: 'border-transparent bg-yellow-500 text-white hover:bg-yellow-600',
  };

  return (
    <div
      id={id}
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors',
        'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
        variantClasses[variant],
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

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

const THEME_COLORS = ['primary', 'secondary', 'destructive', 'muted', 'accent', 'popover', 'card', 'background', 'foreground'];

/**
 * Progress component - progress bar.
 */
export function Progress({
  id,
  className,
  value = 0,
  max = 100,
  showValue = false,
  foregroundColor,
  trackColor,
  striped,
  'data-refast-id': dataRefastId,
}: ProgressProps): React.ReactElement {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const getColors = (color: string | undefined, defaultClass: string) => {
    if (!color) return { className: defaultClass, style: {} };
    if (THEME_COLORS.includes(color)) return { className: `bg-${color}`, style: {} };
    return { className: '', style: { backgroundColor: color } };
  };

  const trackProps = getColors(trackColor, 'bg-secondary');
  const indicatorProps = getColors(foregroundColor, 'bg-primary');

  const stripeStyle = striped ? {
    backgroundImage: 'linear-gradient(45deg,rgba(255,255,255,.15) 25%,transparent 25%,transparent 50%,rgba(255,255,255,.15) 50%,rgba(255,255,255,.15) 75%,transparent 75%,transparent)',
    backgroundSize: '1rem 1rem'
  } : {};
  
  const animatedClass = striped === 'animated' ? 'animate-stripes' : '';

  return (
    <div className={cn('relative', className)} data-refast-id={dataRefastId}>
      <div
        id={id}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        className={cn("relative h-4 w-full overflow-hidden rounded-full", trackProps.className)}
        style={trackProps.style}
      >
        <div
          className={cn("h-full transition-all flex-1", indicatorProps.className, animatedClass)}
          style={{ width: `${percentage}%`, ...indicatorProps.style, ...stripeStyle }}
        />
      </div>
      {showValue && (
        <span className="absolute right-0 top-0 -mt-6 text-sm text-muted-foreground">
          {Math.round(percentage)}%
        </span>
      )}
    </div>
  );
}

interface SpinnerProps {
  id?: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  'data-refast-id'?: string;
}

/**
 * Spinner component - loading spinner.
 */
export function Spinner({
  id,
  className,
  size = 'md',
  'data-refast-id': dataRefastId,
}: SpinnerProps): React.ReactElement {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  return (
    <div
      id={id}
      className={cn(
        'animate-spin rounded-full border-2 border-current border-t-transparent text-primary',
        sizeClasses[size],
        className
      )}
      role="status"
      aria-label="Loading"
      data-refast-id={dataRefastId}
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
}

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
export function Toast({
  id,
  className,
  variant = 'default',
  title,
  description,
  onClose,
  children,
  'data-refast-id': dataRefastId,
}: ToastProps): React.ReactElement {
  const variantClasses = {
    default: 'bg-background border',
    destructive: 'destructive group border-destructive bg-destructive text-destructive-foreground',
    success: 'bg-green-50 border-green-200 text-green-900',
  };

  return (
    <div
      id={id}
      className={cn(
        'group pointer-events-auto relative flex w-full items-center justify-between space-x-4 overflow-hidden rounded-md p-6 pr-8 shadow-lg transition-all',
        variantClasses[variant],
        className
      )}
      data-refast-id={dataRefastId}
    >
      <div className="grid gap-1">
        {title && <div className="text-sm font-semibold">{title}</div>}
        {description && <div className="text-sm opacity-90">{description}</div>}
        {children}
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="absolute right-2 top-2 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity hover:text-foreground focus:opacity-100 focus:outline-none focus:ring-2 group-hover:opacity-100"
        >
          <span className="sr-only">Close</span>
          <span aria-hidden="true">×</span>
        </button>
      )}
    </div>
  );
}

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
export function Skeleton({
  id,
  className,
  width,
  height,
  circle = false,
  'data-refast-id': dataRefastId,
}: SkeletonProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn(
        'animate-pulse bg-muted',
        circle ? 'rounded-full' : 'rounded-md',
        className
      )}
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
      }}
      data-refast-id={dataRefastId}
    />
  );
}
