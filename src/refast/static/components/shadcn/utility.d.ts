import { default as useEmblaCarousel } from 'embla-carousel-react';
import { BaseProps, ChildrenProp } from './types';
/**
 * Utility Components using Radix UI primitives
 * Separator, AspectRatio, ScrollArea, Collapsible, Carousel, Resizable, InputOTP
 */
import * as React from 'react';
export interface SeparatorProps extends BaseProps {
    orientation?: 'horizontal' | 'vertical';
    decorative?: boolean;
}
export declare function Separator({ orientation, decorative, className, ...props }: SeparatorProps): import("react/jsx-runtime").JSX.Element;
export interface AspectRatioProps extends BaseProps, ChildrenProp {
    ratio?: number;
}
export declare function AspectRatio({ ratio, className, children, ...props }: AspectRatioProps): import("react/jsx-runtime").JSX.Element;
export interface ScrollAreaProps {
    className?: string;
    children?: React.ReactNode;
    type?: 'auto' | 'always' | 'scroll' | 'hover';
    scrollHideDelay?: number;
}
export declare function ScrollArea({ type, scrollHideDelay, className, children, }: ScrollAreaProps): import("react/jsx-runtime").JSX.Element;
export interface CollapsibleProps extends BaseProps, ChildrenProp {
    open?: boolean;
    defaultOpen?: boolean;
    onOpenChange?: (open: boolean) => void;
    disabled?: boolean;
    trigger?: React.ReactNode;
}
export declare function Collapsible({ open, defaultOpen, onOpenChange, disabled, trigger, className, children, ...props }: CollapsibleProps): import("react/jsx-runtime").JSX.Element;
export interface CarouselProps extends BaseProps, ChildrenProp {
    orientation?: 'horizontal' | 'vertical';
    opts?: Parameters<typeof useEmblaCarousel>[0];
}
export declare function Carousel({ orientation, opts, className, children, ...props }: CarouselProps): import("react/jsx-runtime").JSX.Element;
export interface CarouselContentProps extends BaseProps, ChildrenProp {
}
export declare function CarouselContent({ className, children, ...props }: CarouselContentProps): import("react/jsx-runtime").JSX.Element;
export interface CarouselItemProps extends BaseProps, ChildrenProp {
}
export declare function CarouselItem({ className, children, ...props }: CarouselItemProps): import("react/jsx-runtime").JSX.Element;
export interface CarouselPreviousProps extends BaseProps {
    onClick?: () => void;
}
export declare function CarouselPrevious({ className, onClick, ...props }: CarouselPreviousProps): import("react/jsx-runtime").JSX.Element;
export interface CarouselNextProps extends BaseProps {
    onClick?: () => void;
}
export declare function CarouselNext({ className, onClick, ...props }: CarouselNextProps): import("react/jsx-runtime").JSX.Element;
export interface ResizableProps extends BaseProps, ChildrenProp {
    direction?: 'horizontal' | 'vertical';
}
export declare function Resizable({ direction, className, children, ...props }: ResizableProps): import("react/jsx-runtime").JSX.Element;
export interface ResizablePanelProps extends BaseProps, ChildrenProp {
    defaultSize?: number;
    minSize?: number;
    maxSize?: number;
}
export declare function ResizablePanel({ defaultSize, minSize, maxSize, className, children, ...props }: ResizablePanelProps): import("react/jsx-runtime").JSX.Element;
export interface ResizableHandleProps extends BaseProps {
    withHandle?: boolean;
}
export declare function ResizableHandle({ withHandle, className, ...props }: ResizableHandleProps): import("react/jsx-runtime").JSX.Element;
export interface InputOTPProps {
    className?: string;
    maxLength?: number;
    value?: string;
    onChange?: (value: string) => void;
    disabled?: boolean;
    pattern?: string;
    autoFocus?: boolean;
}
export declare function InputOTP({ maxLength, value, onChange, disabled, pattern, autoFocus, className, }: InputOTPProps): import("react/jsx-runtime").JSX.Element;
export interface InputOTPGroupProps extends BaseProps, ChildrenProp {
}
export declare function InputOTPGroup({ className, children, ...props }: InputOTPGroupProps): import("react/jsx-runtime").JSX.Element;
export interface InputOTPSlotProps extends BaseProps {
    index: number;
    char?: string;
    hasFakeCaret?: boolean;
    isActive?: boolean;
}
export declare function InputOTPSlot({ index, char, hasFakeCaret, isActive, className, ...props }: InputOTPSlotProps): import("react/jsx-runtime").JSX.Element;
export interface InputOTPSeparatorProps extends BaseProps {
}
export declare function InputOTPSeparator({ className, ...props }: InputOTPSeparatorProps): import("react/jsx-runtime").JSX.Element;
type Theme = 'light' | 'dark' | 'system';
export interface ThemeSwitcherProps extends Omit<BaseProps, 'onChange'> {
    defaultTheme?: Theme;
    storageKey?: string;
    showSystemOption?: boolean;
    mode?: 'toggle' | 'dropdown';
    onChange?: (theme: Theme) => void;
}
export declare function ThemeSwitcher({ defaultTheme, storageKey, showSystemOption, mode, onChange, className, ...props }: ThemeSwitcherProps): import("react/jsx-runtime").JSX.Element;
export declare const UtilityComponents: {
    Separator: typeof Separator;
    AspectRatio: typeof AspectRatio;
    ScrollArea: typeof ScrollArea;
    Collapsible: typeof Collapsible;
    Carousel: typeof Carousel;
    CarouselContent: typeof CarouselContent;
    CarouselItem: typeof CarouselItem;
    CarouselPrevious: typeof CarouselPrevious;
    CarouselNext: typeof CarouselNext;
    Resizable: typeof Resizable;
    ResizablePanel: typeof ResizablePanel;
    ResizableHandle: typeof ResizableHandle;
    InputOTP: typeof InputOTP;
    InputOTPGroup: typeof InputOTPGroup;
    InputOTPSlot: typeof InputOTPSlot;
    InputOTPSeparator: typeof InputOTPSeparator;
    ThemeSwitcher: typeof ThemeSwitcher;
};
export {};
