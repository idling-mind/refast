import React, { useEffect, useCallback, useState } from 'react';
import { Toaster, toast, type ExternalToast } from 'sonner';

interface ToastEventDetail {
  message: string;
  variant?: 'default' | 'success' | 'error' | 'destructive' | 'warning' | 'info' | 'loading';
  description?: string;
  duration?: number;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
  dismissible?: boolean;
  close_button?: boolean;
  invert?: boolean;
  action?: { label: string; callback_id: string };
  cancel?: { label: string; callback_id: string };
  id?: string;
}

interface ToastManagerProps {
  className?: string;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
  richColors?: boolean;
  closeButton?: boolean;
  duration?: number;
  expand?: boolean;
  visibleToasts?: number;
  offset?: string | number;
  gap?: number;
  dir?: 'ltr' | 'rtl' | 'auto';
  hotkey?: string[];
  invert?: boolean;
}

/**
 * ToastManager component - manages and displays toast notifications using Sonner.
 * Listens for 'refast:toast' custom events dispatched by the StateManager.
 *
 * Supports all Sonner toast options:
 * - variant: success, error, warning, info, loading, or default
 * - description: secondary text below the message
 * - duration: time in ms (use Infinity for persistent toasts)
 * - position: override default position
 * - dismissible: whether clicking dismisses the toast
 * - closeButton: show a close button
 * - invert: invert the color scheme
 * - action: primary action button with callback
 * - cancel: secondary cancel button with callback
 * - id: custom ID for updating/dismissing
 */
export function ToastManager({
  className,
  position = 'bottom-right',
  richColors = true,
  closeButton = true,
  duration = 4000,
  expand = false,
  visibleToasts = 3,
  offset,
  gap = 14,
  dir = 'auto',
  hotkey = ['altKey', 'KeyT'],
  invert = false,
}: ToastManagerProps): React.ReactElement {
  // Detect current theme from document element
  // This syncs with ThemeSwitcher which adds 'dark' or 'light' class to <html>
  const [currentTheme, setCurrentTheme] = useState<'light' | 'dark'>(() => {
    if (typeof document !== 'undefined') {
      return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    }
    return 'light';
  });

  // Listen for theme changes via MutationObserver on document.documentElement
  useEffect(() => {
    if (typeof document === 'undefined') return;

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          const isDark = document.documentElement.classList.contains('dark');
          setCurrentTheme(isDark ? 'dark' : 'light');
        }
      }
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, []);

  // Create action/cancel button handlers
  const createActionHandler = useCallback((callbackId: string) => {
    return () => {
      // Dispatch a callback event to be handled by EventManager
      window.dispatchEvent(
        new CustomEvent('refast:callback', {
          detail: { callbackId, data: {} },
        })
      );
    };
  }, []);

  // Listen for refast:toast events
  useEffect(() => {
    const handleToastEvent = (event: CustomEvent<ToastEventDetail>) => {
      const {
        message,
        variant = 'default',
        description,
        duration: customDuration,
        position: customPosition,
        dismissible = true,
        close_button,
        invert: customInvert,
        action,
        cancel,
        id,
      } = event.detail;

      // Build toast options
      const options: ExternalToast = {
        description,
        duration: customDuration,
        position: customPosition,
        dismissible,
        closeButton: close_button,
        invert: customInvert,
        id,
      };

      // Add action button if specified
      if (action) {
        options.action = {
          label: action.label,
          onClick: createActionHandler(action.callback_id),
        };
      }

      // Add cancel button if specified
      if (cancel) {
        options.cancel = {
          label: cancel.label,
          onClick: createActionHandler(cancel.callback_id),
        };
      }

      // Remove undefined values
      Object.keys(options).forEach((key) => {
        if (options[key as keyof ExternalToast] === undefined) {
          delete options[key as keyof ExternalToast];
        }
      });

      // Call the appropriate toast function based on variant
      switch (variant) {
        case 'success':
          toast.success(message, options);
          break;
        case 'destructive':
        case 'error':
          toast.error(message, options);
          break;
        case 'warning':
          toast.warning(message, options);
          break;
        case 'info':
          toast.info(message, options);
          break;
        case 'loading':
          toast.loading(message, options);
          break;
        default:
          toast(message, options);
          break;
      }
    };

    window.addEventListener('refast:toast', handleToastEvent as EventListener);
    return () => {
      window.removeEventListener('refast:toast', handleToastEvent as EventListener);
    };
  }, [createActionHandler]);

  return (
    <Toaster
      className={className}
      position={position}
      richColors={richColors}
      closeButton={closeButton}
      duration={duration}
      expand={expand}
      visibleToasts={visibleToasts}
      theme={currentTheme}
      offset={offset}
      gap={gap}
      dir={dir}
      hotkey={hotkey}
      invert={invert}
      toastOptions={{
        classNames: {
          toast: 'group',
        },
      }}
    />
  );
}

// Export toast function and utilities for programmatic use
export { toast };

/**
 * Dismiss a toast by ID.
 */
export function dismissToast(toastId?: string | number): void {
  toast.dismiss(toastId);
}

/**
 * Show a promise toast that updates based on promise state.
 * Returns the original promise for chaining.
 */
export function promiseToast<T>(
  promise: Promise<T>,
  messages: {
    loading: string;
    success: string | ((data: T) => string);
    error: string | ((error: unknown) => string);
  }
): Promise<T> {
  toast.promise(promise, messages);
  return promise;
}

export default ToastManager;
