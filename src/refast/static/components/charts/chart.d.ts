import { default as React } from 'react';
import { ResponsiveContainer, Tooltip as RechartsTooltip, Legend as RechartsLegend } from 'recharts';

export declare function ChartTooltip({ cursor, content, ...props }: React.ComponentProps<typeof RechartsTooltip>): import("react/jsx-runtime").JSX.Element;
export declare const ChartLegend: typeof RechartsLegend;
interface ChartConfig {
    [key: string]: {
        label: string;
        color?: string;
        icon?: React.ComponentType;
    };
}
export declare function useChart(): ChartConfig;
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
export declare function ChartContainer({ config, children, width, height, minHeight, maxHeight, minWidth, aspect, initialDimension, debounce, className, style, id, onResize, }: ChartContainerProps): import("react/jsx-runtime").JSX.Element;
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
export declare function ChartTooltipContent({ active, payload, label, indicator, hideLabel, hideIndicator, nameKey, labelKey, }: ChartTooltipContentProps): import("react/jsx-runtime").JSX.Element | null;
interface ChartLegendContentProps {
    payload?: any[];
    nameKey?: string;
    hideIcon?: boolean;
}
export declare function ChartLegendContent({ payload, nameKey, hideIcon, }: ChartLegendContentProps): import("react/jsx-runtime").JSX.Element | null;
export {};
