import { default as React } from 'react';

export interface InputWrapperProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    children: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * InputWrapper - A reusable wrapper component for form controls.
 * Provides consistent styling for label, description, required indicator, and error messages.
 *
 * Can be used standalone or internally by form components like Input, Slider, DatePicker, etc.
 */
export declare function InputWrapper({ id, className, label, description, required, error, children, 'data-refast-id': dataRefastId, }: InputWrapperProps): React.ReactElement;
interface OptionItem {
    value: string;
    label: string;
    disabled?: boolean;
}
interface InputProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    type?: 'text' | 'password' | 'email' | 'number' | 'search' | 'tel' | 'url';
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    required?: boolean;
    error?: string;
    name?: string;
    debounce?: number;
    onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
    onKeydown?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
    onKeyup?: (event: React.KeyboardEvent<HTMLInputElement>) => void;
    onInput?: (event: React.FormEvent<HTMLInputElement>) => void;
    'data-refast-id'?: string;
}
/**
 * Input component - shadcn-styled text input with label, description, and error support.
 *
 * The `debounce` prop delays calling `onChange` by the specified milliseconds.
 * This is useful for reducing server calls while the user is typing.
 * Per-action debounce/throttle (on Callback, StoreProp, etc.) is applied
 * independently by the action execution engine in ComponentRenderer.
 */
export declare function Input({ id, className, label, description, type, placeholder, value, defaultValue, disabled, required, error, name, debounce, onChange, onBlur, onFocus, onKeydown, onKeyup, onInput, 'data-refast-id': dataRefastId, }: InputProps): React.ReactElement;
interface TextareaProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    rows?: number;
    name?: string;
    debounce?: number;
    onChange?: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
    onBlur?: (event: React.FocusEvent<HTMLTextAreaElement>) => void;
    onFocus?: (event: React.FocusEvent<HTMLTextAreaElement>) => void;
    'data-refast-id'?: string;
}
/**
 * Textarea component - shadcn-styled textarea with label, description, and error support.
 *
 * The `debounce` prop delays calling `onChange` by the specified milliseconds.
 */
export declare function Textarea({ id, className, label, description, required, error, placeholder, value, defaultValue, disabled, rows, name, debounce, onChange, onBlur, onFocus, 'data-refast-id': dataRefastId, }: TextareaProps): React.ReactElement;
interface SelectOption {
    value: string;
    label: string;
    disabled?: boolean;
}
interface SelectProps {
    id?: string;
    className?: string;
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    placeholder?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    name?: string;
    options?: SelectOption[];
    onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Select component - shadcn-styled select input with label, description, and error support.
 */
export declare function Select({ id, className, label, description, required, error, placeholder, value, defaultValue, disabled, name, options, onChange, children, 'data-refast-id': dataRefastId, }: SelectProps): React.ReactElement;
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
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    checked?: boolean;
    defaultChecked?: boolean;
    disabled?: boolean;
    name?: string;
    value?: string;
    onCheckedChange?: (checked: boolean) => void;
    'data-refast-id'?: string;
}
/**
 * Checkbox component - shadcn-styled checkbox with label, description, and error support.
 */
export declare function Checkbox({ id, className, label, description, required, error, checked, defaultChecked, disabled, name, value, onCheckedChange, 'data-refast-id': dataRefastId, }: CheckboxProps): React.ReactElement;
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
    description?: string;
    required?: boolean;
    error?: string;
    'data-refast-id'?: string;
}
/**
 * Radio component - shadcn-styled radio button.
 */
export declare function Radio({ id, className, checked, defaultChecked, disabled, name, value, onChange, label, description, required, error, 'data-refast-id': dataRefastId, }: RadioProps): React.ReactElement;
interface RadioGroupProps {
    id?: string;
    className?: string;
    name?: string;
    value?: string;
    defaultValue?: string;
    disabled?: boolean;
    orientation?: 'horizontal' | 'vertical';
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    options?: OptionItem[];
    onValueChange?: (value: string) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * RadioGroup component - container for radio buttons using children composition.
 */
export declare function RadioGroup({ id, className, name, value, defaultValue, disabled, orientation, label, description, required, error, options, onValueChange, children, 'data-refast-id': dataRefastId, }: RadioGroupProps): React.ReactElement;
interface CheckboxGroupProps {
    id?: string;
    className?: string;
    name?: string;
    value?: string[];
    defaultValue?: string[];
    disabled?: boolean;
    orientation?: 'horizontal' | 'vertical';
    label?: string;
    description?: string;
    required?: boolean;
    error?: string;
    options?: OptionItem[];
    onChange?: (value: string[]) => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CheckboxGroup component - group of checkboxes using children composition.
 */
export declare function CheckboxGroup({ id, className, name, value, defaultValue, disabled, orientation, label, description, required, error, options, onChange, children, 'data-refast-id': dataRefastId, }: CheckboxGroupProps): React.ReactElement;
export {};
