import { Radar as RechartsRadar, PolarAngleAxis as RechartsPolarAngleAxis, PolarRadiusAxis as RechartsPolarRadiusAxis } from 'recharts';

export declare const RadarChart: import('react').ForwardRefExoticComponent<import('recharts/types/util/types').PolarChartProps & import('react').RefAttributes<SVGSVGElement>>;
export declare const Radar: typeof RechartsRadar;
export declare const PolarGrid: {
    ({ gridType, radialLines, angleAxisId, radiusAxisId, cx: cxFromOutside, cy: cyFromOutside, innerRadius: innerRadiusFromOutside, outerRadius: outerRadiusFromOutside, polarAngles: polarAnglesInput, polarRadius: polarRadiusInput, ...inputs }: import('recharts').PolarGridProps): React.JSX.Element | null;
    displayName: string;
};
export declare const PolarAngleAxis: typeof RechartsPolarAngleAxis;
export declare const PolarRadiusAxis: typeof RechartsPolarRadiusAxis;
