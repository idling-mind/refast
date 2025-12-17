import React from 'react';
import { cn } from '../utils';

interface ContainerProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Container component - basic div wrapper.
 */
export function Container({
  id,
  className,
  style,
  children,
  'data-refast-id': dataRefastId,
}: ContainerProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('', className)}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface TextProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Text component - basic span wrapper.
 */
export function Text({
  id,
  className,
  style,
  children,
  'data-refast-id': dataRefastId,
}: TextProps): React.ReactElement {
  return (
    <span
      id={id}
      className={cn('', className)}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
    </span>
  );
}

interface FragmentProps {
  children?: React.ReactNode;
}

/**
 * Fragment component - renders children without wrapper.
 */
export function Fragment({ children }: FragmentProps): React.ReactElement {
  return <>{children}</>;
}
