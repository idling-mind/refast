import React from 'react';
import { cn } from '../../utils';

interface TableProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Table component - shadcn-styled table.
 */
export function Table({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: TableProps): React.ReactElement {
  return (
    <div className="relative w-full overflow-auto" data-refast-id={dataRefastId}>
      <table
        id={id}
        className={cn('w-full caption-bottom text-sm', className)}
      >
        {children}
      </table>
    </div>
  );
}

interface TableHeaderProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * TableHeader component - table header section.
 */
export function TableHeader({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: TableHeaderProps): React.ReactElement {
  return (
    <thead
      id={id}
      className={cn('[&_tr]:border-b', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </thead>
  );
}

interface TableBodyProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * TableBody component - table body section.
 */
export function TableBody({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: TableBodyProps): React.ReactElement {
  return (
    <tbody
      id={id}
      className={cn('[&_tr:last-child]:border-0', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </tbody>
  );
}

interface TableRowProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * TableRow component - table row.
 */
export function TableRow({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: TableRowProps): React.ReactElement {
  return (
    <tr
      id={id}
      className={cn(
        'border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </tr>
  );
}

interface TableHeadProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * TableHead component - table header cell.
 */
export function TableHead({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: TableHeadProps): React.ReactElement {
  return (
    <th
      id={id}
      className={cn(
        'h-12 px-4 text-left align-middle font-medium text-muted-foreground',
        '[&:has([role=checkbox])]:pr-0',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </th>
  );
}

interface TableCellProps {
  id?: string;
  className?: string;
  colSpan?: number;
  rowSpan?: number;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * TableCell component - table data cell.
 */
export function TableCell({
  id,
  className,
  colSpan,
  rowSpan,
  children,
  'data-refast-id': dataRefastId,
}: TableCellProps): React.ReactElement {
  return (
    <td
      id={id}
      colSpan={colSpan}
      rowSpan={rowSpan}
      className={cn('p-4 align-middle [&:has([role=checkbox])]:pr-0', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </td>
  );
}

interface AvatarProps {
  id?: string;
  className?: string;
  src?: string;
  alt?: string;
  fallback?: string;
  size?: 'sm' | 'md' | 'lg';
  'data-refast-id'?: string;
}

/**
 * Avatar component - user avatar.
 */
export function Avatar({
  id,
  className,
  src,
  alt = '',
  fallback,
  size = 'md',
  'data-refast-id': dataRefastId,
}: AvatarProps): React.ReactElement {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12',
  };

  const [imageError, setImageError] = React.useState(false);

  return (
    <span
      id={id}
      className={cn(
        'relative flex shrink-0 overflow-hidden rounded-full',
        sizeClasses[size],
        className
      )}
      data-refast-id={dataRefastId}
    >
      {src && !imageError ? (
        <img
          src={src}
          alt={alt}
          className="aspect-square h-full w-full"
          onError={() => setImageError(true)}
        />
      ) : (
        <span className="flex h-full w-full items-center justify-center rounded-full bg-muted text-sm font-medium uppercase">
          {fallback || alt?.charAt(0) || '?'}
        </span>
      )}
    </span>
  );
}

interface ImageProps {
  id?: string;
  className?: string;
  src: string;
  alt?: string;
  width?: number | string;
  height?: number | string;
  objectFit?: 'contain' | 'cover' | 'fill' | 'none' | 'scale-down';
  fallback?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Image component - responsive image.
 */
export function Image({
  id,
  className,
  src,
  alt = '',
  width,
  height,
  objectFit = 'cover',
  fallback,
  'data-refast-id': dataRefastId,
}: ImageProps): React.ReactElement {
  const [error, setError] = React.useState(false);

  if (error && fallback) {
    return <>{fallback}</>;
  }

  return (
    <img
      id={id}
      src={src}
      alt={alt}
      className={cn('rounded-md', className)}
      style={{
        width: typeof width === 'number' ? `${width}px` : width,
        height: typeof height === 'number' ? `${height}px` : height,
        objectFit,
      }}
      onError={() => setError(true)}
      data-refast-id={dataRefastId}
    />
  );
}

interface TooltipProps {
  id?: string;
  className?: string;
  content: string;
  side?: 'top' | 'right' | 'bottom' | 'left';
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Tooltip component - hover tooltip.
 */
export function Tooltip({
  id,
  className,
  content,
  side = 'top',
  children,
  'data-refast-id': dataRefastId,
}: TooltipProps): React.ReactElement {
  const [isVisible, setIsVisible] = React.useState(false);

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
  };

  return (
    <div
      id={id}
      className={cn('relative inline-block', className)}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
      data-refast-id={dataRefastId}
    >
      {children}
      {isVisible && (
        <div
          className={cn(
            'absolute z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95',
            positionClasses[side]
          )}
        >
          {content}
        </div>
      )}
    </div>
  );
}

// Tabs Context
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (value: string) => void;
}

const TabsContext = React.createContext<TabsContextValue | null>(null);

interface TabsProps {
  id?: string;
  className?: string;
  defaultValue?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Tabs component - tab container.
 * Children should be TabItem components that will be rendered in a tabbed interface.
 */
export function Tabs({
  id,
  className,
  defaultValue = '',
  value,
  onValueChange,
  children,
  'data-refast-id': dataRefastId,
}: TabsProps): React.ReactElement {
  const [activeTab, setActiveTab] = React.useState(value || defaultValue);

  // Extract tab information from children by looking at their rendered output
  const childArray = React.Children.toArray(children);
  
  // Collect tab metadata from children
  const tabMeta: Array<{ value: string; label: string; disabled: boolean }> = [];
  
  React.Children.forEach(children, (child) => {
    if (React.isValidElement(child)) {
      const props = child.props as Record<string, unknown>;
      // TabItem passes value and label as props
      if (props.value !== undefined) {
        tabMeta.push({
          value: String(props.value || ''),
          label: String(props.label || props.value || ''),
          disabled: Boolean(props.disabled),
        });
      }
    }
  });

  // Initialize activeTab if not set
  React.useEffect(() => {
    if (!activeTab && tabMeta.length > 0) {
      setActiveTab(tabMeta[0].value);
    }
  }, [activeTab, tabMeta]);

  const handleTabChange = (tabValue: string) => {
    setActiveTab(tabValue);
    onValueChange?.(tabValue);
  };

  const contextValue = React.useMemo(
    () => ({ activeTab, setActiveTab: handleTabChange }),
    [activeTab]
  );

  return (
    <TabsContext.Provider value={contextValue}>
      <div id={id} className={cn('w-full', className)} data-refast-id={dataRefastId}>
        {/* Tab buttons */}
        <div className="inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground">
          {tabMeta.map((tab) => {
            const isActive = activeTab === tab.value;
            return (
              <button
                key={tab.value}
                type="button"
                onClick={() => !tab.disabled && handleTabChange(tab.value)}
                disabled={tab.disabled}
                className={cn(
                  'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
                  isActive
                    ? 'bg-background text-foreground shadow-sm'
                    : 'hover:bg-background/50'
                )}
              >
                {tab.label}
              </button>
            );
          })}
        </div>
        {/* Tab content - rendered children handle visibility via context */}
        <div className="mt-2">
          {childArray.map((child, index) => {
            if (React.isValidElement(child)) {
              const props = child.props as Record<string, unknown>;
              const tabValue = String(props.value || '');
              // Only show the active tab's content
              if (tabValue !== activeTab) {
                return null;
              }
              return <React.Fragment key={tabValue || index}>{child}</React.Fragment>;
            }
            return null;
          })}
        </div>
      </div>
    </TabsContext.Provider>
  );
}

interface TabItemProps {
  id?: string;
  className?: string;
  value: string;
  label: string;
  disabled?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * TabItem component - individual tab panel.
 * The visibility is controlled by the parent Tabs component.
 */
export function TabItem({
  id,
  className,
  value,
  label,
  disabled = false,
  children,
  'data-refast-id': dataRefastId,
}: TabItemProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2', className)}
      role="tabpanel"
      data-value={value}
      data-label={label}
      data-disabled={disabled}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}
