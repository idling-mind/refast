import { default as React } from 'react';

interface HeadingProps {
    id?: string;
    className?: string;
    level?: 1 | 2 | 3 | 4 | 5 | 6;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Heading component - typography heading.
 */
export declare function Heading({ id, className, level, children, 'data-refast-id': dataRefastId, }: HeadingProps): React.ReactElement;
interface ParagraphProps {
    id?: string;
    className?: string;
    lead?: boolean;
    muted?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Paragraph component - typography paragraph.
 */
export declare function Paragraph({ id, className, lead, muted, children, 'data-refast-id': dataRefastId, }: ParagraphProps): React.ReactElement;
interface LinkProps {
    id?: string;
    className?: string;
    href?: string;
    target?: '_blank' | '_self' | '_parent' | '_top';
    external?: boolean;
    onClick?: () => void;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Link component - typography link.
 */
export declare function Link({ id, className, href, target, external, onClick, children, 'data-refast-id': dataRefastId, }: LinkProps): React.ReactElement;
interface CodeProps {
    id?: string;
    className?: string;
    inline?: boolean;
    language?: string;
    code?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Code component - typography code with syntax highlighting.
 * Automatically adapts to light/dark theme.
 */
export declare function Code({ id, className, inline, language, code, children, 'data-refast-id': dataRefastId, }: CodeProps): React.ReactElement;
interface BlockQuoteProps {
    id?: string;
    className?: string;
    cite?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * BlockQuote component - typography blockquote.
 */
export declare function BlockQuote({ id, className, cite, children, 'data-refast-id': dataRefastId, }: BlockQuoteProps): React.ReactElement;
interface ListProps {
    id?: string;
    className?: string;
    ordered?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * List component - typography list.
 */
export declare function List({ id, className, ordered, children, 'data-refast-id': dataRefastId, }: ListProps): React.ReactElement;
interface ListItemProps {
    id?: string;
    className?: string;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * ListItem component - typography list item.
 */
export declare function ListItem({ id, className, children, 'data-refast-id': dataRefastId, }: ListItemProps): React.ReactElement;
interface LabelProps {
    id?: string;
    className?: string;
    htmlFor?: string;
    required?: boolean;
    children?: React.ReactNode;
    'data-refast-id'?: string;
}
/**
 * Label component - typography label.
 */
export declare function Label({ id, className, htmlFor, required, children, 'data-refast-id': dataRefastId, }: LabelProps): React.ReactElement;
interface MarkdownProps {
    id?: string;
    className?: string;
    content: string;
    allowLatex?: boolean;
    allowHtml?: boolean;
    'data-refast-id'?: string;
}
/**
 * Markdown component - renders Markdown content with optional LaTeX support.
 * Uses react-markdown with remark-gfm for GitHub Flavored Markdown.
 * When allowLatex is true, supports inline math with $...$ and display math with $$...$$.
 * Automatically adapts code block styling to light/dark theme.
 */
export declare function Markdown({ id, className, content, allowLatex, allowHtml, 'data-refast-id': dataRefastId, }: MarkdownProps): React.ReactElement;
export {};
