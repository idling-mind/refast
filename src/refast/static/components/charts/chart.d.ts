import { default as React } from 'react';
import { Tooltip as RechartsTooltip, Legend as RechartsLegend } from 'recharts';

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
    className?: string;
    aspectRatio?: number;
    minHeight?: number | string;
    children: React.ReactNode;
}
export declare function ChartContainer({ config, className, aspectRatio, minHeight, children, }: ChartContainerProps): import("react/jsx-runtime").JSX.Element;
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
