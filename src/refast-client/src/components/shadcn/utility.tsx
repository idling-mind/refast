/**
 * Utility Components using Radix UI primitives
 * Separator, AspectRatio, ScrollArea, Collapsible, Carousel, Resizable, InputOTP
 */

import * as React from 'react';
import * as SeparatorPrimitive from '@radix-ui/react-separator';
import * as AspectRatioPrimitive from '@radix-ui/react-aspect-ratio';
import * as ScrollAreaPrimitive from '@radix-ui/react-scroll-area';
import * as CollapsiblePrimitive from '@radix-ui/react-collapsible';
import * as ResizablePrimitive from "react-resizable-panels";
import { GripVertical } from "lucide-react";
import useEmblaCarousel from 'embla-carousel-react';
import { cn } from '../../utils';
import type { BaseProps, ChildrenProp } from './types';

// ============================================================================
// Separator
// ============================================================================

export interface SeparatorProps extends BaseProps {
  orientation?: 'horizontal' | 'vertical';
  decorative?: boolean;
}

export function Separator({
  orientation = 'horizontal',
  decorative = true,
  className,
  ...props
}: SeparatorProps) {
  return (
    <SeparatorPrimitive.Root
      decorative={decorative}
      orientation={orientation}
      className={cn(
        'shrink-0 bg-border',
        orientation === 'horizontal' ? 'h-[1px] w-full' : 'h-full w-[1px]',
        className
      )}
      {...props}
    />
  );
}

// ============================================================================
// AspectRatio
// ============================================================================

export interface AspectRatioProps extends BaseProps, ChildrenProp {
  ratio?: number;
}

export function AspectRatio({
  ratio = 16 / 9,
  className,
  children,
  ...props
}: AspectRatioProps) {
  return (
    <AspectRatioPrimitive.Root ratio={ratio} className={className} {...props}>
      {children}
    </AspectRatioPrimitive.Root>
  );
}

// ============================================================================
// ScrollArea
// ============================================================================

export interface ScrollAreaProps {
  className?: string;
  children?: React.ReactNode;
  type?: 'auto' | 'always' | 'scroll' | 'hover';
  scrollHideDelay?: number;
}

export function ScrollArea({
  type = 'hover',
  scrollHideDelay = 600,
  className,
  children,
}: ScrollAreaProps) {
  return (
    <ScrollAreaPrimitive.Root
      type={type}
      scrollHideDelay={scrollHideDelay}
      className={cn('relative overflow-hidden', className)}
    >
      <ScrollAreaPrimitive.Viewport className="h-full w-full rounded-[inherit]">
        {children}
      </ScrollAreaPrimitive.Viewport>
      <ScrollAreaPrimitive.Scrollbar
        orientation="vertical"
        className={cn(
          'flex touch-none select-none transition-colors',
          'h-full w-2.5 border-l border-l-transparent p-[1px]'
        )}
      >
        <ScrollAreaPrimitive.Thumb
          className={cn(
            'relative flex-1 rounded-full bg-border',
            'before:absolute before:left-1/2 before:top-1/2',
            'before:h-full before:min-h-[44px] before:w-full before:min-w-[44px]',
            'before:-translate-x-1/2 before:-translate-y-1/2 before:content-[""]'
          )}
        />
      </ScrollAreaPrimitive.Scrollbar>
      <ScrollAreaPrimitive.Scrollbar
        orientation="horizontal"
        className={cn(
          'flex touch-none select-none transition-colors',
          'h-2.5 flex-col border-t border-t-transparent p-[1px]'
        )}
      >
        <ScrollAreaPrimitive.Thumb
          className={cn(
            'relative flex-1 rounded-full bg-border',
            'before:absolute before:left-1/2 before:top-1/2',
            'before:h-full before:min-h-[44px] before:w-full before:min-w-[44px]',
            'before:-translate-x-1/2 before:-translate-y-1/2 before:content-[""]'
          )}
        />
      </ScrollAreaPrimitive.Scrollbar>
      <ScrollAreaPrimitive.Corner />
    </ScrollAreaPrimitive.Root>
  );
}

// ============================================================================
// Collapsible
// ============================================================================

export interface CollapsibleProps extends BaseProps, ChildrenProp {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  disabled?: boolean;
  trigger?: React.ReactNode;
}

export function Collapsible({
  open,
  defaultOpen,
  onOpenChange,
  disabled,
  trigger,
  className,
  children,
  ...props
}: CollapsibleProps) {
  // Compositional mode (no trigger provided)
  if (!trigger && children && React.Children.count(children) > 0) {
    return (
      <CollapsiblePrimitive.Root
        open={open}
        defaultOpen={defaultOpen}
        onOpenChange={onOpenChange}
        disabled={disabled}
        className={cn('space-y-2', className)}
        {...props}
      >
        {children}
      </CollapsiblePrimitive.Root>
    );
  }

  // High-level wrapper
  return (
    <CollapsiblePrimitive.Root
      open={open}
      defaultOpen={defaultOpen}
      onOpenChange={onOpenChange}
      disabled={disabled}
      className={cn('space-y-2', className)}
      {...props}
    >
      {trigger && (
        <CollapsiblePrimitive.Trigger asChild>
          {trigger}
        </CollapsiblePrimitive.Trigger>
      )}
      <CollapsiblePrimitive.Content
        className={cn(
          'overflow-hidden',
          'data-[state=closed]:animate-collapsible-up',
          'data-[state=open]:animate-collapsible-down'
        )}
      >
        {children}
      </CollapsiblePrimitive.Content>
    </CollapsiblePrimitive.Root>
  );
}

// ============================================================================
// Collapsible Compositional API
// ============================================================================

export interface CollapsibleTriggerProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function CollapsibleTrigger({
  asChild = true,
  className,
  children,
}: CollapsibleTriggerProps) {
  return (
    <CollapsiblePrimitive.Trigger asChild={asChild} className={className}>
      {children}
    </CollapsiblePrimitive.Trigger>
  );
}

export interface CollapsibleContentProps extends ChildrenProp {
  className?: string;
}

export function CollapsibleContent({
  className,
  children,
}: CollapsibleContentProps) {
  return (
    <CollapsiblePrimitive.Content
      className={cn(
        'overflow-hidden',
        'data-[state=closed]:animate-collapsible-up',
        'data-[state=open]:animate-collapsible-down',
        className
      )}
    >
      {children}
    </CollapsiblePrimitive.Content>
  );
}

// ============================================================================
// Carousel
// ============================================================================

type CarouselApi = ReturnType<typeof useEmblaCarousel>[1];

interface CarouselContextType {
  carouselRef: ReturnType<typeof useEmblaCarousel>[0];
  api: CarouselApi;
  scrollPrev: () => void;
  scrollNext: () => void;
  canScrollPrev: boolean;
  canScrollNext: boolean;
}

const CarouselContext = React.createContext<CarouselContextType | null>(null);

function useCarousel() {
  const context = React.useContext(CarouselContext);
  if (!context) {
    throw new Error('useCarousel must be used within a <Carousel />');
  }
  return context;
}

export interface CarouselProps extends BaseProps, ChildrenProp {
  orientation?: 'horizontal' | 'vertical';
  opts?: Parameters<typeof useEmblaCarousel>[0];
}

export function Carousel({
  orientation = 'horizontal',
  opts,
  className,
  children,
  ...props
}: CarouselProps) {
  const [carouselRef, api] = useEmblaCarousel({
    ...opts,
    axis: orientation === 'horizontal' ? 'x' : 'y',
  });
  const [canScrollPrev, setCanScrollPrev] = React.useState(false);
  const [canScrollNext, setCanScrollNext] = React.useState(false);

  const onSelect = React.useCallback((api: CarouselApi) => {
    if (!api) return;
    setCanScrollPrev(api.canScrollPrev());
    setCanScrollNext(api.canScrollNext());
  }, []);

  const scrollPrev = React.useCallback(() => {
    api?.scrollPrev();
  }, [api]);

  const scrollNext = React.useCallback(() => {
    api?.scrollNext();
  }, [api]);

  React.useEffect(() => {
    if (!api) return;
    onSelect(api);
    api.on('reInit', onSelect);
    api.on('select', onSelect);
    return () => {
      api?.off('select', onSelect);
    };
  }, [api, onSelect]);

  return (
    <CarouselContext.Provider
      value={{
        carouselRef,
        api,
        scrollPrev,
        scrollNext,
        canScrollPrev,
        canScrollNext,
      }}
    >
      <div
        className={cn('relative', className)}
        role="region"
        aria-roledescription="carousel"
        {...props}
      >
        {children}
      </div>
    </CarouselContext.Provider>
  );
}

export interface CarouselContentProps extends BaseProps, ChildrenProp {}

export function CarouselContent({
  className,
  children,
  ...props
}: CarouselContentProps) {
  const { carouselRef } = useCarousel();

  return (
    <div ref={carouselRef} className="overflow-hidden">
      <div className={cn('flex', className)} {...props}>
        {children}
      </div>
    </div>
  );
}

export interface CarouselItemProps extends BaseProps, ChildrenProp {}

export function CarouselItem({
  className,
  children,
  ...props
}: CarouselItemProps) {
  return (
    <div
      role="group"
      aria-roledescription="slide"
      className={cn('min-w-0 shrink-0 grow-0 basis-full', className)}
      {...props}
    >
      {children}
    </div>
  );
}

export interface CarouselPreviousProps extends BaseProps {
  onClick?: () => void;
}

export function CarouselPrevious({
  className,
  onClick,
  ...props
}: CarouselPreviousProps) {
  const { scrollPrev, canScrollPrev } = useCarousel();

  return (
    <button
      type="button"
      className={cn(
        'absolute left-2 top-1/2 -translate-y-1/2 z-10',
        'inline-flex h-8 w-8 items-center justify-center rounded-full',
        'border bg-background shadow-sm',
        'disabled:pointer-events-none disabled:opacity-50',
        'hover:bg-accent hover:text-accent-foreground',
        className
      )}
      disabled={!canScrollPrev}
      onClick={() => {
        scrollPrev();
        onClick?.();
      }}
      {...props}
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
        className="h-4 w-4"
      >
        <polyline points="15 18 9 12 15 6" />
      </svg>
      <span className="sr-only">Previous slide</span>
    </button>
  );
}

export interface CarouselNextProps extends BaseProps {
  onClick?: () => void;
}

export function CarouselNext({
  className,
  onClick,
  ...props
}: CarouselNextProps) {
  const { scrollNext, canScrollNext } = useCarousel();

  return (
    <button
      type="button"
      className={cn(
        'absolute right-2 top-1/2 -translate-y-1/2 z-10',
        'inline-flex h-8 w-8 items-center justify-center rounded-full',
        'border bg-background shadow-sm',
        'disabled:pointer-events-none disabled:opacity-50',
        'hover:bg-accent hover:text-accent-foreground',
        className
      )}
      disabled={!canScrollNext}
      onClick={() => {
        scrollNext();
        onClick?.();
      }}
      {...props}
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
        className="h-4 w-4"
      >
        <polyline points="9 18 15 12 9 6" />
      </svg>
      <span className="sr-only">Next slide</span>
    </button>
  );
}

// ============================================================================
// Resizable
// ============================================================================

export function ResizablePanelGroup({
  className,
  ...props
}: React.ComponentProps<typeof ResizablePrimitive.PanelGroup> & BaseProps) {
  return (
    <ResizablePrimitive.PanelGroup
      className={cn(
        "flex h-full w-full data-[panel-group-direction=vertical]:flex-col",
        className
      )}
      {...props}
    />
  )
}

export function ResizablePanel({
  className,
  defaultSize,
  minSize,
  maxSize,
  ...props
}: React.ComponentProps<typeof ResizablePrimitive.Panel> & BaseProps) {
  // Convert nulls (from Python None) to undefined so library defaults apply
  return (
    <ResizablePrimitive.Panel
      className={cn(className)}
      defaultSize={defaultSize ?? undefined}
      minSize={minSize ?? undefined}
      maxSize={maxSize ?? undefined}
      {...props}
    />
  )
}

export type ResizableHandleProps = React.ComponentProps<typeof ResizablePrimitive.PanelResizeHandle> & {
  withHandle?: boolean
} & BaseProps

export function ResizableHandle({
  withHandle,
  className,
  ...props
}: ResizableHandleProps) {
  return (
    <ResizablePrimitive.PanelResizeHandle
      className={cn(
        "relative flex w-px items-center justify-center bg-border after:absolute after:inset-y-0 after:left-1/2 after:w-1 after:-translate-x-1/2 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-1 data-[panel-group-direction=vertical]:h-px data-[panel-group-direction=vertical]:w-full data-[panel-group-direction=vertical]:after:left-0 data-[panel-group-direction=vertical]:after:h-1 data-[panel-group-direction=vertical]:after:w-full data-[panel-group-direction=vertical]:after:-translate-y-1/2 data-[panel-group-direction=vertical]:after:translate-x-0 [&[data-panel-group-direction=vertical]>div]:rotate-90",
        className
      )}
      {...props}
    >
      {withHandle && (
        <div className="z-10 flex h-4 w-3 items-center justify-center rounded-sm border bg-border">
          <GripVertical className="h-2.5 w-2.5" />
        </div>
      )}
    </ResizablePrimitive.PanelResizeHandle>
  )
}

// ============================================================================
// InputOTP
// ============================================================================

export interface InputOTPProps {
  className?: string;
  maxLength?: number;
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
  pattern?: string;
  autoFocus?: boolean;
}

export function InputOTP({
  maxLength = 6,
  value = '',
  onChange,
  disabled,
  pattern = '^[0-9]+$',
  autoFocus,
  className,
}: InputOTPProps) {
  const inputRefs = React.useRef<(HTMLInputElement | null)[]>([]);
  const [values, setValues] = React.useState<string[]>(
    value.split('').concat(Array(maxLength - value.length).fill(''))
  );

  const handleChange = (index: number, newValue: string) => {
    const regex = new RegExp(pattern);
    if (newValue && !regex.test(newValue)) return;

    const newValues = [...values];
    newValues[index] = newValue.slice(-1);
    setValues(newValues);

    const combinedValue = newValues.join('');
    onChange?.(combinedValue);

    // Move to next input
    if (newValue && index < maxLength - 1) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !values[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
    if (e.key === 'ArrowLeft' && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
    if (e.key === 'ArrowRight' && index < maxLength - 1) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').slice(0, maxLength);
    const regex = new RegExp(pattern);
    
    if (regex.test(pastedData)) {
      const newValues = pastedData
        .split('')
        .concat(Array(maxLength - pastedData.length).fill(''));
      setValues(newValues);
      onChange?.(pastedData);
      inputRefs.current[Math.min(pastedData.length, maxLength - 1)]?.focus();
    }
  };

  return (
    <div
      className={cn('flex items-center gap-2', className)}
    >
      {Array.from({ length: maxLength }).map((_, index) => (
        <React.Fragment key={index}>
          <input
            ref={(el) => (inputRefs.current[index] = el)}
            type="text"
            inputMode="numeric"
            autoComplete="one-time-code"
            disabled={disabled}
            autoFocus={autoFocus && index === 0}
            value={values[index]}
            onChange={(e) => handleChange(index, e.target.value)}
            onKeyDown={(e) => handleKeyDown(index, e)}
            onPaste={handlePaste}
            className={cn(
              'h-10 w-10 text-center text-sm font-medium',
              'rounded-md border border-input bg-background',
              'ring-offset-background transition-all',
              'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
              'disabled:cursor-not-allowed disabled:opacity-50'
            )}
          />
          {index === 2 && maxLength > 3 && (
            <div className="text-muted-foreground">-</div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}

export interface InputOTPGroupProps extends BaseProps, ChildrenProp {}

export function InputOTPGroup({
  className,
  children,
  ...props
}: InputOTPGroupProps) {
  return (
    <div className={cn('flex items-center', className)} {...props}>
      {children}
    </div>
  );
}

export interface InputOTPSlotProps extends BaseProps {
  index: number;
  char?: string;
  hasFakeCaret?: boolean;
  isActive?: boolean;
}

export function InputOTPSlot({
  index,
  char,
  hasFakeCaret,
  isActive,
  className,
  ...props
}: InputOTPSlotProps) {
  return (
    <div
      className={cn(
        'relative flex h-10 w-10 items-center justify-center',
        'border-y border-r border-input text-sm transition-all',
        'first:rounded-l-md first:border-l last:rounded-r-md',
        isActive && 'z-10 ring-2 ring-ring ring-offset-background',
        className
      )}
      {...props}
    >
      {char}
      {hasFakeCaret && (
        <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
          <div className="h-4 w-px animate-caret-blink bg-foreground duration-1000" />
        </div>
      )}
    </div>
  );
}

export interface InputOTPSeparatorProps extends BaseProps {}

export function InputOTPSeparator({
  className,
  ...props
}: InputOTPSeparatorProps) {
  return (
    <div
      role="separator"
      className={cn('flex items-center text-muted-foreground', className)}
      {...props}
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
        className="h-4 w-4"
      >
        <circle cx="12" cy="12" r="1" />
      </svg>
    </div>
  );
}

// ============================================================================
// ThemeSwitcher
// ============================================================================

type Theme = 'light' | 'dark' | 'system';

export interface ThemeSwitcherProps extends Omit<BaseProps, 'onChange'> {
  defaultTheme?: Theme;
  storageKey?: string;
  showSystemOption?: boolean;
  mode?: 'toggle' | 'dropdown';
  onChange?: (theme: Theme) => void;
}

// Sun icon component
function SunIcon({ className }: { className?: string }) {
  return (
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
      className={className}
    >
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2" />
      <path d="M12 20v2" />
      <path d="m4.93 4.93 1.41 1.41" />
      <path d="m17.66 17.66 1.41 1.41" />
      <path d="M2 12h2" />
      <path d="M20 12h2" />
      <path d="m6.34 17.66-1.41 1.41" />
      <path d="m19.07 4.93-1.41 1.41" />
    </svg>
  );
}

// Moon icon component
function MoonIcon({ className }: { className?: string }) {
  return (
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
      className={className}
    >
      <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
    </svg>
  );
}

// Monitor icon component for system theme
function MonitorIcon({ className }: { className?: string }) {
  return (
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
      className={className}
    >
      <rect width="20" height="14" x="2" y="3" rx="2" />
      <line x1="8" x2="16" y1="21" y2="21" />
      <line x1="12" x2="12" y1="17" y2="21" />
    </svg>
  );
}

/**
 * Get the effective theme based on system preference
 */
function getSystemTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * Apply theme to the document
 */
function applyTheme(theme: Theme) {
  if (typeof document === 'undefined') return;
  
  const effectiveTheme = theme === 'system' ? getSystemTheme() : theme;
  const root = document.documentElement;
  
  root.classList.remove('light', 'dark');
  root.classList.add(effectiveTheme);
}

export function ThemeSwitcher({
  defaultTheme = 'system',
  storageKey = 'refast-theme',
  showSystemOption = true,
  mode = 'toggle',
  onChange,
  className,
  ...props
}: ThemeSwitcherProps) {
  const [theme, setThemeState] = React.useState<Theme>(() => {
    // Try to get from localStorage
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem(storageKey) as Theme | null;
      if (stored && ['light', 'dark', 'system'].includes(stored)) {
        return stored;
      }
    }
    return defaultTheme;
  });
  
  const [mounted, setMounted] = React.useState(false);

  // Apply theme on mount and when theme changes
  React.useEffect(() => {
    setMounted(true);
    applyTheme(theme);
  }, [theme]);

  // Listen for system theme changes
  React.useEffect(() => {
    if (theme !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => applyTheme('system');

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);

  const setTheme = React.useCallback((newTheme: Theme) => {
    setThemeState(newTheme);
    if (typeof window !== 'undefined') {
      localStorage.setItem(storageKey, newTheme);
    }
    onChange?.(newTheme);
  }, [storageKey, onChange]);

  // Toggle between light and dark (for toggle mode)
  const toggleTheme = React.useCallback(() => {
    const currentEffective = theme === 'system' ? getSystemTheme() : theme;
    const newTheme = currentEffective === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
  }, [theme, setTheme]);

  // Get current effective theme for display
  const effectiveTheme = theme === 'system' ? getSystemTheme() : theme;

  // Prevent hydration mismatch
  if (!mounted) {
    return (
      <button
        className={cn(
          'inline-flex h-10 w-10 items-center justify-center rounded-md border border-input bg-background',
          'text-sm font-medium ring-offset-background transition-colors',
          'hover:bg-accent hover:text-accent-foreground',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',
          className
        )}
        disabled
        {...props}
      >
        <span className="h-5 w-5" />
      </button>
    );
  }

  if (mode === 'toggle') {
    return (
      <button
        type="button"
        onClick={toggleTheme}
        className={cn(
          'inline-flex h-10 w-10 items-center justify-center rounded-md border border-input bg-background',
          'text-sm font-medium ring-offset-background transition-colors',
          'hover:bg-accent hover:text-accent-foreground',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:pointer-events-none disabled:opacity-50',
          className
        )}
        aria-label={`Switch to ${effectiveTheme === 'light' ? 'dark' : 'light'} theme`}
        {...props}
      >
        {effectiveTheme === 'light' ? (
          <SunIcon className="h-5 w-5" />
        ) : (
          <MoonIcon className="h-5 w-5" />
        )}
      </button>
    );
  }

  // Dropdown mode
  const [isOpen, setIsOpen] = React.useState(false);
  
  return (
    <div className={cn('relative', className)} {...props}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={cn(
          'inline-flex h-10 w-10 items-center justify-center rounded-md border border-input bg-background',
          'text-sm font-medium ring-offset-background transition-colors',
          'hover:bg-accent hover:text-accent-foreground',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2'
        )}
        aria-label="Select theme"
        aria-expanded={isOpen}
        aria-haspopup="menu"
      >
        {effectiveTheme === 'light' ? (
          <SunIcon className="h-5 w-5" />
        ) : (
          <MoonIcon className="h-5 w-5" />
        )}
      </button>
      
      {isOpen && (
        <>
          {/* Backdrop to close on click outside */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          
          <div
            className={cn(
              'absolute right-0 top-full z-50 mt-2 min-w-[8rem]',
              'rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
              'animate-in fade-in-0 zoom-in-95'
            )}
            role="menu"
          >
            <button
              type="button"
              onClick={() => {
                setTheme('light');
                setIsOpen(false);
              }}
              className={cn(
                'relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none',
                'hover:bg-accent hover:text-accent-foreground',
                theme === 'light' && 'bg-accent'
              )}
              role="menuitem"
            >
              <SunIcon className="h-4 w-4" />
              Light
            </button>
            
            <button
              type="button"
              onClick={() => {
                setTheme('dark');
                setIsOpen(false);
              }}
              className={cn(
                'relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none',
                'hover:bg-accent hover:text-accent-foreground',
                theme === 'dark' && 'bg-accent'
              )}
              role="menuitem"
            >
              <MoonIcon className="h-4 w-4" />
              Dark
            </button>
            
            {showSystemOption && (
              <button
                type="button"
                onClick={() => {
                  setTheme('system');
                  setIsOpen(false);
                }}
                className={cn(
                  'relative flex w-full cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none',
                  'hover:bg-accent hover:text-accent-foreground',
                  theme === 'system' && 'bg-accent'
                )}
                role="menuitem"
              >
                <MonitorIcon className="h-4 w-4" />
                System
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
}

// ============================================================================
// Export all
// ============================================================================

export const UtilityComponents = {
  Separator,
  AspectRatio,
  ScrollArea,
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent,
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
  InputOTPSeparator,
  ThemeSwitcher,
};
