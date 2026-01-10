import { default as React } from 'react';

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
export declare function Slider({ id, className, value, defaultValue, min, max, step, disabled, orientation, onValueChange, onValueCommit, 'data-refast-id': dataRefastId, }: SliderProps): React.ReactElement;
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
export declare function ToggleGroupItem({ id, className, label, value, disabled, variant, size, children, 'data-refast-id': dataRefastId, }: ToggleGroupItemProps): React.ReactElement;
interface CalendarProps {
    id?: string;
    className?: string;
    mode?: 'single' | 'multiple' | 'range';
    selected?: Date | Date[] | {
        from: Date;
        to: Date;
    };
    defaultMonth?: Date;
    disabled?: boolean;
    showOutsideDays?: boolean;
    onSelect?: (date: Date | Date[] | {
        from: Date;
        to: Date;
    } | undefined) => void;
    onMonthChange?: (month: Date) => void;
    'data-refast-id'?: string;
}
export declare function Calendar({ id, className, mode: _mode, selected: _selected, showOutsideDays: _showOutsideDays, onSelect: _onSelect, 'data-refast-id': dataRefastId, }: CalendarProps): React.ReactElement;
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
export declare function DatePicker({ id, className, value, placeholder, disabled, onChange, 'data-refast-id': dataRefastId, }: DatePickerProps): React.ReactElement;
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
export declare function Combobox({ id, className, options, value, placeholder, searchPlaceholder, emptyText, multiselect, disabled, onSelect, 'data-refast-id': dataRefastId, }: ComboboxProps): React.ReactElement;
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
export declare function InputOTP({ id, className, maxLength, value, disabled, onChange, onComplete, children, 'data-refast-id': dataRefastId, }: InputOTPProps): React.ReactElement;
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
