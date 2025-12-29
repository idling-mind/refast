import React from 'react';
import * as SwitchPrimitive from '@radix-ui/react-switch';
import * as SliderPrimitive from '@radix-ui/react-slider';
import * as TogglePrimitive from '@radix-ui/react-toggle';
import * as ToggleGroupPrimitive from '@radix-ui/react-toggle-group';
import { cn } from '../../utils';

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
  onValueChange?: (value: string | string[]) => void;
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
  const Component = type === 'single' 
    ? ToggleGroupPrimitive.Root 
    : ToggleGroupPrimitive.Root;

  return (
    <Component
      id={id}
      type={type as 'single'}
      value={value as string}
      defaultValue={defaultValue as string}
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
    </Component>
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
      {children || label}
    </ToggleGroupPrimitive.Item>
  );
}

// ============================================================================
// Calendar (using react-day-picker)
// ============================================================================

interface CalendarProps {
  id?: string;
  className?: string;
  mode?: 'single' | 'multiple' | 'range';
  selected?: Date | Date[] | { from: Date; to: Date };
  defaultMonth?: Date;
  disabled?: boolean;
  showOutsideDays?: boolean;
  onSelect?: (date: Date | Date[] | { from: Date; to: Date } | undefined) => void;
  onMonthChange?: (month: Date) => void;
  'data-refast-id'?: string;
}

export function Calendar({
  id,
  className,
  mode: _mode = 'single',
  selected: _selected,
  showOutsideDays: _showOutsideDays = true,
  onSelect: _onSelect,
  'data-refast-id': dataRefastId,
}: CalendarProps): React.ReactElement {
  // Note: Full implementation requires react-day-picker
  // This is a placeholder that will be enhanced when the package is installed
  const [currentDate] = React.useState(new Date());
  const monthName = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });

  return (
    <div
      id={id}
      className={cn('p-3', className)}
      data-refast-id={dataRefastId}
    >
      <div className="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
        <div className="space-y-4">
          <div className="flex justify-center pt-1 relative items-center">
            <span className="text-sm font-medium">{monthName}</span>
          </div>
          <div className="w-full border-collapse space-y-1">
            <div className="flex">
              {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((day) => (
                <div
                  key={day}
                  className="text-muted-foreground rounded-md w-9 font-normal text-[0.8rem] text-center"
                >
                  {day}
                </div>
              ))}
            </div>
            {/* Calendar grid placeholder */}
            <div className="text-sm text-muted-foreground text-center py-4">
              Calendar requires react-day-picker
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// DatePicker
// ============================================================================

interface DatePickerProps {
  id?: string;
  className?: string;
  value?: string;
  placeholder?: string;
  disabled?: boolean;
  format?: string;
  onChange?: (date: string | undefined) => void;
  'data-refast-id'?: string;
}

export function DatePicker({
  id,
  className,
  value,
  placeholder = 'Pick a date',
  disabled = false,
  onChange,
  'data-refast-id': dataRefastId,
}: DatePickerProps): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const [selectedDate, setSelectedDate] = React.useState<Date | undefined>(
    value ? new Date(value) : undefined
  );

  const displayValue = selectedDate
    ? selectedDate.toLocaleDateString()
    : placeholder;

  return (
    <div className={cn('relative', className)} data-refast-id={dataRefastId}>
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
          !selectedDate && 'text-muted-foreground'
        )}
      >
        <span>{displayValue}</span>
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
          className="ml-2 h-4 w-4 opacity-50"
        >
          <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
          <line x1="16" x2="16" y1="2" y2="6" />
          <line x1="8" x2="8" y1="2" y2="6" />
          <line x1="3" x2="21" y1="10" y2="10" />
        </svg>
      </button>
      {open && (
        <div className="absolute top-full left-0 z-50 mt-2 rounded-md border bg-popover p-0 text-popover-foreground shadow-md">
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={(date) => {
              setSelectedDate(date as Date);
              setOpen(false);
              if (onChange) {
                onChange(date ? (date as Date).toISOString() : undefined);
              }
            }}
          />
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
  value?: string;
  placeholder?: string;
  searchPlaceholder?: string;
  emptyText?: string;
  disabled?: boolean;
  onSelect?: (value: string) => void;
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
  disabled = false,
  onSelect,
  'data-refast-id': dataRefastId,
}: ComboboxProps): React.ReactElement {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');

  const filteredOptions = options.filter((option) =>
    option.label?.toLowerCase().includes(search.toLowerCase()) ?? false
  );

  const selectedOption = options.find((opt) => opt.value === value);

  return (
    <div className={cn('relative', className)} data-refast-id={dataRefastId}>
      <button
        id={id}
        type="button"
        disabled={disabled}
        onClick={() => setOpen(!open)}
        className={cn(
          'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm',
          'ring-offset-background placeholder:text-muted-foreground',
          'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50'
        )}
      >
        <span className={!selectedOption ? 'text-muted-foreground' : ''}>
          {selectedOption?.label || placeholder}
        </span>
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
              filteredOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => {
                    if (onSelect) onSelect(option.value);
                    setOpen(false);
                    setSearch('');
                  }}
                  className={cn(
                    'relative flex w-full cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
                    'hover:bg-accent hover:text-accent-foreground',
                    option.value === value && 'bg-accent text-accent-foreground'
                  )}
                >
                  {option.value === value && (
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
                  <span className={option.value !== value ? 'pl-6' : ''}>
                    {option.label}
                  </span>
                </button>
              ))
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
