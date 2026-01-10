import React from 'react';
import { Command as CommandPrimitive } from 'cmdk';
import * as NavigationMenuPrimitive from '@radix-ui/react-navigation-menu';
import * as MenubarPrimitive from '@radix-ui/react-menubar';
import { cn } from '../../utils';

// ============================================================================
// Breadcrumb
// ============================================================================

interface BreadcrumbProps {
  id?: string;
  className?: string;
  separator?: React.ReactNode;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function Breadcrumb({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: BreadcrumbProps): React.ReactElement {
  return (
    <nav
      id={id}
      aria-label="breadcrumb"
      className={className}
      data-refast-id={dataRefastId}
    >
      <ol className="flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5">
        {children}
      </ol>
    </nav>
  );
}

interface BreadcrumbListProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function BreadcrumbList({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: BreadcrumbListProps): React.ReactElement {
  return (
    <ol
      id={id}
      className={cn(
        'flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </ol>
  );
}

interface BreadcrumbItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function BreadcrumbItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: BreadcrumbItemProps): React.ReactElement {
  return (
    <li
      id={id}
      className={cn('inline-flex items-center gap-1.5', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </li>
  );
}

interface BreadcrumbLinkProps {
  id?: string;
  className?: string;
  href?: string;
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function BreadcrumbLink({
  id,
  className,
  href = '#',
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: BreadcrumbLinkProps): React.ReactElement {
  return (
    <a
      id={id}
      href={href}
      onClick={(e) => {
        if (onClick) {
          e.preventDefault();
          onClick();
        }
      }}
      className={cn('transition-colors hover:text-foreground', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </a>
  );
}

interface BreadcrumbPageProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function BreadcrumbPage({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: BreadcrumbPageProps): React.ReactElement {
  return (
    <span
      id={id}
      role="link"
      aria-disabled="true"
      aria-current="page"
      className={cn('font-normal text-foreground', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </span>
  );
}

interface BreadcrumbSeparatorProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function BreadcrumbSeparator({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: BreadcrumbSeparatorProps): React.ReactElement {
  return (
    <li
      id={id}
      role="presentation"
      aria-hidden="true"
      className={cn('[&>svg]:size-3.5', className)}
      data-refast-id={dataRefastId}
    >
      {children || (
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
        >
          <path d="m9 18 6-6-6-6" />
        </svg>
      )}
    </li>
  );
}

interface BreadcrumbEllipsisProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function BreadcrumbEllipsis({
  id,
  className,
  'data-refast-id': dataRefastId,
}: BreadcrumbEllipsisProps): React.ReactElement {
  return (
    <span
      id={id}
      role="presentation"
      aria-hidden="true"
      className={cn('flex h-9 w-9 items-center justify-center', className)}
      data-refast-id={dataRefastId}
    >
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
        className="h-4 w-4"
      >
        <circle cx="12" cy="12" r="1" />
        <circle cx="19" cy="12" r="1" />
        <circle cx="5" cy="12" r="1" />
      </svg>
      <span className="sr-only">More</span>
    </span>
  );
}

// ============================================================================
// NavigationMenu
// ============================================================================

interface NavigationMenuProps {
  id?: string;
  className?: string;
  orientation?: 'horizontal' | 'vertical';
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function NavigationMenu({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: NavigationMenuProps): React.ReactElement {
  return (
    <NavigationMenuPrimitive.Root
      id={id}
      className={cn(
        'relative z-10 flex max-w-max flex-1 items-center justify-center',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
      <NavigationMenuViewport />
    </NavigationMenuPrimitive.Root>
  );
}

function NavigationMenuViewport(): React.ReactElement {
  return (
    <div className="absolute left-0 top-full flex justify-center">
      <NavigationMenuPrimitive.Viewport
        className={cn(
          'origin-top-center relative mt-1.5 h-[var(--radix-navigation-menu-viewport-height)] w-full overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-lg',
          'data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-90',
          'md:w-[var(--radix-navigation-menu-viewport-width)]'
        )}
      />
    </div>
  );
}

interface NavigationMenuListProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function NavigationMenuList({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: NavigationMenuListProps): React.ReactElement {
  return (
    <NavigationMenuPrimitive.List
      id={id}
      className={cn(
        'group flex flex-1 list-none items-center justify-center space-x-1',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </NavigationMenuPrimitive.List>
  );
}

interface NavigationMenuItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function NavigationMenuItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: NavigationMenuItemProps): React.ReactElement {
  return (
    <NavigationMenuPrimitive.Item
      id={id}
      className={className}
      data-refast-id={dataRefastId}
    >
      {children}
    </NavigationMenuPrimitive.Item>
  );
}

interface NavigationMenuTriggerProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function NavigationMenuTrigger({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: NavigationMenuTriggerProps): React.ReactElement {
  return (
    <NavigationMenuPrimitive.Trigger
      id={id}
      className={cn(
        'group inline-flex h-10 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors',
        'hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none',
        'disabled:pointer-events-none disabled:opacity-50 data-[active]:bg-accent/50 data-[state=open]:bg-accent/50',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
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
        className="relative top-[1px] ml-1 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180"
        aria-hidden="true"
      >
        <path d="m6 9 6 6 6-6" />
      </svg>
    </NavigationMenuPrimitive.Trigger>
  );
}

interface NavigationMenuContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function NavigationMenuContent({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: NavigationMenuContentProps): React.ReactElement {
  return (
    <NavigationMenuPrimitive.Content
      id={id}
      className={cn(
        'left-0 top-0 w-full data-[motion^=from-]:animate-in data-[motion^=to-]:animate-out',
        'data-[motion^=from-]:fade-in data-[motion^=to-]:fade-out',
        'data-[motion=from-end]:slide-in-from-right-52 data-[motion=from-start]:slide-in-from-left-52',
        'data-[motion=to-end]:slide-out-to-right-52 data-[motion=to-start]:slide-out-to-left-52',
        'md:absolute md:w-auto',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </NavigationMenuPrimitive.Content>
  );
}

interface NavigationMenuLinkProps {
  id?: string;
  className?: string;
  href?: string;
  active?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function NavigationMenuLink({
  id,
  className,
  href = '#',
  active,
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: NavigationMenuLinkProps): React.ReactElement {
  return (
    <NavigationMenuPrimitive.Link
      id={id}
      href={href}
      active={active}
      onClick={(e) => {
        if (onClick) {
          e.preventDefault();
          onClick();
        }
      }}
      className={cn(
        'block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors',
        'hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </NavigationMenuPrimitive.Link>
  );
}

// ============================================================================
// Pagination
// ============================================================================

interface PaginationProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function Pagination({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: PaginationProps): React.ReactElement {
  return (
    <nav
      id={id}
      role="navigation"
      aria-label="pagination"
      className={cn('mx-auto flex w-full justify-center', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </nav>
  );
}

interface PaginationContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function PaginationContent({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: PaginationContentProps): React.ReactElement {
  return (
    <ul
      id={id}
      className={cn('flex flex-row items-center gap-1', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </ul>
  );
}

interface PaginationItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function PaginationItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: PaginationItemProps): React.ReactElement {
  return (
    <li id={id} className={className} data-refast-id={dataRefastId}>
      {children}
    </li>
  );
}

interface PaginationLinkProps {
  id?: string;
  className?: string;
  href?: string;
  active?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function PaginationLink({
  id,
  className,
  href = '#',
  active,
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: PaginationLinkProps): React.ReactElement {
  return (
    <a
      id={id}
      href={href}
      onClick={(e) => {
        if (onClick) {
          e.preventDefault();
          onClick();
        }
      }}
      aria-current={active ? 'page' : undefined}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'h-10 w-10',
        active
          ? 'border border-input bg-background hover:bg-accent hover:text-accent-foreground'
          : 'hover:bg-accent hover:text-accent-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </a>
  );
}

interface PaginationPreviousProps {
  id?: string;
  className?: string;
  href?: string;
  onClick?: () => void;
  'data-refast-id'?: string;
}

export function PaginationPrevious({
  id,
  className,
  href = '#',
  onClick,
  'data-refast-id': dataRefastId,
}: PaginationPreviousProps): React.ReactElement {
  return (
    <a
      id={id}
      href={href}
      onClick={(e) => {
        if (onClick) {
          e.preventDefault();
          onClick();
        }
      }}
      aria-label="Go to previous page"
      className={cn(
        'inline-flex items-center justify-center gap-1 pl-2.5 pr-4 h-10 rounded-md text-sm font-medium',
        'hover:bg-accent hover:text-accent-foreground transition-colors',
        className
      )}
      data-refast-id={dataRefastId}
    >
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
        className="h-4 w-4"
      >
        <path d="m15 18-6-6 6-6" />
      </svg>
      <span>Previous</span>
    </a>
  );
}

interface PaginationNextProps {
  id?: string;
  className?: string;
  href?: string;
  onClick?: () => void;
  'data-refast-id'?: string;
}

export function PaginationNext({
  id,
  className,
  href = '#',
  onClick,
  'data-refast-id': dataRefastId,
}: PaginationNextProps): React.ReactElement {
  return (
    <a
      id={id}
      href={href}
      onClick={(e) => {
        if (onClick) {
          e.preventDefault();
          onClick();
        }
      }}
      aria-label="Go to next page"
      className={cn(
        'inline-flex items-center justify-center gap-1 pr-2.5 pl-4 h-10 rounded-md text-sm font-medium',
        'hover:bg-accent hover:text-accent-foreground transition-colors',
        className
      )}
      data-refast-id={dataRefastId}
    >
      <span>Next</span>
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
        className="h-4 w-4"
      >
        <path d="m9 18 6-6-6-6" />
      </svg>
    </a>
  );
}

interface PaginationEllipsisProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function PaginationEllipsis({
  id,
  className,
  'data-refast-id': dataRefastId,
}: PaginationEllipsisProps): React.ReactElement {
  return (
    <span
      id={id}
      aria-hidden
      className={cn('flex h-9 w-9 items-center justify-center', className)}
      data-refast-id={dataRefastId}
    >
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
        className="h-4 w-4"
      >
        <circle cx="12" cy="12" r="1" />
        <circle cx="19" cy="12" r="1" />
        <circle cx="5" cy="12" r="1" />
      </svg>
      <span className="sr-only">More pages</span>
    </span>
  );
}

// ============================================================================
// Menubar
// ============================================================================

interface MenubarProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function Menubar({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: MenubarProps): React.ReactElement {
  return (
    <MenubarPrimitive.Root
      id={id}
      className={cn(
        'flex h-10 items-center space-x-1 rounded-md border bg-background p-1',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </MenubarPrimitive.Root>
  );
}

interface MenubarMenuProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarMenu({
  children,
  'data-refast-id': dataRefastId,
}: MenubarMenuProps): React.ReactElement {
  return (
    <MenubarPrimitive.Menu data-refast-id={dataRefastId}>
      {children}
    </MenubarPrimitive.Menu>
  );
}

interface MenubarTriggerProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarTrigger({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: MenubarTriggerProps): React.ReactElement {
  return (
    <MenubarPrimitive.Trigger
      id={id}
      className={cn(
        'flex cursor-default select-none items-center rounded-sm px-3 py-1.5 text-sm font-medium outline-none',
        'focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </MenubarPrimitive.Trigger>
  );
}

interface MenubarContentProps {
  id?: string;
  className?: string;
  align?: 'start' | 'center' | 'end';
  sideOffset?: number;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarContent({
  id,
  className,
  align = 'start',
  sideOffset = 5,
  children,
  'data-refast-id': dataRefastId,
}: MenubarContentProps): React.ReactElement {
  return (
    <MenubarPrimitive.Portal>
      <MenubarPrimitive.Content
        id={id}
        align={align}
        sideOffset={sideOffset}
        className={cn(
          'z-50 min-w-[12rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
          'data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
          'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className
        )}
        data-refast-id={dataRefastId}
      >
        {children}
      </MenubarPrimitive.Content>
    </MenubarPrimitive.Portal>
  );
}

interface MenubarItemProps {
  id?: string;
  className?: string;
  shortcut?: string;
  disabled?: boolean;
  onSelect?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarItem({
  id,
  className,
  shortcut,
  disabled,
  onSelect,
  children,
  'data-refast-id': dataRefastId,
}: MenubarItemProps): React.ReactElement {
  return (
    <MenubarPrimitive.Item
      id={id}
      disabled={disabled}
      onSelect={onSelect}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
        'focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
      {shortcut && (
        <span className="ml-auto text-xs tracking-widest text-muted-foreground">
          {shortcut}
        </span>
      )}
    </MenubarPrimitive.Item>
  );
}

interface MenubarSeparatorProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function MenubarSeparator({
  id,
  className,
  'data-refast-id': dataRefastId,
}: MenubarSeparatorProps): React.ReactElement {
  return (
    <MenubarPrimitive.Separator
      id={id}
      className={cn('-mx-1 my-1 h-px bg-muted', className)}
      data-refast-id={dataRefastId}
    />
  );
}

interface MenubarCheckboxItemProps {
  id?: string;
  className?: string;
  checked?: boolean;
  onCheckedChange?: (checked: boolean) => void;
  disabled?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarCheckboxItem({
  id,
  className,
  checked,
  onCheckedChange,
  disabled,
  children,
  'data-refast-id': dataRefastId,
}: MenubarCheckboxItemProps): React.ReactElement {
  return (
    <MenubarPrimitive.CheckboxItem
      id={id}
      checked={checked}
      onCheckedChange={onCheckedChange}
      disabled={disabled}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none',
        'focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    >
      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
        <MenubarPrimitive.ItemIndicator>
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
            className="h-4 w-4"
          >
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </MenubarPrimitive.ItemIndicator>
      </span>
      {children}
    </MenubarPrimitive.CheckboxItem>
  );
}

interface MenubarRadioGroupProps {
  id?: string;
  className?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarRadioGroup({
  id,
  className,
  value,
  onValueChange,
  children,
  'data-refast-id': dataRefastId,
}: MenubarRadioGroupProps): React.ReactElement {
  return (
    <MenubarPrimitive.RadioGroup
      id={id}
      value={value}
      onValueChange={onValueChange}
      className={className}
      data-refast-id={dataRefastId}
    >
      {children}
    </MenubarPrimitive.RadioGroup>
  );
}

interface MenubarRadioItemProps {
  id?: string;
  className?: string;
  value: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarRadioItem({
  id,
  className,
  value,
  children,
  'data-refast-id': dataRefastId,
}: MenubarRadioItemProps): React.ReactElement {
  return (
    <MenubarPrimitive.RadioItem
      id={id}
      value={value}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none',
        'focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    >
      <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
        <MenubarPrimitive.ItemIndicator>
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
            className="h-2 w-2 fill-current"
          >
            <circle cx="12" cy="12" r="10" />
          </svg>
        </MenubarPrimitive.ItemIndicator>
      </span>
      {children}
    </MenubarPrimitive.RadioItem>
  );
}

interface MenubarSubProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarSub({
  children,
  'data-refast-id': dataRefastId,
}: MenubarSubProps): React.ReactElement {
  return (
    <MenubarPrimitive.Sub data-refast-id={dataRefastId}>
      {children}
    </MenubarPrimitive.Sub>
  );
}

interface MenubarSubTriggerProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarSubTrigger({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: MenubarSubTriggerProps): React.ReactElement {
  return (
    <MenubarPrimitive.SubTrigger
      id={id}
      className={cn(
        'flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
        'focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
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
        className="ml-auto h-4 w-4"
      >
        <path d="m9 18 6-6-6-6" />
      </svg>
    </MenubarPrimitive.SubTrigger>
  );
}

interface MenubarSubContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function MenubarSubContent({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: MenubarSubContentProps): React.ReactElement {
  return (
    <MenubarPrimitive.Portal>
      <MenubarPrimitive.SubContent
        id={id}
        className={cn(
          'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground',
          'data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
          'data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95',
          'data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2',
          'data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
          className
        )}
        data-refast-id={dataRefastId}
      >
        {children}
      </MenubarPrimitive.SubContent>
    </MenubarPrimitive.Portal>
  );
}

// ============================================================================
// Command (using cmdk)
// ============================================================================

interface CommandProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function Command({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CommandProps): React.ReactElement {
  return (
    <CommandPrimitive
      id={id}
      className={cn(
        'flex h-full w-full flex-col overflow-hidden rounded-md bg-popover text-popover-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </CommandPrimitive>
  );
}

interface CommandInputProps {
  id?: string;
  className?: string;
  placeholder?: string;
  value?: string;
  onValueChange?: (value: string) => void;
  'data-refast-id'?: string;
}

export function CommandInput({
  id,
  className,
  placeholder = 'Search...',
  value,
  onValueChange,
  'data-refast-id': dataRefastId,
}: CommandInputProps): React.ReactElement {
  return (
    <div className="flex items-center border-b px-3" cmdk-input-wrapper="" data-refast-id={dataRefastId}>
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
      <CommandPrimitive.Input
        id={id}
        value={value}
        onValueChange={onValueChange}
        placeholder={placeholder}
        className={cn(
          'flex h-11 w-full rounded-md bg-transparent py-3 text-sm outline-none',
          'placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50',
          className
        )}
      />
    </div>
  );
}

interface CommandListProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function CommandList({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CommandListProps): React.ReactElement {
  return (
    <CommandPrimitive.List
      id={id}
      className={cn('max-h-[300px] overflow-y-auto overflow-x-hidden', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </CommandPrimitive.List>
  );
}

interface CommandEmptyProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function CommandEmpty({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CommandEmptyProps): React.ReactElement {
  return (
    <CommandPrimitive.Empty
      id={id}
      className={cn('py-6 text-center text-sm', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </CommandPrimitive.Empty>
  );
}

interface CommandGroupProps {
  id?: string;
  className?: string;
  heading?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function CommandGroup({
  id,
  className,
  heading,
  children,
  'data-refast-id': dataRefastId,
}: CommandGroupProps): React.ReactElement {
  return (
    <CommandPrimitive.Group
      id={id}
      heading={heading}
      className={cn(
        'overflow-hidden p-1 text-foreground',
        '[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1.5 [&_[cmdk-group-heading]]:text-xs',
        '[&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </CommandPrimitive.Group>
  );
}

interface CommandItemProps {
  id?: string;
  className?: string;
  icon?: string;
  value?: string;
  disabled?: boolean;
  onSelect?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function CommandItem({
  id,
  className,
  value,
  disabled,
  onSelect,
  children,
  'data-refast-id': dataRefastId,
}: CommandItemProps): React.ReactElement {
  return (
    <CommandPrimitive.Item
      id={id}
      value={value}
      disabled={disabled}
      onSelect={onSelect}
      className={cn(
        'relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none',
        'aria-selected:bg-accent aria-selected:text-accent-foreground',
        'data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </CommandPrimitive.Item>
  );
}

interface CommandSeparatorProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function CommandSeparator({
  id,
  className,
  'data-refast-id': dataRefastId,
}: CommandSeparatorProps): React.ReactElement {
  return (
    <CommandPrimitive.Separator
      id={id}
      className={cn('-mx-1 h-px bg-border', className)}
      data-refast-id={dataRefastId}
    />
  );
}

interface CommandShortcutProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function CommandShortcut({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: CommandShortcutProps): React.ReactElement {
  return (
    <span
      id={id}
      className={cn('ml-auto text-xs tracking-widest text-muted-foreground', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </span>
  );
}

// ============================================================================
// Sidebar - Full implementation based on shadcn/ui
// ============================================================================

const SIDEBAR_WIDTH = '16rem';
const SIDEBAR_WIDTH_MOBILE = '18rem';
const SIDEBAR_WIDTH_ICON = '3rem';
const SIDEBAR_KEYBOARD_SHORTCUT = 'b';

interface SidebarContextValue {
  state: 'expanded' | 'collapsed';
  open: boolean;
  setOpen: (open: boolean) => void;
  openMobile: boolean;
  setOpenMobile: (open: boolean) => void;
  isMobile: boolean;
  toggleSidebar: () => void;
}

const SidebarContext = React.createContext<SidebarContextValue | null>(null);

export function useSidebar() {
  const context = React.useContext(SidebarContext);
  if (!context) {
    throw new Error('useSidebar must be used within a SidebarProvider.');
  }
  return context;
}

interface SidebarProviderProps {
  id?: string;
  className?: string;
  defaultOpen?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  'data-refast-id'?: string;
}

export function SidebarProvider({
  id,
  className,
  defaultOpen = true,
  open: openProp,
  onOpenChange: setOpenProp,
  children,
  style,
  'data-refast-id': dataRefastId,
}: SidebarProviderProps): React.ReactElement {
  const [isMobile, setIsMobile] = React.useState(false);
  const [openMobile, setOpenMobile] = React.useState(false);
  const [_open, _setOpen] = React.useState(defaultOpen);
  const open = openProp ?? _open;

  const setOpen = React.useCallback(
    (value: boolean | ((value: boolean) => boolean)) => {
      const openState = typeof value === 'function' ? value(open) : value;
      if (setOpenProp) {
        setOpenProp(openState);
      } else {
        _setOpen(openState);
      }
    },
    [setOpenProp, open]
  );

  const toggleSidebar = React.useCallback(() => {
    return isMobile ? setOpenMobile((open) => !open) : setOpen((open) => !open);
  }, [isMobile, setOpen, setOpenMobile]);

  // Check for mobile
  React.useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Keyboard shortcut
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (
        event.key === SIDEBAR_KEYBOARD_SHORTCUT &&
        (event.metaKey || event.ctrlKey)
      ) {
        event.preventDefault();
        toggleSidebar();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [toggleSidebar]);

  const state = open ? 'expanded' : 'collapsed';

  const contextValue = React.useMemo<SidebarContextValue>(
    () => ({
      state,
      open,
      setOpen,
      isMobile,
      openMobile,
      setOpenMobile,
      toggleSidebar,
    }),
    [state, open, setOpen, isMobile, openMobile, setOpenMobile, toggleSidebar]
  );

  return (
    <SidebarContext.Provider value={contextValue}>
      <div
        id={id}
        style={
          {
            '--sidebar-width': SIDEBAR_WIDTH,
            '--sidebar-width-mobile': SIDEBAR_WIDTH_MOBILE,
            '--sidebar-width-icon': SIDEBAR_WIDTH_ICON,
            ...style,
          } as React.CSSProperties
        }
        className={cn(
          'group/sidebar-wrapper flex min-h-svh w-full has-[[data-variant=inset]]:bg-sidebar',
          className
        )}
        data-refast-id={dataRefastId}
      >
        {children}
      </div>
    </SidebarContext.Provider>
  );
}

interface SidebarProps {
  id?: string;
  className?: string;
  side?: 'left' | 'right';
  variant?: 'sidebar' | 'floating' | 'inset';
  collapsible?: 'offcanvas' | 'icon' | 'none';
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function Sidebar({
  id,
  className,
  side = 'left',
  variant = 'sidebar',
  collapsible = 'offcanvas',
  children,
  'data-refast-id': dataRefastId,
}: SidebarProps): React.ReactElement {
  const context = React.useContext(SidebarContext);
  
  // If no context, render a simple sidebar
  if (!context) {
    return (
      <aside
        id={id}
        className={cn(
          'flex h-full w-64 flex-col bg-sidebar text-sidebar-foreground border-r border-sidebar-border',
          side === 'right' && 'border-l border-r-0',
          className
        )}
        data-refast-id={dataRefastId}
      >
        {children}
      </aside>
    );
  }

  const { isMobile, state, openMobile, setOpenMobile } = context;

  if (collapsible === 'none') {
    return (
      <div
        id={id}
        className={cn(
          'flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground',
          className
        )}
        data-refast-id={dataRefastId}
      >
        {children}
      </div>
    );
  }

  if (isMobile) {
    return (
      <>
        {/* Mobile overlay */}
        {openMobile && (
          <div
            className="fixed inset-0 z-50 bg-black/80"
            onClick={() => setOpenMobile(false)}
          />
        )}
        {/* Mobile sidebar */}
        <aside
          id={id}
          className={cn(
            'fixed inset-y-0 z-50 flex h-svh w-[--sidebar-width-mobile] flex-col bg-sidebar text-sidebar-foreground',
            'transition-transform duration-200 ease-in-out',
            side === 'left' ? 'left-0' : 'right-0',
            openMobile
              ? 'translate-x-0'
              : side === 'left'
              ? '-translate-x-full'
              : 'translate-x-full',
            className
          )}
          data-refast-id={dataRefastId}
        >
          {children}
        </aside>
      </>
    );
  }

  return (
    <div
      className="group peer hidden md:block text-sidebar-foreground"
      data-state={state}
      data-collapsible={state === 'collapsed' ? collapsible : ''}
      data-variant={variant}
      data-side={side}
    >
      {/* Spacer for the sidebar */}
      <div
        className={cn(
          'relative h-svh w-[--sidebar-width] bg-transparent transition-[width] duration-200 ease-linear',
          'group-data-[collapsible=offcanvas]:w-0',
          'group-data-[side=right]:rotate-180',
          variant === 'floating' || variant === 'inset'
            ? 'group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4))]'
            : 'group-data-[collapsible=icon]:w-[--sidebar-width-icon]'
        )}
      />
      <aside
        id={id}
        className={cn(
          'fixed inset-y-0 z-10 hidden h-svh w-[--sidebar-width] transition-[left,right,width] duration-200 ease-linear md:flex',
          side === 'left'
            ? 'left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]'
            : 'right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]',
          'group-data-[collapsible=icon]:w-[--sidebar-width-icon] group-data-[collapsible=icon]:overflow-hidden',
          variant === 'floating' || variant === 'inset'
            ? 'p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4)_+2px)]'
            : 'group-data-[side=left]:border-r group-data-[side=right]:border-l border-sidebar-border',
          className
        )}
        data-refast-id={dataRefastId}
      >
        <div
          data-sidebar="sidebar"
          className={cn(
            'flex h-full w-full flex-col bg-sidebar',
            variant === 'floating' && 'rounded-lg border border-sidebar-border shadow',
            variant === 'inset' && 'rounded-lg border border-sidebar-border shadow'
          )}
        >
          {children}
        </div>
      </aside>
    </div>
  );
}

interface SidebarInsetProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarInset({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarInsetProps): React.ReactElement {
  return (
    <main
      id={id}
      className={cn(
        'relative flex min-h-svh flex-1 flex-col bg-background',
        'peer-data-[variant=inset]:min-h-[calc(100svh-theme(spacing.4))] md:peer-data-[variant=inset]:m-2 md:peer-data-[state=collapsed]:peer-data-[variant=inset]:ml-2 md:peer-data-[variant=inset]:ml-0 md:peer-data-[variant=inset]:rounded-xl md:peer-data-[variant=inset]:shadow',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </main>
  );
}

interface SidebarHeaderProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarHeader({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarHeaderProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="header"
      className={cn('flex flex-col gap-2 p-2', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarContent({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarContentProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="content"
      className={cn(
        'flex min-h-0 flex-1 flex-col gap-2 overflow-auto group-data-[collapsible=icon]:overflow-hidden',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarFooterProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarFooter({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarFooterProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="footer"
      className={cn('flex flex-col gap-2 p-2', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarSeparatorProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function SidebarSeparator({
  id,
  className,
  'data-refast-id': dataRefastId,
}: SidebarSeparatorProps): React.ReactElement {
  return (
    <hr
      id={id}
      data-sidebar="separator"
      className={cn('mx-2 w-auto bg-sidebar-border', className)}
      data-refast-id={dataRefastId}
    />
  );
}

interface SidebarGroupProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarGroup({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarGroupProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="group"
      className={cn('relative flex w-full min-w-0 flex-col p-2', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarGroupLabelProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarGroupLabel({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarGroupLabelProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="group-label"
      className={cn(
        'flex h-8 shrink-0 items-center rounded-md px-2 text-xs font-medium text-sidebar-foreground/70 outline-none ring-sidebar-ring transition-[margin,opa] duration-200 ease-linear',
        'focus-visible:ring-2 [&>svg]:size-4 [&>svg]:shrink-0',
        'group-data-[collapsible=icon]:-mt-8 group-data-[collapsible=icon]:opacity-0',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarGroupActionProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  onClick?: () => void;
  title?: string;
  'data-refast-id'?: string;
}

export function SidebarGroupAction({
  id,
  className,
  children,
  onClick,
  title,
  'data-refast-id': dataRefastId,
}: SidebarGroupActionProps): React.ReactElement {
  return (
    <button
      id={id}
      data-sidebar="group-action"
      onClick={onClick}
      title={title}
      className={cn(
        'absolute right-3 top-3.5 flex aspect-square w-5 items-center justify-center rounded-md p-0 text-sidebar-foreground outline-none ring-sidebar-ring transition-transform hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2',
        '[&>svg]:size-4 [&>svg]:shrink-0',
        'after:absolute after:-inset-2 after:md:hidden',
        'group-data-[collapsible=icon]:hidden',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </button>
  );
}

interface SidebarGroupContentProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarGroupContent({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarGroupContentProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="group-content"
      className={cn('w-full text-sm', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarMenuProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenu({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuProps): React.ReactElement {
  return (
    <ul
      id={id}
      data-sidebar="menu"
      className={cn('flex w-full min-w-0 flex-col gap-1', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </ul>
  );
}

interface SidebarMenuItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuItemProps): React.ReactElement {
  return (
    <li
      id={id}
      data-sidebar="menu-item"
      className={cn('group/menu-item relative', className)}
      data-refast-id={dataRefastId}
    >
      {children}
    </li>
  );
}

interface SidebarMenuButtonProps {
  id?: string;
  className?: string;
  icon?: string;
  isActive?: boolean;
  tooltip?: string;
  variant?: 'default' | 'outline';
  size?: 'default' | 'sm' | 'lg';
  onClick?: () => void;
  href?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuButton({
  id,
  className,
  icon,
  isActive = false,
  variant = 'default',
  size = 'default',
  onClick,
  href,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuButtonProps): React.ReactElement {
  const buttonClasses = cn(
    'peer/menu-button flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm outline-none ring-sidebar-ring transition-[width,height,padding] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 group-has-[[data-sidebar=menu-action]]/menu-item:pr-8 aria-disabled:pointer-events-none aria-disabled:opacity-50 data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium data-[active=true]:text-sidebar-accent-foreground data-[state=open]:hover:bg-sidebar-accent data-[state=open]:hover:text-sidebar-accent-foreground',
    'group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0',
    variant === 'outline' &&
      'bg-background shadow-[0_0_0_1px_hsl(var(--sidebar-border))] hover:bg-sidebar-accent hover:text-sidebar-accent-foreground hover:shadow-[0_0_0_1px_hsl(var(--sidebar-accent))]',
    size === 'sm' && 'h-7 text-xs',
    size === 'lg' && 'h-12 text-sm group-data-[collapsible=icon]:!p-0',
    className
  );

  const content = (
    <>
      {icon && (
        <span className="flex size-4 shrink-0 items-center justify-center">
          {icon}
        </span>
      )}
      <span className="truncate">{children}</span>
    </>
  );

  if (href) {
    return (
      <a
        id={id}
        href={href}
        data-sidebar="menu-button"
        data-size={size}
        data-active={isActive}
        className={buttonClasses}
        data-refast-id={dataRefastId}
      >
        {content}
      </a>
    );
  }

  return (
    <button
      id={id}
      data-sidebar="menu-button"
      data-size={size}
      data-active={isActive}
      onClick={onClick}
      className={buttonClasses}
      data-refast-id={dataRefastId}
    >
      {content}
    </button>
  );
}

interface SidebarMenuActionProps {
  id?: string;
  className?: string;
  showOnHover?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuAction({
  id,
  className,
  showOnHover = false,
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuActionProps): React.ReactElement {
  return (
    <button
      id={id}
      data-sidebar="menu-action"
      onClick={onClick}
      className={cn(
        'absolute right-1 top-1.5 flex aspect-square w-5 items-center justify-center rounded-md p-0 text-sidebar-foreground outline-none ring-sidebar-ring transition-transform hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 peer-hover/menu-button:text-sidebar-accent-foreground',
        '[&>svg]:size-4 [&>svg]:shrink-0',
        'after:absolute after:-inset-2 after:md:hidden',
        'peer-data-[size=sm]/menu-button:top-1',
        'peer-data-[size=default]/menu-button:top-1.5',
        'peer-data-[size=lg]/menu-button:top-2.5',
        'group-data-[collapsible=icon]:hidden',
        showOnHover &&
          'group-focus-within/menu-item:opacity-100 group-hover/menu-item:opacity-100 data-[state=open]:opacity-100 peer-data-[active=true]/menu-button:text-sidebar-accent-foreground md:opacity-0',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </button>
  );
}

interface SidebarMenuBadgeProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuBadge({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuBadgeProps): React.ReactElement {
  return (
    <div
      id={id}
      data-sidebar="menu-badge"
      className={cn(
        'absolute right-1 flex h-5 min-w-5 items-center justify-center rounded-md px-1 text-xs font-medium tabular-nums text-sidebar-foreground select-none pointer-events-none',
        'peer-hover/menu-button:text-sidebar-accent-foreground peer-data-[active=true]/menu-button:text-sidebar-accent-foreground',
        'peer-data-[size=sm]/menu-button:top-1',
        'peer-data-[size=default]/menu-button:top-1.5',
        'peer-data-[size=lg]/menu-button:top-2.5',
        'group-data-[collapsible=icon]:hidden',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}

interface SidebarMenuSubProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuSub({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuSubProps): React.ReactElement {
  return (
    <ul
      id={id}
      data-sidebar="menu-sub"
      className={cn(
        'mx-3.5 flex min-w-0 translate-x-px flex-col gap-1 border-l border-sidebar-border px-2.5 py-0.5',
        'group-data-[collapsible=icon]:hidden',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </ul>
  );
}

interface SidebarMenuSubItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuSubItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuSubItemProps): React.ReactElement {
  return (
    <li
      id={id}
      className={className}
      data-refast-id={dataRefastId}
    >
      {children}
    </li>
  );
}

interface SidebarMenuSubButtonProps {
  id?: string;
  className?: string;
  isActive?: boolean;
  size?: 'sm' | 'md';
  href?: string;
  onClick?: () => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

export function SidebarMenuSubButton({
  id,
  className,
  isActive = false,
  size = 'md',
  href,
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: SidebarMenuSubButtonProps): React.ReactElement {
  const classes = cn(
    'flex h-7 min-w-0 -translate-x-px items-center gap-2 overflow-hidden rounded-md px-2 text-sidebar-foreground outline-none ring-sidebar-ring hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 active:bg-sidebar-accent active:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 [&>svg]:text-sidebar-accent-foreground',
    isActive && 'bg-sidebar-accent text-sidebar-accent-foreground',
    size === 'sm' && 'text-xs',
    size === 'md' && 'text-sm',
    className
  );

  if (href) {
    return (
      <a
        id={id}
        href={href}
        data-sidebar="menu-sub-button"
        data-size={size}
        data-active={isActive}
        className={classes}
        data-refast-id={dataRefastId}
      >
        {children}
      </a>
    );
  }

  return (
    <button
      id={id}
      data-sidebar="menu-sub-button"
      data-size={size}
      data-active={isActive}
      onClick={onClick}
      className={classes}
      data-refast-id={dataRefastId}
    >
      {children}
    </button>
  );
}

interface SidebarMenuSkeletonProps {
  id?: string;
  className?: string;
  showIcon?: boolean;
  'data-refast-id'?: string;
}

export function SidebarMenuSkeleton({
  id,
  className,
  showIcon = false,
  'data-refast-id': dataRefastId,
}: SidebarMenuSkeletonProps): React.ReactElement {
  const width = React.useMemo(() => {
    return `${Math.floor(Math.random() * 40) + 50}%`;
  }, []);

  return (
    <div
      id={id}
      data-sidebar="menu-skeleton"
      className={cn('rounded-md h-8 flex gap-2 px-2 items-center', className)}
      data-refast-id={dataRefastId}
    >
      {showIcon && (
        <div className="size-4 rounded-md bg-sidebar-accent animate-pulse" />
      )}
      <div
        className="h-4 flex-1 max-w-[--skeleton-width] rounded-md bg-sidebar-accent animate-pulse"
        style={{ '--skeleton-width': width } as React.CSSProperties}
      />
    </div>
  );
}

interface SidebarRailProps {
  id?: string;
  className?: string;
  'data-refast-id'?: string;
}

export function SidebarRail({
  id,
  className,
  'data-refast-id': dataRefastId,
}: SidebarRailProps): React.ReactElement {
  const context = React.useContext(SidebarContext);
  const toggleSidebar = context?.toggleSidebar;

  return (
    <button
      id={id}
      data-sidebar="rail"
      aria-label="Toggle Sidebar"
      tabIndex={-1}
      onClick={toggleSidebar}
      title="Toggle Sidebar"
      className={cn(
        'absolute inset-y-0 z-20 hidden w-4 -translate-x-1/2 transition-all ease-linear after:absolute after:inset-y-0 after:left-1/2 after:w-[2px] hover:after:bg-sidebar-border group-data-[side=left]:-right-4 group-data-[side=right]:left-0 sm:flex',
        '[[data-side=left]_&]:cursor-w-resize [[data-side=right]_&]:cursor-e-resize',
        '[[data-side=left][data-state=collapsed]_&]:cursor-e-resize [[data-side=right][data-state=collapsed]_&]:cursor-w-resize',
        'group-data-[collapsible=offcanvas]:translate-x-0 group-data-[collapsible=offcanvas]:after:left-full group-data-[collapsible=offcanvas]:hover:bg-sidebar',
        '[[data-side=left][data-collapsible=offcanvas]_&]:-right-2',
        '[[data-side=right][data-collapsible=offcanvas]_&]:-left-2',
        className
      )}
      data-refast-id={dataRefastId}
    />
  );
}

interface SidebarTriggerProps {
  id?: string;
  className?: string;
  onClick?: () => void;
  'data-refast-id'?: string;
}

export function SidebarTrigger({
  id,
  className,
  onClick,
  'data-refast-id': dataRefastId,
}: SidebarTriggerProps): React.ReactElement {
  const context = React.useContext(SidebarContext);

  const handleClick = () => {
    if (onClick) {
      onClick();
    } else if (context?.toggleSidebar) {
      context.toggleSidebar();
    }
  };

  return (
    <button
      id={id}
      data-sidebar="trigger"
      onClick={handleClick}
      className={cn(
        'inline-flex h-7 w-7 items-center justify-center rounded-md text-sm font-medium',
        'ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        className
      )}
      data-refast-id={dataRefastId}
    >
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
        className="size-4"
      >
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M9 3v18" />
      </svg>
      <span className="sr-only">Toggle Sidebar</span>
    </button>
  );
}

