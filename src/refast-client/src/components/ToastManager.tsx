import React, { useEffect, useState, useCallback } from 'react';
import { cn } from '../utils';

interface ToastItem {
  id: string;
  message: string;
  variant: 'default' | 'destructive' | 'success' | 'info' | 'warning';
  duration: number;
  createdAt: number;
}

interface ToastManagerProps {
  className?: string;
}

/**
 * ToastManager component - manages and displays toast notifications.
 * Listens for 'refast:toast' custom events dispatched by the StateManager.
 */
export function ToastManager({ className }: ToastManagerProps): React.ReactElement {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  // Add a new toast
  const addToast = useCallback((message: string, variant: string = 'default', duration: number = 3000) => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
    const toast: ToastItem = {
      id,
      message,
      variant: variant as ToastItem['variant'],
      duration,
      createdAt: Date.now(),
    };

    setToasts((prev) => [...prev, toast]);

    // Auto-remove after duration
    setTimeout(() => {
      removeToast(id);
    }, duration);
  }, []);

  // Remove a toast by id
  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  // Listen for refast:toast events
  useEffect(() => {
    const handleToastEvent = (event: CustomEvent<{ message: string; variant?: string; duration?: number }>) => {
      console.log('[Refast ToastManager] Received toast event:', event.detail);
      const { message, variant = 'default', duration = 3000 } = event.detail;
      addToast(message, variant, duration);
    };

    window.addEventListener('refast:toast', handleToastEvent as EventListener);
    console.log('[Refast ToastManager] Listening for refast:toast events');
    return () => {
      window.removeEventListener('refast:toast', handleToastEvent as EventListener);
    };
  }, [addToast]);

  const variantClasses: Record<ToastItem['variant'], string> = {
    default: 'bg-background border border-border text-foreground',
    destructive: 'bg-destructive border-destructive text-destructive-foreground',
    success: 'bg-green-500 border-green-600 text-white',
    info: 'bg-blue-500 border-blue-600 text-white',
    warning: 'bg-yellow-500 border-yellow-600 text-white',
  };

  if (toasts.length === 0) {
    return <></>;
  }

  return (
    <div
      className={cn(
        'fixed bottom-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none',
        className
      )}
    >
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            'pointer-events-auto relative flex w-80 items-center justify-between overflow-hidden rounded-md p-4 pr-8 shadow-lg transition-all animate-in slide-in-from-right-full duration-300',
            variantClasses[toast.variant]
          )}
          role="alert"
          aria-live="polite"
        >
          <div className="flex-1">
            <p className="text-sm font-medium">{toast.message}</p>
          </div>
          <button
            onClick={() => removeToast(toast.id)}
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md p-1 opacity-70 transition-opacity hover:opacity-100 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring"
            aria-label="Close notification"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      ))}
    </div>
  );
}

export default ToastManager;
