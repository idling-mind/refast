import React from 'react';
import { cva } from 'class-variance-authority';
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

export const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive:
          "bg-destructive text-white hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60",
        outline:
          "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground dark:bg-input/30 dark:border-input dark:hover:bg-input/50",
        secondary:
          "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost:
          "hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/50",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3",
        sm: "h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5",
        lg: "h-10 rounded-md px-6 has-[>svg]:px-4",
        icon: "size-9",
        "icon-sm": "size-8",
        "icon-lg": "size-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)