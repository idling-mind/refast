import { default as React } from 'react';

export interface IconProps {
    name: string;
    size?: number;
    color?: string;
    strokeWidth?: number;
    className?: string;
    'data-refast-id'?: string;
}
/**
 * Icon component that renders Lucide icons by name.
 *
 * Falls back to rendering the name as text if the icon is not found,
 * which allows for backward compatibility with emoji icons.
 */
export declare function Icon({ name, size, color, strokeWidth, className, 'data-refast-id': dataRefastId, }: IconProps): React.ReactElement;
/**
 * Check if an icon name exists in the icon map.
 */
export declare function hasIcon(name: string): boolean;
/**
 * Get list of all available icon names.
 */
export declare function getIconNames(): string[];
