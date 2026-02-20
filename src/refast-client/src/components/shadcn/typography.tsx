import React from 'react';
import { cn } from '../../utils';

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
  'data-refast-id': dataRefastId,
}: HeadingProps): React.ReactElement {
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
      data-refast-id={dataRefastId}
    >
      {children}
    </Tag>
  );
}

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
export function Paragraph({
  id,
  className,
  lead = false,
  muted = false,
  children,
  'data-refast-id': dataRefastId,
}: ParagraphProps): React.ReactElement {
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
  'data-refast-id'?: string;
}

/**
 * Link component - typography link.
 */
export function Link({
  id,
  className,
  href = '#',
  target,
  external = false,
  onClick,
  children,
  'data-refast-id': dataRefastId,
}: LinkProps): React.ReactElement {
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
      data-refast-id={dataRefastId}
    >
      {children}
    </a>
  );
}

interface CodeProps {
  id?: string;
  className?: string;
  inline?: boolean;
  showLineNumbers?: boolean;
  language?: string;
  code?: string;
  children?: React.ReactNode;
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
  'data-refast-id': dataRefastId,
}: CodeProps): React.ReactElement {
  const theme = useTheme();
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [SyntaxHighlighter, setSyntaxHighlighter] = React.useState<React.ComponentType<any> | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [styles, setStyles] = React.useState<{
    light: Record<string, React.CSSProperties>;
    dark: Record<string, React.CSSProperties>;
  } | null>(null);

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
        return extractText(node.props.children);
      }
      return '';
    };
    return extractText(children);
  }, [children, code]);

  React.useEffect(() => {
    if (!inline) {
      // Dynamically import syntax highlighter for block code
      // Use PrismLight with only commonly used languages to reduce bundle size
      const loadHighlighter = async () => {
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
          setStyles({
            light: oneLightModule.default as Record<string, React.CSSProperties>,
            dark: oneDarkModule.default as Record<string, React.CSSProperties>,
          });
        } catch (error) {
          console.error('Failed to load syntax highlighter:', error);
        }
      };
      loadHighlighter();
    }
  }, [inline]);

  // Get the current style based on theme
  const currentStyle = styles ? styles[theme] : null;

  if (inline) {
    return (
      <code
        id={id}
        className={cn(
          'relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold',
          className
        )}
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
        className={cn('mb-4 mt-6 overflow-x-auto rounded-lg border', className)}
        data-refast-id={dataRefastId}
        data-language={language}
      >
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
    );
  }

  // Fallback to plain code block while loading
  return (
    <pre
      id={id}
      className={cn(
        'mb-4 mt-6 overflow-x-auto rounded-lg border py-4',
        theme === 'dark' ? 'bg-zinc-950 text-white' : 'bg-zinc-100 text-zinc-900',
        className
      )}
      data-refast-id={dataRefastId}
      data-language={language}
    >
      <code className="relative rounded bg-transparent px-4 py-[0.2rem] font-mono text-sm text-inherit">
        {codeString}
      </code>
    </pre>
  );
}

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
export function BlockQuote({
  id,
  className,
  cite,
  children,
  'data-refast-id': dataRefastId,
}: BlockQuoteProps): React.ReactElement {
  return (
    <blockquote
      id={id}
      cite={cite}
      className={cn(
        'mt-6 border-l-2 pl-6 italic text-muted-foreground',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </blockquote>
  );
}

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
export function List({
  id,
  className,
  ordered = false,
  children,
  'data-refast-id': dataRefastId,
}: ListProps): React.ReactElement {
  const Tag = ordered ? 'ol' : 'ul';

  return (
    <Tag
      id={id}
      className={cn(
        'my-6 ml-6',
        ordered ? 'list-decimal' : 'list-disc',
        '[&>li]:mt-2',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
    </Tag>
  );
}

interface ListItemProps {
  id?: string;
  className?: string;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * ListItem component - typography list item.
 */
export function ListItem({
  id,
  className,
  children,
  'data-refast-id': dataRefastId,
}: ListItemProps): React.ReactElement {
  return (
    <li id={id} className={cn('', className)} data-refast-id={dataRefastId}>
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
  'data-refast-id': dataRefastId,
}: LabelProps): React.ReactElement {
  return (
    <label
      id={id}
      htmlFor={htmlFor}
      className={cn(
        'text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70',
        className
      )}
      data-refast-id={dataRefastId}
    >
      {children}
      {required && <span className="ml-1 text-destructive">*</span>}
    </label>
  );
}

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
export function Markdown({
  id,
  className,
  content,
  allowLatex = true,
  allowHtml = false,
  'data-refast-id': dataRefastId,
}: MarkdownProps): React.ReactElement {
  const theme = useTheme();
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [ReactMarkdown, setReactMarkdown] = React.useState<React.ComponentType<any> | null>(null);
  const [plugins, setPlugins] = React.useState<{
    remarkGfm?: unknown;
    remarkMath?: unknown;
    rehypeKatex?: unknown;
  }>({});
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [SyntaxHighlighter, setSyntaxHighlighter] = React.useState<React.ComponentType<any> | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [highlightStyles, setHighlightStyles] = React.useState<{
    light: Record<string, React.CSSProperties>;
    dark: Record<string, React.CSSProperties>;
  } | null>(null);

  React.useEffect(() => {
    // Dynamically import markdown libraries
    const loadMarkdown = async () => {
      try {
        const [reactMarkdownModule, remarkGfmModule] = await Promise.all([
          import('react-markdown'),
          import('remark-gfm'),
        ]);
        
        setReactMarkdown(() => reactMarkdownModule.default as React.ComponentType<any>);
        
        const newPlugins: typeof plugins = {
          remarkGfm: remarkGfmModule.default,
        };

        if (allowLatex) {
          const [remarkMathModule, rehypeKatexModule] = await Promise.all([
            import('remark-math'),
            import('rehype-katex'),
          ]);
          newPlugins.remarkMath = remarkMathModule.default;
          newPlugins.rehypeKatex = rehypeKatexModule.default;
        }

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

        setPlugins(newPlugins);
      } catch (error) {
        console.error('Failed to load markdown libraries:', error);
      }
    };

    loadMarkdown();
  }, [allowLatex]);

  if (!ReactMarkdown) {
    // Loading state or fallback to raw content
    return (
      <div
        id={id}
        className={cn('prose prose-sm dark:prose-invert max-w-none', className)}
        data-refast-id={dataRefastId}
      >
        <pre className="whitespace-pre-wrap text-sm">{content}</pre>
      </div>
    );
  }

  const remarkPlugins: unknown[] = [];
  const rehypePlugins: unknown[] = [];

  if (plugins.remarkGfm) {
    remarkPlugins.push(plugins.remarkGfm);
  }
  if (allowLatex && plugins.remarkMath) {
    remarkPlugins.push(plugins.remarkMath);
  }
  if (allowLatex && plugins.rehypeKatex) {
    rehypePlugins.push(plugins.rehypeKatex);
  }

  // Custom components for styling
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const components: Record<string, React.ComponentType<any>> = {
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
      const isInline = !className;
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

      const currentHighlightStyle = highlightStyles ? highlightStyles[theme] : null;

      if (SyntaxHighlighter && currentHighlightStyle) {
        return (
          <SyntaxHighlighter
            language={language}
            style={currentHighlightStyle}
            customStyle={{
              margin: 0,
              borderRadius: '0.5rem',
              fontSize: '0.875rem',
            }}
            showLineNumbers={false}
          >
            {codeString}
          </SyntaxHighlighter>
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
          <div className="mb-4 mt-6 overflow-x-auto rounded-lg border">
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
  };

  return (
    <div
      id={id}
      className={cn('prose prose-sm dark:prose-invert max-w-none', className)}
      data-refast-id={dataRefastId}
    >
      <ReactMarkdown
        remarkPlugins={remarkPlugins}
        rehypePlugins={rehypePlugins}
        components={allowHtml ? undefined : components}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
