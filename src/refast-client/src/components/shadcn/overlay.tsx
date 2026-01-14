/**
 * Overlay Components using Radix UI primitives
 * Dialog, Sheet, Drawer, HoverCard, Popover
 */

import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import * as PopoverPrimitive from '@radix-ui/react-popover';
import * as HoverCardPrimitive from '@radix-ui/react-hover-card';
import { cn } from '../../utils';
import type { BaseProps, ChildrenProp } from './types';
import { Icon } from './icon';

// ============================================================================
// Dialog
// ============================================================================

export interface DialogProps extends BaseProps, ChildrenProp {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  title?: string;
  description?: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm?: () => void;
  onCancel?: () => void;
  trigger?: React.ReactNode;
  variant?: 'default' | 'destructive';
}

export function Dialog({
  open,
  onOpenChange,
  title,
  description,
  confirmLabel = 'Continue',
  cancelLabel = 'Cancel',
  onConfirm,
  onCancel,
  trigger,
  variant = 'default',
  className,
  children,
  ...props
}: DialogProps) {
  // Compositional API usage (when trigger is not provided prop but likely in children)
  if (!trigger && children && React.Children.count(children) > 0) {
    return (
      <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
        {children}
      </DialogPrimitive.Root>
    );
  }

  // High-level API usage
  const handleConfirm = () => {
    onConfirm?.();
    onOpenChange?.(false);
  };

  const handleCancel = () => {
    onCancel?.();
    onOpenChange?.(false);
  };

  return (
    <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
      {trigger && (
        <DialogPrimitive.Trigger asChild>
          {trigger}
        </DialogPrimitive.Trigger>
      )}
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay
          className={cn(
            'fixed inset-0 z-50 bg-black/80',
            'data-[state=open]:animate-in data-[state=closed]:animate-out',
            'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0'
          )}
        />
        <DialogPrimitive.Content
          className={cn(
            'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4',
            'border bg-background p-6 shadow-lg duration-200',
            'data-[state=open]:animate-in data-[state=closed]:animate-out',
            'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
            'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
            'data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]',
            'data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]',
            'sm:rounded-lg',
            className
          )}
          {...props}
        >
          <div className="flex flex-col space-y-2 text-center sm:text-left">
            {title && (
              <DialogPrimitive.Title className="text-lg font-semibold">
                {title}
              </DialogPrimitive.Title>
            )}
            {description && (
              <DialogPrimitive.Description className="text-sm text-muted-foreground">
                {description}
              </DialogPrimitive.Description>
            )}
          </div>
          {children}
          <div className="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2">
            <button
              type="button"
              onClick={handleCancel}
              className={cn(
                'inline-flex h-10 items-center justify-center rounded-md px-4 py-2',
                'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
                'text-sm font-medium ring-offset-background transition-colors',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:pointer-events-none disabled:opacity-50',
                'mt-2 sm:mt-0'
              )}
            >
              {cancelLabel}
            </button>
            <button
              type="button"
              onClick={handleConfirm}
              className={cn(
                'inline-flex h-10 items-center justify-center rounded-md px-4 py-2',
                'text-sm font-medium ring-offset-background transition-colors',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:pointer-events-none disabled:opacity-50',
                variant === 'destructive'
                  ? 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
                  : 'bg-primary text-primary-foreground hover:bg-primary/90'
              )}
            >
              {confirmLabel}
            </button>
          </div>
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
}

// ============================================================================
// Dialog (Compositional API)
// ============================================================================

export interface DialogTriggerProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function DialogTrigger({
  asChild = true,
  className,
  children,
}: DialogTriggerProps) {
  const childrenArray = React.Children.toArray(children);
  const singleChild = childrenArray.length === 1 ? childrenArray[0] : null;
  const shouldUseAsChild = asChild && !!singleChild;

  return (
    <DialogPrimitive.Trigger asChild={shouldUseAsChild} className={className}>
      {shouldUseAsChild ? singleChild : children}
    </DialogPrimitive.Trigger>
  );
}

export interface DialogContentProps extends ChildrenProp {
  className?: string;
}

export function DialogContent({
  className,
  children,
}: DialogContentProps) {
  return (
    <DialogPrimitive.Portal>
      <DialogPrimitive.Overlay
        className={cn(
          'fixed inset-0 z-50 bg-black/80',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0'
        )}
      />
      <DialogPrimitive.Content
        className={cn(
          'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4',
          'border bg-background p-6 shadow-lg duration-200',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%]',
          'data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]',
          'sm:rounded-lg',
          className
        )}
      >
        {children}
      </DialogPrimitive.Content>
    </DialogPrimitive.Portal>
  );
}

export interface DialogHeaderProps extends ChildrenProp {
  className?: string;
}

export function DialogHeader({
  className,
  children,
}: DialogHeaderProps) {
  return (
    <div className={cn('flex flex-col space-y-2 text-center sm:text-left', className)}>
      {children}
    </div>
  );
}

export interface DialogFooterProps extends ChildrenProp {
  className?: string;
}

export function DialogFooter({
  className,
  children,
}: DialogFooterProps) {
  return (
    <div className={cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)}>
      {children}
    </div>
  );
}

export interface DialogTitleProps extends ChildrenProp {
  title?: string;
  className?: string;
}

export function DialogTitle({
  title,
  className,
  children,
}: DialogTitleProps) {
  return (
    <DialogPrimitive.Title className={cn('text-lg font-semibold', className)}>
      {title || children}
    </DialogPrimitive.Title>
  );
}

export interface DialogDescriptionProps extends ChildrenProp {
  description?: string;
  className?: string;
}

export function DialogDescription({
  description,
  className,
  children,
}: DialogDescriptionProps) {
  return (
    <DialogPrimitive.Description className={cn('text-sm text-muted-foreground', className)}>
      {description || children}
    </DialogPrimitive.Description>
  );
}

export interface DialogActionProps extends ChildrenProp {
  label?: string;
  onClick?: () => void;
  className?: string;
}

export function DialogAction({
  label,
  onClick,
  className,
  children,
}: DialogActionProps) {
  return (
    <DialogPrimitive.Close
      onClick={onClick}
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md px-4 py-2',
        'bg-primary text-primary-foreground hover:bg-primary/90',
        'text-sm font-medium ring-offset-background transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        className
      )}
    >
      {label || children}
    </DialogPrimitive.Close>
  );
}

export interface DialogCancelProps extends ChildrenProp {
  label?: string;
  onClick?: () => void;
  className?: string;
}

export function DialogCancel({
  label,
  onClick,
  className,
  children,
}: DialogCancelProps) {
  return (
    <DialogPrimitive.Close
      onClick={onClick}
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md px-4 py-2',
        'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        'text-sm font-medium ring-offset-background transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        'mt-2 sm:mt-0',
        className
      )}
    >
      {label || children}
    </DialogPrimitive.Close>
  );
}

// ============================================================================
// Sheet (Compositional API)
// ============================================================================

import * as SheetPrimitive from '@radix-ui/react-dialog';

export interface SheetProps extends ChildrenProp {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function Sheet({
  open,
  defaultOpen = false,
  onOpenChange,
  children,
}: SheetProps) {
  return (
    <SheetPrimitive.Root
      open={open ?? undefined}
      defaultOpen={defaultOpen}
      onOpenChange={onOpenChange}
    >
      {children}
    </SheetPrimitive.Root>
  );
}

export interface SheetTriggerProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function SheetTrigger({
  asChild = false,
  className,
  children,
}: SheetTriggerProps) {
  const childrenArray = React.Children.toArray(children);
  const singleChild = childrenArray.length === 1 ? childrenArray[0] : null;
  
  // When asChild is false, Radix renders its own button element
  // When asChild is true, we need to ensure we have a proper element to clone into
  if (asChild && singleChild) {
    return (
      <SheetPrimitive.Trigger asChild className={className}>
        {singleChild}
      </SheetPrimitive.Trigger>
    );
  }
  
  // Render as a native button that contains the children
  return (
    <SheetPrimitive.Trigger className={cn('inline-flex', className)}>
      {children}
    </SheetPrimitive.Trigger>
  );
}

export interface SheetCloseProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function SheetClose({
  asChild = true,
  className,
  children,
}: SheetCloseProps) {
  return (
    <SheetPrimitive.Close asChild={asChild} className={className}>
      {children}
    </SheetPrimitive.Close>
  );
}

export interface SheetContentProps extends ChildrenProp {
  side?: 'top' | 'right' | 'bottom' | 'left';
  className?: string;
}

export function SheetContent({
  side = 'right',
  className,
  children,
}: SheetContentProps) {
  const sideClasses = {
    top: 'inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top',
    bottom: 'inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom',
    left: 'inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm',
    right: 'inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm',
  };

  return (
    <SheetPrimitive.Portal>
      <SheetPrimitive.Overlay
        className={cn(
          'fixed inset-0 z-50 bg-black/80',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0'
        )}
      />
      <SheetPrimitive.Content
        className={cn(
          'fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:duration-300 data-[state=open]:duration-500',
          sideClasses[side],
          className
        )}
      >
        {children}
        <SheetPrimitive.Close
          className={cn(
            'absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity',
            'hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
            'disabled:pointer-events-none data-[state=open]:bg-secondary'
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
            className="h-4 w-4"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
          <span className="sr-only">Close</span>
        </SheetPrimitive.Close>
      </SheetPrimitive.Content>
    </SheetPrimitive.Portal>
  );
}

export interface SheetHeaderProps extends ChildrenProp {
  className?: string;
}

export function SheetHeader({
  className,
  children,
}: SheetHeaderProps) {
  return (
    <div className={cn('flex flex-col space-y-2 text-center sm:text-left', className)}>
      {children}
    </div>
  );
}

export interface SheetFooterProps extends ChildrenProp {
  className?: string;
}

export function SheetFooter({
  className,
  children,
}: SheetFooterProps) {
  return (
    <div className={cn('flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2', className)}>
      {children}
    </div>
  );
}

export interface SheetTitleProps extends ChildrenProp {
  title?: string;
  className?: string;
}

export function SheetTitle({
  title,
  className,
  children,
}: SheetTitleProps) {
  return (
    <SheetPrimitive.Title className={cn('text-lg font-semibold text-foreground', className)}>
      {title || children}
    </SheetPrimitive.Title>
  );
}

export interface SheetDescriptionProps extends ChildrenProp {
  description?: string;
  className?: string;
}

export function SheetDescription({
  description,
  className,
  children,
}: SheetDescriptionProps) {
  return (
    <SheetPrimitive.Description className={cn('text-sm text-muted-foreground', className)}>
      {description || children}
    </SheetPrimitive.Description>
  );
}

// ============================================================================
// Drawer
// ============================================================================

export interface DrawerProps extends BaseProps, ChildrenProp {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  title?: string;
  description?: string;
  trigger?: React.ReactNode;
}

export function Drawer({
  open,
  onOpenChange,
  title,
  description,
  trigger,
  className,
  children,
  ...props
}: DrawerProps) {
  return (
    <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
      {trigger && (
        <DialogPrimitive.Trigger asChild>
          {trigger}
        </DialogPrimitive.Trigger>
      )}
      <DialogPrimitive.Portal>
        <DialogPrimitive.Overlay
          className={cn(
            'fixed inset-0 z-50 bg-black/80',
            'data-[state=open]:animate-in data-[state=closed]:animate-out',
            'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0'
          )}
        />
        <DialogPrimitive.Content
          className={cn(
            'fixed inset-x-0 bottom-0 z-50 mt-24 flex h-auto flex-col rounded-t-[10px] border bg-background',
            'data-[state=open]:animate-in data-[state=closed]:animate-out',
            'data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom',
            className
          )}
          {...props}
        >
          <div className="mx-auto mt-4 h-2 w-[100px] rounded-full bg-muted" />
          <div className="p-4">
            {title && (
              <DialogPrimitive.Title className="text-lg font-semibold text-foreground">
                {title}
              </DialogPrimitive.Title>
            )}
            {description && (
              <DialogPrimitive.Description className="text-sm text-muted-foreground">
                {description}
              </DialogPrimitive.Description>
            )}
          </div>
          <div className="p-4">{children}</div>
        </DialogPrimitive.Content>
      </DialogPrimitive.Portal>
    </DialogPrimitive.Root>
  );
}

// ============================================================================
// HoverCard
// ============================================================================

export interface HoverCardProps extends BaseProps, ChildrenProp {
  trigger?: React.ReactNode;
  openDelay?: number;
  closeDelay?: number;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
}

export function HoverCard({
  trigger,
  openDelay = 700,
  closeDelay = 300,
  side = 'bottom',
  align = 'center',
  className,
  children,
  ...props
}: HoverCardProps) {
  // Compositional API (when trigger is missing)
  if (!trigger && children && React.Children.count(children) > 0) {
    return (
      <HoverCardPrimitive.Root openDelay={openDelay} closeDelay={closeDelay}>
        {children}
      </HoverCardPrimitive.Root>
    );
  }

  // High-level wrapper
  return (
    <HoverCardPrimitive.Root openDelay={openDelay} closeDelay={closeDelay}>
      <HoverCardPrimitive.Trigger asChild>
        {trigger}
      </HoverCardPrimitive.Trigger>
      <HoverCardPrimitive.Content
        side={side}
        align={align}
        sideOffset={4}
        className={cn(
          'z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
          'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className
        )}
        {...props}
      >
        {children}
      </HoverCardPrimitive.Content>
    </HoverCardPrimitive.Root>
  );
}

// ============================================================================
// Popover
// ============================================================================

export interface PopoverProps extends BaseProps, ChildrenProp {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  trigger: React.ReactNode;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
}

export function Popover({
  open,
  onOpenChange,
  trigger,
  side = 'bottom',
  align = 'center',
  className,
  children,
  ...props
}: PopoverProps) {
  // Compositional API usage (when trigger is not provided prop)
  if (!trigger && children && React.Children.count(children) > 0) {
    return (
      <PopoverPrimitive.Root open={open} onOpenChange={onOpenChange}>
        {children}
      </PopoverPrimitive.Root>
    );
  }

  // High-level wrapper
  return (
    <PopoverPrimitive.Root open={open} onOpenChange={onOpenChange}>
      <PopoverPrimitive.Trigger asChild>
        {trigger}
      </PopoverPrimitive.Trigger>
      <PopoverPrimitive.Portal>
        <PopoverPrimitive.Content
          side={side}
          align={align}
          sideOffset={4}
          className={cn(
            'z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none',
            'data-[state=open]:animate-in data-[state=closed]:animate-out',
            'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
            'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
            'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
            'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
            className
          )}
          {...props}
        >
          {children}
          <PopoverPrimitive.Arrow className="fill-popover" />
        </PopoverPrimitive.Content>
      </PopoverPrimitive.Portal>
    </PopoverPrimitive.Root>
  );
}

// ============================================================================
// HoverCard Compositional API
// ============================================================================

export interface HoverCardTriggerProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function HoverCardTrigger({
  asChild = true,
  className,
  children,
}: HoverCardTriggerProps) {
  const childrenArray = React.Children.toArray(children);
  const singleChild = childrenArray.length === 1 ? childrenArray[0] : null;
  const shouldUseAsChild = asChild && !!singleChild;

  return (
    <HoverCardPrimitive.Trigger asChild={shouldUseAsChild} className={className}>
      {shouldUseAsChild ? singleChild : children}
    </HoverCardPrimitive.Trigger>
  );
}

export interface HoverCardContentProps extends ChildrenProp {
  className?: string;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
  sideOffset?: number;
}

export function HoverCardContent({
  className,
  side = 'bottom',
  align = 'center',
  sideOffset = 4,
  children,
}: HoverCardContentProps) {
  return (
    <HoverCardPrimitive.Content
      side={side}
      align={align}
      sideOffset={sideOffset}
      className={cn(
        'z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none',
        'data-[state=open]:animate-in data-[state=closed]:animate-out',
        'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
        'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
        'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
        'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
        className
      )}
    >
      {children}
    </HoverCardPrimitive.Content>
  );
}

// ============================================================================
// Popover Compositional API
// ============================================================================

export interface PopoverTriggerProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function PopoverTrigger({
  asChild = true,
  className,
  children,
}: PopoverTriggerProps) {
  const childrenArray = React.Children.toArray(children);
  const singleChild = childrenArray.length === 1 ? childrenArray[0] : null;
  const shouldUseAsChild = asChild && !!singleChild;

  return (
    <PopoverPrimitive.Trigger asChild={shouldUseAsChild} className={className}>
      {shouldUseAsChild ? singleChild : children}
    </PopoverPrimitive.Trigger>
  );
}

export interface PopoverContentProps extends ChildrenProp {
  className?: string;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
  sideOffset?: number;
}

export function PopoverContent({
  className,
  side = 'bottom',
  align = 'center',
  sideOffset = 4,
  children,
}: PopoverContentProps) {
  return (
    <PopoverPrimitive.Portal>
      <PopoverPrimitive.Content
        side={side}
        align={align}
        sideOffset={sideOffset}
        className={cn(
          'z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
          'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className
        )}
      >
        {children}
      </PopoverPrimitive.Content>
    </PopoverPrimitive.Portal>
  );
}

// ============================================================================
// DropdownMenu Components
// ============================================================================

import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';

export interface DropdownMenuProps extends ChildrenProp {
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function DropdownMenu({
  open,
  defaultOpen = false,
  onOpenChange,
  children,
}: DropdownMenuProps) {
  return (
    <DropdownMenuPrimitive.Root
      open={open ?? undefined}
      defaultOpen={defaultOpen}
      onOpenChange={onOpenChange}
    >
      {children}
    </DropdownMenuPrimitive.Root>
  );
}

export interface DropdownMenuTriggerProps extends BaseProps, ChildrenProp {
  asChild?: boolean;
}

export function DropdownMenuTrigger({
  asChild = false,
  className,
  children,
}: DropdownMenuTriggerProps) {
  const childrenArray = React.Children.toArray(children);
  const singleChild = childrenArray.length === 1 ? childrenArray[0] : null;

  // When asChild is false, Radix renders its own button element
  if (asChild && singleChild) {
    return (
      <DropdownMenuPrimitive.Trigger asChild className={className}>
        {singleChild}
      </DropdownMenuPrimitive.Trigger>
    );
  }
  
  return (
    <DropdownMenuPrimitive.Trigger className={cn('inline-flex', className)}>
      {children}
    </DropdownMenuPrimitive.Trigger>
  );
}

export interface DropdownMenuContentProps extends BaseProps, ChildrenProp {
  side?: 'top' | 'right' | 'bottom' | 'left';
  sideOffset?: number;
  align?: 'start' | 'center' | 'end';
}

export function DropdownMenuContent({
  side = 'bottom',
  sideOffset = 4,
  align = 'start',
  className,
  children,
  ...props
}: DropdownMenuContentProps) {
  return (
    <DropdownMenuPrimitive.Portal>
      <DropdownMenuPrimitive.Content
        side={side}
        sideOffset={sideOffset}
        align={align}
        className={cn(
          'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
          'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className
        )}
        {...props}
      >
        {children}
      </DropdownMenuPrimitive.Content>
    </DropdownMenuPrimitive.Portal>
  );
}

export interface DropdownMenuItemProps extends Omit<BaseProps, 'onSelect'>, ChildrenProp {
  icon?: string;
  shortcut?: string;
  disabled?: boolean;
  onSelect?: () => void;
}

export function DropdownMenuItem({
  icon,
  shortcut,
  disabled = false,
  onSelect,
  className,
  children,
  ...props
}: DropdownMenuItemProps) {
  return (
    <DropdownMenuPrimitive.Item
      disabled={disabled}
      onSelect={onSelect}
      className={cn(
        'relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none',
        'transition-colors focus:bg-accent focus:text-accent-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      {...props}
    >
      {icon && <Icon name={icon} size={16} className="shrink-0" />}
      <span className="flex-1">{children}</span>
      {shortcut && (
        <span className="ml-auto text-xs tracking-widest text-muted-foreground">
          {shortcut}
        </span>
      )}
    </DropdownMenuPrimitive.Item>
  );
}

export interface DropdownMenuLabelProps extends BaseProps, ChildrenProp {
  inset?: boolean;
}

export function DropdownMenuLabel({
  inset = false,
  className,
  children,
  ...props
}: DropdownMenuLabelProps) {
  return (
    <DropdownMenuPrimitive.Label
      className={cn(
        'px-2 py-1.5 text-sm font-semibold',
        inset && 'pl-8',
        className
      )}
      {...props}
    >
      {children}
    </DropdownMenuPrimitive.Label>
  );
}

export interface DropdownMenuSeparatorProps extends BaseProps {}

export function DropdownMenuSeparator({
  className,
  ...props
}: DropdownMenuSeparatorProps) {
  return (
    <DropdownMenuPrimitive.Separator
      className={cn('-mx-1 my-1 h-px bg-muted', className)}
      {...props}
    />
  );
}

export interface DropdownMenuCheckboxItemProps extends ChildrenProp {
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  className?: string;
}

export function DropdownMenuCheckboxItem({
  checked = false,
  onCheckedChange,
  disabled = false,
  className,
  children,
}: DropdownMenuCheckboxItemProps) {
  return (
    <DropdownMenuPrimitive.CheckboxItem
      checked={checked}
      onCheckedChange={onCheckedChange}
      disabled={disabled}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none',
        'transition-colors focus:bg-accent focus:text-accent-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
    >
      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
        <DropdownMenuPrimitive.ItemIndicator>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </DropdownMenuPrimitive.ItemIndicator>
      </span>
      {children}
    </DropdownMenuPrimitive.CheckboxItem>
  );
}

export interface DropdownMenuRadioGroupProps extends BaseProps, ChildrenProp {
  value?: string;
  onValueChange?: (value: string) => void;
}

export function DropdownMenuRadioGroup({
  value,
  onValueChange,
  className,
  children,
  ...props
}: DropdownMenuRadioGroupProps) {
  return (
    <DropdownMenuPrimitive.RadioGroup
      value={value}
      onValueChange={onValueChange}
      className={className}
      {...props}
    >
      {children}
    </DropdownMenuPrimitive.RadioGroup>
  );
}

export interface DropdownMenuRadioItemProps extends ChildrenProp {
  value: string;
  className?: string;
}

export function DropdownMenuRadioItem({
  value,
  className,
  children,
}: DropdownMenuRadioItemProps) {
  return (
    <DropdownMenuPrimitive.RadioItem
      value={value}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none',
        'transition-colors focus:bg-accent focus:text-accent-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
    >
      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
        <DropdownMenuPrimitive.ItemIndicator>
          <svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10" />
          </svg>
        </DropdownMenuPrimitive.ItemIndicator>
      </span>
      {children}
    </DropdownMenuPrimitive.RadioItem>
  );
}

export interface DropdownMenuSubProps extends ChildrenProp {}

export function DropdownMenuSub({
  children,
}: DropdownMenuSubProps) {
  return (
    <DropdownMenuPrimitive.Sub>
      {children}
    </DropdownMenuPrimitive.Sub>
  );
}

export interface DropdownMenuSubTriggerProps extends BaseProps, ChildrenProp {
  inset?: boolean;
}

export function DropdownMenuSubTrigger({
  inset = false,
  className,
  children,
  ...props
}: DropdownMenuSubTriggerProps) {
  return (
    <DropdownMenuPrimitive.SubTrigger
      className={cn(
        'flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
        'focus:bg-accent data-[state=open]:bg-accent',
        inset && 'pl-8',
        className
      )}
      {...props}
    >
      {children}
      <svg className="ml-auto h-4 w-4" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="9 18 15 12 9 6" />
      </svg>
    </DropdownMenuPrimitive.SubTrigger>
  );
}

export interface DropdownMenuSubContentProps extends BaseProps, ChildrenProp {}

export function DropdownMenuSubContent({
  className,
  children,
  ...props
}: DropdownMenuSubContentProps) {
  return (
    <DropdownMenuPrimitive.Portal>
      <DropdownMenuPrimitive.SubContent
        className={cn(
          'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg',
          'data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
          'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className
        )}
        {...props}
      >
        {children}
      </DropdownMenuPrimitive.SubContent>
    </DropdownMenuPrimitive.Portal>
  );
}

// ============================================================================
// ContextMenu Components
// ============================================================================

import * as ContextMenuPrimitive from '@radix-ui/react-context-menu';

export interface ContextMenuProps extends ChildrenProp {
  className?: string;
}

export function ContextMenu({
  children,
}: ContextMenuProps) {
  return (
    <ContextMenuPrimitive.Root>
      {children}
    </ContextMenuPrimitive.Root>
  );
}

export interface ContextMenuTriggerProps extends ChildrenProp {
  asChild?: boolean;
  className?: string;
}

export function ContextMenuTrigger({
  asChild = false,
  className,
  children,
}: ContextMenuTriggerProps) {
  const childrenArray = React.Children.toArray(children);
  const singleChild = childrenArray.length === 1 ? childrenArray[0] : null;

  // Context menu trigger usually wraps a larger area for right-click
  if (asChild && singleChild) {
    return (
      <ContextMenuPrimitive.Trigger asChild className={className}>
        {singleChild}
      </ContextMenuPrimitive.Trigger>
    );
  }
  
  return (
    <ContextMenuPrimitive.Trigger className={className}>
      {children}
    </ContextMenuPrimitive.Trigger>
  );
}

export interface ContextMenuContentProps extends BaseProps, ChildrenProp {}

export function ContextMenuContent({
  className,
  children,
  ...props
}: ContextMenuContentProps) {
  return (
    <ContextMenuPrimitive.Portal>
      <ContextMenuPrimitive.Content
        className={cn(
          'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
          'animate-in fade-in-80 data-[state=open]:animate-in data-[state=closed]:animate-out',
          'data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          className
        )}
        {...props}
      >
        {children}
      </ContextMenuPrimitive.Content>
    </ContextMenuPrimitive.Portal>
  );
}

export interface ContextMenuItemProps extends Omit<BaseProps, 'onSelect'>, ChildrenProp {
  icon?: string;
  shortcut?: string;
  disabled?: boolean;
  onSelect?: () => void;
}

export function ContextMenuItem({
  icon,
  shortcut,
  disabled = false,
  onSelect,
  className,
  children,
  ...props
}: ContextMenuItemProps) {
  return (
    <ContextMenuPrimitive.Item
      disabled={disabled}
      onSelect={onSelect}
      className={cn(
        'relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none',
        'transition-colors focus:bg-accent focus:text-accent-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      {...props}
    >
      {icon && <Icon name={icon} size={16} className="shrink-0" />}
      <span className="flex-1">{children}</span>
      {shortcut && (
        <span className="ml-auto text-xs tracking-widest text-muted-foreground">
          {shortcut}
        </span>
      )}
    </ContextMenuPrimitive.Item>
  );
}

export interface ContextMenuSeparatorProps extends BaseProps {}

export function ContextMenuSeparator({
  className,
  ...props
}: ContextMenuSeparatorProps) {
  return (
    <ContextMenuPrimitive.Separator
      className={cn('-mx-1 my-1 h-px bg-muted', className)}
      {...props}
    />
  );
}

export interface ContextMenuCheckboxItemProps extends ChildrenProp {
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  className?: string;
}

export function ContextMenuCheckboxItem({
  checked = false,
  onCheckedChange,
  disabled = false,
  className,
  children,
}: ContextMenuCheckboxItemProps) {
  return (
    <ContextMenuPrimitive.CheckboxItem
      checked={checked}
      onCheckedChange={onCheckedChange}
      disabled={disabled}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none',
        'transition-colors focus:bg-accent focus:text-accent-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
    >
      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
        <ContextMenuPrimitive.ItemIndicator>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </ContextMenuPrimitive.ItemIndicator>
      </span>
      {children}
    </ContextMenuPrimitive.CheckboxItem>
  );
}

// ============================================================================
// Export all
// ============================================================================

export const OverlayComponents = {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogAction,
  DialogCancel,
  Sheet,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetFooter,
  SheetTitle,
  SheetDescription,
  SheetClose,
  Drawer,
  HoverCard,
  HoverCardTrigger,
  HoverCardContent,
  Popover,
  PopoverTrigger,
  PopoverContent,
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
  ContextMenu,
  ContextMenuTrigger,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuSeparator,
  ContextMenuCheckboxItem,
};
