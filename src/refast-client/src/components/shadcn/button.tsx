import React from 'react';
import { cn } from '../../utils';
import { Icon } from './icon';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  loading?: boolean;
  icon?: string;
  iconPosition?: 'left' | 'right';
  'data-refast-id'?: string;
}

/**
 * Button component - shadcn/ui styled button with Tailwind CSS.
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({
  className,
  variant = 'default',
  size = 'md',
  loading = false,
  icon,
  iconPosition = 'left',
  children,
  'data-refast-id': dataRefastId,
  ...props
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

  const iconSize = size === 'lg' ? 20 : size === 'sm' ? 14 : 16;
  const hasChildren = React.Children.count(children) > 0 || (typeof children === 'string' && children.length > 0);

  return (
    <button
      ref={ref}
      disabled={props.disabled || loading}
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        variantClasses[variant],
        sizeClasses[size],
        className
      )}
      data-refast-id={dataRefastId}
      {...props}
    >
      {loading && (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {!loading && icon && iconPosition === 'left' && (
        <Icon name={icon} size={iconSize} />
      )}
      {hasChildren && <span>{children}</span>}
      {!loading && icon && iconPosition === 'right' && (
        <Icon name={icon} size={iconSize} />
      )}
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
 * Uses Lucide icons via the Icon component.
 */
export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(({
  id,
  className,
  icon,
  variant = 'ghost',
  size = 'md',
  disabled = false,
  onClick,
  ariaLabel,
  'data-refast-id': dataRefastId,
}, ref) => {
  const iconSize = size === 'lg' ? 20 : size === 'sm' ? 14 : 16;

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
      aria-label={ariaLabel || icon}
    >
      <Icon name={icon} size={iconSize} />
    </Button>
  );
});
IconButton.displayName = 'IconButton';
