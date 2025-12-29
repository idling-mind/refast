/**
 * Shared types for shadcn components
 */

import { ReactNode, HTMLAttributes } from 'react';

/**
 * Base props for all components
 */
export interface BaseProps extends Omit<HTMLAttributes<HTMLElement>, 'children'> {
  className?: string;
  id?: string;
}

/**
 * Props for components that accept children
 */
export interface ChildrenProp {
  children?: ReactNode;
}

/**
 * Common callback interface matching Python callback serialization
 */
export interface CallbackProp {
  callbackId: string;
  boundArgs?: Record<string, unknown>;
  debounce?: number;
  throttle?: number;
}
