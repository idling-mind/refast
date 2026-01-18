import { default as React } from 'react';

interface OptionItem {
    value: string;
    label: string;
    disabled?: boolean;
}
interface InputProps {
    id?: string;
    className?: string;
    type?: 'text' | 'password' | 'email' | 'number' | 'search' | 'tel' | 'url';
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    required?: boolean;
    name?: string;
    debounce?: number;
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
    'data-refast-id'?: string;
}
/**
 * Input component - shadcn-styled text input.
 */
export declare function Input({ id, className, type, placeholder, value, defaultValue, disabled, required, name, debounce, onChange, onBlur, onFocus, 'data-refast-id': dataRefastId, }: InputProps): React.ReactElement;
interface TextareaProps {
    id?: string;
    className?: string;
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    required?: boolean;
    rows?: number;
    name?: string;
    debounce?: number;
    onChange?: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
    onBlur?: (event: React.FocusEvent<HTMLTextAreaElement>) => void;
    onFocus?: (event: React.FocusEvent<HTMLTextAreaElement>) => void;
    'data-refast-id'?: string;
}
/**
 * Textarea component - shadcn-styled textarea.
 */
export declare function Textarea({ id, className, placeholder, value, defaultValue, disabled, required, rows, name, debounce, onChange, onBlur, onFocus, 'data-refast-id': dataRefastId, }: TextareaProps): React.ReactElement;
interface SelectOption {
    value: string;
    label: string;
    disabled?: boolean;
}
interface SelectProps {
    id?: string;
    className?: string;
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    required?: boolean;
    name?: string;
    options?: SelectOption[];
    onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Select component - shadcn-styled select input.
 */
export declare function Select({ id, className, placeholder, value, defaultValue, disabled, required, name, options, onChange, children, 'data-refast-id': dataRefastId, }: SelectProps): React.ReactElement;
interface SelectOptionProps {
    value: string;
    disabled?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * SelectOption component - option for Select.
 */
export declare function SelectOption({ value, disabled, children, 'data-refast-id': dataRefastId, }: SelectOptionProps): React.ReactElement;
interface CheckboxProps {
    id?: string;
    className?: string;
    checked?: boolean;
    defaultChecked?: boolean;
    disabled?: boolean;
    name?: string;
    value?: string;
    onCheckedChange?: (checked: boolean) => void;
    label?: string;
    'data-refast-id'?: string;
}
/**
 * Checkbox component - shadcn-styled checkbox.
 */
export declare function Checkbox({ id, className, checked, defaultChecked, disabled, name, value, onCheckedChange, label, 'data-refast-id': dataRefastId, }: CheckboxProps): React.ReactElement;
interface RadioProps {
    id?: string;
    className?: string;
    checked?: boolean;
    defaultChecked?: boolean;
    disabled?: boolean;
    name?: string;
    value?: string;
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
    label?: string;
    'data-refast-id'?: string;
}
/**
 * Radio component - shadcn-styled radio button.
 */
export declare function Radio({ id, className, checked, defaultChecked, disabled, name, value, onChange, label, 'data-refast-id': dataRefastId, }: RadioProps): React.ReactElement;
interface RadioGroupProps {
    id?: string;
    className?: string;
    name?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    orientation?: 'horizontal' | 'vertical';
    label?: string;
    options?: OptionItem[];
    onValueChange?: (value: string) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * RadioGroup component - container for radio buttons using children composition.
 */
export declare function RadioGroup({ id, className, name, value, defaultValue, disabled, orientation, label, options, onValueChange, children, 'data-refast-id': dataRefastId, }: RadioGroupProps): React.ReactElement;
interface CheckboxGroupProps {
    id?: string;
    className?: string;
    name?: string;
    value?: string[];
    defaultValue?: string[];
    disabled?: boolean;
    orientation?: 'horizontal' | 'vertical';
    label?: string;
    options?: OptionItem[];
    onChange?: (value: string[]) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CheckboxGroup component - group of checkboxes using children composition.
 */
export declare function CheckboxGroup({ id, className, name, value, defaultValue, disabled, orientation, label, options, onChange, children, 'data-refast-id': dataRefastId, }: CheckboxGroupProps): React.ReactElement;
export {};
