import React, { type JSX } from 'react';
import { ExternalLink, Copy, Check, X } from 'lucide-react';
import { cn } from '../../utils';
import { Icon } from './icon';
import { ComponentRenderer } from '../ComponentRenderer';

/**
 * Internal copy-to-clipboard button shown on hover over code blocks.
 */
function CopyButton({ text }: { text: string }): React.ReactElement<any> {
  const [status, setStatus] = React.useState<'idle' | 'copied' | 'error'>('idle');

  const handleCopy = async () => {
    // navigator.clipboard requires a secure context (HTTPS / localhost).
    // Fall back to a selection-based copy for plain HTTP deployments.
    const copyViaSelection = (): boolean => {
      const el = document.createElement('textarea');
      el.value = text;
      el.setAttribute('readonly', '');
      el.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
      document.body.appendChild(el);
      el.select();
      // eslint-disable-next-line @typescript-eslint/no-deprecated
      const ok = document.execCommand('copy');
      document.body.removeChild(el);
      return ok;
    };

    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(text);
      } else if (!copyViaSelection()) {
        throw new Error('copy failed');
      }
      setStatus('copied');
      setTimeout(() => setStatus('idle'), 2000);
    } catch {
      setStatus('error');
      setTimeout(() => setStatus('idle'), 2000);
    }
  };

  return (
    <button
      type="button"
      onClick={handleCopy}
      className="absolute top-2 right-2 z-10 p-1.5 rounded-md bg-background/80 hover:bg-muted border border-border text-muted-foreground hover:text-foreground transition-all opacity-0 group-hover:opacity-100 focus:opacity-100"
      title={status === 'copied' ? 'Copied!' : status === 'error' ? 'Copy failed' : 'Copy code'}
      aria-label="Copy code to clipboard"
    >
      {status === 'copied' ? <Check size={14} /> : status === 'error' ? <X size={14} /> : <Copy size={14} />}
    </button>
  );
}

/**
 * Hook to detect current theme (light/dark) from document.documentElement.
 * Watches for class changes on the <html> element.
 */
function useTheme(): 'light' | 'dark' {
  const [theme, setTheme] = React.useState<'light' | 'dark'>(() => {
    if (typeof document !== 'undefined') {
      return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    }
    return 'light';
  });

  React.useEffect(() => {
    if (typeof document === 'undefined') return;

    // Do an initial check in case the class was changed before the effect ran
    const isInitialDark = document.documentElement.classList.contains('dark');
    if ((isInitialDark && theme === 'light') || (!isInitialDark && theme === 'dark')) {
      setTheme(isInitialDark ? 'dark' : 'light');
    }

    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          const isDark = document.documentElement.classList.contains('dark');
          setTheme(isDark ? 'dark' : 'light');
        }
      }
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class'],
    });

    return () => observer.disconnect();
  }, []);

  return theme;
}

interface HeadingProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  level?: 1 | 2 | 3 | 4 | 5 | 6;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Heading component - typography heading.
 */
export function Heading({
  id,
  className,
  level = 1,
  children,
  style,
  'data-refast-id': dataRefastId,
}: HeadingProps): React.ReactElement<any> {
  const sizeClasses = {
    1: 'scroll-m-20 text-4xl font-bold tracking-tight',
    2: 'scroll-m-20 text-3xl font-semibold tracking-tight',
    3: 'scroll-m-20 text-2xl font-semibold tracking-tight',
    4: 'scroll-m-20 text-xl font-semibold tracking-tight',
    5: 'scroll-m-20 text-lg font-semibold tracking-tight',
    6: 'scroll-m-20 text-base font-semibold tracking-tight',
  };

  const Tag = `h${level}` as keyof JSX.IntrinsicElements;

  return (
    <Tag
      id={id}
      className={cn(sizeClasses[level], className)}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
    </Tag>
  );
}

interface ParagraphProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  lead?: boolean;
  muted?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Paragraph component - typography paragraph.
 */
export function Paragraph({
  id,
  className,
  lead = false,
  muted = false,
  children,
  style,
  'data-refast-id': dataRefastId,
}: ParagraphProps): React.ReactElement<any> {
  return (
    <p
      id={id}
      className={cn(
        'leading-7',
        lead && 'text-xl text-muted-foreground',
        muted && 'text-sm text-muted-foreground',
        !lead && !muted && '[&:not(:first-child)]:mt-6',
        className
      )}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
    </p>
  );
}

interface LinkProps {
  id?: string;
  className?: string;
  href?: string;
  target?: '_blank' | '_self' | '_parent' | '_top';
  external?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  'data-refast-id'?: string;
}

/**
 * Link component - typography link.
 */
export function Link({
  id,
  className,
  href = '#',
  target = '_self',
  external = false,
  onClick,
  children,
  style,
  'data-refast-id': dataRefastId,
}: LinkProps): React.ReactElement<any> {
  return (
    <a
      id={id}
      href={href}
      target={external ? '_blank' : target}
      rel={external ? 'noopener noreferrer' : undefined}
      onClick={onClick}
      className={cn(
        'font-medium text-primary px-2 hover:bg-accent',
        className
      )}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
      {external && (
        <ExternalLink className="inline-block ml-1 align-middle" size={12} />
      )}
    </a>
  );
}

// ── Syntax-highlighter singleton ──────────────────────────────────────────
// Loaded once at module level so the first Code block render can read the
// result synchronously (via useState initializer) if the promise already
// resolved. This eliminates the flash-of-unstyled-code on first page load.

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type _SHType = React.ComponentType<any>;
type _SHCache = {
  SyntaxHighlighter: _SHType;
  styles: { light: Record<string, React.CSSProperties>; dark: Record<string, React.CSSProperties> };
};

let _shCache: _SHCache | null = null;
let _shPromise: Promise<void> | null = null;
const _shListeners = new Set<() => void>();

function _loadSyntaxHighlighter(): Promise<void> {
  if (_shPromise) return _shPromise;
  _shPromise = (async () => {
    try {
      const [PrismLightModule, oneDarkModule, oneLightModule] = await Promise.all([
        import('react-syntax-highlighter/dist/esm/prism-light'),
        import('react-syntax-highlighter/dist/esm/styles/prism/one-dark'),
        import('react-syntax-highlighter/dist/esm/styles/prism/one-light'),
      ]);
      const PrismLight = PrismLightModule.default;
      const [javascript, typescript, python, bash, json, css, jsx, tsx, sql, yaml, markdown] = await Promise.all([
        import('react-syntax-highlighter/dist/esm/languages/prism/javascript'),
        import('react-syntax-highlighter/dist/esm/languages/prism/typescript'),
        import('react-syntax-highlighter/dist/esm/languages/prism/python'),
        import('react-syntax-highlighter/dist/esm/languages/prism/bash'),
        import('react-syntax-highlighter/dist/esm/languages/prism/json'),
        import('react-syntax-highlighter/dist/esm/languages/prism/css'),
        import('react-syntax-highlighter/dist/esm/languages/prism/jsx'),
        import('react-syntax-highlighter/dist/esm/languages/prism/tsx'),
        import('react-syntax-highlighter/dist/esm/languages/prism/sql'),
        import('react-syntax-highlighter/dist/esm/languages/prism/yaml'),
        import('react-syntax-highlighter/dist/esm/languages/prism/markdown'),
      ]);
      PrismLight.registerLanguage('javascript', javascript.default);
      PrismLight.registerLanguage('js', javascript.default);
      PrismLight.registerLanguage('typescript', typescript.default);
      PrismLight.registerLanguage('ts', typescript.default);
      PrismLight.registerLanguage('python', python.default);
      PrismLight.registerLanguage('py', python.default);
      PrismLight.registerLanguage('bash', bash.default);
      PrismLight.registerLanguage('shell', bash.default);
      PrismLight.registerLanguage('sh', bash.default);
      PrismLight.registerLanguage('json', json.default);
      PrismLight.registerLanguage('css', css.default);
      PrismLight.registerLanguage('jsx', jsx.default);
      PrismLight.registerLanguage('tsx', tsx.default);
      PrismLight.registerLanguage('sql', sql.default);
      PrismLight.registerLanguage('yaml', yaml.default);
      PrismLight.registerLanguage('yml', yaml.default);
      PrismLight.registerLanguage('markdown', markdown.default);
      PrismLight.registerLanguage('md', markdown.default);
      _shCache = {
        SyntaxHighlighter: PrismLight,
        styles: {
          light: oneLightModule.default as Record<string, React.CSSProperties>,
          dark: oneDarkModule.default as Record<string, React.CSSProperties>,
        },
      };
      _shListeners.forEach((fn) => fn());
    } catch (error) {
      console.error('Failed to load syntax highlighter:', error);
    }
  })();
  return _shPromise;
}

// Kick off loading as soon as this module is imported so the chunks are
// in-flight before any Code component is rendered.
_loadSyntaxHighlighter();

// ─────────────────────────────────────────────────────────────────────────────

interface CodeProps {
  id?: string;
  className?: string;
  inline?: boolean;
  showLineNumbers?: boolean;
  language?: string;
  code?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  'data-refast-id'?: string;
}

/**
 * Code component - typography code with syntax highlighting.
 * Automatically adapts to light/dark theme.
 */
export function Code({
  id,
  className,
  inline = true,
  showLineNumbers = false,
  language,
  code,
  children,
  style,
  'data-refast-id': dataRefastId,
}: CodeProps): React.ReactElement<any> {
  const theme = useTheme();

  // Read from the singleton cache synchronously so that components mounting
  // after the first load never see the plain-text fallback.
  const [highlighter, setHighlighter] = React.useState<_SHCache | null>(() => _shCache);

  // Extract code string from children (which might be React nodes or strings)
  const codeString = React.useMemo(() => {
    if (code) return code;

    const extractText = (node: React.ReactNode): string => {
      if (typeof node === 'string') return node;
      if (typeof node === 'number') return String(node);
      if (!node) return '';
      if (Array.isArray(node)) return node.map(extractText).join('');
      if (React.isValidElement(node)) {
        // Extract text from React element's children
        // In React 19, element.props is typed as unknown — cast to access children
        return extractText((node.props as { children?: React.ReactNode }).children);
      }
      return '';
    };
    return extractText(children);
  }, [children, code]);

  React.useEffect(() => {
    if (inline) return;
    // Already loaded — nothing to do.
    if (_shCache) {
      if (!highlighter) setHighlighter(_shCache);
      return;
    }
    // Subscribe so we re-render once the singleton resolves.
    const notify = () => setHighlighter(_shCache);
    _shListeners.add(notify);
    _loadSyntaxHighlighter();
    return () => { _shListeners.delete(notify); };
  }, [inline, highlighter]);

  // Get the current style based on theme
  const SyntaxHighlighter = highlighter?.SyntaxHighlighter ?? null;
  const currentStyle = highlighter ? highlighter.styles[theme] : null;

  if (inline) {
    return (
      <code
        id={id}
        className={cn(
          'relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold',
          className
        )}
        style={style}
        data-refast-id={dataRefastId}
        data-language={language}
      >
        {codeString}
      </code>
    );
  }

  // Use syntax highlighter if loaded
  if (SyntaxHighlighter && currentStyle) {
    return (
      <div
        id={id}
        className={cn('relative group mb-4 mt-6 rounded-lg border', className)}
        style={style}
        data-refast-id={dataRefastId}
        data-language={language}
      >
        <div className="overflow-x-auto">
          <SyntaxHighlighter
            language={language || 'text'}
            style={currentStyle}
            customStyle={{
              margin: 0,
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
            }}
            showLineNumbers={showLineNumbers}
          >
            {codeString}
          </SyntaxHighlighter>
        </div>
        <CopyButton text={codeString} />
      </div>
    );
  }

  // Fallback to plain code block while loading
  return (
    <div
      id={id}
      className={cn('relative group mb-4 mt-6 rounded-lg border', className)}
      data-refast-id={dataRefastId}
      data-language={language}
      style={style}
    >
      <div className="overflow-x-auto">
        <pre
          className={cn(
            'py-4',
            theme === 'dark' ? 'bg-zinc-950 text-white' : 'bg-zinc-100 text-zinc-900',
          )}
        >
          <code className="relative rounded bg-transparent px-4 py-[0.2rem] font-mono text-sm text-inherit">
            {codeString}
          </code>
        </pre>
      </div>
      <CopyButton text={codeString} />
    </div>
  );
}

type BlockQuoteColor = 'default' | 'secondary' | 'destructive' | 'info' | 'success' | 'warning';

const NAMED_COLORS = new Set<string>(['default', 'secondary', 'destructive', 'info', 'success', 'warning']);

/** Tailwind classes for named color variants */
const namedColorClasses: Record<BlockQuoteColor, { border: string; bg: string; iconColor: string }> = {
  default:     { border: 'border-border',       bg: 'bg-muted/50',            iconColor: 'text-foreground' },
  secondary:   { border: 'border-secondary',    bg: 'bg-secondary/20',        iconColor: 'text-secondary-foreground' },
  destructive: { border: 'border-destructive',  bg: 'bg-destructive/10',      iconColor: 'text-destructive' },
  info:        { border: 'border-info',         bg: 'bg-info/10',             iconColor: 'text-info' },
  success:     { border: 'border-success',      bg: 'bg-success/10',          iconColor: 'text-success' },
  warning:     { border: 'border-warning',      bg: 'bg-warning/10',          iconColor: 'text-warning' },
};

interface BlockQuoteProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  /** Attribution / author displayed below the quote. */
  cite?: string;
  /** Color variant (named) or any CSS color value for background and border. */
  color?: string;
  /** Lucide icon name to display above the quote body. */
  icon?: string;
  /** Icon size in pixels. */
  iconSize?: number;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * BlockQuote component - styled blockquote with optional icon, color, and attribution.
 */
export function BlockQuote({
  id,
  className,
  style,
  cite,
  color = 'default',
  icon,
  iconSize = 20,
  children,
  'data-refast-id': dataRefastId,
}: BlockQuoteProps): React.ReactElement<any> {
  const isNamed = NAMED_COLORS.has(color);
  const namedClasses = isNamed ? namedColorClasses[color as BlockQuoteColor] : null;

  // For generic/arbitrary CSS colors build inline styles
  const genericStyle: React.CSSProperties = isNamed
    ? {}
    : {
        borderColor: color,
        backgroundColor: `color-mix(in srgb, ${color} 12%, transparent)`,
      };

  return (
    <blockquote
      id={id}
      className={cn(
        'border-l-4 rounded-md p-4 my-4 space-y-2',
        namedClasses ? `${namedClasses.border} ${namedClasses.bg}` : '',
        className
      )}
      style={{ ...genericStyle, ...style }}
      data-refast-id={dataRefastId}
    >
      {icon && (
        <div
          className={cn(
            'mb-1',
            namedClasses ? namedClasses.iconColor : ''
          )}
          style={!isNamed ? { color } : undefined}
        >
          <Icon name={icon} size={iconSize} />
        </div>
      )}
      <p className="italic text-foreground leading-relaxed">
        {children}
      </p>
      {cite && (
        <footer className="text-sm text-muted-foreground">
          &mdash;&nbsp;{cite}
        </footer>
      )}
    </blockquote>
  );
}

interface ListProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  ordered?: boolean;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * List component - typography list.
 */
export function List({
  id,
  className,
  style,
  ordered = false,
  children,
  'data-refast-id': dataRefastId,
}: ListProps): React.ReactElement<any> {
  const Tag = ordered ? 'ol' : 'ul';

  // Auto-wrap children that aren't already <li> elements
  const wrappedChildren = React.Children.map(children, (child) => {
    if (React.isValidElement(child) && (child.type === 'li' || (child as React.ReactElement<{ className?: string }>).props?.className?.includes('list-item'))) {
      return child;
    }
    return <li>{child}</li>;
  });

  return (
    <Tag
      id={id}
      className={cn(
        'my-6 ml-6',
        ordered ? 'list-decimal' : 'list-disc',
        '[&>li]:mt-2',
        className
      )}
      style={style}
      data-refast-id={dataRefastId}
    >
      {wrappedChildren}
    </Tag>
  );
}

interface ListItemProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * ListItem component - typography list item.
 */
export function ListItem({
  id,
  className,
  style,
  children,
  'data-refast-id': dataRefastId,
}: ListItemProps): React.ReactElement<any> {
  return (
    <li id={id} className={cn('', className)} data-refast-id={dataRefastId} style={style}>
      {children}
    </li>
  );
}

interface LabelProps {
  id?: string;
  className?: string;
  htmlFor?: string;
  required?: boolean;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  'data-refast-id'?: string;
}

/**
 * Label component - typography label.
 */
export function Label({
  id,
  className,
  htmlFor,
  required = false,
  children,
  style,
  'data-refast-id': dataRefastId,
}: LabelProps): React.ReactElement<any> {
  return (
    <label
      id={id}
      htmlFor={htmlFor}
      className={cn(
        'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
        className
      )}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
      {required && <span className="ml-1 text-destructive">*</span>}
    </label>
  );
}

/**
 * Internal component that lazy-loads Mermaid and renders a diagram.
 */
interface MermaidDiagramProps {
  code: string;
  theme: 'light' | 'dark';
}

function MermaidDiagram({ code, theme }: MermaidDiagramProps) {
  const [svg, setSvg] = React.useState<string>('');
  const [error, setError] = React.useState<string>('');
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    let cancelled = false;

    const renderDiagram = async () => {
      try {
        const mermaidModule = await import('mermaid');
        const mermaidLib = mermaidModule.default;

        mermaidLib.initialize({
          startOnLoad: false,
          theme: theme === 'dark' ? 'dark' : 'default',
        });

        const uniqueId = `mermaid-${Math.random().toString(36).slice(2)}`;
        const { svg: renderedSvg } = await mermaidLib.render(uniqueId, code);

        if (!cancelled) {
          setSvg(renderedSvg);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to render diagram');
          setLoading(false);
        }
      }
    };

    renderDiagram();
    return () => { cancelled = true; };
  // Re-render only when code or theme actually changes
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code, theme]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8 text-muted-foreground text-sm">
        Loading diagram…
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded border border-destructive p-4 text-destructive text-sm font-mono whitespace-pre-wrap">
        {error}
      </div>
    );
  }

  return (
    <div
      className="flex justify-center overflow-auto py-4"
      // The SVG comes from Mermaid (trusted local renderer), not user input
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}

interface MarkdownProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  content: string;
  allowHtml?: boolean;
  /** Enable Mermaid diagram rendering in fenced ```mermaid blocks. Loaded on demand. */
  enableMermaid?: boolean;
  /** Enable LaTeX / KaTeX math rendering ($…$ and $$…$$). Loaded on demand. */
  enableLatex?: boolean;
  customComponents?: Record<string, any>;
  'data-refast-id'?: string;
}

/**
 * Markdown component - renders Markdown content.
 * Uses react-markdown with remark-gfm for GitHub Flavored Markdown.
 * Automatically adapts code block styling to light/dark theme.
 */
export function Markdown({
  id,
  className,
  style,
  content,
  allowHtml = false,
  enableMermaid = false,
  enableLatex = false,
  customComponents,
  'data-refast-id': dataRefastId,
}: MarkdownProps): React.ReactElement<any> {
  const theme = useTheme();
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [ReactMarkdown, setReactMarkdown] = React.useState<React.ComponentType<any> | null>(null);
  const [remarkGfm, setRemarkGfm] = React.useState<unknown>(null);
  const [rehypeRaw, setRehypeRaw] = React.useState<unknown>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [SyntaxHighlighter, setSyntaxHighlighter] = React.useState<React.ComponentType<any> | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [highlightStyles, setHighlightStyles] = React.useState<{
    light: Record<string, React.CSSProperties>;
    dark: Record<string, React.CSSProperties>;
  } | null>(null);
  const [remarkMath, setRemarkMath] = React.useState<unknown>(null);
  const [rehypeKatex, setRehypeKatex] = React.useState<unknown>(null);

  React.useEffect(() => {
    // Dynamically import markdown libraries
    const loadMarkdown = async () => {
      try {
        const [reactMarkdownModule, remarkGfmModule, rehypeRawModule] = await Promise.all([
          import('react-markdown'),
          import('remark-gfm'),
          import('rehype-raw'),
        ]);
        
        setReactMarkdown(() => reactMarkdownModule.default as React.ComponentType<any>);
        setRemarkGfm(() => remarkGfmModule.default);
        setRehypeRaw(() => rehypeRawModule.default);

        // Load syntax highlighter with PrismLight for smaller bundle
        try {
          const [PrismLightModule, oneDarkModule, oneLightModule] = await Promise.all([
            import('react-syntax-highlighter/dist/esm/prism-light'),
            import('react-syntax-highlighter/dist/esm/styles/prism/one-dark'),
            import('react-syntax-highlighter/dist/esm/styles/prism/one-light'),
          ]);
          
          const PrismLight = PrismLightModule.default;
          
          // Register commonly used languages
          const [javascript, typescript, python, bash, json, css, jsx, tsx, sql, yaml, markdown] = await Promise.all([
            import('react-syntax-highlighter/dist/esm/languages/prism/javascript'),
            import('react-syntax-highlighter/dist/esm/languages/prism/typescript'),
            import('react-syntax-highlighter/dist/esm/languages/prism/python'),
            import('react-syntax-highlighter/dist/esm/languages/prism/bash'),
            import('react-syntax-highlighter/dist/esm/languages/prism/json'),
            import('react-syntax-highlighter/dist/esm/languages/prism/css'),
            import('react-syntax-highlighter/dist/esm/languages/prism/jsx'),
            import('react-syntax-highlighter/dist/esm/languages/prism/tsx'),
            import('react-syntax-highlighter/dist/esm/languages/prism/sql'),
            import('react-syntax-highlighter/dist/esm/languages/prism/yaml'),
            import('react-syntax-highlighter/dist/esm/languages/prism/markdown'),
          ]);
          
          PrismLight.registerLanguage('javascript', javascript.default);
          PrismLight.registerLanguage('js', javascript.default);
          PrismLight.registerLanguage('typescript', typescript.default);
          PrismLight.registerLanguage('ts', typescript.default);
          PrismLight.registerLanguage('python', python.default);
          PrismLight.registerLanguage('py', python.default);
          PrismLight.registerLanguage('bash', bash.default);
          PrismLight.registerLanguage('shell', bash.default);
          PrismLight.registerLanguage('sh', bash.default);
          PrismLight.registerLanguage('json', json.default);
          PrismLight.registerLanguage('css', css.default);
          PrismLight.registerLanguage('jsx', jsx.default);
          PrismLight.registerLanguage('tsx', tsx.default);
          PrismLight.registerLanguage('sql', sql.default);
          PrismLight.registerLanguage('yaml', yaml.default);
          PrismLight.registerLanguage('yml', yaml.default);
          PrismLight.registerLanguage('markdown', markdown.default);
          PrismLight.registerLanguage('md', markdown.default);
          
          setSyntaxHighlighter(() => PrismLight);
          setHighlightStyles({
            light: oneLightModule.default as Record<string, React.CSSProperties>,
            dark: oneDarkModule.default as Record<string, React.CSSProperties>,
          });
        } catch (err) {
          console.error('Failed to load syntax highlighter:', err);
        }

        // Load KaTeX (LaTeX math) plugins on demand via dedicated loader
        // module so that the main bundle has zero static reference to katex.
        if (enableLatex) {
          try {
            const { remarkMath: rM, rehypeKatex: rHK } =
              await import('../../loaders/katex-loader');
            setRemarkMath(() => rM);
            setRehypeKatex(() => rHK);
          } catch (err) {
            console.error('Failed to load LaTeX plugins:', err);
          }
        }
      } catch (error) {
        console.error('Failed to load markdown libraries:', error);
      }
    };

    loadMarkdown();
  // enableLatex is intentionally included so plugins load if the prop is changed dynamically
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enableLatex]);

  // Custom components for styling
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const components = React.useMemo<Record<string, React.ComponentType<any>>>(() => ({
    // Headers
    h1: ({ children }) => (
      <h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl mb-4">
        {children}
      </h1>
    ),
    h2: ({ children }) => (
      <h2 className="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight first:mt-0 mt-8 mb-4">
        {children}
      </h2>
    ),
    h3: ({ children }) => (
      <h3 className="scroll-m-20 text-2xl font-semibold tracking-tight mt-6 mb-3">
        {children}
      </h3>
    ),
    h4: ({ children }) => (
      <h4 className="scroll-m-20 text-xl font-semibold tracking-tight mt-4 mb-2">
        {children}
      </h4>
    ),
    // Paragraph
    p: ({ children }) => (
      <p className="leading-7 [&:not(:first-child)]:mt-4">{children}</p>
    ),
    // Lists
    ul: ({ children }) => (
      <ul className="my-4 ml-6 list-disc [&>li]:mt-2">{children}</ul>
    ),
    ol: ({ children }) => (
      <ol className="my-4 ml-6 list-decimal [&>li]:mt-2">{children}</ol>
    ),
    // Blockquote
    blockquote: ({ children }) => (
      <blockquote className="mt-6 border-l-2 pl-6 italic text-muted-foreground">
        {children}
      </blockquote>
    ),
    // Code with syntax highlighting
    code: ({ className, children }) => {
      // Fenced code blocks (even without a language) always end with a trailing \n;
      // inline code does not.  Using only !className incorrectly treats no-language
      // fenced blocks as inline code.
      const isInline = !className && !String(children).endsWith('\n');
      if (isInline) {
        return (
          <code className="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold">
            {children}
          </code>
        );
      }
      // Extract language from className (e.g., "language-javascript")
      const match = /language-(\w+)/.exec(className || '');
      const language = match ? match[1] : 'text';
      const codeString = String(children).replace(/\n$/, '');

      // Render Mermaid diagrams when enabled
      if (enableMermaid && language === 'mermaid') {
        return <MermaidDiagram code={codeString} theme={theme} />;
      }

      const currentHighlightStyle = highlightStyles ? highlightStyles[theme] : null;

      if (SyntaxHighlighter && currentHighlightStyle) {
        return (
          <div className="relative group">
            <div className="overflow-x-auto">
              <SyntaxHighlighter
                language={language}
                style={currentHighlightStyle}
                customStyle={{
                  margin: 0,
                  borderRadius: '0',
                  fontSize: '0.875rem',
                }}
                showLineNumbers={false}
              >
                {codeString}
              </SyntaxHighlighter>
            </div>
            <CopyButton text={codeString} />
          </div>
        );
      }
      return (
        <code className="relative rounded bg-transparent font-mono text-sm">
          {children}
        </code>
      );
    },
    pre: ({ children }) => {
      // If using syntax highlighter, just render children (which will be the highlighted code)
      const currentHighlightStyle = highlightStyles ? highlightStyles[theme] : null;
      if (SyntaxHighlighter && currentHighlightStyle) {
        return (
          <div className="mb-4 mt-6 rounded-lg border overflow-hidden">
            {children}
          </div>
        );
      }
      return (
        <pre className={cn(
          "mb-4 mt-6 overflow-x-auto rounded-lg border py-4 px-4",
          theme === 'dark' ? 'bg-zinc-950 text-white' : 'bg-zinc-100 text-zinc-900'
        )}>
          {children}
        </pre>
      );
    },
    // Links
    a: ({ href, children }) => (
      <a
        href={href}
        className="font-medium text-primary underline underline-offset-4 hover:no-underline"
        target={href?.startsWith('http') ? '_blank' : undefined}
        rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
      >
        {children}
      </a>
    ),
    // Table
    table: ({ children }) => (
      <div className="my-6 w-full overflow-y-auto">
        <table className="w-full">{children}</table>
      </div>
    ),
    th: ({ children }) => (
      <th className="border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right">
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td className="border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right">
        {children}
      </td>
    ),
    // Horizontal rule
    hr: () => <hr className="my-6 border-muted" />,
    img: ({ src, alt }) => {
      if (src && src.startsWith('/refast-component/')) {
        const componentId = src.substring(18);
        const childTree = customComponents?.[componentId];
        if (childTree) {
          return <ComponentRenderer tree={childTree} />;
        }
        return null;
      }
      return <img src={src} alt={alt} className="max-w-full h-auto rounded-md" />;
    },
  }), [theme, SyntaxHighlighter, highlightStyles, enableMermaid, customComponents]);

  if (!ReactMarkdown) {
    // Loading state or fallback to raw content
    return (
      <div
        id={id}
        className={cn('prose prose-sm dark:prose-invert max-w-none', className)}
        style={style}
        data-refast-id={dataRefastId}
      >
        <pre className="whitespace-pre-wrap text-sm">{content}</pre>
      </div>
    );
  }

  const remarkPlugins: unknown[] = [];
  if (remarkGfm) remarkPlugins.push(remarkGfm);
  if (enableLatex && remarkMath) remarkPlugins.push(remarkMath);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const rehypePlugins: any[] = [];
  if (allowHtml && rehypeRaw) rehypePlugins.push(rehypeRaw);
  if (enableLatex && rehypeKatex) rehypePlugins.push(rehypeKatex);

  // include a readiness flag in the key so that the entire markdown tree
  // is recreated when the syntax highlighter / latex plugins finish loading.
  const ready = Boolean(SyntaxHighlighter && highlightStyles) &&
    (!enableLatex || Boolean(remarkMath && rehypeKatex));
  const markdownKey = `${theme}-${ready}`;

  return (
    <div
      key={markdownKey}
      id={id}
      className={cn('prose prose-sm dark:prose-invert max-w-none', className)}
      style={style}
      data-refast-id={dataRefastId}
    >
      <ReactMarkdown
        remarkPlugins={remarkPlugins}
        rehypePlugins={rehypePlugins.length > 0 ? rehypePlugins : undefined}
        components={components}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

interface KbdProps {
  id?: string;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Kbd component - renders a keyboard key in a styled <kbd> element.
 */
export function Kbd({
  id,
  className,
  style,
  children,
  'data-refast-id': dataRefastId,
}: KbdProps): React.ReactElement<any> {
  return (
    <kbd
      id={id}
      className={cn(
        'pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground',
        className
      )}
      style={style}
      data-refast-id={dataRefastId}
    >
      {children}
    </kbd>
  );
}
