import React from 'react';
import { cn } from '../../utils';

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
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void;
  'data-refast-id'?: string;
}

/**
 * Input component - shadcn-styled text input.
 */
export function Input({
  id,
  className,
  type = 'text',
  placeholder,
  value,
  defaultValue,
  disabled = false,
  required = false,
  name,
  onChange,
  onBlur,
  onFocus,
  'data-refast-id': dataRefastId,
}: InputProps): React.ReactElement {
  const [localValue, setLocalValue] = React.useState(value !== undefined ? value : (defaultValue || ''));

  React.useEffect(() => {
    if (value !== undefined) {
      setLocalValue(value);
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalValue(e.target.value);
    if (onChange) {
      onChange(e);
    }
  };

  return (
    <input
      id={id}
      type={type}
      placeholder={placeholder}
      value={localValue}
      disabled={disabled}
      required={required}
      name={name}
      onChange={handleChange}
      onBlur={onBlur}
      onFocus={onFocus}
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm',
        'ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium',
        'placeholder:text-muted-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    />
  );
}

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
  onChange?: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onBlur?: (event: React.FocusEvent<HTMLTextAreaElement>) => void;
  onFocus?: (event: React.FocusEvent<HTMLTextAreaElement>) => void;
  'data-refast-id'?: string;
}

/**
 * Textarea component - shadcn-styled textarea.
 */
export function Textarea({
  id,
  className,
  placeholder,
  value,
  defaultValue,
  disabled = false,
  required = false,
  rows = 3,
  name,
  onChange,
  onBlur,
  onFocus,
  'data-refast-id': dataRefastId,
}: TextareaProps): React.ReactElement {
  const [localValue, setLocalValue] = React.useState(value !== undefined ? value : (defaultValue || ''));

  React.useEffect(() => {
    if (value !== undefined) {
      setLocalValue(value);
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setLocalValue(e.target.value);
    if (onChange) {
      onChange(e);
    }
  };

  return (
    <textarea
      id={id}
      placeholder={placeholder}
      value={localValue}
      disabled={disabled}
      required={required}
      rows={rows}
      name={name}
      onChange={handleChange}
      onBlur={onBlur}
      onFocus={onFocus}
      className={cn(
        'flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm',
        'ring-offset-background placeholder:text-muted-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    />
  );
}

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
export function Select({
  id,
  className,
  placeholder,
  value,
  defaultValue,
  disabled = false,
  required = false,
  name,
  options,
  onChange,
  children,
  'data-refast-id': dataRefastId,
}: SelectProps): React.ReactElement {
  const [localValue, setLocalValue] = React.useState(value !== undefined ? value : (defaultValue || ''));

  React.useEffect(() => {
    if (value !== undefined) {
      setLocalValue(value);
    }
  }, [value]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLocalValue(e.target.value);
    if (onChange) {
      onChange(e);
    }
  };

  return (
    <select
      id={id}
      value={localValue}
      disabled={disabled}
      required={required}
      name={name}
      onChange={handleChange}
      className={cn(
        'flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm',
        'ring-offset-background placeholder:text-muted-foreground',
        'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {placeholder && (
        <option value="" disabled>
          {placeholder}
        </option>
      )}
      {options?.map((option) => (
        <option key={option.value} value={option.value} disabled={option.disabled}>
          {option.label}
        </option>
      ))}
      {children}
    </select>
  );
}

interface SelectOptionProps {
  value: string;
  disabled?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * SelectOption component - option for Select.
 */
export function SelectOption({
  value,
  disabled = false,
  children,
  'data-refast-id': dataRefastId,
}: SelectOptionProps): React.ReactElement {
  return (
    <option value={value} disabled={disabled} data-refast-id={dataRefastId}>
      {children}
    </option>
  );
}

interface CheckboxProps {
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
 * Checkbox component - shadcn-styled checkbox.
 */
export function Checkbox({
  id,
  className,
  checked,
  defaultChecked,
  disabled = false,
  name,
  value,
  onChange,
  label,
  'data-refast-id': dataRefastId,
}: CheckboxProps): React.ReactElement {
  const [localChecked, setLocalChecked] = React.useState(checked !== undefined ? checked : (defaultChecked || false));

  React.useEffect(() => {
    if (checked !== undefined) {
      setLocalChecked(checked);
    }
  }, [checked]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalChecked(e.target.checked);
    if (onChange) {
      onChange(e);
    }
  };

  return (
    <label className={cn('flex items-center space-x-2', className)} data-refast-id={dataRefastId}>
      <input
        id={id}
        type="checkbox"
        checked={localChecked}
        disabled={disabled}
        name={name}
        value={value}
        onChange={handleChange}
        className={cn(
          'h-4 w-4 shrink-0 rounded border border-primary ring-offset-background',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground'
        )}
      />
      {label && <span className="text-sm font-medium leading-none">{label}</span>}
    </label>
  );
}

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
export function Radio({
  id,
  className,
  checked,
  defaultChecked,
  disabled = false,
  name,
  value,
  onChange,
  label,
  'data-refast-id': dataRefastId,
}: RadioProps): React.ReactElement {
  const [localChecked, setLocalChecked] = React.useState(checked !== undefined ? checked : (defaultChecked || false));

  React.useEffect(() => {
    if (checked !== undefined) {
      setLocalChecked(checked);
    }
  }, [checked]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalChecked(e.target.checked);
    if (onChange) {
      onChange(e);
    }
  };

  return (
    <label className={cn('flex items-center space-x-2', className)} data-refast-id={dataRefastId}>
      <input
        id={id}
        type="radio"
        checked={localChecked}
        disabled={disabled}
        name={name}
        value={value}
        onChange={handleChange}
        className={cn(
          'aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background',
          'focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50'
        )}
      />
      {label && <span className="text-sm font-medium leading-none">{label}</span>}
    </label>
  );
}

interface RadioGroupProps {
  id?: string;
  className?: string;
  name?: string;
  value?: string;
  defaultValue?: string;
  disabled?: boolean;
  orientation?: 'horizontal' | 'vertical';
  onChange?: (value: string) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * RadioGroup component - container for radio buttons.
 */
export function RadioGroup({
  id,
  className,
  orientation = 'vertical',
  children,
  'data-refast-id': dataRefastId,
}: RadioGroupProps): React.ReactElement {
  return (
    <div
      id={id}
      role="radiogroup"
      className={cn(
        'flex',
        orientation === 'vertical' ? 'flex-col space-y-2' : 'flex-row space-x-4',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </div>
  );
}
