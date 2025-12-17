import React from 'react';
import { cn } from '../../utils';

interface HeadingProps {
  id?: string;
  className?: string;
  level?: 1 | 2 | 3 | 4 | 5 | 6;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Heading component - typography heading.
 */
export function Heading({
  id,
  className,
  level = 1,
  children,
  'data-refast-id': dataRefastId,
}: HeadingProps): React.ReactElement {
  const sizeClasses = {
    1: 'scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl',
    2: 'scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0',
    3: 'scroll-m-20 text-2xl font-semibold tracking-tight',
    4: 'scroll-m-20 text-xl font-semibold tracking-tight',
    5: 'scroll-m-20 text-lg font-semibold tracking-tight',
    6: 'scroll-m-20 text-base font-semibold tracking-tight',
  };

  const Tag = `h${level}` as keyof JSX.IntrinsicElements;

  return (
    <Tag
      id={id}
      className={cn(sizeClasses[level], className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </Tag>
  );
}

interface ParagraphProps {
  id?: string;
  className?: string;
  lead?: boolean;
  muted?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Paragraph component - typography paragraph.
 */
export function Paragraph({
  id,
  className,
  lead = false,
  muted = false,
  children,
  'data-refast-id': dataRefastId,
}: ParagraphProps): React.ReactElement {
  return (
    <p
      id={id}
      className={cn(
        'leading-7',
        lead && 'text-xl text-muted-foreground',
        muted && 'text-sm text-muted-foreground',
        !lead && !muted && '[&:not(:first-child)]:mt-6',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </p>
  );
}

interface LinkProps {
  id?: string;
  className?: string;
  href?: string;
  target?: '_blank' | '_self' | '_parent' | '_top';
  external?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Link component - typography link.
 */
export function Link({
  id,
  className,
  href = '#',
  target,
  external = false,
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: LinkProps): React.ReactElement {
  return (
    <a
      id={id}
      href={href}
      target={external ? '_blank' : target}
      rel={external ? 'noopener noreferrer' : undefined}
      onClick={onClick}
      className={cn(
        'font-medium text-primary underline underline-offset-4 hover:text-primary/80',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </a>
  );
}

interface CodeProps {
  id?: string;
  className?: string;
  inline?: boolean;
  language?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Code component - typography code.
 */
export function Code({
  id,
  className,
  inline = true,
  language,
  children,
  'data-refast-id': dataRefastId,
}: CodeProps): React.ReactElement {
  if (inline) {
    return (
      <code
        id={id}
        className={cn(
          'relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold',
          className
        )}
        data-refast-id={dataRefastId}
        data-language={language}
      >
        {children}
      </code>
    );
  }

  return (
    <pre
      id={id}
      className={cn(
        'mb-4 mt-6 overflow-x-auto rounded-lg border bg-black py-4',
        className
      )}
      data-refast-id={dataRefastId}
      data-language={language}
    >
      <code className="relative rounded bg-transparent px-4 py-[0.2rem] font-mono text-sm text-white">
        {children}
      </code>
    </pre>
  );
}

interface BlockQuoteProps {
  id?: string;
  className?: string;
  cite?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * BlockQuote component - typography blockquote.
 */
export function BlockQuote({
  id,
  className,
  cite,
  children,
  'data-refast-id': dataRefastId,
}: BlockQuoteProps): React.ReactElement {
  return (
    <blockquote
      id={id}
      cite={cite}
      className={cn(
        'mt-6 border-l-2 pl-6 italic text-muted-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </blockquote>
  );
}

interface ListProps {
  id?: string;
  className?: string;
  ordered?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * List component - typography list.
 */
export function List({
  id,
  className,
  ordered = false,
  children,
  'data-refast-id': dataRefastId,
}: ListProps): React.ReactElement {
  const Tag = ordered ? 'ol' : 'ul';

  return (
    <Tag
      id={id}
      className={cn(
        'my-6 ml-6',
        ordered ? 'list-decimal' : 'list-disc',
        '[&>li]:mt-2',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </Tag>
  );
}

interface ListItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * ListItem component - typography list item.
 */
export function ListItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: ListItemProps): React.ReactElement {
  return (
    <li id={id} className={cn('', className)} data-refast-id={dataRefastId}>
      {children}
    </li>
  );
}

interface LabelProps {
  id?: string;
  className?: string;
  htmlFor?: string;
  required?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Label component - typography label.
 */
export function Label({
  id,
  className,
  htmlFor,
  required = false,
  children,
  'data-refast-id': dataRefastId,
}: LabelProps): React.ReactElement {
  return (
    <label
      id={id}
      htmlFor={htmlFor}
      className={cn(
        'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
      {required && <span className="ml-1 text-destructive">*</span>}
    </label>
  );
}
