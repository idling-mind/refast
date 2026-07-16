import * as React from 'react';
import { Toaster as SonnerToaster } from 'sonner';
import type { BaseProps } from './types';

export interface ToasterProps extends BaseProps {
  position?: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right';
  expand?: boolean;
  duration?: number;
  visibleToasts?: number;
  closeButton?: boolean;
  richColors?: boolean;
  theme?: 'light' | 'dark' | 'system';
  offset?: string | number;
  gap?: number;
  dir?: 'ltr' | 'rtl' | 'auto';
  hotkey?: string[];
  invert?: boolean;
}

/**
 * Toaster component - renders the Sonner toast container.
 * Place this once in your app layout to enable toast notifications.
 */
export function Toaster({
  className,
  position = 'bottom-right',
  expand = false,
  duration = 4000,
  visibleToasts = 3,
  closeButton = false,
  richColors = false,
  theme = 'system',
  offset,
  gap = 14,
  dir = 'auto',
  hotkey = ['altKey', 'KeyT'],
  invert = false,
}: ToasterProps): React.ReactElement<any> {
  return (
    <SonnerToaster
      className={className}
      position={position}
      expand={expand}
      duration={duration}
      visibleToasts={visibleToasts}
      closeButton={closeButton}
      richColors={richColors}
      theme={theme}
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
