import React from 'react';
import * as SwitchPrimitive from '@radix-ui/react-switch';
import * as SliderPrimitive from '@radix-ui/react-slider';
import * as TogglePrimitive from '@radix-ui/react-toggle';
import * as ToggleGroupPrimitive from '@radix-ui/react-toggle-group';
import { DayPicker, DayButton, getDefaultClassNames, type Matcher } from 'react-day-picker';
import {
  ChevronDownIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "lucide-react"
import { Button, buttonVariants } from './button';
import { cn } from '../../utils';
import { Icon } from './icon';

// ============================================================================
// Switch
// ============================================================================

interface SwitchProps {
  id?: string;
  className?: string;
  checked?: boolean;
  defaultChecked?: boolean;
  disabled?: boolean;
  name?: string;
  onCheckedChange?: (checked: boolean) => void;
  'data-refast-id'?: string;
}

export function Switch({
  id,
  className,
  checked,
  defaultChecked,
  disabled = false,
  name,
  onCheckedChange,
  'data-refast-id': dataRefastId,
}: SwitchProps): React.ReactElement {
  return (
    <SwitchPrimitive.Root
      id={id}
      checked={checked}
      defaultChecked={defaultChecked}
      disabled={disabled}
      name={name}
      onCheckedChange={onCheckedChange}
      className={cn(
        'peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent',
        'transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50',
        'data-[state=checked]:bg-primary data-[state=unchecked]:bg-input',
        className
      )}
      data-refast-id={dataRefastId}
    >
      <SwitchPrimitive.Thumb
        className={cn(
          'pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform',
          'data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0'
        )}
      />
    </SwitchPrimitive.Root>
  );
}

// ============================================================================
// Slider
// ============================================================================

interface SliderProps {
  id?: string;
  className?: string;
  value?: number[];
  defaultValue?: number[];
  min?: number;
  max?: number;
  step?: number;
  disabled?: boolean;
  orientation?: 'horizontal' | 'vertical';
  onValueChange?: (value: number[]) => void;
  onValueCommit?: (value: number[]) => void;
  'data-refast-id'?: string;
}

export function Slider({
  id,
  className,
  value,
  defaultValue = [0],
  min = 0,
  max = 100,
  step = 1,
  disabled = false,
  orientation = 'horizontal',
  onValueChange,
  onValueCommit,
  'data-refast-id': dataRefastId,
}: SliderProps): React.ReactElement {
  return (
    <SliderPrimitive.Root
      id={id}
      value={value}
      defaultValue={defaultValue}
      min={min}
      max={max}
      step={step}
      disabled={disabled}
      orientation={orientation}
      onValueChange={onValueChange}
      onValueCommit={onValueCommit}
      className={cn(
        'relative flex w-full touch-none select-none items-center',
        orientation === 'vertical' && 'flex-col h-full w-auto',
        className
      )}
      data-refast-id={dataRefastId}
    >
      <SliderPrimitive.Track
        className={cn(
          'relative grow overflow-hidden rounded-full bg-secondary',
          orientation === 'horizontal' ? 'h-2 w-full' : 'h-full w-2'
        )}
      >
        <SliderPrimitive.Range className="absolute bg-primary h-full" />
      </SliderPrimitive.Track>
      {(value || defaultValue).map((_, index) => (
        <SliderPrimitive.Thumb
          key={index}
          className={cn(
            'block h-5 w-5 rounded-full border-2 border-primary bg-background ring-offset-background',
            'transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
            'disabled:pointer-events-none disabled:opacity-50'
          )}
        />
      ))}
    </SliderPrimitive.Root>
  );
}

// ============================================================================
// Toggle
// ============================================================================

interface ToggleProps {
  id?: string;
  className?: string;
  label?: string;
  icon?: string;
  pressed?: boolean;
  defaultPressed?: boolean;
  disabled?: boolean;
  variant?: 'default' | 'outline';
  size?: 'sm' | 'default' | 'lg';
  onPressedChange?: (pressed: boolean) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

const toggleVariants = {
  default: 'bg-transparent',
  outline: 'border border-input bg-transparent hover:bg-accent hover:text-accent-foreground',
};

const toggleSizes = {
  sm: 'h-9 px-2.5',
  default: 'h-10 px-3',
  lg: 'h-11 px-5',
};

export function Toggle({
  id,
  className,
  label,
  pressed,
  defaultPressed,
  disabled = false,
  variant = 'default',
  size = 'default',
  onPressedChange,
  children,
  'data-refast-id': dataRefastId,
}: ToggleProps): React.ReactElement {
  return (
    <TogglePrimitive.Root
      id={id}
      pressed={pressed}
      defaultPressed={defaultPressed}
      disabled={disabled}
      onPressedChange={onPressedChange}
      className={cn(
        'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors',
        'hover:bg-muted hover:text-muted-foreground focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        'data-[state=on]:bg-accent data-[state=on]:text-accent-foreground',
        toggleVariants[variant],
        toggleSizes[size],
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children || label}
    </TogglePrimitive.Root>
  );
}

// ============================================================================
// ToggleGroup
// ============================================================================

interface ToggleGroupProps {
  id?: string;
  className?: string;
  type?: 'single' | 'multiple';
  value?: string | string[];
  defaultValue?: string | string[];
  disabled?: boolean;
  variant?: 'default' | 'outline';
  size?: 'sm' | 'default' | 'lg';
  onValueChange?: (value: string | string[] | Record<string, boolean>) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function ToggleGroup({
  id,
  className,
  type = 'single',
  value,
  defaultValue,
  disabled = false,
  variant = 'default',
  size = 'default',
  onValueChange,
  children,
  'data-refast-id': dataRefastId,
}: ToggleGroupProps): React.ReactElement {
  // Handle value based on type - Radix UI expects array for "multiple" type
  const resolvedValue = type === 'multiple' 
    ? (value as string[] | undefined)
    : (value as string | undefined);
  
  const resolvedDefaultValue = type === 'multiple'
    ? (defaultValue as string[] | undefined)
    : (defaultValue as string | undefined);

  if (type === 'multiple') {
    const handleValueChange = (newValues: string[]) => {
      if (!onValueChange) return;

      // Collect all possible values from children to construct the boolean map
      const allValues = new Set<string>();
      React.Children.forEach(children, (child) => {
        if (!React.isValidElement(child)) return;
        
        // Try to get value from tree prop (ComponentRenderer) or direct props
        const props = child.props as any;
        const value = props.tree?.props?.value || props.value;
        
        if (value) {
          allValues.add(value);
        }
      });
      // Also ensure any currently selected values are included
      newValues.forEach(v => allValues.add(v));

      const resultMap: Record<string, boolean> = {};
      allValues.forEach(v => {
        resultMap[v] = newValues.includes(v);
      });

      onValueChange(resultMap);
    };

    return (
      <ToggleGroupPrimitive.Root
        id={id}
        type="multiple"
        value={resolvedValue as string[]}
        defaultValue={resolvedDefaultValue as string[]}
        disabled={disabled}
        onValueChange={handleValueChange}
        className={cn(
          'inline-flex items-center justify-center gap-1',
          className
        )}
        data-refast-id={dataRefastId}
      >
        {React.Children.map(children, (child) => {
          if (React.isValidElement(child)) {
            return React.cloneElement(child as React.ReactElement<{ variant?: string; size?: string }>, {
              variant,
              size,
            });
          }
          return child;
        })}
      </ToggleGroupPrimitive.Root>
    );
  }

  return (
    <ToggleGroupPrimitive.Root
      id={id}
      type="single"
      value={resolvedValue as string}
      defaultValue={resolvedDefaultValue as string}
      disabled={disabled}
      onValueChange={onValueChange as (value: string) => void}
      className={cn(
        'inline-flex items-center justify-center gap-1',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child as React.ReactElement<{ variant?: string; size?: string }>, {
            variant,
            size,
          });
        }
        return child;
      })}
    </ToggleGroupPrimitive.Root>
  );
}

interface ToggleGroupItemProps {
  id?: string;
  className?: string;
  label?: string;
  icon?: string;
  value: string;
  disabled?: boolean;
  variant?: 'default' | 'outline';
  size?: 'sm' | 'default' | 'lg';
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function ToggleGroupItem({
  id,
  className,
  label,
  icon,
  value,
  disabled = false,
  variant = 'default',
  size = 'default',
  children,
  'data-refast-id': dataRefastId,
}: ToggleGroupItemProps): React.ReactElement {
  return (
    <ToggleGroupPrimitive.Item
      id={id}
      value={value}
      disabled={disabled}
      className={cn(
        'inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors',
        'hover:bg-muted hover:text-muted-foreground focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
        'data-[state=on]:bg-accent data-[state=on]:text-accent-foreground',
        toggleVariants[variant],
        toggleSizes[size],
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children || (icon && <Icon name={icon} size={16} />) || label}
    </ToggleGroupPrimitive.Item>
  );
}

// ============================================================================
// Calendar (using react-day-picker)
// ============================================================================

// Helper to parse a date string or Date to Date object
function parseDate(value: string | Date | undefined | null): Date | undefined {
  if (!value) return undefined;
  if (value instanceof Date) return value;
  if (typeof value === 'string') {
    const parsed = new Date(value);
    return isNaN(parsed.getTime()) ? undefined : parsed;
  }
  return undefined;
}

// Helper to parse date range from various formats
function parseDateRange(
  value: string | { from?: string | Date; to?: string | Date } | undefined | null
): { from: Date | undefined; to: Date | undefined } | undefined {
  if (!value) return undefined;
  if (typeof value === 'object' && 'from' in value) {
    return {
      from: parseDate(value.from as string | Date | undefined),
      to: parseDate(value.to as string | Date | undefined),
    };
  }
  return undefined;
}

// Helper to parse array of dates
function parseDateArray(value: (string | Date)[] | undefined | null): Date[] | undefined {
  if (!value || !Array.isArray(value)) return undefined;
  return value.map(d => parseDate(d)).filter((d): d is Date => d !== undefined);
}

interface CalendarProps {
  id?: string;
  className?: string;
  classNames?: Partial<React.ComponentProps<typeof DayPicker>['classNames']>;
  captionLayout?: 'label' | 'dropdown' | 'dropdown-years' | 'dropdown-months';
  mode?: 'single' | 'multiple' | 'range';
  buttonVariant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
  formatters?: Partial<React.ComponentProps<typeof DayPicker>['formatters']>;
  components?: Partial<React.ComponentProps<typeof DayPicker>['components']>;
  // Accept both Date objects and ISO strings from Python
  selected?: Date | Date[] | { from?: Date | string; to?: Date | string } | string | string[];
  defaultMonth?: Date | string;
  disabled?: boolean | ((date: Date) => boolean);
  // Min/max date constraints
  minDate?: Date | string;
  maxDate?: Date | string;
  showOutsideDays?: boolean;
  showWeekNumber?: boolean;
  numberOfMonths?: number;
  // Callbacks that serialize dates to ISO strings for Python
  onSelect?: (date: Date | Date[] | { from: Date; to: Date } | undefined) => void;
  onMonthChange?: (month: Date) => void;
  'data-refast-id'?: string;
}

export function Calendar({
  id,
  className,
  classNames,
  mode = 'single',
  showOutsideDays = true,
  captionLayout = "label",
  buttonVariant = "ghost",
  formatters,
  components,
  selected,
  defaultMonth,
  disabled,
  minDate,
  maxDate,
  numberOfMonths,
  onSelect,
  onMonthChange,
  showWeekNumber,
  ...restProps
}: CalendarProps) {
  const defaultClassNames = getDefaultClassNames();

  // Parse selected value based on mode
  const parsedSelected = React.useMemo(() => {
    if (mode === 'range') {
      return parseDateRange(selected as { from?: string | Date; to?: string | Date } | undefined);
    } else if (mode === 'multiple') {
      return parseDateArray(selected as (string | Date)[] | undefined);
    } else {
      return parseDate(selected as string | Date | undefined);
    }
  }, [mode, selected]);

  // Parse defaultMonth
  const parsedDefaultMonth = React.useMemo(() => parseDate(defaultMonth as string | Date | undefined), [defaultMonth]);

  // Parse min/max dates and create disabled matcher
  const parsedMinDate = React.useMemo(() => parseDate(minDate as string | Date | undefined), [minDate]);
  const parsedMaxDate = React.useMemo(() => parseDate(maxDate as string | Date | undefined), [maxDate]);

  // Build disabled matcher combining min/max with any existing disabled prop
  const disabledMatcher = React.useMemo((): Matcher | Matcher[] | undefined => {
    const matchers: Matcher[] = [];
    
    if (parsedMinDate) {
      matchers.push({ before: parsedMinDate });
    }
    if (parsedMaxDate) {
      matchers.push({ after: parsedMaxDate });
    }
    if (typeof disabled === 'function') {
      matchers.push(disabled);
    } else if (disabled === true) {
      // If disabled is true, disable all dates
      matchers.push(() => true);
    }
    
    return matchers.length > 0 ? matchers : undefined;
  }, [parsedMinDate, parsedMaxDate, disabled]);

  // Handle select and serialize dates back to ISO strings
  const handleSelect = React.useCallback((value: Date | Date[] | { from?: Date; to?: Date } | undefined) => {
    if (!onSelect) return;
    
    if (!value) {
      onSelect(undefined);
      return;
    }
    
    // For range mode, serialize the range object
    if (mode === 'range' && typeof value === 'object' && 'from' in value) {
      const range = value as { from?: Date; to?: Date };
      // Send as object with ISO strings - will be converted in callback handler
      onSelect({
        from: range.from!,
        to: range.to!,
      } as { from: Date; to: Date });
      return;
    }
    
    // For multiple mode, serialize array
    if (mode === 'multiple' && Array.isArray(value)) {
      onSelect(value);
      return;
    }
    
    // For single mode
    onSelect(value as Date);
  }, [mode, onSelect]);

  // Handle month change
  const handleMonthChange = React.useCallback((month: Date) => {
    if (onMonthChange) {
      onMonthChange(month);
    }
  }, [onMonthChange]);

  // Build props based on mode
  const modeProps = React.useMemo(() => {
    if (mode === 'range') {
      return {
        mode: 'range' as const,
        selected: parsedSelected as { from: Date | undefined; to: Date | undefined } | undefined,
        onSelect: handleSelect as (range: { from?: Date; to?: Date } | undefined) => void,
      };
    } else if (mode === 'multiple') {
      return {
        mode: 'multiple' as const,
        selected: parsedSelected as Date[] | undefined,
        onSelect: handleSelect as (dates: Date[] | undefined) => void,
      };
    } else {
      return {
        mode: 'single' as const,
        selected: parsedSelected as Date | undefined,
        onSelect: handleSelect as (date: Date | undefined) => void,
      };
    }
  }, [mode, parsedSelected, handleSelect]);

  return (
    <DayPicker
      showOutsideDays={showOutsideDays}
      className={cn(
        "bg-background group/calendar p-3 [--cell-size:2.5rem] [[data-slot=card-content]_&]:bg-transparent [[data-slot=popover-content]_&]:bg-transparent",
        String.raw`rtl:**:[.rdp-button\_next>svg]:rotate-180`,
        String.raw`rtl:**:[.rdp-button\_previous>svg]:rotate-180`,
        className
      )}
      captionLayout={captionLayout}
      defaultMonth={parsedDefaultMonth}
      disabled={disabledMatcher}
      numberOfMonths={numberOfMonths}
      onMonthChange={handleMonthChange}
      formatters={{
        formatMonthDropdown: (date) =>
          date.toLocaleString("default", { month: "short" }),
        ...formatters,
      }}
      classNames={{
        root: cn("w-fit", defaultClassNames.root),
        months: cn(
          "flex gap-4 flex-col md:flex-row relative",
          defaultClassNames.months
        ),
        month: cn("flex flex-col w-full gap-4", defaultClassNames.month),
        nav: cn(
          "flex items-center gap-1 w-full absolute top-0 inset-x-0 justify-between",
          defaultClassNames.nav
        ),
        button_previous: cn(
          buttonVariants({ variant: buttonVariant }),
          "size-[var(--cell-size)] aria-disabled:opacity-50 p-0 select-none",
          defaultClassNames.button_previous
        ),
        button_next: cn(
          buttonVariants({ variant: buttonVariant }),
          "size-[var(--cell-size)] aria-disabled:opacity-50 p-0 select-none",
          defaultClassNames.button_next
        ),
        month_caption: cn(
          "flex items-center justify-center h-[var(--cell-size)] w-full px-[var(--cell-size)]",
          defaultClassNames.month_caption
        ),
        dropdowns: cn(
          "w-full flex items-center text-sm font-medium justify-center h-[var(--cell-size)] gap-2",
          defaultClassNames.dropdowns
        ),
        dropdown_root: cn(
          "relative",
          defaultClassNames.dropdown_root
        ),
        dropdown: cn(
          "absolute inset-0 cursor-pointer opacity-0 z-10 w-full h-full",
          defaultClassNames.dropdown
        ),
        months_dropdown: cn(
          "inline-flex items-center justify-center gap-1 rounded-md border border-input bg-background px-3 py-1.5 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring cursor-pointer",
        ),
        years_dropdown: cn(
          "inline-flex items-center justify-center gap-1 rounded-md border border-input bg-background px-3 py-1.5 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring cursor-pointer",
        ),
        caption_label: cn(
          "select-none font-medium",
          captionLayout === "label"
            ? "text-sm"
            : "rounded-md px-2 flex items-center gap-1 text-sm h-8 [&>svg]:text-muted-foreground [&>svg]:size-3.5",
          defaultClassNames.caption_label
        ),
        table: "w-full border-collapse",
        weekdays: cn("flex", defaultClassNames.weekdays),
        weekday: cn(
          "text-muted-foreground rounded-md flex-1 font-normal text-sm select-none w-[var(--cell-size)] h-[var(--cell-size)] flex items-center justify-center",
          defaultClassNames.weekday
        ),
        week: cn("flex w-full mt-2", defaultClassNames.week),
        week_number_header: cn(
          "select-none w-[var(--cell-size)]",
          defaultClassNames.week_number_header
        ),
        week_number: cn(
          "text-sm select-none text-muted-foreground",
          defaultClassNames.week_number
        ),
        day: cn(
          "relative w-[var(--cell-size)] h-[var(--cell-size)] p-0 text-center [&:last-child[data-selected=true]_button]:rounded-r-md group/day select-none",
          showWeekNumber
            ? "[&:nth-child(2)[data-selected=true]_button]:rounded-l-md"
            : "[&:first-child[data-selected=true]_button]:rounded-l-md",
          defaultClassNames.day
        ),
        range_start: cn(
          "rounded-l-md bg-accent",
          defaultClassNames.range_start
        ),
        range_middle: cn("rounded-none", defaultClassNames.range_middle),
        range_end: cn("rounded-r-md bg-accent", defaultClassNames.range_end),
        today: cn(
          "bg-accent text-accent-foreground rounded-md data-[selected=true]:rounded-none",
          defaultClassNames.today
        ),
        outside: cn(
          "text-muted-foreground aria-selected:text-muted-foreground",
          defaultClassNames.outside
        ),
        disabled: cn(
          "text-muted-foreground opacity-50",
          defaultClassNames.disabled
        ),
        hidden: cn("invisible", defaultClassNames.hidden),
        ...classNames,
      }}
      components={{
        Root: ({ className, rootRef, ...props }) => {
          return (
            <div
              data-slot="calendar"
              ref={rootRef}
              className={cn(className)}
              {...props}
            />
          )
        },
        Chevron: ({ className, orientation, ...props }) => {
          if (orientation === "left") {
            return (
              <ChevronLeftIcon className={cn("size-4", className)} {...props} />
            )
          }
          if (orientation === "right") {
            return (
              <ChevronRightIcon
                className={cn("size-4", className)}
                {...props}
              />
            )
          }
          return (
            <ChevronDownIcon className={cn("size-4", className)} {...props} />
          )
        },
        DayButton: CalendarDayButton,
        WeekNumber: ({ children, ...props }) => {
          return (
            <td {...props}>
              <div className="flex size-[var(--cell-size)] items-center justify-center text-center">
                {children}
              </div>
            </td>
          )
        },
        ...components,
      }}
      {...modeProps}
      {...restProps}
    />
  )
}
function CalendarDayButton({
  className,
  day,
  modifiers,
  ...props
}: React.ComponentProps<typeof DayButton>) {
  const defaultClassNames = getDefaultClassNames()
  const ref = React.useRef<HTMLButtonElement>(null)
  React.useEffect(() => {
    if (modifiers.focused) ref.current?.focus()
  }, [modifiers.focused])
  return (
    <Button
      ref={ref}
      variant="ghost"
      size="icon"
      data-day={day.date.toLocaleDateString()}
      data-selected-single={
        modifiers.selected &&
        !modifiers.range_start &&
        !modifiers.range_end &&
        !modifiers.range_middle
      }
      data-range-start={modifiers.range_start}
      data-range-end={modifiers.range_end}
      data-range-middle={modifiers.range_middle}
      className={cn(
        "data-[selected-single=true]:bg-primary data-[selected-single=true]:text-primary-foreground",
        "data-[range-middle=true]:bg-accent data-[range-middle=true]:text-accent-foreground",
        "data-[range-start=true]:bg-primary data-[range-start=true]:text-primary-foreground",
        "data-[range-end=true]:bg-primary data-[range-end=true]:text-primary-foreground",
        "group-data-[focused=true]/day:border-ring group-data-[focused=true]/day:ring-ring/50",
        "dark:hover:text-accent-foreground",
        "flex size-[var(--cell-size)] items-center justify-center",
        "leading-none font-normal text-sm",
        "group-data-[focused=true]/day:relative group-data-[focused=true]/day:z-10 group-data-[focused=true]/day:ring-[3px]",
        "data-[range-end=true]:rounded-md data-[range-end=true]:rounded-r-md",
        "data-[range-middle=true]:rounded-none",
        "data-[range-start=true]:rounded-md data-[range-start=true]:rounded-l-md",
        defaultClassNames.day,
        className
      )}
      {...props}
    />
  )
}


// ============================================================================
// DatePicker
// ============================================================================

interface DatePickerProps {
  id?: string;
  className?: string;
  // For single mode: ISO string or Date; for range mode: { from?: string, to?: string }
  value?: string | { from?: string; to?: string };
  placeholder?: string;
  disabled?: boolean;
  format?: string;
  mode?: 'single' | 'range';
  captionLayout?: 'label' | 'dropdown' | 'dropdown-years' | 'dropdown-months';
  minDate?: string;
  maxDate?: string;
  numberOfMonths?: number;
  // onChange sends ISO strings back to Python
  onChange?: (date: string | { from?: string; to?: string } | undefined) => void;
  'data-refast-id'?: string;
}

export function DatePicker({
  id,
  className,
  value,
  placeholder = 'Pick a date',
  disabled = false,
  mode = 'single',
  captionLayout = 'label',
  minDate,
  maxDate,
  numberOfMonths,
  onChange,
  'data-refast-id': dataRefastId,
}: DatePickerProps): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement>(null);

  // Parse the value based on mode
  const parsedValue = React.useMemo(() => {
    if (mode === 'range') {
      if (!value) return undefined;
      if (typeof value === 'object' && ('from' in value || 'to' in value)) {
        return {
          from: value.from ? new Date(value.from) : undefined,
          to: value.to ? new Date(value.to) : undefined,
        };
      }
      return undefined;
    } else {
      if (!value) return undefined;
      if (typeof value === 'string') {
        const parsed = new Date(value);
        return isNaN(parsed.getTime()) ? undefined : parsed;
      }
      return undefined;
    }
  }, [mode, value]);

  // Local state for selection
  const [selectedDate, setSelectedDate] = React.useState<Date | undefined>(
    mode === 'single' ? (parsedValue as Date | undefined) : undefined
  );
  const [selectedRange, setSelectedRange] = React.useState<{ from?: Date; to?: Date } | undefined>(
    mode === 'range' ? (parsedValue as { from?: Date; to?: Date } | undefined) : undefined
  );

  // Sync local state with prop changes
  React.useEffect(() => {
    if (mode === 'single') {
      setSelectedDate(parsedValue as Date | undefined);
    } else {
      setSelectedRange(parsedValue as { from?: Date; to?: Date } | undefined);
    }
  }, [mode, parsedValue]);

  // Close on click outside
  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    };

    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [open]);

  // Format display value
  const displayValue = React.useMemo(() => {
    if (mode === 'range') {
      if (!selectedRange?.from) return placeholder;
      if (!selectedRange.to) {
        return selectedRange.from.toLocaleDateString();
      }
      return `${selectedRange.from.toLocaleDateString()} - ${selectedRange.to.toLocaleDateString()}`;
    } else {
      return selectedDate ? selectedDate.toLocaleDateString() : placeholder;
    }
  }, [mode, selectedDate, selectedRange, placeholder]);

  // Handle single date selection
  const handleSingleSelect = (date: Date | undefined) => {
    setSelectedDate(date);
    setOpen(false);
    if (onChange) {
      onChange(date ? date.toISOString() : undefined);
    }
  };

  // Handle range selection
  const handleRangeSelect = (range: { from?: Date; to?: Date } | undefined) => {
    setSelectedRange(range);
    // Close only when both dates are selected
    if (range?.from && range?.to) {
      setOpen(false);
    }
    if (onChange) {
      if (!range) {
        onChange(undefined);
      } else {
        onChange({
          from: range.from?.toISOString(),
          to: range.to?.toISOString(),
        });
      }
    }
  };

  const hasValue = mode === 'range' ? !!selectedRange?.from : !!selectedDate;

  return (
    <div ref={containerRef} className={cn('relative', className)} data-refast-id={dataRefastId}>
      <button
        id={id}
        type="button"
        disabled={disabled}
        onClick={() => setOpen(!open)}
        className={cn(
          'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm',
          'ring-offset-background placeholder:text-muted-foreground',
          'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          !hasValue && 'text-muted-foreground'
        )}
      >
        <span className="truncate">{displayValue}</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="ml-2 h-4 w-4 shrink-0 opacity-50"
        >
          <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
          <line x1="16" x2="16" y1="2" y2="6" />
          <line x1="8" x2="8" y1="2" y2="6" />
          <line x1="3" x2="21" y1="10" y2="10" />
        </svg>
      </button>
      {open && (
        <div className="absolute top-full left-0 z-50 mt-2 rounded-md border bg-popover p-0 text-popover-foreground shadow-md">
          {mode === 'range' ? (
            <Calendar
              mode="range"
              captionLayout={captionLayout}
              selected={selectedRange}
              onSelect={(value) => handleRangeSelect(value as { from?: Date; to?: Date } | undefined)}
              minDate={minDate}
              maxDate={maxDate}
              numberOfMonths={numberOfMonths || 2}
            />
          ) : (
            <Calendar
              mode="single"
              captionLayout={captionLayout}
              selected={selectedDate}
              onSelect={(value) => handleSingleSelect(value as Date | undefined)}
              minDate={minDate}
              maxDate={maxDate}
            />
          )}
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Combobox
// ============================================================================

interface ComboboxOption {
  value: string;
  label: string;
}

interface ComboboxProps {
  id?: string;
  className?: string;
  options?: ComboboxOption[];
  value?: string | string[];
  placeholder?: string;
  searchPlaceholder?: string;
  emptyText?: string;
  multiselect?: boolean;
  disabled?: boolean;
  onSelect?: (value: string | string[]) => void;
  'data-refast-id'?: string;
}

export function Combobox({
  id,
  className,
  options = [],
  value,
  placeholder = 'Select...',
  searchPlaceholder = 'Search...',
  emptyText = 'No results found.',
  multiselect = false,
  disabled = false,
  onSelect,
  'data-refast-id': dataRefastId,
}: ComboboxProps): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');

  const [internalValue, setInternalValue] = React.useState<string | string[]>(
    value !== undefined ? value : (multiselect ? [] : '')
  );

  const containerRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setOpen(false);
      }
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setOpen(false);
      }
    };

    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [open]);

  React.useEffect(() => {
    if (value !== undefined) {
      setInternalValue(value);
    }
  }, [value]);

  // Ensure internalValue is array if multiselect is true
  React.useEffect(() => {
    if (multiselect && !Array.isArray(internalValue)) {
      setInternalValue(internalValue ? [internalValue as string] : []);
    }
  }, [multiselect]); // removed internalValue from deps to avoid loop if modifying it

  const filteredOptions = options.filter((option) => {
    if (!option || typeof option.label !== 'string') return false;
    return option.label.toLowerCase().includes(search.toLowerCase());
  });

  const isSelected = (val: string) => {
    if (multiselect && Array.isArray(internalValue)) {
      return internalValue.includes(val);
    }
    return internalValue === val;
  };

  const handleSelect = (val: string) => {
    if (multiselect) {
      const current = Array.isArray(internalValue) ? internalValue : [];
      let next: string[];
      if (current.includes(val)) {
        next = current.filter((v) => v !== val);
      } else {
        next = [...current, val];
      }
      setInternalValue(next);
      if (onSelect) onSelect(next);
      // Keep open for multiselect
    } else {
      setInternalValue(val);
      if (onSelect) onSelect(val);
      setOpen(false);
      setSearch('');
    }
  };

  const removeValue = (e: React.MouseEvent, val: string) => {
    e.stopPropagation();
    if (multiselect && Array.isArray(internalValue)) {
      const next = internalValue.filter((v) => v !== val);
      setInternalValue(next);
      if (onSelect) onSelect(next);
    }
  };

  return (
    <div
      ref={containerRef}
      className={cn('relative', className)}
      data-refast-id={dataRefastId}
    >
      <button
        id={id}
        type="button"
        disabled={disabled}
        onClick={() => setOpen(!open)}
        className={cn(
          'flex min-h-[2.5rem] w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm',
          'ring-offset-background placeholder:text-muted-foreground',
          'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50'
        )}
      >
        {multiselect && Array.isArray(internalValue) && internalValue.length > 0 ? (
          <div className="flex flex-wrap gap-1">
            {internalValue.map((val) => {
              const label = options.find((o) => o.value === val)?.label || val;
              return (
                <div
                  key={val}
                  className="flex items-center gap-1 rounded bg-secondary px-1.5 py-0.5 text-xs font-medium text-secondary-foreground"
                >
                  {label}
                  <div
                    role="button"
                    className="ml-1 cursor-pointer rounded-full p-0.5 hover:bg-secondary-foreground/20"
                    onClick={(e) => removeValue(e, val)}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="12"
                      height="12"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <path d="M18 6 6 18" />
                      <path d="m6 6 12 12" />
                    </svg>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <span className={!internalValue || (Array.isArray(internalValue) && internalValue.length === 0) ? 'text-muted-foreground' : ''}>
            {(!multiselect && typeof internalValue === 'string' && options.find((opt) => opt.value === internalValue)?.label) || placeholder}
          </span>
        )}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="ml-2 h-4 w-4 shrink-0 opacity-50"
        >
          <path d="m7 15 5 5 5-5" />
          <path d="m7 9 5-5 5 5" />
        </svg>
      </button>
      {open && (
        <div className="absolute top-full left-0 z-50 mt-2 w-full rounded-md border bg-popover text-popover-foreground shadow-md">
          <div className="flex items-center border-b px-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="mr-2 h-4 w-4 shrink-0 opacity-50"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.3-4.3" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={searchPlaceholder}
              className="flex h-10 w-full bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground"
            />
          </div>
          <div className="max-h-[300px] overflow-y-auto p-1">
            {filteredOptions.length === 0 ? (
              <div className="py-6 text-center text-sm text-muted-foreground">
                {emptyText}
              </div>
            ) : (
              filteredOptions.map((option) => {
                const selected = isSelected(option.value);
                return (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => handleSelect(option.value)}
                    className={cn(
                      'relative flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
                      'hover:bg-accent hover:text-accent-foreground',
                      selected && 'bg-accent text-accent-foreground'
                    )}
                  >
                    {selected && (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="mr-2 h-4 w-4"
                      >
                        <polyline points="20 6 9 17 4 12" />
                      </svg>
                    )}
                    <span className={!selected ? 'pl-6' : ''}>
                      {option.label}
                    </span>
                  </button>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// InputOTP
// ============================================================================

interface InputOTPProps {
  id?: string;
  className?: string;
  maxLength?: number;
  value?: string;
  disabled?: boolean;
  pattern?: string;
  onChange?: (value: string) => void;
  onComplete?: (value: string) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function InputOTP({
  id,
  className,
  maxLength = 6,
  value = '',
  disabled = false,
  onChange,
  onComplete,
  children,
  'data-refast-id': dataRefastId,
}: InputOTPProps): React.ReactElement {
  const [localValue, setLocalValue] = React.useState(value);
  const inputRefs = React.useRef<(HTMLInputElement | null)[]>([]);

  const handleChange = (index: number, char: string) => {
    const newValue = localValue.split('');
    newValue[index] = char;
    const joined = newValue.join('').slice(0, maxLength);
    setLocalValue(joined);
    if (onChange) onChange(joined);

    if (char && index < maxLength - 1) {
      inputRefs.current[index + 1]?.focus();
    }

    if (joined.length === maxLength && onComplete) {
      onComplete(joined);
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !localValue[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  // If children are provided, render them (for custom layout)
  if (children) {
    return (
      <div
        id={id}
        className={cn('flex items-center gap-2', className)}
        data-refast-id={dataRefastId}
      >
        {children}
      </div>
    );
  }

  // Default simple layout
  return (
    <div
      id={id}
      className={cn('flex items-center gap-2', className)}
      data-refast-id={dataRefastId}
    >
      {Array.from({ length: maxLength }).map((_, index) => (
        <input
          key={index}
          ref={(el) => { inputRefs.current[index] = el; }}
          type="text"
          inputMode="numeric"
          maxLength={1}
          value={localValue[index] || ''}
          disabled={disabled}
          onChange={(e) => handleChange(index, e.target.value)}
          onKeyDown={(e) => handleKeyDown(index, e)}
          className={cn(
            'h-10 w-10 rounded-md border border-input bg-background text-center text-sm',
            'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50'
          )}
        />
      ))}
    </div>
  );
}

interface InputOTPGroupProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function InputOTPGroup({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: InputOTPGroupProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn('flex items-center', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface InputOTPSlotProps {
  id?: string;
  className?: string;
  index: number;
  'data-refast-id'?: string;
}

export function InputOTPSlot({
  id,
  className,
  index: _index,
  'data-refast-id': dataRefastId,
}: InputOTPSlotProps): React.ReactElement {
  return (
    <div
      id={id}
      className={cn(
        'relative flex h-10 w-10 items-center justify-center border-y border-r border-input text-sm transition-all',
        'first:rounded-l-md first:border-l last:rounded-r-md',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {/* Slot placeholder - actual value comes from parent InputOTP */}
      <span className="text-muted-foreground">-</span>
    </div>
  );
}

interface InputOTPSeparatorProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function InputOTPSeparator({
  id,
  className,
  'data-refast-id': dataRefastId,
}: InputOTPSeparatorProps): React.ReactElement {
  return (
    <div
      id={id}
      role="separator"
      className={cn('flex items-center justify-center', className)}
      data-refast-id={dataRefastId}
    >
      <span className="text-muted-foreground">-</span>
    </div>
  );
}
