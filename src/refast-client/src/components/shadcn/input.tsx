import React from 'react';
import * as CheckboxPrimitive from '@radix-ui/react-checkbox';
import * as RadioGroupPrimitive from '@radix-ui/react-radio-group';
import { Check, Circle } from 'lucide-react';
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
  debounce?: number;
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
  debounce = 0,
  onChange,
  onBlur,
  onFocus,
  'data-refast-id': dataRefastId,
}: InputProps): React.ReactElement {
  const [localValue, setLocalValue] = React.useState(value !== undefined ? value : (defaultValue || ''));
  const debounceTimeout = React.useRef<number | null>(null);
  const onChangeRef = React.useRef(onChange);
  const lastValueRef = React.useRef(value);

  React.useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  React.useEffect(() => {
    if (value !== undefined && value !== lastValueRef.current) {
      lastValueRef.current = value;
      if (!debounceTimeout.current) {
        setLocalValue(value);
      }
    }
  }, [value]);

  React.useEffect(() => () => {
    if (debounceTimeout.current !== null) {
      window.clearTimeout(debounceTimeout.current);
      debounceTimeout.current = null;
    }
  }, []);

  const handleChange = React.useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const nextValue = e.target.value;
      setLocalValue(nextValue);

      if (!onChangeRef.current) {
        return;
      }

      if (debounce > 0) {
        if (debounceTimeout.current !== null) {
          window.clearTimeout(debounceTimeout.current);
        }

        const syntheticEvent = {
          ...e,
          target: { ...e.target, value: nextValue },
          currentTarget: { ...e.currentTarget, value: nextValue },
        } as React.ChangeEvent<HTMLInputElement>;

        debounceTimeout.current = window.setTimeout(() => {
          debounceTimeout.current = null;
          onChangeRef.current?.(syntheticEvent);
        }, debounce);

        return;
      }

      onChangeRef.current(e);
    },
    [debounce]
  );

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
  debounce?: number;
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
  debounce = 0,
  onChange,
  onBlur,
  onFocus,
  'data-refast-id': dataRefastId,
}: TextareaProps): React.ReactElement {
  const [localValue, setLocalValue] = React.useState(value !== undefined ? value : (defaultValue || ''));
  const debounceTimeout = React.useRef<number | null>(null);
  const onChangeRef = React.useRef(onChange);
  const lastValueRef = React.useRef(value);

  React.useEffect(() => {
    onChangeRef.current = onChange;
  }, [onChange]);

  React.useEffect(() => {
    if (value !== undefined && value !== lastValueRef.current) {
      lastValueRef.current = value;
      if (!debounceTimeout.current) {
        setLocalValue(value);
      }
    }
  }, [value]);

  React.useEffect(() => () => {
    if (debounceTimeout.current !== null) {
      window.clearTimeout(debounceTimeout.current);
      debounceTimeout.current = null;
    }
  }, []);

  const handleChange = React.useCallback(
    (e: React.ChangeEvent<HTMLTextAreaElement>) => {
      const nextValue = e.target.value;
      setLocalValue(nextValue);

      if (!onChangeRef.current) {
        return;
      }

      if (debounce > 0) {
        if (debounceTimeout.current !== null) {
          window.clearTimeout(debounceTimeout.current);
        }

        const syntheticEvent = {
          ...e,
          target: { ...e.target, value: nextValue },
          currentTarget: { ...e.currentTarget, value: nextValue },
        } as React.ChangeEvent<HTMLTextAreaElement>;

        debounceTimeout.current = window.setTimeout(() => {
          debounceTimeout.current = null;
          onChangeRef.current?.(syntheticEvent);
        }, debounce);

        return;
      }

      onChangeRef.current(e);
    },
    [debounce]
  );

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
  onCheckedChange?: (checked: boolean) => void;
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
  onCheckedChange,
  label,
  'data-refast-id': dataRefastId,
}: CheckboxProps): React.ReactElement {
  const generatedId = React.useId();
  const checkboxId = id || generatedId;

  const [localChecked, setLocalChecked] = React.useState(checked !== undefined ? checked : (defaultChecked || false));

  React.useEffect(() => {
    if (checked !== undefined) {
      setLocalChecked(checked);
    }
  }, [checked]);

  const handleCheckedChange = (checked: boolean | 'indeterminate') => {
    const newChecked = checked === true;
    setLocalChecked(newChecked);
    if (onCheckedChange) {
      onCheckedChange(newChecked);
    }
  };

  return (
    <div className={cn('flex items-center space-x-2', className)} data-refast-id={dataRefastId}>
      <CheckboxPrimitive.Root
        id={checkboxId}
        name={name}
        value={value}
        checked={localChecked}
        defaultChecked={defaultChecked}
        disabled={disabled}
        onCheckedChange={handleCheckedChange}
        className={cn(
          'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground'
        )}
      >
        <CheckboxPrimitive.Indicator className={cn('flex items-center justify-center text-current')}>
          <Check className="h-4 w-4" />
        </CheckboxPrimitive.Indicator>
      </CheckboxPrimitive.Root>
      {label && (
        <label
          htmlFor={checkboxId}
          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          {label}
        </label>
      )}
    </div>
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
  options?: Array<{ value: string; label: string; disabled?: boolean }>;
  label?: string;
  onValueChange?: (value: string) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * RadioGroup component - container for radio buttons with options support.
 */
export function RadioGroup({
  id,
  className,
  name,
  value,
  defaultValue,
  disabled = false,
  orientation = 'vertical',
  options,
  label,
  onValueChange,
  children,
  'data-refast-id': dataRefastId,
}: RadioGroupProps): React.ReactElement {
  const generatedId = React.useId();
  const rootId = id || generatedId;

  const [localValue, setLocalValue] = React.useState(value !== undefined ? value : (defaultValue || ''));

  React.useEffect(() => {
    if (value !== undefined) {
      setLocalValue(value);
    }
  }, [value]);

  const handleValueChange = (newValue: string) => {
    setLocalValue(newValue);
    if (onValueChange) {
      onValueChange(newValue);
    }
  };

  return (
    <div className={cn('space-y-2', className)} data-refast-id={dataRefastId}>
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
        </label>
      )}
      <RadioGroupPrimitive.Root
        className={cn(
          'flex',
          orientation === 'vertical' ? 'flex-col space-y-2' : 'flex-row space-x-4'
        )}
        value={localValue}
        defaultValue={defaultValue}
        disabled={disabled}
        name={name}
        onValueChange={handleValueChange}
        orientation={orientation}
        id={rootId}
      >
        {options?.map((option) => (
          <div className="flex items-center space-x-2" key={option.value}>
            <RadioGroupPrimitive.Item
              value={option.value}
              id={`${rootId}-${option.value}`}
              disabled={disabled || option.disabled}
              className={cn(
                'aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background',
                'focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:cursor-not-allowed disabled:opacity-50'
              )}
            >
              <RadioGroupPrimitive.Indicator className="flex items-center justify-center">
                <Circle className="h-2.5 w-2.5 fill-current text-current" />
              </RadioGroupPrimitive.Indicator>
            </RadioGroupPrimitive.Item>
            <label
              htmlFor={`${rootId}-${option.value}`}
              className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              {option.label}
            </label>
          </div>
        ))}
        {children}
      </RadioGroupPrimitive.Root>
    </div>
  );
}

interface CheckboxGroupOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface CheckboxGroupProps {
  id?: string;
  className?: string;
  name?: string;
  value?: string[];
  defaultValue?: string[];
  disabled?: boolean;
  orientation?: 'horizontal' | 'vertical';
  options?: CheckboxGroupOption[];
  label?: string;
  onChange?: (value: string[]) => void;
  'data-refast-id'?: string;
}

/**
 * CheckboxGroup component - group of checkboxes for multi-selection.
 */
export function CheckboxGroup({
  id,
  className,
  name,
  value,
  defaultValue,
  disabled = false,
  orientation = 'vertical',
  options,
  label,
  onChange,
  'data-refast-id': dataRefastId,
}: CheckboxGroupProps): React.ReactElement {
  const generatedId = React.useId();
  const rootId = id || generatedId;

  const [localValue, setLocalValue] = React.useState<string[]>(
    value !== undefined ? value : (defaultValue || [])
  );

  React.useEffect(() => {
    if (value !== undefined) {
      setLocalValue(value);
    }
  }, [value]);

  const handleCheckedChange = (optionValue: string, checked: boolean) => {
    let newValue: string[];
    if (checked) {
      if (!localValue.includes(optionValue)) {
        newValue = [...localValue, optionValue];
      } else {
        newValue = localValue;
      }
    } else {
      newValue = localValue.filter((v) => v !== optionValue);
    }
    setLocalValue(newValue);
    if (onChange) {
      onChange(newValue);
    }
  };

  return (
    <div
      id={rootId}
      role="group"
      className={cn('space-y-2', className)}
      data-refast-id={dataRefastId}
    >
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
        </label>
      )}
      <div
        className={cn(
          'flex',
          orientation === 'vertical' ? 'flex-col space-y-2' : 'flex-row space-x-4'
        )}
      >
        {options?.map((option) => (
          <Checkbox
            key={option.value}
            id={`${rootId}-${option.value}`}
            name={name}
            checked={localValue.includes(option.value)}
            disabled={disabled || option.disabled}
            onCheckedChange={(checked) => handleCheckedChange(option.value, checked)}
            label={option.label}
          />
        ))}
      </div>
    </div>
  );
}
