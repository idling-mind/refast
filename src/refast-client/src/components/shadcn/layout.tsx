import React from 'react';
import { cn } from '../../utils';

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
export function Row({
  id,
  className,
  justify = 'start',
  align = 'start',
  gap = 0,
  wrap = false,
  children,
  'data-refast-id': dataRefastId,
}: RowProps): React.ReactElement {
  const justifyClass = {
    start: 'justify-start',
    end: 'justify-end',
    center: 'justify-center',
    between: 'justify-between',
    around: 'justify-around',
    evenly: 'justify-evenly',
  }[justify];

  const alignClass = {
    start: 'items-start',
    end: 'items-end',
    center: 'items-center',
    stretch: 'items-stretch',
    baseline: 'items-baseline',
  }[align];

  return (
    <div
      id={id}
      className={cn(
        'flex flex-row',
        justifyClass,
        alignClass,
        wrap && 'flex-wrap',
        className
      )}
      style={{ gap: typeof gap === 'number' ? `${gap * 0.25}rem` : gap }}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface ColumnProps {
  id?: string;
  className?: string;
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
  align?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
  gap?: number | string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Column component - vertical flex container.
 */
export function Column({
  id,
  className,
  justify = 'start',
  align = 'stretch',
  gap = 0,
  children,
  'data-refast-id': dataRefastId,
}: ColumnProps): React.ReactElement {
  const justifyClass = {
    start: 'justify-start',
    end: 'justify-end',
    center: 'justify-center',
    between: 'justify-between',
    around: 'justify-around',
    evenly: 'justify-evenly',
  }[justify];

  const alignClass = {
    start: 'items-start',
    end: 'items-end',
    center: 'items-center',
    stretch: 'items-stretch',
    baseline: 'items-baseline',
  }[align];

  return (
    <div
      id={id}
      className={cn('flex flex-col', justifyClass, alignClass, className)}
      style={{ gap: typeof gap === 'number' ? `${gap * 0.25}rem` : gap }}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface StackProps {
  id?: string;
  className?: string;
  spacing?: number | string;
  direction?: 'vertical' | 'horizontal';
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Stack component - flex container with spacing.
 */
export function Stack({
  id,
  className,
  spacing = 4,
  direction = 'vertical',
  children,
  'data-refast-id': dataRefastId,
}: StackProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn(
        'flex',
        direction === 'vertical' ? 'flex-col' : 'flex-row',
        className
      )}
      style={{
        gap: typeof spacing === 'number' ? `${spacing * 0.25}rem` : spacing,
      }}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

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
export function Grid({
  id,
  className,
  columns = 1,
  rows,
  gap = 0,
  children,
  'data-refast-id': dataRefastId,
}: GridProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('grid', className)}
      style={{
        gridTemplateColumns:
          typeof columns === 'number' ? `repeat(${columns}, 1fr)` : columns,
        gridTemplateRows: rows
          ? typeof rows === 'number'
            ? `repeat(${rows}, 1fr)`
            : rows
          : undefined,
        gap: typeof gap === 'number' ? `${gap * 0.25}rem` : gap,
      }}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface FlexProps extends RowProps {
  direction?: 'row' | 'column';
}

/**
 * Flex component - configurable flex container.
 */
export function Flex({
  direction = 'row',
  ...rest
}: FlexProps): React.ReactElement {
  if (direction === 'column') {
    return <Column {...rest} />;
  }
  return <Row {...rest} />;
}

interface CenterProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Center component - centers content horizontally and vertically.
 */
export function Center({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CenterProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('flex items-center justify-center', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SpacerProps {
  size?: number | string;
  'data-refast-id'?: string;
}

/**
 * Spacer component - flexible space element.
 */
export function Spacer({
  size,
  'data-refast-id': dataRefastId,
}: SpacerProps): React.ReactElement {
  return (
    <div
      className="flex-grow"
      style={size ? { flexGrow: 0, flexBasis: typeof size === 'number' ? `${size * 0.25}rem` : size } : undefined}
      data-refast-id={dataRefastId}
    />
  );
}

interface DividerProps {
  id?: string;
  orientation?: 'horizontal' | 'vertical';
  className?: string;
  'data-refast-id'?: string;
}

/**
 * Divider component - visual separator.
 */
export function Divider({
  id,
  orientation = 'horizontal',
  className,
  'data-refast-id': dataRefastId,
}: DividerProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn(
        'bg-border',
        orientation === 'horizontal' ? 'h-px w-full' : 'w-px h-full',
        className
      )}
      data-refast-id={dataRefastId}
    />
  );
}
