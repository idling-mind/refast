import { default as React } from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Card component - shadcn-styled card container.
 */
export declare function Card({ id, className, children, 'data-refast-id': dataRefastId, ...props }: CardProps): React.ReactElement;
interface CardHeaderProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CardHeader component - card header section.
 */
export declare function CardHeader({ id, className, children, 'data-refast-id': dataRefastId, }: CardHeaderProps): React.ReactElement;
interface CardTitleProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CardTitle component - card title text.
 */
export declare function CardTitle({ id, className, children, 'data-refast-id': dataRefastId, }: CardTitleProps): React.ReactElement;
interface CardDescriptionProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CardDescription component - card description text.
 */
export declare function CardDescription({ id, className, children, 'data-refast-id': dataRefastId, }: CardDescriptionProps): React.ReactElement;
interface CardContentProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CardContent component - card content section.
 */
export declare function CardContent({ id, className, children, 'data-refast-id': dataRefastId, }: CardContentProps): React.ReactElement;
interface CardFooterProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * CardFooter component - card footer section.
 */
export declare function CardFooter({ id, className, children, 'data-refast-id': dataRefastId, }: CardFooterProps): React.ReactElement;
export {};
