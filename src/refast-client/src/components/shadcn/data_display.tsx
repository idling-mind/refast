import React from 'react';
import * as TooltipPrimitive from '@radix-ui/react-tooltip';
import * as AccordionPrimitive from '@radix-ui/react-accordion';
import { ChevronDown } from 'lucide-react';
import { cn } from '../../utils';

// ============================================================================
// Accordion Components
// ============================================================================

interface AccordionProps {
  id?: string;
  className?: string;
  type?: 'single' | 'multiple';
  collapsible?: boolean;
  defaultValue?: string | string[];
  value?: string | string[];
  onValueChange?: (value: string | string[]) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Accordion component - expandable/collapsible sections.
 */
export function Accordion({
  id,
  className,
  type = 'single',
  collapsible = true,
  defaultValue,
  value,
  onValueChange,
  children,
  'data-refast-id': dataRefastId,
}: AccordionProps): React.ReactElement {
  // Handle controlled vs uncontrolled based on type
  if (type === 'single') {
    return (
      <AccordionPrimitive.Root
        id={id}
        type="single"
        collapsible={collapsible}
        defaultValue={defaultValue as string | undefined}
        value={value as string | undefined}
        onValueChange={onValueChange as ((value: string) => void) | undefined}
        className={cn('w-full', className)}
        data-refast-id={dataRefastId}
      >
        {children}
      </AccordionPrimitive.Root>
    );
  }

  return (
    <AccordionPrimitive.Root
      id={id}
      type="multiple"
      defaultValue={defaultValue as string[] | undefined}
      value={value as string[] | undefined}
      onValueChange={onValueChange as ((value: string[]) => void) | undefined}
      className={cn('w-full', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </AccordionPrimitive.Root>
  );
}

interface AccordionItemProps {
  id?: string;
  className?: string;
  value: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * AccordionItem component - individual accordion section.
 */
export function AccordionItem({
  id,
  className,
  value,
  children,
  'data-refast-id': dataRefastId,
}: AccordionItemProps): React.ReactElement {
  return (
    <AccordionPrimitive.Item
      id={id}
      value={value}
      className={cn('border-b', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </AccordionPrimitive.Item>
  );
}

interface AccordionTriggerProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * AccordionTrigger component - clickable header to toggle section.
 */
export const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  AccordionTriggerProps
>(({ id, className, children, 'data-refast-id': dataRefastId }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      id={id}
      className={cn(
        'flex flex-1 items-center justify-between py-4 font-medium transition-all hover:underline [&[data-state=open]>svg]:rotate-180',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
      <ChevronDown className="h-4 w-4 shrink-0 transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
));
AccordionTrigger.displayName = 'AccordionTrigger';

interface AccordionContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * AccordionContent component - content revealed when section is open.
 */
export const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  AccordionContentProps
>(({ id, className, children, 'data-refast-id': dataRefastId }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    id={id}
    className="overflow-hidden text-sm transition-all data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
    data-refast-id={dataRefastId}
  >
    <div className={cn('pb-4 pt-0', className)}>{children}</div>
  </AccordionPrimitive.Content>
));
AccordionContent.displayName = 'AccordionContent';

// ============================================================================
// Table Components
// ============================================================================

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

// ============================================================================
// DataTable Component
// ============================================================================

interface DataTableColumn {
  /** Data key used to look up values in each row. */
  key: string;
  /** Column header label. */
  header: string;
  /** Per-column sortable override. Falls back to the component-level `sortable` prop. */
  sortable?: boolean;
  /** CSS column width (e.g. "200px", "20%"). */
  width?: string;
  /** Text alignment – "left" (default), "center", or "right". */
  align?: 'left' | 'center' | 'right';
}

interface DataTableProps {
  id?: string;
  className?: string;
  columns: DataTableColumn[];
  data: Record<string, unknown>[];
  sortable?: boolean;
  filterable?: boolean;
  paginated?: boolean;
  pageSize?: number;
  loading?: boolean;
  emptyMessage?: string;
  currentPage?: number;
  onRowClick?: (row: Record<string, unknown>) => void;
  onSortChange?: (sort: { key: string; direction: 'asc' | 'desc' } | null) => void;
  onFilterChange?: (filter: { value: string }) => void;
  onPageChange?: (page: { page: number }) => void;
  'data-refast-id'?: string;
}

/**
 * DataTable component – high-level table with sorting, filtering, and pagination.
 */
export function DataTable({
  id,
  className,
  columns = [],
  data = [],
  sortable = true,
  filterable = true,
  paginated = true,
  pageSize = 10,
  loading = false,
  emptyMessage = 'No data available',
  currentPage: controlledPage,
  onRowClick,
  onSortChange,
  onFilterChange,
  onPageChange,
  'data-refast-id': dataRefastId,
}: DataTableProps): React.ReactElement {
  const [filterValue, setFilterValue] = React.useState('');
  const [sortState, setSortState] = React.useState<{
    key: string;
    direction: 'asc' | 'desc';
  } | null>(null);
  const [internalPage, setInternalPage] = React.useState(1);

  // Use controlled page when provided, otherwise internal state
  const currentPage = controlledPage !== undefined ? controlledPage : internalPage;

  // Client-side filter
  const filteredData = React.useMemo(() => {
    if (!filterValue) return data;
    const lower = filterValue.toLowerCase();
    return data.filter((row) =>
      Object.values(row).some((val) => String(val ?? '').toLowerCase().includes(lower))
    );
  }, [data, filterValue]);

  // Client-side sort
  const sortedData = React.useMemo(() => {
    if (!sortState) return filteredData;
    return [...filteredData].sort((a, b) => {
      const aVal = String(a[sortState.key] ?? '');
      const bVal = String(b[sortState.key] ?? '');
      const cmp = aVal.localeCompare(bVal);
      return sortState.direction === 'asc' ? cmp : -cmp;
    });
  }, [filteredData, sortState]);

  // Pagination
  const totalPages = paginated ? Math.max(1, Math.ceil(sortedData.length / pageSize)) : 1;
  const paginatedData = paginated
    ? sortedData.slice((currentPage - 1) * pageSize, currentPage * pageSize)
    : sortedData;

  const handleSort = (col: DataTableColumn) => {
    const colSortable = col.sortable !== undefined ? col.sortable : sortable;
    if (!colSortable) return;

    let newSort: { key: string; direction: 'asc' | 'desc' } | null;
    if (!sortState || sortState.key !== col.key) {
      newSort = { key: col.key, direction: 'asc' };
    } else if (sortState.direction === 'asc') {
      newSort = { key: col.key, direction: 'desc' };
    } else {
      newSort = null;
    }
    setSortState(newSort);
    onSortChange?.(newSort);
  };

  const handleFilter = (value: string) => {
    setFilterValue(value);
    if (controlledPage === undefined) setInternalPage(1);
    onFilterChange?.({ value });
  };

  const handlePageChange = (newPage: number) => {
    if (controlledPage === undefined) setInternalPage(newPage);
    onPageChange?.({ page: newPage });
  };

  // Build visible page numbers (up to 5 around current)
  const visiblePages = React.useMemo(() => {
    const pages: number[] = [];
    const count = Math.min(totalPages, 5);
    let start: number;
    if (currentPage <= 3 || totalPages <= 5) {
      start = 1;
    } else if (currentPage >= totalPages - 2) {
      start = totalPages - 4;
    } else {
      start = currentPage - 2;
    }
    for (let i = 0; i < count; i++) pages.push(start + i);
    return pages;
  }, [totalPages, currentPage]);

  return (
    <div id={id} className={cn('w-full space-y-4', className)} data-refast-id={dataRefastId}>
      {/* Filter input */}
      {filterable && (
        <input
          type="text"
          placeholder="Filter..."
          value={filterValue}
          onChange={(e) => handleFilter(e.target.value)}
          className="flex h-9 w-full max-w-sm rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        />
      )}

      {/* Table */}
      <div className="relative w-full overflow-auto rounded-md border">
        {loading && (
          <div className="absolute inset-0 z-10 flex items-center justify-center rounded-md bg-background/60">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          </div>
        )}
        <table className="w-full caption-bottom text-sm">
          <thead className="[&_tr]:border-b">
            <tr className="border-b transition-colors">
              {columns.map((col) => {
                const colSortable = col.sortable !== undefined ? col.sortable : sortable;
                const isActive = sortState?.key === col.key;
                return (
                  <th
                    key={col.key}
                    style={col.width ? { width: col.width } : undefined}
                    className={cn(
                      'h-10 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0',
                      col.align === 'center' && 'text-center',
                      col.align === 'right' && 'text-right',
                      colSortable && 'cursor-pointer select-none hover:text-foreground'
                    )}
                    onClick={() => handleSort(col)}
                  >
                    <span className="inline-flex items-center gap-1">
                      {col.header}
                      {colSortable && (
                        <span className="text-xs opacity-60">
                          {isActive ? (sortState?.direction === 'asc' ? '↑' : '↓') : '↕'}
                        </span>
                      )}
                    </span>
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="[&_tr:last-child]:border-0">
            {paginatedData.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length || 1}
                  className="py-8 text-center text-sm text-muted-foreground"
                >
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              paginatedData.map((row, rowIndex) => (
                <tr
                  key={rowIndex}
                  className={cn(
                    'border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted',
                    onRowClick && 'cursor-pointer'
                  )}
                  onClick={() => onRowClick?.(row)}
                >
                  {columns.map((col) => (
                    <td
                      key={col.key}
                      className={cn(
                        'p-4 align-middle',
                        col.align === 'center' && 'text-center',
                        col.align === 'right' && 'text-right'
                      )}
                    >
                      {String(row[col.key] ?? '')}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {paginated && totalPages > 1 && (
        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <span>
            Showing {(currentPage - 1) * pageSize + 1}–
            {Math.min(currentPage * pageSize, sortedData.length)} of {sortedData.length}
          </span>
          <div className="flex gap-1">
            <button
              type="button"
              disabled={currentPage <= 1}
              onClick={() => handlePageChange(currentPage - 1)}
              className="inline-flex h-8 items-center justify-center rounded-md border px-3 text-sm disabled:opacity-50 hover:bg-accent"
            >
              Previous
            </button>
            {visiblePages.map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => handlePageChange(p)}
                className={cn(
                  'inline-flex h-8 w-8 items-center justify-center rounded-md border text-sm',
                  currentPage === p
                    ? 'border-primary bg-primary text-primary-foreground'
                    : 'hover:bg-accent'
                )}
              >
                {p}
              </button>
            ))}
            <button
              type="button"
              disabled={currentPage >= totalPages}
              onClick={() => handlePageChange(currentPage + 1)}
              className="inline-flex h-8 items-center justify-center rounded-md border px-3 text-sm disabled:opacity-50 hover:bg-accent"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
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
  loading?: boolean;
  fallbackSrc?: string;
  fallback?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Image component - responsive image with loading state and fallback support.
 */
export function Image({
  id,
  className,
  src,
  alt = '',
  width,
  height,
  objectFit = 'cover',
  loading = false,
  fallbackSrc,
  fallback,
  'data-refast-id': dataRefastId,
}: ImageProps): React.ReactElement {
  const [isLoading, setIsLoading] = React.useState(loading);
  const [error, setError] = React.useState(false);
  const [currentSrc, setCurrentSrc] = React.useState(src);

  // Reset state when src changes
  React.useEffect(() => {
    setCurrentSrc(src);
    setError(false);
    if (loading) {
      setIsLoading(true);
    }
  }, [src, loading]);

  const handleLoad = () => {
    setIsLoading(false);
  };

  const handleError = () => {
    if (fallbackSrc && currentSrc !== fallbackSrc) {
      setCurrentSrc(fallbackSrc);
      setError(false);
    } else {
      setError(true);
      setIsLoading(false);
    }
  };

  const imageStyle = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
    objectFit,
  };

  // Show custom fallback React node if provided and error occurred
  if (error && fallback) {
    return <>{fallback}</>;
  }

  // Show a placeholder when error and no fallback
  if (error && !fallbackSrc) {
    return (
      <div
        id={id}
        className={cn(
          'flex items-center justify-center rounded-md bg-muted text-muted-foreground',
          className
        )}
        style={imageStyle}
        data-refast-id={dataRefastId}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="opacity-50"
        >
          <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
          <circle cx="9" cy="9" r="2" />
          <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
        </svg>
      </div>
    );
  }

  return (
    <div className="relative inline-block" style={imageStyle}>
      {isLoading && (
        <div
          className={cn(
            'absolute inset-0 animate-pulse rounded-md bg-muted',
            className
          )}
          style={imageStyle}
        />
      )}
      <img
        id={id}
        src={currentSrc}
        alt={alt}
        className={cn(
          'rounded-md',
          isLoading && 'invisible',
          className
        )}
        style={imageStyle}
        onLoad={handleLoad}
        onError={handleError}
        data-refast-id={dataRefastId}
      />
    </div>
  );
}

interface TooltipProps {
  id?: string;
  className?: string;
  content: string;
  side?: 'top' | 'right' | 'bottom' | 'left';
  sideOffset?: number;
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
  sideOffset,
  children,
  'data-refast-id': dataRefastId,
}: TooltipProps): React.ReactElement {
  // Ensure trigger is a single element for Radix's asChild and attach id/data-refast-id to it
  const trigger = React.Children.count(children) === 1 && React.isValidElement(children)
    ? React.cloneElement(children as React.ReactElement, { id, 'data-refast-id': dataRefastId })
    : <span id={id} data-refast-id={dataRefastId}>{children}</span>;

  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root>
        <TooltipPrimitive.Trigger asChild>
          {trigger}
        </TooltipPrimitive.Trigger>
        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content
              side={side}
              sideOffset={typeof sideOffset === 'number' ? sideOffset : 4}
            className={cn(
              'z-50 rounded-md bg-foreground text-background text-sm px-3 py-1.5 shadow-md animate-in fade-in-0 zoom-in-95',
              className
            )}
          >
            {content}
            <TooltipPrimitive.Arrow className="fill-foreground" />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
}

// Re-exports for convenience (match shadcn API surface)
export const TooltipTrigger = TooltipPrimitive.Trigger;
export const TooltipContent = TooltipPrimitive.Content;
export const TooltipProvider = TooltipPrimitive.Provider;

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
      
      let itemValue: string | undefined;
      let itemLabel: string | undefined;
      let itemDisabled: boolean | undefined;

      // Handle ComponentRenderer children (wrapped)
      if ('tree' in props && typeof props.tree === 'object' && props.tree !== null) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const treeProps = (props.tree as any).props || {};
        itemValue = treeProps.value;
        itemLabel = treeProps.label;
        itemDisabled = treeProps.disabled;
      } else {
        // Handle direct usage
        itemValue = props.value as string;
        itemLabel = props.label as string;
        itemDisabled = props.disabled as boolean;
      }

      // If value is found, add to meta
      if (itemValue !== undefined) {
        tabMeta.push({
          value: String(itemValue || ''),
          label: String(itemLabel || itemValue || ''),
          disabled: Boolean(itemDisabled),
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
              let itemValue: string | undefined;

              // Handle ComponentRenderer children (wrapped)
              if ('tree' in props && typeof props.tree === 'object' && props.tree !== null) {
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                const treeProps = (props.tree as any).props || {};
                itemValue = treeProps.value;
              } else {
                // Handle direct usage
                itemValue = props.value as string;
              }

              const tabValue = String(itemValue || '');
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
