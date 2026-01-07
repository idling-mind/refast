import { default as React } from 'react';

interface BreadcrumbProps {
    id?: string;
    className?: string;
    separator?: React.ReactNode;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function Breadcrumb({ id, className, children, 'data-refast-id': dataRefastId, }: BreadcrumbProps): React.ReactElement;
interface BreadcrumbListProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function BreadcrumbList({ id, className, children, 'data-refast-id': dataRefastId, }: BreadcrumbListProps): React.ReactElement;
interface BreadcrumbItemProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function BreadcrumbItem({ id, className, children, 'data-refast-id': dataRefastId, }: BreadcrumbItemProps): React.ReactElement;
interface BreadcrumbLinkProps {
    id?: string;
    className?: string;
    href?: string;
    onClick?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function BreadcrumbLink({ id, className, href, onClick, children, 'data-refast-id': dataRefastId, }: BreadcrumbLinkProps): React.ReactElement;
interface BreadcrumbPageProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function BreadcrumbPage({ id, className, children, 'data-refast-id': dataRefastId, }: BreadcrumbPageProps): React.ReactElement;
interface BreadcrumbSeparatorProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function BreadcrumbSeparator({ id, className, children, 'data-refast-id': dataRefastId, }: BreadcrumbSeparatorProps): React.ReactElement;
interface BreadcrumbEllipsisProps {
    id?: string;
    className?: string;
    'data-refast-id'?: string;
}
export declare function BreadcrumbEllipsis({ id, className, 'data-refast-id': dataRefastId, }: BreadcrumbEllipsisProps): React.ReactElement;
interface NavigationMenuProps {
    id?: string;
    className?: string;
    orientation?: 'horizontal' | 'vertical';
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function NavigationMenu({ id, className, children, 'data-refast-id': dataRefastId, }: NavigationMenuProps): React.ReactElement;
interface NavigationMenuListProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function NavigationMenuList({ id, className, children, 'data-refast-id': dataRefastId, }: NavigationMenuListProps): React.ReactElement;
interface NavigationMenuItemProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function NavigationMenuItem({ id, className, children, 'data-refast-id': dataRefastId, }: NavigationMenuItemProps): React.ReactElement;
interface NavigationMenuTriggerProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function NavigationMenuTrigger({ id, className, children, 'data-refast-id': dataRefastId, }: NavigationMenuTriggerProps): React.ReactElement;
interface NavigationMenuContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function NavigationMenuContent({ id, className, children, 'data-refast-id': dataRefastId, }: NavigationMenuContentProps): React.ReactElement;
interface NavigationMenuLinkProps {
    id?: string;
    className?: string;
    href?: string;
    active?: boolean;
    onClick?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function NavigationMenuLink({ id, className, href, active, onClick, children, 'data-refast-id': dataRefastId, }: NavigationMenuLinkProps): React.ReactElement;
interface PaginationProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function Pagination({ id, className, children, 'data-refast-id': dataRefastId, }: PaginationProps): React.ReactElement;
interface PaginationContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function PaginationContent({ id, className, children, 'data-refast-id': dataRefastId, }: PaginationContentProps): React.ReactElement;
interface PaginationItemProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function PaginationItem({ id, className, children, 'data-refast-id': dataRefastId, }: PaginationItemProps): React.ReactElement;
interface PaginationLinkProps {
    id?: string;
    className?: string;
    href?: string;
    active?: boolean;
    onClick?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function PaginationLink({ id, className, href, active, onClick, children, 'data-refast-id': dataRefastId, }: PaginationLinkProps): React.ReactElement;
interface PaginationPreviousProps {
    id?: string;
    className?: string;
    href?: string;
    onClick?: () => void;
    'data-refast-id'?: string;
}
export declare function PaginationPrevious({ id, className, href, onClick, 'data-refast-id': dataRefastId, }: PaginationPreviousProps): React.ReactElement;
interface PaginationNextProps {
    id?: string;
    className?: string;
    href?: string;
    onClick?: () => void;
    'data-refast-id'?: string;
}
export declare function PaginationNext({ id, className, href, onClick, 'data-refast-id': dataRefastId, }: PaginationNextProps): React.ReactElement;
interface PaginationEllipsisProps {
    id?: string;
    className?: string;
    'data-refast-id'?: string;
}
export declare function PaginationEllipsis({ id, className, 'data-refast-id': dataRefastId, }: PaginationEllipsisProps): React.ReactElement;
interface MenubarProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function Menubar({ id, className, children, 'data-refast-id': dataRefastId, }: MenubarProps): React.ReactElement;
interface MenubarMenuProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarMenu({ children, 'data-refast-id': dataRefastId, }: MenubarMenuProps): React.ReactElement;
interface MenubarTriggerProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarTrigger({ id, className, children, 'data-refast-id': dataRefastId, }: MenubarTriggerProps): React.ReactElement;
interface MenubarContentProps {
    id?: string;
    className?: string;
    align?: 'start' | 'center' | 'end';
    sideOffset?: number;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarContent({ id, className, align, sideOffset, children, 'data-refast-id': dataRefastId, }: MenubarContentProps): React.ReactElement;
interface MenubarItemProps {
    id?: string;
    className?: string;
    shortcut?: string;
    disabled?: boolean;
    onSelect?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarItem({ id, className, shortcut, disabled, onSelect, children, 'data-refast-id': dataRefastId, }: MenubarItemProps): React.ReactElement;
interface MenubarSeparatorProps {
    id?: string;
    className?: string;
    'data-refast-id'?: string;
}
export declare function MenubarSeparator({ id, className, 'data-refast-id': dataRefastId, }: MenubarSeparatorProps): React.ReactElement;
interface MenubarCheckboxItemProps {
    id?: string;
    className?: string;
    checked?: boolean;
    onCheckedChange?: (checked: boolean) => void;
    disabled?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarCheckboxItem({ id, className, checked, onCheckedChange, disabled, children, 'data-refast-id': dataRefastId, }: MenubarCheckboxItemProps): React.ReactElement;
interface MenubarRadioGroupProps {
    id?: string;
    className?: string;
    value?: string;
    onValueChange?: (value: string) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarRadioGroup({ id, className, value, onValueChange, children, 'data-refast-id': dataRefastId, }: MenubarRadioGroupProps): React.ReactElement;
interface MenubarRadioItemProps {
    id?: string;
    className?: string;
    value: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarRadioItem({ id, className, value, children, 'data-refast-id': dataRefastId, }: MenubarRadioItemProps): React.ReactElement;
interface MenubarSubProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarSub({ children, 'data-refast-id': dataRefastId, }: MenubarSubProps): React.ReactElement;
interface MenubarSubTriggerProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarSubTrigger({ id, className, children, 'data-refast-id': dataRefastId, }: MenubarSubTriggerProps): React.ReactElement;
interface MenubarSubContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function MenubarSubContent({ id, className, children, 'data-refast-id': dataRefastId, }: MenubarSubContentProps): React.ReactElement;
interface CommandProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function Command({ id, className, children, 'data-refast-id': dataRefastId, }: CommandProps): React.ReactElement;
interface CommandInputProps {
    id?: string;
    className?: string;
    placeholder?: string;
    value?: string;
    onValueChange?: (value: string) => void;
    'data-refast-id'?: string;
}
export declare function CommandInput({ id, className, placeholder, value, onValueChange, 'data-refast-id': dataRefastId, }: CommandInputProps): React.ReactElement;
interface CommandListProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function CommandList({ id, className, children, 'data-refast-id': dataRefastId, }: CommandListProps): React.ReactElement;
interface CommandEmptyProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function CommandEmpty({ id, className, children, 'data-refast-id': dataRefastId, }: CommandEmptyProps): React.ReactElement;
interface CommandGroupProps {
    id?: string;
    className?: string;
    heading?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function CommandGroup({ id, className, heading, children, 'data-refast-id': dataRefastId, }: CommandGroupProps): React.ReactElement;
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
export declare function CommandItem({ id, className, value, disabled, onSelect, children, 'data-refast-id': dataRefastId, }: CommandItemProps): React.ReactElement;
interface CommandSeparatorProps {
    id?: string;
    className?: string;
    'data-refast-id'?: string;
}
export declare function CommandSeparator({ id, className, 'data-refast-id': dataRefastId, }: CommandSeparatorProps): React.ReactElement;
interface CommandShortcutProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function CommandShortcut({ id, className, children, 'data-refast-id': dataRefastId, }: CommandShortcutProps): React.ReactElement;
interface SidebarProps {
    id?: string;
    className?: string;
    side?: 'left' | 'right';
    variant?: 'sidebar' | 'floating' | 'inset';
    collapsible?: 'offcanvas' | 'icon' | 'none';
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function Sidebar({ id, className, side, children, 'data-refast-id': dataRefastId, }: SidebarProps): React.ReactElement;
interface SidebarHeaderProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarHeader({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarHeaderProps): React.ReactElement;
interface SidebarContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarContent({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarContentProps): React.ReactElement;
interface SidebarFooterProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarFooter({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarFooterProps): React.ReactElement;
interface SidebarGroupProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarGroup({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarGroupProps): React.ReactElement;
interface SidebarGroupLabelProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarGroupLabel({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarGroupLabelProps): React.ReactElement;
interface SidebarGroupContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarGroupContent({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarGroupContentProps): React.ReactElement;
interface SidebarMenuProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarMenu({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarMenuProps): React.ReactElement;
interface SidebarMenuItemProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarMenuItem({ id, className, children, 'data-refast-id': dataRefastId, }: SidebarMenuItemProps): React.ReactElement;
interface SidebarMenuButtonProps {
    id?: string;
    className?: string;
    icon?: string;
    active?: boolean;
    onClick?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function SidebarMenuButton({ id, className, active, onClick, children, 'data-refast-id': dataRefastId, }: SidebarMenuButtonProps): React.ReactElement;
interface SidebarTriggerProps {
    id?: string;
    className?: string;
    'data-refast-id'?: string;
}
export declare function SidebarTrigger({ id, className, 'data-refast-id': dataRefastId, }: SidebarTriggerProps): React.ReactElement;
export {};
