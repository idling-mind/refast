import React from 'react';
import { cva } from 'class-variance-authority';
import { cn } from '../../utils';
import { Icon } from './icon';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  icon?: string;
  iconPosition?: 'left' | 'right';
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  'data-refast-id'?: string;
  ref?: React.Ref<HTMLButtonElement>;
}

/**
 * Button component - shadcn/ui styled button with Tailwind CSS.
 */
export function Button({
  className,
  variant = 'default',
  size = 'md',
  loading = false,
  icon,
  iconPosition = 'left',
  children,
  'data-refast-id': dataRefastId,
  ref,
  ...props
}: ButtonProps) {
  const variantClasses = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
    link: 'text-primary underline-offset-4 hover:underline',
  };

  const sizeClasses: Record<string, string> = {
    xs: 'h-7 px-2 text-xs',
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4 py-2',
    lg: 'h-11 px-8 text-lg',
    xl: 'h-12 px-10 text-xl',
  };

  const iconSizeMap: Record<string, number> = { xs: 12, sm: 14, md: 16, lg: 20, xl: 24 };
  const iconSize = iconSizeMap[size ?? 'md'] ?? 16;
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
}
Button.displayName = 'Button';

interface IconButtonProps {
  id?: string;
  className?: string;
  icon: string;
  variant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'ghost';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  disabled?: boolean;
  onClick?: () => void;
  ariaLabel?: string;
  'data-refast-id'?: string;
  ref?: React.Ref<HTMLButtonElement>;
}

/**
 * IconButton component - button with icon.
 * Uses Lucide icons via the Icon component.
 */
export function IconButton({
  id,
  className,
  icon,
  variant = 'ghost',
  size = 'md',
  disabled = false,
  onClick,
  ariaLabel,
  'data-refast-id': dataRefastId,
  ref,
  ...props
}: IconButtonProps) {
  const variantClasses: Record<string, string> = {
    default: 'bg-primary text-primary-foreground hover:bg-primary/90',
    secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
    destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
    outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
    ghost: 'hover:bg-accent hover:text-accent-foreground',
  };

  const buttonSizeClasses: Record<string, string> = {
    xs: 'h-7 w-7',
    sm: 'h-9 w-9',
    md: 'h-10 w-10',
    lg: 'h-11 w-11',
    xl: 'h-12 w-12',
  };

  const iconSizeMap: Record<string, number> = { xs: 12, sm: 14, md: 16, lg: 20, xl: 24 };

  return (
    <button
      ref={ref}
      id={id}
      disabled={disabled}
      onClick={onClick}
      data-refast-id={dataRefastId}
      aria-label={ariaLabel || icon}
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        variantClasses[variant],
        buttonSizeClasses[size],
        className
      )}
      {...props}
    >
      <Icon name={icon} size={iconSizeMap[size] ?? 16} />
    </button>
  );
}
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


interface ButtonGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'horizontal' | 'vertical';
  children?: React.ReactNode;
  'aria-label'?: string;
  'aria-labelledby'?: string;
  'data-refast-id'?: string;
  ref?: React.Ref<HTMLDivElement>;
}

export function ButtonGroup({
  orientation = 'horizontal',
  className,
  children,
  'aria-label': ariaLabel,
  'aria-labelledby': ariaLabelledby,
  'data-refast-id': dataRefastId,
  ref,
  ...props
}: ButtonGroupProps) {
  return (
    <div
      ref={ref}
      role="group"
      aria-orientation={orientation}
      aria-label={ariaLabel}
      aria-labelledby={ariaLabelledby}
      data-refast-id={dataRefastId}
      className={cn(
        'inline-flex',
        // Premium rounding and overlapping borders
        orientation === 'vertical'
          ? 'flex-col [&>*]:rounded-none first:[&>*]:rounded-t-md last:[&>*]:rounded-b-md [&>*]:-mt-px first:[&>*]:mt-0'
          : 'flex-row [&>*]:rounded-none first:[&>*]:rounded-l-md last:[&>*]:rounded-r-md [&>*]:-ml-px first:[&>*]:ml-0',
        // Hover/focus ring z-indexing overlay fix
        '[&>*]:relative hover:[&>*]:z-10 focus-within:[&>*]:z-10',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
ButtonGroup.displayName = 'ButtonGroup';


interface ButtonGroupSeparatorProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'horizontal' | 'vertical';
  'data-refast-id'?: string;
  ref?: React.Ref<HTMLDivElement>;
}

export function ButtonGroupSeparator({
  orientation = 'vertical',
  className,
  'data-refast-id': dataRefastId,
  ref,
  ...props
}: ButtonGroupSeparatorProps) {
  return (
    <div
      ref={ref}
      data-refast-id={dataRefastId}
      className={cn(
        'shrink-0 bg-border',
        orientation === 'vertical' ? 'w-px h-auto self-stretch my-2' : 'h-px w-full mx-2',
        className
      )}
      {...props}
    />
  );
}
ButtonGroupSeparator.displayName = 'ButtonGroupSeparator';


interface ButtonGroupTextProps extends React.HTMLAttributes<HTMLSpanElement> {
  asChild?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
  ref?: React.Ref<HTMLSpanElement>;
}

export function ButtonGroupText({
  asChild = false,
  children,
  className,
  'data-refast-id': dataRefastId,
  ref,
  ...props
}: ButtonGroupTextProps) {
  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children, {
      ...props,
      'data-refast-id': dataRefastId,
      className: cn(
        'text-sm text-muted-foreground px-3 flex items-center justify-center',
        className,
        (children.props as any).className
      ),
    } as any);
  }

  return (
    <span
      ref={ref}
      data-refast-id={dataRefastId}
      className={cn(
        'text-sm text-muted-foreground px-3 flex items-center justify-center',
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
ButtonGroupText.displayName = 'ButtonGroupText';