import React from 'react';
import { cn } from '../../utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Card component - shadcn-styled card container.
 */
export function Card({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
  ...props
}: CardProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn(
        'rounded-lg border bg-card text-card-foreground shadow-sm',
        className
      )}
      data-refast-id={dataRefastId}
      {...props}
    >
      {children}
    </div>
  );
}

interface CardHeaderProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * CardHeader component - card header section.
 */
export function CardHeader({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CardHeaderProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('flex flex-col space-y-1.5 p-6', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface CardTitleProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * CardTitle component - card title text.
 */
export function CardTitle({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CardTitleProps): React.ReactElement {
  return (
    <h3
      id={id}
      className={cn(
        'text-2xl font-semibold leading-none tracking-tight',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </h3>
  );
}

interface CardDescriptionProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * CardDescription component - card description text.
 */
export function CardDescription({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CardDescriptionProps): React.ReactElement {
  return (
    <p
      id={id}
      className={cn('text-sm text-muted-foreground', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </p>
  );
}

interface CardContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * CardContent component - card content section.
 */
export function CardContent({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CardContentProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('p-6 pt-0', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface CardFooterProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * CardFooter component - card footer section.
 */
export function CardFooter({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CardFooterProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('flex items-center p-6 pt-0', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}
