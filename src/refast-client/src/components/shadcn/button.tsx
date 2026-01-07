import React from 'react';
import { cn } from '../../utils';

interface ButtonProps {
  id?: string;
  className?: string;
  variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Button component - shadcn/ui styled button with Tailwind CSS.
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({
  id,
  className,
  variant = 'default',
  size = 'md',
  disabled = false,
  loading = false,
  type = 'button',
  onClick,
  children,
  'data-refast-id': dataRefastId,
}, ref) => {
  const variantClasses = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
    link: 'text-primary underline-offset-4 hover:underline',
  };

  const sizeClasses = {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-11 px-8 text-lg',
    icon: 'h-10 w-10',
  };

  return (
    <button
      ref={ref}
      id={id}
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      data-refast-id={dataRefastId}
    >
      {loading && (
        <span className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  );
});
Button.displayName = 'Button';

interface IconButtonProps {
  id?: string;
  className?: string;
  icon: string;
  variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  ariaLabel?: string;
  'data-refast-id'?: string;
}

/**
 * IconButton component - button with icon.
 */
export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(({
  id,
  className,
  icon,
  variant = 'ghost',
  disabled = false,
  onClick,
  ariaLabel,
  'data-refast-id': dataRefastId,
}, ref) => {
  return (
    <Button
      ref={ref}
      id={id}
      className={className}
      variant={variant}
      size="icon"
      disabled={disabled}
      onClick={onClick}
      data-refast-id={dataRefastId}
    >
      <span className="sr-only">{ariaLabel || icon}</span>
      <span aria-hidden="true">{icon}</span>
    </Button>
  );
});
IconButton.displayName = 'IconButton';
