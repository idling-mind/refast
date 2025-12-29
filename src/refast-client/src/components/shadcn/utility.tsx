/**
 * Utility Components using Radix UI primitives
 * Separator, AspectRatio, ScrollArea, Collapsible, Carousel, Resizable, InputOTP
 */

import * as React from 'react';
import * as SeparatorPrimitive from '@radix-ui/react-separator';
import * as AspectRatioPrimitive from '@radix-ui/react-aspect-ratio';
import * as ScrollAreaPrimitive from '@radix-ui/react-scroll-area';
import * as CollapsiblePrimitive from '@radix-ui/react-collapsible';
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

export interface ResizableProps extends BaseProps, ChildrenProp {
  direction?: 'horizontal' | 'vertical';
}

export function Resizable({
  direction = 'horizontal',
  className,
  children,
  ...props
}: ResizableProps) {
  return (
    <div
      className={cn(
        'flex h-full w-full',
        direction === 'vertical' ? 'flex-col' : 'flex-row',
        className
      )}
      data-panel-group
      data-panel-group-direction={direction}
      {...props}
    >
      {children}
    </div>
  );
}

export interface ResizablePanelProps extends BaseProps, ChildrenProp {
  defaultSize?: number;
  minSize?: number;
  maxSize?: number;
}

export function ResizablePanel({
  defaultSize = 50,
  minSize = 10,
  maxSize = 90,
  className,
  children,
  ...props
}: ResizablePanelProps) {
  return (
    <div
      className={cn('flex-1', className)}
      data-panel
      data-panel-size={defaultSize}
      data-panel-min-size={minSize}
      data-panel-max-size={maxSize}
      style={{ flexBasis: `${defaultSize}%` }}
      {...props}
    >
      {children}
    </div>
  );
}

export interface ResizableHandleProps extends BaseProps {
  withHandle?: boolean;
}

export function ResizableHandle({
  withHandle = false,
  className,
  ...props
}: ResizableHandleProps) {
  return (
    <div
      className={cn(
        'relative flex w-px items-center justify-center bg-border',
        'after:absolute after:inset-y-0 after:left-1/2 after:w-1 after:-translate-x-1/2',
        'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-1',
        'data-[panel-group-direction=vertical]:h-px data-[panel-group-direction=vertical]:w-full',
        'data-[panel-group-direction=vertical]:after:left-0 data-[panel-group-direction=vertical]:after:h-1',
        'data-[panel-group-direction=vertical]:after:w-full data-[panel-group-direction=vertical]:after:-translate-y-1/2',
        'data-[panel-group-direction=vertical]:after:translate-x-0',
        className
      )}
      data-panel-resize-handle
      {...props}
    >
      {withHandle && (
        <div
          className={cn(
            'z-10 flex h-4 w-3 items-center justify-center rounded-sm border bg-border'
          )}
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
            className="h-2.5 w-2.5"
          >
            <circle cx="12" cy="5" r="1" />
            <circle cx="12" cy="12" r="1" />
            <circle cx="12" cy="19" r="1" />
          </svg>
        </div>
      )}
    </div>
  );
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
// Export all
// ============================================================================

export const UtilityComponents = {
  Separator,
  AspectRatio,
  ScrollArea,
  Collapsible,
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
  Resizable,
  ResizablePanel,
  ResizableHandle,
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
  InputOTPSeparator,
};
