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
  className?: string;
  aspectRatio?: number;
  minHeight?: number | string;
  children: React.ReactNode;
}

export function ChartContainer({
  config,
  className,
  aspectRatio,
  minHeight = 200,
  children,
}: ChartContainerProps) {
  // Generate CSS variables for colors
  const style = React.useMemo(() => {
    const vars: Record<string, string> = {};
    Object.entries(config).forEach(([key, value]) => {
      if (value.color) {
        vars[`--color-${key}`] = value.color;
      }
    });
    return vars;
  }, [config]);

  const minHeightNum = React.useMemo(() => {
    if (typeof minHeight === 'number') return minHeight;
    const parsed = parseInt(minHeight as string);
    return isNaN(parsed) ? 0 : parsed;
  }, [minHeight]);

  return (
    <ChartContext.Provider value={config}>
      <div
        className={cn('w-full', className)}
        style={{
          ...style,
          minHeight,
          aspectRatio: aspectRatio ? `${aspectRatio}` : undefined,
        }}
      >
        <ResponsiveContainer width="100%" height="100%" minHeight={minHeightNum}>
          {children as React.ReactElement}
        </ResponsiveContainer>
      </div>
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
