import { default as React } from 'react';

interface ToastManagerProps {
    className?: string;
}
/**
 * ToastManager component - manages and displays toast notifications.
 * Listens for 'refast:toast' custom events dispatched by the StateManager.
 */
export declare function ToastManager({ className }: ToastManagerProps): React.ReactElement;
export default ToastManager;
