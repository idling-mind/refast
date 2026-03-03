import React, { useEffect, useState } from 'react';
import { Toaster, toast, type ExternalToast } from 'sonner';
import { AnyActionRef, ComponentTree } from '../types';
import { useEventManager } from '../events/EventManager';
import { createSingleActionExecutor } from '../utils/actionExecutor';
import { ComponentRenderer } from './ComponentRenderer';
import { applyUpdate } from '../state/StateManager';

function DynamicToastContent({ initialTree }: { initialTree: ComponentTree }) {
  const [tree, setTree] = useState<ComponentTree>(initialTree);
  const eventManager = useEventManager();

  useEffect(() => {
    return eventManager.onUpdate((message: any) => {
      if (message.type === 'update') {
        if (message.targetId && message.operation) {
          let updateObj: ComponentTree | null = message.component || null;

          if (message.operation === 'update_children' && message.children) {
            updateObj = { type: '', id: '', props: {}, children: message.children } as unknown as ComponentTree;
          } else if (message.operation === 'update_props' && (message.props || message.children)) {
            updateObj = { type: '', id: '', props: message.props || {}, children: message.children || [] } as unknown as ComponentTree;
            // Flag whether children were explicitly provided in the message
            (updateObj as any).__hasChildren = 'children' in message;
          } else if (message.operation === 'append_prop' && message.propName !== undefined) {
            updateObj = { type: '', id: '', props: { __propName: message.propName, __value: message.value } } as unknown as ComponentTree;
          }

          setTree((currentTree) => {
            if (!currentTree) return currentTree;
            return applyUpdate(currentTree, message.targetId, updateObj, message.operation);
          });
        }
      }
    });
  }, [eventManager]);

  return <ComponentRenderer tree={tree} />;
}

interface ToastEventDetail {
  message?: string;
  component?: ComponentTree;
  variant?: 'default' | 'success' | 'error' | 'destructive' | 'warning' | 'info' | 'loading';
  description?: string;
  duration?: number;
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'top-center' | 'bottom-center';
  dismissible?: boolean;
  close_button?: boolean;
  invert?: boolean;
  action?: { label: string; callback: AnyActionRef };
  cancel?: { label: string; callback: AnyActionRef };
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
  const eventManager = useEventManager();

  // Detect current theme from document element
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

  // Listen for refast:toast events
  useEffect(() => {
    const handleToastEvent = (event: CustomEvent<ToastEventDetail>) => {
      const {
        message,
        component,
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
        const executor = createSingleActionExecutor(action.callback, eventManager);
        options.action = {
          label: action.label,
          onClick: () => { executor({}, []); },
        };
      }

      // Add cancel button if specified
      if (cancel) {
        const executor = createSingleActionExecutor(cancel.callback, eventManager);
        options.cancel = {
          label: cancel.label,
          onClick: () => { executor({}, []); },
        };
      }

      // Remove undefined values
      Object.keys(options).forEach((key) => {
        if (options[key as keyof ExternalToast] === undefined) {
          delete options[key as keyof ExternalToast];
        }
      });

      const content = component ? <DynamicToastContent initialTree={component} /> : (message || '');

      // Call the appropriate toast function based on variant
      switch (variant) {
        case 'success':
          toast.success(content, options);
          break;
        case 'destructive':
        case 'error':
          toast.error(content, options);
          break;
        case 'warning':
          toast.warning(content, options);
          break;
        case 'info':
          toast.info(content, options);
          break;
        case 'loading':
          toast.loading(content, options);
          break;
        default:
          toast(content as any, options);
          break;
      }
    };

    window.addEventListener('refast:toast', handleToastEvent as EventListener);
    return () => {
      window.removeEventListener('refast:toast', handleToastEvent as EventListener);
    };
  }, [eventManager]);

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
        }
      }}
      style={{
        fontFamily: 'inherit'
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
