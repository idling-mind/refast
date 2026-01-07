import { BaseProps, ChildrenProp } from './types';
/**
 * Overlay Components using Radix UI primitives
 * AlertDialog, Sheet, Drawer, HoverCard, Popover
 */
import * as React from 'react';
export interface AlertDialogProps extends BaseProps, ChildrenProp {
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
export declare function AlertDialog({ open, onOpenChange, title, description, confirmLabel, cancelLabel, onConfirm, onCancel, trigger, variant, className, children, ...props }: AlertDialogProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogTriggerProps extends ChildrenProp {
    asChild?: boolean;
    className?: string;
}
export declare function AlertDialogTrigger({ asChild, className, children, }: AlertDialogTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogContentProps extends ChildrenProp {
    className?: string;
}
export declare function AlertDialogContent({ className, children, }: AlertDialogContentProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogHeaderProps extends ChildrenProp {
    className?: string;
}
export declare function AlertDialogHeader({ className, children, }: AlertDialogHeaderProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogFooterProps extends ChildrenProp {
    className?: string;
}
export declare function AlertDialogFooter({ className, children, }: AlertDialogFooterProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogTitleProps extends ChildrenProp {
    title?: string;
    className?: string;
}
export declare function AlertDialogTitle({ title, className, children, }: AlertDialogTitleProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogDescriptionProps extends ChildrenProp {
    description?: string;
    className?: string;
}
export declare function AlertDialogDescription({ description, className, children, }: AlertDialogDescriptionProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogActionProps extends ChildrenProp {
    label?: string;
    onClick?: () => void;
    className?: string;
}
export declare function AlertDialogAction({ label, onClick, className, children, }: AlertDialogActionProps): import("react/jsx-runtime").JSX.Element;
export interface AlertDialogCancelProps extends ChildrenProp {
    label?: string;
    onClick?: () => void;
    className?: string;
}
export declare function AlertDialogCancel({ label, onClick, className, children, }: AlertDialogCancelProps): import("react/jsx-runtime").JSX.Element;
export interface SheetProps extends ChildrenProp {
    open?: boolean;
    defaultOpen?: boolean;
    onOpenChange?: (open: boolean) => void;
}
export declare function Sheet({ open, defaultOpen, onOpenChange, children, }: SheetProps): import("react/jsx-runtime").JSX.Element;
export interface SheetTriggerProps extends ChildrenProp {
    asChild?: boolean;
    className?: string;
}
export declare function SheetTrigger({ asChild, className, children, }: SheetTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface SheetCloseProps extends ChildrenProp {
    asChild?: boolean;
    className?: string;
}
export declare function SheetClose({ asChild, className, children, }: SheetCloseProps): import("react/jsx-runtime").JSX.Element;
export interface SheetContentProps extends ChildrenProp {
    side?: 'top' | 'right' | 'bottom' | 'left';
    className?: string;
}
export declare function SheetContent({ side, className, children, }: SheetContentProps): import("react/jsx-runtime").JSX.Element;
export interface SheetHeaderProps extends ChildrenProp {
    className?: string;
}
export declare function SheetHeader({ className, children, }: SheetHeaderProps): import("react/jsx-runtime").JSX.Element;
export interface SheetFooterProps extends ChildrenProp {
    className?: string;
}
export declare function SheetFooter({ className, children, }: SheetFooterProps): import("react/jsx-runtime").JSX.Element;
export interface SheetTitleProps extends ChildrenProp {
    title?: string;
    className?: string;
}
export declare function SheetTitle({ title, className, children, }: SheetTitleProps): import("react/jsx-runtime").JSX.Element;
export interface SheetDescriptionProps extends ChildrenProp {
    description?: string;
    className?: string;
}
export declare function SheetDescription({ description, className, children, }: SheetDescriptionProps): import("react/jsx-runtime").JSX.Element;
export interface DrawerProps extends BaseProps, ChildrenProp {
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
    title?: string;
    description?: string;
    trigger?: React.ReactNode;
}
export declare function Drawer({ open, onOpenChange, title, description, trigger, className, children, ...props }: DrawerProps): import("react/jsx-runtime").JSX.Element;
export interface HoverCardProps extends BaseProps, ChildrenProp {
    trigger?: React.ReactNode;
    openDelay?: number;
    closeDelay?: number;
    side?: 'top' | 'right' | 'bottom' | 'left';
    align?: 'start' | 'center' | 'end';
}
export declare function HoverCard({ trigger, openDelay, closeDelay, side, align, className, children, ...props }: HoverCardProps): import("react/jsx-runtime").JSX.Element;
export interface PopoverProps extends BaseProps, ChildrenProp {
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
    trigger: React.ReactNode;
    side?: 'top' | 'right' | 'bottom' | 'left';
    align?: 'start' | 'center' | 'end';
}
export declare function Popover({ open, onOpenChange, trigger, side, align, className, children, ...props }: PopoverProps): import("react/jsx-runtime").JSX.Element;
export interface HoverCardTriggerProps extends ChildrenProp {
    asChild?: boolean;
    className?: string;
}
export declare function HoverCardTrigger({ asChild, className, children, }: HoverCardTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface HoverCardContentProps extends ChildrenProp {
    className?: string;
    side?: 'top' | 'right' | 'bottom' | 'left';
    align?: 'start' | 'center' | 'end';
    sideOffset?: number;
}
export declare function HoverCardContent({ className, side, align, sideOffset, children, }: HoverCardContentProps): import("react/jsx-runtime").JSX.Element;
export interface PopoverTriggerProps extends ChildrenProp {
    asChild?: boolean;
    className?: string;
}
export declare function PopoverTrigger({ asChild, className, children, }: PopoverTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface PopoverContentProps extends ChildrenProp {
    className?: string;
    side?: 'top' | 'right' | 'bottom' | 'left';
    align?: 'start' | 'center' | 'end';
    sideOffset?: number;
}
export declare function PopoverContent({ className, side, align, sideOffset, children, }: PopoverContentProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuProps extends ChildrenProp {
    open?: boolean;
    defaultOpen?: boolean;
    onOpenChange?: (open: boolean) => void;
}
export declare function DropdownMenu({ open, defaultOpen, onOpenChange, children, }: DropdownMenuProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuTriggerProps extends BaseProps, ChildrenProp {
    asChild?: boolean;
}
export declare function DropdownMenuTrigger({ asChild, className, children, }: DropdownMenuTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuContentProps extends BaseProps, ChildrenProp {
    side?: 'top' | 'right' | 'bottom' | 'left';
    sideOffset?: number;
    align?: 'start' | 'center' | 'end';
}
export declare function DropdownMenuContent({ side, sideOffset, align, className, children, ...props }: DropdownMenuContentProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuItemProps extends Omit<BaseProps, 'onSelect'>, ChildrenProp {
    icon?: string;
    shortcut?: string;
    disabled?: boolean;
    onSelect?: () => void;
}
export declare function DropdownMenuItem({ icon, shortcut, disabled, onSelect, className, children, ...props }: DropdownMenuItemProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuLabelProps extends BaseProps, ChildrenProp {
    inset?: boolean;
}
export declare function DropdownMenuLabel({ inset, className, children, ...props }: DropdownMenuLabelProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuSeparatorProps extends BaseProps {
}
export declare function DropdownMenuSeparator({ className, ...props }: DropdownMenuSeparatorProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuCheckboxItemProps extends ChildrenProp {
    checked?: boolean;
    onCheckedChange?: (checked: boolean) => void;
    disabled?: boolean;
    className?: string;
}
export declare function DropdownMenuCheckboxItem({ checked, onCheckedChange, disabled, className, children, }: DropdownMenuCheckboxItemProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuRadioGroupProps extends BaseProps, ChildrenProp {
    value?: string;
    onValueChange?: (value: string) => void;
}
export declare function DropdownMenuRadioGroup({ value, onValueChange, className, children, ...props }: DropdownMenuRadioGroupProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuRadioItemProps extends ChildrenProp {
    value: string;
    className?: string;
}
export declare function DropdownMenuRadioItem({ value, className, children, }: DropdownMenuRadioItemProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuSubProps extends ChildrenProp {
}
export declare function DropdownMenuSub({ children, }: DropdownMenuSubProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuSubTriggerProps extends BaseProps, ChildrenProp {
    inset?: boolean;
}
export declare function DropdownMenuSubTrigger({ inset, className, children, ...props }: DropdownMenuSubTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface DropdownMenuSubContentProps extends BaseProps, ChildrenProp {
}
export declare function DropdownMenuSubContent({ className, children, ...props }: DropdownMenuSubContentProps): import("react/jsx-runtime").JSX.Element;
export interface ContextMenuProps extends ChildrenProp {
    className?: string;
}
export declare function ContextMenu({ children, }: ContextMenuProps): import("react/jsx-runtime").JSX.Element;
export interface ContextMenuTriggerProps extends ChildrenProp {
    asChild?: boolean;
    className?: string;
}
export declare function ContextMenuTrigger({ asChild, className, children, }: ContextMenuTriggerProps): import("react/jsx-runtime").JSX.Element;
export interface ContextMenuContentProps extends BaseProps, ChildrenProp {
}
export declare function ContextMenuContent({ className, children, ...props }: ContextMenuContentProps): import("react/jsx-runtime").JSX.Element;
export interface ContextMenuItemProps extends Omit<BaseProps, 'onSelect'>, ChildrenProp {
    icon?: string;
    shortcut?: string;
    disabled?: boolean;
    onSelect?: () => void;
}
export declare function ContextMenuItem({ icon, shortcut, disabled, onSelect, className, children, ...props }: ContextMenuItemProps): import("react/jsx-runtime").JSX.Element;
export interface ContextMenuSeparatorProps extends BaseProps {
}
export declare function ContextMenuSeparator({ className, ...props }: ContextMenuSeparatorProps): import("react/jsx-runtime").JSX.Element;
export interface ContextMenuCheckboxItemProps extends ChildrenProp {
    checked?: boolean;
    onCheckedChange?: (checked: boolean) => void;
    disabled?: boolean;
    className?: string;
}
export declare function ContextMenuCheckboxItem({ checked, onCheckedChange, disabled, className, children, }: ContextMenuCheckboxItemProps): import("react/jsx-runtime").JSX.Element;
export declare const OverlayComponents: {
    AlertDialog: typeof AlertDialog;
    AlertDialogTrigger: typeof AlertDialogTrigger;
    AlertDialogContent: typeof AlertDialogContent;
    AlertDialogHeader: typeof AlertDialogHeader;
    AlertDialogFooter: typeof AlertDialogFooter;
    AlertDialogTitle: typeof AlertDialogTitle;
    AlertDialogDescription: typeof AlertDialogDescription;
    AlertDialogAction: typeof AlertDialogAction;
    AlertDialogCancel: typeof AlertDialogCancel;
    Sheet: typeof Sheet;
    SheetTrigger: typeof SheetTrigger;
    SheetContent: typeof SheetContent;
    SheetHeader: typeof SheetHeader;
    SheetFooter: typeof SheetFooter;
    SheetTitle: typeof SheetTitle;
    SheetDescription: typeof SheetDescription;
    SheetClose: typeof SheetClose;
    Drawer: typeof Drawer;
    HoverCard: typeof HoverCard;
    HoverCardTrigger: typeof HoverCardTrigger;
    HoverCardContent: typeof HoverCardContent;
    Popover: typeof Popover;
    PopoverTrigger: typeof PopoverTrigger;
    PopoverContent: typeof PopoverContent;
    DropdownMenu: typeof DropdownMenu;
    DropdownMenuTrigger: typeof DropdownMenuTrigger;
    DropdownMenuContent: typeof DropdownMenuContent;
    DropdownMenuItem: typeof DropdownMenuItem;
    DropdownMenuLabel: typeof DropdownMenuLabel;
    DropdownMenuSeparator: typeof DropdownMenuSeparator;
    DropdownMenuCheckboxItem: typeof DropdownMenuCheckboxItem;
    DropdownMenuRadioGroup: typeof DropdownMenuRadioGroup;
    DropdownMenuRadioItem: typeof DropdownMenuRadioItem;
    DropdownMenuSub: typeof DropdownMenuSub;
    DropdownMenuSubTrigger: typeof DropdownMenuSubTrigger;
    DropdownMenuSubContent: typeof DropdownMenuSubContent;
    ContextMenu: typeof ContextMenu;
    ContextMenuTrigger: typeof ContextMenuTrigger;
    ContextMenuContent: typeof ContextMenuContent;
    ContextMenuItem: typeof ContextMenuItem;
    ContextMenuSeparator: typeof ContextMenuSeparator;
    ContextMenuCheckboxItem: typeof ContextMenuCheckboxItem;
};
