import React from 'react';
import * as CheckboxPrimitive from '@radix-ui/react-checkbox';
import * as RadioGroupPrimitive from '@radix-ui/react-radio-group';
import { Check, Circle } from 'lucide-react';
import { cn } from '../../utils';

// ============================================================================
// InputWrapper - Reusable wrapper for form controls with label, description, error
// ============================================================================

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
export function InputWrapper({
  id,
  className,
  label,
  description,
  required = false,
  error,
  children,
  'data-refast-id': dataRefastId,
}: InputWrapperProps): React.ReactElement {
  // If no label, description, or error, just return the children
  if (!label && !description && !error) {
    return <>{children}</>;
  }

  return (
    <div className={cn('mb-2', className)} data-input-wrapper data-refast-id={dataRefastId}>
    {/* <div className={className} data-input-wrapper data-refast-id={dataRefastId}> */}
      {label && (
        <label
          htmlFor={id}
          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          {label}
          {required && <span className="text-destructive ml-1">*</span>}
        </label>
      )}
      {description && (
        <p className="text-sm text-muted-foreground">{description}</p>
      )}
      <div className="my-1">
        {children}
      </div>
      {error && (
        <p className="text-xs text-destructive">{error}</p>
      )}
    </div>
  );
}

// Type for options array used in RadioGroup and CheckboxGroup
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
 * Per-action debounce/throttle (on Callback, SaveProp, etc.) is applied
 * independently by the action execution engine in ComponentRenderer.
 */
export function Input({
  id,
  className,
  label,
  description,
  type = 'text',
  placeholder,
  value,
  defaultValue,
  disabled = false,
  required = false,
  error,
  name,
  debounce = 0,
  onChange,
  onBlur,
  onFocus,
  onKeydown,
  onKeyup,
  onInput,
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

  // Listen for force-value-sync events from update_props.
  // This handles the edge case where the prop value string hasn't changed
  // (e.g. "" → "") but localValue has drifted due to user typing.
  React.useEffect(() => {
    const handleForceSync = (e: Event) => {
      const { targetId, value: newValue } = (e as CustomEvent).detail;
      if (targetId === id && newValue !== undefined) {
        lastValueRef.current = newValue;
        setLocalValue(newValue);
        // Cancel any pending debounced onChange so it doesn't push
        // a stale user-typed value back via save_prop.
        if (debounceTimeout.current !== null) {
          window.clearTimeout(debounceTimeout.current);
          debounceTimeout.current = null;
        }
      }
    };
    window.addEventListener('refast:force-value-sync', handleForceSync);
    return () => window.removeEventListener('refast:force-value-sync', handleForceSync);
  }, [id]);

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

        // Spread only copies own enumerable properties from the DOM element.
        // tagName, name, type live on the prototype chain and must be
        // copied explicitly so that extractEventData can identify this as
        // a form element and extract its value.
        const syntheticEvent = {
          ...e,
          target: { ...e.target, tagName: e.target.tagName, name: e.target.name, type: e.target.type, value: nextValue },
          currentTarget: { ...e.currentTarget, tagName: e.currentTarget.tagName, name: e.currentTarget.name, type: e.currentTarget.type, value: nextValue },
        } as React.ChangeEvent<HTMLInputElement>;

        debounceTimeout.current = window.setTimeout(() => {
          debounceTimeout.current = null;
          onChangeRef.current?.(syntheticEvent);
        }, debounce);

        return;
      }

      onChangeRef.current(e);
    },
    [debounce, name]
  );

  const inputElement = (
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
      onKeyDown={onKeydown}
      onKeyUp={onKeyup}
      onInput={onInput}
      className={cn(
        'flex h-10 w-full rounded-md border bg-background px-3 py-2 text-sm',
        'ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        error
          ? 'border-destructive placeholder:text-destructive'
          : 'border-input placeholder:text-muted-foreground',
        className
      )}
    />
  );

  // Wrap with InputWrapper if label, description, or error is provided
  if (label || description || error) {
    return (
      <InputWrapper
        id={id}
        label={label}
        description={description}
        required={required}
        error={error}
        data-refast-id={dataRefastId}
      >
        {inputElement}
      </InputWrapper>
    );
  }

  return <div data-refast-id={dataRefastId}>{inputElement}</div>;
}

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
  onKeydown?: (event: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  onKeyup?: (event: React.KeyboardEvent<HTMLTextAreaElement>) => void;
  onInput?: (event: React.FormEvent<HTMLTextAreaElement>) => void;
  'data-refast-id'?: string;
}

/**
 * Textarea component - shadcn-styled textarea with label, description, and error support.
 * 
 * The `debounce` prop delays calling `onChange` by the specified milliseconds.
 */
export function Textarea({
  id,
  className,
  label,
  description,
  required = false,
  error,
  placeholder,
  value,
  defaultValue,
  disabled = false,
  rows = 3,
  name,
  debounce = 0,
  onChange,
  onBlur,
  onFocus,
  onKeydown,
  onKeyup,
  onInput,
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

  // Listen for force-value-sync events from update_props.
  React.useEffect(() => {
    const handleForceSync = (e: Event) => {
      const { targetId, value: newValue } = (e as CustomEvent).detail;
      if (targetId === id && newValue !== undefined) {
        lastValueRef.current = newValue;
        setLocalValue(newValue);
        if (debounceTimeout.current !== null) {
          window.clearTimeout(debounceTimeout.current);
          debounceTimeout.current = null;
        }
      }
    };
    window.addEventListener('refast:force-value-sync', handleForceSync);
    return () => window.removeEventListener('refast:force-value-sync', handleForceSync);
  }, [id]);

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

        // Spread only copies own enumerable properties from the DOM element.
        // tagName, name live on the prototype chain and must be copied
        // explicitly so that extractEventData can identify this as a
        // form element and extract its value.
        const syntheticEvent = {
          ...e,
          target: { ...e.target, tagName: e.target.tagName, name: e.target.name, value: nextValue },
          currentTarget: { ...e.currentTarget, tagName: e.currentTarget.tagName, name: e.currentTarget.name, value: nextValue },
        } as React.ChangeEvent<HTMLTextAreaElement>;

        debounceTimeout.current = window.setTimeout(() => {
          debounceTimeout.current = null;
          onChangeRef.current?.(syntheticEvent);
        }, debounce);

        return;
      }

      onChangeRef.current(e);
    },
    [debounce, name]
  );

  const textareaElement = (
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
      onKeyDown={onKeydown}
      onKeyUp={onKeyup}
      onInput={onInput}
      className={cn(
        'flex min-h-[80px] w-full rounded-md border bg-background px-3 py-2 text-sm',
        'ring-offset-background placeholder:text-muted-foreground',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        error ? 'border-destructive' : 'border-input',
        className
      )}
    />
  );

  if (label || description || error) {
    return (
      <InputWrapper
        id={id}
        label={label}
        description={description}
        required={required}
        error={error}
        data-refast-id={dataRefastId}
      >
        {textareaElement}
      </InputWrapper>
    );
  }

  return <div data-refast-id={dataRefastId}>{textareaElement}</div>;
}

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
export function Select({
  id,
  className,
  label,
  description,
  required = false,
  error,
  placeholder,
  value,
  defaultValue,
  disabled = false,
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

  // Listen for force-value-sync events from update_props.
  React.useEffect(() => {
    const handleForceSync = (e: Event) => {
      const { targetId, value: newValue } = (e as CustomEvent).detail;
      if (targetId === id && newValue !== undefined) {
        setLocalValue(newValue);
      }
    };
    window.addEventListener('refast:force-value-sync', handleForceSync);
    return () => window.removeEventListener('refast:force-value-sync', handleForceSync);
  }, [id]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLocalValue(e.target.value);
    if (onChange) {
      onChange(e);
    }
  };

  const selectElement = (
    <select
      id={id}
      value={localValue}
      disabled={disabled}
      required={required}
      name={name}
      onChange={handleChange}
      className={cn(
        'flex h-10 w-full items-center justify-between rounded-md border bg-background px-3 py-2 text-sm',
        'ring-offset-background placeholder:text-muted-foreground',
        'focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
        'disabled:cursor-not-allowed disabled:opacity-50',
        error ? 'border-destructive' : 'border-input',
        className
      )}
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

  if (label || description || error) {
    return (
      <InputWrapper
        id={id}
        label={label}
        description={description}
        required={required}
        error={error}
        data-refast-id={dataRefastId}
      >
        {selectElement}
      </InputWrapper>
    );
  }

  return <div data-refast-id={dataRefastId}>{selectElement}</div>;
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
export function Checkbox({
  id,
  className,
  label,
  description,
  required = false,
  error,
  checked,
  defaultChecked,
  disabled = false,
  name,
  value,
  onCheckedChange,
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

  const handleCheckedChange = (checkedState: boolean | 'indeterminate') => {
    const newChecked = checkedState === true;
    setLocalChecked(newChecked);
    if (onCheckedChange) {
      onCheckedChange(newChecked);
    }
  };

  const checkboxElement = (
    <div className="flex items-center space-x-2">
      <CheckboxPrimitive.Root
        id={checkboxId}
        name={name}
        value={value}
        checked={localChecked}
        defaultChecked={defaultChecked}
        disabled={disabled}
        onCheckedChange={handleCheckedChange}
        className={cn(
          'peer h-4 w-4 shrink-0 rounded-sm border ring-offset-background',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground',
          error ? 'border-destructive' : 'border-primary'
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
          {required && <span className="text-destructive ml-1">*</span>}
        </label>
      )}
    </div>
  );

  if (description || error) {
    return (
      <div className={cn('space-y-1', className)} data-refast-id={dataRefastId}>
        {checkboxElement}
        {description && (
          <p className="text-sm text-muted-foreground ml-6">{description}</p>
        )}
        {error && (
          <p className="text-xs text-destructive ml-6">{error}</p>
        )}
      </div>
    );
  }

  return <div className={className} data-refast-id={dataRefastId}>{checkboxElement}</div>;
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
  description?: string;
  required?: boolean;
  error?: string;
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
  description,
  required,
  error,
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
    <div className="space-y-1" data-refast-id={dataRefastId}>
      <label className={cn('flex items-center space-x-2', className)}>
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
            'disabled:cursor-not-allowed disabled:opacity-50',
            error && 'border-destructive'
          )}
        />
        {label && (
          <span className="text-sm font-medium leading-none">
            {label}
            {required && <span className="text-destructive ml-1">*</span>}
          </span>
        )}
      </label>
      {(description || error) && (
        <div className="ml-6">
          {description && !error && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
          {error && <p className="text-sm text-destructive">{error}</p>}
        </div>
      )}
    </div>
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
export function RadioGroup({
  id,
  className,
  name,
  value,
  defaultValue,
  disabled = false,
  orientation = 'vertical',
  label,
  description,
  required,
  error,
  options,
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

  // Listen for force-value-sync events from update_props.
  React.useEffect(() => {
    const handleForceSync = (e: Event) => {
      const { targetId, value: newValue } = (e as CustomEvent).detail;
      if (targetId === id && newValue !== undefined) {
        setLocalValue(newValue);
      }
    };
    window.addEventListener('refast:force-value-sync', handleForceSync);
    return () => window.removeEventListener('refast:force-value-sync', handleForceSync);
  }, [id]);

  const handleValueChange = (newValue: string) => {
    setLocalValue(newValue);
    if (onValueChange) {
      onValueChange(newValue);
    }
  };

  // Render radio items from options if provided
  const renderItems = () => {
    if (options && options.length > 0) {
      return options.map((option) => (
        <div key={option.value} className="flex items-center space-x-2">
          <RadioGroupPrimitive.Item
            value={option.value}
            id={`${rootId}-${option.value}`}
            disabled={option.disabled}
            className={cn(
              'aspect-square h-4 w-4 rounded-full border border-primary text-primary ring-offset-background',
              'focus:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
              'disabled:cursor-not-allowed disabled:opacity-50',
              error && 'border-destructive'
            )}
          >
            <RadioGroupPrimitive.Indicator className="flex items-center justify-center">
              <Circle className="h-2.5 w-2.5 fill-current text-current" />
            </RadioGroupPrimitive.Indicator>
          </RadioGroupPrimitive.Item>
          <label
            htmlFor={`${rootId}-${option.value}`}
            className={cn(
              'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
              option.disabled && 'cursor-not-allowed opacity-70'
            )}
          >
            {option.label}
          </label>
        </div>
      ));
    }
    return children;
  };

  return (
    <div className={cn('space-y-1', className)} data-refast-id={dataRefastId}>
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
          {required && <span className="text-destructive ml-1">*</span>}
        </label>
      )}
      {description && !error && (
        <p className="text-sm text-muted-foreground">{description}</p>
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
        {renderItems()}
      </RadioGroupPrimitive.Root>
      {error && <p className="text-sm text-destructive">{error}</p>}
    </div>
  );
}

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
export function CheckboxGroup({
  id,
  className,
  name,
  value,
  defaultValue,
  disabled = false,
  orientation = 'vertical',
  label,
  description,
  required,
  error,
  options,
  onChange,
  children,
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

  // Render checkbox items from options if provided
  const renderItems = () => {
    if (options && options.length > 0) {
      return options.map((option) => {
        const checkboxId = `${rootId}-${option.value}`;
        const isChecked = localValue.includes(option.value);
        const isDisabled = disabled || option.disabled;
        return (
          <div key={option.value} className="flex items-center space-x-2">
            <CheckboxPrimitive.Root
              id={checkboxId}
              name={name}
              value={option.value}
              checked={isChecked}
              disabled={isDisabled}
              onCheckedChange={(checked) => handleCheckedChange(option.value, checked === true)}
              className={cn(
                'peer h-4 w-4 shrink-0 rounded-sm border border-primary ring-offset-background',
                'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
                'disabled:cursor-not-allowed disabled:opacity-50',
                'data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground',
                error && 'border-destructive'
              )}
            >
              <CheckboxPrimitive.Indicator className={cn('flex items-center justify-center text-current')}>
                <Check className="h-4 w-4" />
              </CheckboxPrimitive.Indicator>
            </CheckboxPrimitive.Root>
            <label
              htmlFor={checkboxId}
              className={cn(
                'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
                isDisabled && 'cursor-not-allowed opacity-70'
              )}
            >
              {option.label}
            </label>
          </div>
        );
      });
    }
    // Fall back to children composition
    return React.Children.map(children, (child) => {
      if (React.isValidElement(child) && child.props.value) {
        const childValue = child.props.value as string;
        return React.cloneElement(child as React.ReactElement<CheckboxProps>, {
          name,
          checked: localValue.includes(childValue),
          disabled: disabled || child.props.disabled,
          onCheckedChange: (checked: boolean) => handleCheckedChange(childValue, checked),
        });
      }
      return child;
    });
  };

  return (
    <div
      id={rootId}
      role="group"
      className={cn('space-y-1', className)}
      data-refast-id={dataRefastId}
    >
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
          {required && <span className="text-destructive ml-1">*</span>}
        </label>
      )}
      {description && !error && (
        <p className="text-sm text-muted-foreground">{description}</p>
      )}
      <div
        className={cn(
          'flex',
          orientation === 'vertical' ? 'flex-col space-y-2' : 'flex-row space-x-4'
        )}
      >
        {renderItems()}
      </div>
      {error && <p className="text-sm text-destructive">{error}</p>}
    </div>
  );
}
