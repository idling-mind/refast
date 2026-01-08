import React from 'react';
import {
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  Legend as RechartsLegend,
} from 'recharts';
import { cn } from '../../utils';

export const ChartTooltip = RechartsTooltip;
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
    <div className="rounded-lg border bg-background p-2 shadow-sm">
      {!hideLabel && label && (
        <div className="mb-1 font-medium">{labelKey ? payload[0]?.payload?.[labelKey] : label}</div>
      )}
      <div className="flex flex-col gap-1">
        {payload.map((item, index) => {
          const key = nameKey ? item.payload?.[nameKey] : item.dataKey;
          const configItem = config?.[key];
          
          return (
            <div key={index} className="flex items-center gap-2 text-sm">
              {!hideIndicator && (
                <div
                  className={cn(
                    'h-2 w-2 rounded-full',
                    indicator === 'line' && 'h-0.5 w-4 rounded-none',
                    indicator === 'dashed' && 'h-0.5 w-4 rounded-none border-dashed border-t-2'
                  )}
                  style={{ backgroundColor: item.color }}
                />
              )}
              <span className="text-muted-foreground">
                {configItem?.label || key}:
              </span>
              <span className="font-medium">{item.value}</span>
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
