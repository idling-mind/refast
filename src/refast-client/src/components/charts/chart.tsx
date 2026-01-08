import React from 'react';
import {
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  Legend as RechartsLegend,
} from 'recharts';
import { cn } from '../../utils';

export function ChartTooltip({
  cursor = false,
  content,
  ...props
}: React.ComponentProps<typeof RechartsTooltip>) {
  return (
    <RechartsTooltip
      content={content || <ChartTooltipContent />}
      cursor={cursor}
      {...props}
    />
  );
}
export const ChartLegend = RechartsLegend;

// Chart context for theming
interface ChartConfig {
  [key: string]: {
    label: string;
    color?: string;
    icon?: React.ComponentType;
  };
}

const ChartContext = React.createContext<ChartConfig | null>(null);

export function useChart() {
  const context = React.useContext(ChartContext);
  if (!context) {
    throw new Error('useChart must be used within a ChartContainer');
  }
  return context;
}

interface ChartContainerProps {
  config: ChartConfig;
  children: React.ReactNode;
  width?: React.ComponentProps<typeof ResponsiveContainer>['width'];
  height?: React.ComponentProps<typeof ResponsiveContainer>['height'];
  minHeight?: React.ComponentProps<typeof ResponsiveContainer>['minHeight'];
  maxHeight?: React.ComponentProps<typeof ResponsiveContainer>['maxHeight'];
  minWidth?: React.ComponentProps<typeof ResponsiveContainer>['minWidth'];
  aspect?: React.ComponentProps<typeof ResponsiveContainer>['aspect'];
  initialDimension?: React.ComponentProps<typeof ResponsiveContainer>['initialDimension'];
  debounce?: React.ComponentProps<typeof ResponsiveContainer>['debounce'];
  className?: string;
  style?: React.CSSProperties;
  id?: string;
  onResize?: React.ComponentProps<typeof ResponsiveContainer>['onResize'];
}

export function ChartContainer({
  config,
  children,
  width,
  height,
  minHeight,
  maxHeight,
  minWidth,
  aspect,
  initialDimension,
  debounce,
  className,
  style,
  id,
  onResize,
}: ChartContainerProps) {
  // Generate CSS variables for colors
  const cssVars = React.useMemo(() => {
    const vars: Record<string, string> = {};
    Object.entries(config).forEach(([key, value]) => {
      if (value.color) {
        vars[`--color-${key}`] = value.color;
      }
    });
    return vars;
  }, [config]);

  return (
    <ChartContext.Provider value={config}>
      <ResponsiveContainer
        width={width ?? '100%'}
        height={height ?? '100%'}
        minHeight={minHeight ?? 200}
        maxHeight={maxHeight ?? undefined}
        minWidth={minWidth ?? undefined}
        aspect={aspect ?? undefined}
        initialDimension={initialDimension ?? undefined}
        debounce={debounce ?? undefined}
        className={cn('w-full', className)}
        id={id}
        style={{
          ...cssVars,
          ...style,
        }}
        onResize={onResize ?? undefined}
      >
        {children as React.ReactElement}
      </ResponsiveContainer>
    </ChartContext.Provider>
  );
}

// Tooltip components
interface ChartTooltipContentProps {
  active?: boolean;
  payload?: any[];
  label?: string;
  indicator?: 'line' | 'dot' | 'dashed';
  hideLabel?: boolean;
  hideIndicator?: boolean;
  nameKey?: string;
  labelKey?: string;
}

export function ChartTooltipContent({
  active,
  payload,
  label,
  indicator = 'dot',
  hideLabel = false,
  hideIndicator = false,
  nameKey,
  labelKey,
}: ChartTooltipContentProps) {
  const config = React.useContext(ChartContext);

  if (!active || !payload?.length) {
    return null;
  }

  return (
    <div className="grid items-start gap-2 rounded-lg border border-border bg-background p-2 text-xs shadow-xl" style={{ minWidth: '8rem' }}>
      {!hideLabel && label && (
        <div className="font-medium text-foreground">{labelKey ? payload[0]?.payload?.[labelKey] : label}</div>
      )}
      <div className="grid gap-2">
        {payload.map((item, index) => {
          const key = nameKey ? item.payload?.[nameKey] : item.dataKey;
          const configItem = config?.[key];
          
          return (
            <div key={index} className="flex w-full flex-wrap items-stretch gap-2">
              {!hideIndicator && (
                <div
                  className={cn(
                    'h-2 w-2 shrink-0 rounded-sm',
                    indicator === 'dot' && 'rounded-full',
                    indicator === 'line' && 'w-1',
                    indicator === 'dashed' && 'w-0 border-2 border-dashed bg-transparent'
                  )}
                  style={{ 
                    backgroundColor: indicator === 'dashed' ? undefined : item.color,
                    borderColor: indicator === 'dashed' ? item.color : undefined
                  }}
                />
              )}
              <div className="flex flex-1 justify-between leading-none">
                <span className="text-muted-foreground">
                  {configItem?.label || key}
                </span>
                <span className="font-medium text-foreground">
                  {item.value}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Legend components
interface ChartLegendContentProps {
  payload?: any[];
  nameKey?: string;
  hideIcon?: boolean;
}

export function ChartLegendContent({
  payload,
  nameKey,
  hideIcon = false,
}: ChartLegendContentProps) {
  const config = React.useContext(ChartContext);

  if (!payload?.length) {
    return null;
  }

  return (
    <div className="flex flex-wrap items-center justify-center gap-4">
      {payload.map((item, index) => {
        const key = nameKey ? item.payload?.[nameKey] : item.dataKey;
        const configItem = config?.[key];

        return (
          <div key={index} className="flex items-center gap-1.5 text-sm">
            {!hideIcon && (
              <div
                className="h-2 w-2 rounded-full"
                style={{ backgroundColor: item.color }}
              />
            )}
            <span className="text-muted-foreground">
              {configItem?.label || key}
            </span>
          </div>
        );
      })}
    </div>
  );
}
