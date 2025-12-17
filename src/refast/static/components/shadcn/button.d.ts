import { default as React } from 'react';

interface ButtonProps {
    id?: string;
    className?: string;
    variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
    size?: 'sm' | 'md' | 'lg' | 'icon';
    disabled?: boolean;
    loading?: boolean;
    type?: 'button' | 'submit' | 'reset';
    onClick?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Button component - shadcn/ui styled button with Tailwind CSS.
 */
export declare function Button({ id, className, variant, size, disabled, loading, type, onClick, children, 'data-refast-id': dataRefastId, }: ButtonProps): React.ReactElement;
interface IconButtonProps {
    id?: string;
    className?: string;
    icon: string;
    variant?: 'default' | 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    onClick?: () => void;
    ariaLabel?: string;
    'data-refast-id'?: string;
}
/**
 * IconButton component - button with icon.
 */
export declare function IconButton({ id, className, icon, variant, disabled, onClick, ariaLabel, 'data-refast-id': dataRefastId, }: IconButtonProps): React.ReactElement;
export {};
