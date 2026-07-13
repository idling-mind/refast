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
  /** Whether to include disabled form input values in the payload. Defaults to true. */
  includeDisabled?: boolean;
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
  includeDisabled = true,
  'data-refast-id': dataRefastId,
  ...props
}: FormProps): React.ReactElement<any> {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (onSubmit) {
      const formData = new FormData(event.currentTarget);

      if (includeDisabled) {
        // Include disabled input fields' values in the form payload
        const disabledElements = event.currentTarget.querySelectorAll<
          HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
        >('input[name]:disabled, select[name]:disabled, textarea[name]:disabled');

        disabledElements.forEach((el) => {
          const name = el.name;
          if (!name) return;

          if (el instanceof HTMLInputElement) {
            if (el.type === 'checkbox' || el.type === 'radio') {
              if (el.checked) {
                formData.append(name, el.value);
              }
            } else if (el.type === 'file') {
              if (el.files) {
                for (let i = 0; i < el.files.length; i++) {
                  formData.append(name, el.files[i]);
                }
              }
            } else {
              formData.append(name, el.value);
            }
          } else if (el instanceof HTMLSelectElement) {
            if (el.multiple) {
              for (let i = 0; i < el.options.length; i++) {
                if (el.options[i].selected) {
                  formData.append(name, el.options[i].value);
                }
              }
            } else {
              formData.append(name, el.value);
            }
          } else if (el instanceof HTMLTextAreaElement) {
            formData.append(name, el.value);
          }
        });
      }

      const data: Record<string, string | string[]> = {};
      formData.forEach((value, key) => {
        const valStr = value.toString();
        if (key in data) {
          const existing = data[key];
          if (Array.isArray(existing)) {
            existing.push(valStr);
          } else {
            data[key] = [existing, valStr];
          }
        } else {
          data[key] = valStr;
        }
      });
      onSubmit(data as Record<string, string>);
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
}: FormFieldProps): React.ReactElement<any> {
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
