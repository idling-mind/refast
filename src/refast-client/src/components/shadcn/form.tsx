import React from 'react';
import { cn } from '../../utils';

// ============================================================================
// Form - intercepts the native submit event and routes data to a server callback
// ============================================================================

interface FormProps {
  id?: string;
  className?: string;
  /** Callback fired when the form is submitted. Receives all named field values. */
  onSubmit?: (data: Record<string, string>) => void;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Form component - wraps a native <form> element, prevents the default browser
 * submit and calls `onSubmit` with a plain key→value map of all named fields.
 *
 * The Refast ComponentRenderer converts the Python `on_submit` callback into
 * a handler that expects a plain object as its first argument.  By constructing
 * `data` from `FormData`, the server callback receives all field values as
 * keyword arguments.
 */
export function Form({
  id,
  className,
  onSubmit,
  children,
  'data-refast-id': dataRefastId,
  ...props
}: FormProps): React.ReactElement {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (onSubmit) {
      const formData = new FormData(event.currentTarget);
      const data: Record<string, string> = {};
      formData.forEach((value, key) => {
        data[key] = value.toString();
      });
      onSubmit(data);
    }
  };

  return (
    <form
      id={id}
      className={cn('space-y-4', className)}
      onSubmit={handleSubmit}
      data-refast-id={dataRefastId}
      {...props}
    >
      {children}
    </form>
  );
}

// ============================================================================
// FormField - pairs an input with a label, hint text, and validation error
// ============================================================================

interface FormFieldProps {
  id?: string;
  className?: string;
  /** Label text displayed above the field. */
  label?: string;
  /** Hint text displayed between the label and the input. */
  hint?: string;
  /** Validation error message displayed below the input. */
  error?: string;
  /** Shows a required asterisk next to the label. */
  required?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * FormField component - wraps form controls with a consistent label / hint /
 * error layout.
 */
export function FormField({
  id,
  className,
  label,
  hint,
  error,
  required = false,
  children,
  'data-refast-id': dataRefastId,
}: FormFieldProps): React.ReactElement {
  return (
    <div id={id} className={cn('space-y-1', className)} data-refast-id={dataRefastId}>
      {label && (
        <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
          {label}
          {required && <span className="ml-1 text-destructive">*</span>}
        </label>
      )}
      {hint && (
        <p className="text-xs text-muted-foreground">{hint}</p>
      )}
      {children}
      {error && (
        <p className="text-xs text-destructive">{error}</p>
      )}
    </div>
  );
}
