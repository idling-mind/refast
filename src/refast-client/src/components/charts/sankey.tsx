import { Sankey as RechartsSankey, Tooltip } from 'recharts';

const COLORS = [
  'hsl(var(--chart-1))',
  'hsl(var(--chart-2))',
  'hsl(var(--chart-3))',
  'hsl(var(--chart-4))',
  'hsl(var(--chart-5))',
];

/** Stable color for a node name — same result in renderers and tooltip. */
function nameToColor(name: string): string {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = (hash * 31 + name.charCodeAt(i)) & 0xffffffff;
  }
  return COLORS[Math.abs(hash) % COLORS.length];
}

function SankeyNode({ x, y, width, height, payload, containerWidth }: any) {
  const color = nameToColor(payload?.name ?? '');
  // If the label would overflow to the right, place it to the left of the node.
  const isRight = x + width + 6 > containerWidth;
  return (
    <g>
      <rect x={x} y={y} width={width} height={height} fill={color} fillOpacity={0.9} rx={2} />
      <text
        textAnchor={isRight ? 'end' : 'start'}
        x={isRight ? x - 6 : x + width + 6}
        y={y + height / 2}
        dominantBaseline="middle"
        fontSize={12}
        fill="hsl(var(--foreground))"
      >
        {payload.name}
      </text>
    </g>
  );
}

function SankeyLink({
  sourceX,
  sourceY,
  sourceControlX,
  targetX,
  targetY,
  targetControlX,
  linkWidth,
  payload,
}: any) {
  // Color by source node name so links visually connect to their source node
  const color = nameToColor(payload?.source?.name ?? '');
  const half = linkWidth / 2;
  return (
    <path
      d={[
        `M ${sourceX},${sourceY - half}`,
        `C ${sourceControlX},${sourceY - half} ${targetControlX},${targetY - half} ${targetX},${targetY - half}`,
        `L ${targetX},${targetY + half}`,
        `C ${targetControlX},${targetY + half} ${sourceControlX},${sourceY + half} ${sourceX},${sourceY + half}`,
        'Z',
      ].join(' ')}
      fill={color}
      fillOpacity={0.2}
      stroke={color}
      strokeOpacity={0.3}
      strokeWidth={1}
    />
  );
}

function SankeyTooltipContent({ active, payload }: any) {
  if (!active || !payload?.length) return null;
  const item = payload[0];
  const data = item?.payload;
  if (!data) return null;

  // value is set directly on the payload item by Recharts' sankeyPayloadSearcher
  const value = item.value;
  const formattedValue = typeof value === 'number' ? value.toLocaleString() : value;

  if (data.source && data.target) {
    // Link hover — color matches source node
    const color = nameToColor(data.source?.name ?? '');
    return (
      <div className="rounded-lg border border-border bg-background px-3 py-2 text-xs shadow-xl">
        <div className="font-medium text-foreground mb-1">
          {data.source.name} → {data.target.name}
        </div>
        <div className="flex items-center gap-1.5 text-muted-foreground">
          <span className="inline-block h-2 w-2 shrink-0 rounded-full" style={{ backgroundColor: color }} />
          Flow: <span className="font-medium text-foreground">{formattedValue}</span>
        </div>
      </div>
    );
  }

  // Node hover — color matches the node rectangle
  const color = nameToColor(data.name ?? '');
  return (
    <div className="rounded-lg border border-border bg-background px-3 py-2 text-xs shadow-xl">
      <div className="flex items-center gap-1.5 mb-1">
        <span className="inline-block h-2 w-2 shrink-0 rounded-full" style={{ backgroundColor: color }} />
        <span className="font-medium text-foreground">{data.name}</span>
      </div>
      {value != null && (
        <div className="text-muted-foreground">
          Value: <span className="font-medium text-foreground">{formattedValue}</span>
        </div>
      )}
    </div>
  );
}

export function Sankey({ node: _node, link: _link, children, ...props }: any) {
  return (
    <RechartsSankey node={SankeyNode} link={SankeyLink} {...props}>
      <Tooltip content={<SankeyTooltipContent />} />
      {children}
    </RechartsSankey>
  );
}
