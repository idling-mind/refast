/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  safelist: [
    // Core Layout (Structure only, use style for dimensions)
    { pattern: /^(m|p)[xytrbl]?-(0|1|2|3|4|5|6|8|10|12|16|auto)$/ }, // Limited Spacing only (0-4rem)
    
    // Core Sizing (Essential Only)
    { pattern: /^(w|h)-(full|screen|auto|min|max|fit)$/ },
    { pattern: /^max-w-(xs|sm|md|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|full|min|max|fit|prose|screen-(sm|md|lg|xl|2xl))$/ },
    
    { pattern: /^(block|inline|flex|grid|table|hidden)$/, variants: ['xs', 'sm', 'md', 'lg', 'xl', '2xl'] }, // Display
    { pattern: /^gap(-[xy])?-(0|1|2|3|4|5|6|8)$/, variants: ['xs', 'sm', 'md', 'lg', 'xl', '2xl'] }, // Limited Gap
    
    // Layout Alignment & Flex/Grid Behavior
    { pattern: /^flex-(row|col|row-reverse|col-reverse|wrap|nowrap|1|auto|none)$/, variants: ['xs', 'sm', 'md', 'lg', 'xl', '2xl'] },
    { pattern: /^grid-cols-(1|2|3|4|5|6|12|none)$/, variants: ['xs', 'sm', 'md', 'lg', 'xl', '2xl'] },
    { pattern: /^(justify|items|content|self)-(start|end|center|between|around|evenly|stretch|baseline)$/ },
    { pattern: /^(col|row)-span-(1|2|3|4|6|12|full)$/, variants: ['xs', 'sm', 'md', 'lg', 'xl', '2xl'] },
    { pattern: /^(order)-(first|last|none)$/ },
    { pattern: /^(shrink|grow)(-0)?$/ },
    
    // Positioning
    { pattern: /^(absolute|relative|fixed|sticky)$/ },
    { pattern: /^(top|right|bottom|left|inset)-0$/ }, // Only 0 for reset
    { pattern: /^z-(0|10|20|30|40|50)$/ },
    { pattern: /^overflow-(auto|hidden|visible|scroll)$/ }, // Specific overflows
    
    // Typography (Essential)
    { pattern: /^text-(xs|sm|base|lg|xl|2xl|3xl)$/ }, // Limit massive sizes, use style for exceptions
    { pattern: /^font-(normal|medium|semibold|bold)$/ }, // Limit weights
    { pattern: /^text-(left|center|right|justify)$/ },
    { pattern: /^whitespace-(nowrap|pre|normal)$/ },
    
    // Visual & Theming
    // STRICT: Only specific rounded sizes and sides
    { pattern: /^rounded(-(sm|md|lg|xl|2xl|3xl|full|none|t|r|b|l|tl|tr|br|bl))?$/ },
    
    // STRICT: Only specific border widths and sides
    { pattern: /^border(-[xytrbl])?(-(0|2|4|8))?$/ },
    
    // STRICT: Only specific shadows
    { pattern: /^shadow(-(sm|md|lg|xl|2xl|inner|none))?$/ },
    
    // Semantic Colors (Optimized)
    // Removed 'active', 'disabled', 'group-hover' to save space.
    // Removed 'outline' property as it is rarely used with colors.
    { 
      pattern: /^(bg|text|border)-(background|foreground|primary|secondary|destructive|muted|accent|popover|card|input|border)$/,
      variants: ['hover'],
    },
    // Ring usually only needs focus
    { 
      pattern: /^ring-(background|foreground|primary|secondary|destructive|muted|accent|popover|card|input|border)$/,
      variants: ['focus'],
    },
    
    // Interactive
    { pattern: /^cursor-(pointer|not-allowed|text|move)$/ },
    { pattern: /^outline-none$/ },
    
    // Essential Animation
    { pattern: /^transition(-.*)?$/ },
    { pattern: /^duration-(100|200|300|500|700|1000)$/ },
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
    },
  },
  plugins: [],
};
