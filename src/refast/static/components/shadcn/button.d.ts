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
export declare const Button: React.ForwardRefExoticComponent<ButtonProps & React.RefAttributes<HTMLButtonElement>>;
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
export declare const IconButton: React.ForwardRefExoticComponent<IconButtonProps & React.RefAttributes<HTMLButtonElement>>;
export {};
