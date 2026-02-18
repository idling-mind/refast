import { default as React } from 'react';
import { DayPicker } from 'react-day-picker';

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
export declare function Switch({ id, className, checked, defaultChecked, disabled, name, onCheckedChange, 'data-refast-id': dataRefastId, }: SwitchProps): React.ReactElement;
interface SliderProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
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
export declare function Slider({ id, className, label, description, required, error, value, defaultValue, min, max, step, disabled, orientation, onValueChange, onValueCommit, 'data-refast-id': dataRefastId, }: SliderProps): React.ReactElement;
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
export declare function Toggle({ id, className, label, pressed, defaultPressed, disabled, variant, size, onPressedChange, children, 'data-refast-id': dataRefastId, }: ToggleProps): React.ReactElement;
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
export declare function ToggleGroup({ id, className, type, value, defaultValue, disabled, variant, size, onValueChange, children, 'data-refast-id': dataRefastId, }: ToggleGroupProps): React.ReactElement;
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
export declare function ToggleGroupItem({ id, className, label, icon, value, disabled, variant, size, children, 'data-refast-id': dataRefastId, }: ToggleGroupItemProps): React.ReactElement;
interface CalendarProps {
    id?: string;
    className?: string;
    classNames?: Partial<React.ComponentProps<typeof DayPicker>['classNames']>;
    captionLayout?: 'label' | 'dropdown' | 'dropdown-years' | 'dropdown-months';
    mode?: 'single' | 'multiple' | 'range';
    buttonVariant?: 'default' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
    formatters?: Partial<React.ComponentProps<typeof DayPicker>['formatters']>;
    components?: Partial<React.ComponentProps<typeof DayPicker>['components']>;
    selected?: Date | Date[] | {
        from?: Date | string;
        to?: Date | string;
    } | string | string[];
    defaultMonth?: Date | string;
    disabled?: boolean | ((date: Date) => boolean);
    minDate?: Date | string;
    maxDate?: Date | string;
    showOutsideDays?: boolean;
    showWeekNumber?: boolean;
    numberOfMonths?: number;
    onSelect?: (date: Date | Date[] | {
        from: Date;
        to: Date;
    } | undefined) => void;
    onMonthChange?: (month: Date) => void;
    'data-refast-id'?: string;
}
export declare function Calendar({ id, className, classNames, mode, showOutsideDays, captionLayout, buttonVariant, formatters, components, selected, defaultMonth, disabled, minDate, maxDate, numberOfMonths, onSelect, onMonthChange, showWeekNumber, ...restProps }: CalendarProps): import("react/jsx-runtime").JSX.Element;
interface DatePickerProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    value?: string | string[] | {
        from?: string;
        to?: string;
    };
    placeholder?: string;
    disabled?: boolean;
    format?: string;
    mode?: 'single' | 'multiple' | 'range';
    captionLayout?: 'label' | 'dropdown' | 'dropdown-years' | 'dropdown-months';
    minDate?: string;
    maxDate?: string;
    numberOfMonths?: number;
    onChange?: (date: string | string[] | {
        from?: string;
        to?: string;
    } | undefined) => void;
    'data-refast-id'?: string;
}
export declare function DatePicker({ id, className, label, description, required, error, value, placeholder, disabled, mode, captionLayout, minDate, maxDate, numberOfMonths, onChange, 'data-refast-id': dataRefastId, }: DatePickerProps): React.ReactElement;
interface ComboboxOption {
    value: string;
    label: string;
}
interface ComboboxProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
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
export declare function Combobox({ id, className, label, description, required, error, options, value, placeholder, searchPlaceholder, emptyText, multiselect, disabled, onSelect, 'data-refast-id': dataRefastId, }: ComboboxProps): React.ReactElement;
interface InputOTPProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    maxLength?: number;
    value?: string;
    disabled?: boolean;
    pattern?: string;
    onChange?: (value: string) => void;
    onComplete?: (value: string) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function InputOTP({ id, className, label, description, required, error, maxLength, value, disabled, onChange, onComplete, children, 'data-refast-id': dataRefastId, }: InputOTPProps): React.ReactElement;
interface InputOTPGroupProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
export declare function InputOTPGroup({ id, className, children, 'data-refast-id': dataRefastId, }: InputOTPGroupProps): React.ReactElement;
interface InputOTPSlotProps {
    id?: string;
    className?: string;
    index: number;
    'data-refast-id'?: string;
}
export declare function InputOTPSlot({ id, className, index: _index, 'data-refast-id': dataRefastId, }: InputOTPSlotProps): React.ReactElement;
interface InputOTPSeparatorProps {
    id?: string;
    className?: string;
    'data-refast-id'?: string;
}
export declare function InputOTPSeparator({ id, className, 'data-refast-id': dataRefastId, }: InputOTPSeparatorProps): React.ReactElement;
export {};
