import { default as React } from 'react';
import { toast } from 'sonner';

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
export declare function ToastManager({ className, position, richColors, closeButton, duration, expand, visibleToasts, offset, gap, dir, hotkey, invert, }: ToastManagerProps): React.ReactElement;
export { toast };
/**
 * Dismiss a toast by ID.
 */
export declare function dismissToast(toastId?: string | number): void;
/**
 * Show a promise toast that updates based on promise state.
 * Returns the original promise for chaining.
 */
export declare function promiseToast<T>(promise: Promise<T>, messages: {
    loading: string;
    success: string | ((data: T) => string);
    error: string | ((error: unknown) => string);
}): Promise<T>;
export default ToastManager;
