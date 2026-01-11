# Stage 10: shadcn/ui Charts

## Progress

- [ ] Task 10.1: Chart infrastructure setup
- [ ] Task 10.2: Area charts
- [ ] Task 10.3: Bar charts
- [ ] Task 10.4: Line charts
- [ ] Task 10.5: Pie charts
- [ ] Task 10.6: Radar charts
- [ ] Task 10.7: Radial charts
- [ ] Task 10.8: Chart utilities (tooltips, legends)

## Objectives

Implement a comprehensive charting system using Recharts, following shadcn/ui chart patterns from https://ui.shadcn.com/charts.

This stage adds:
- Full Recharts integration
- Area, Bar, Line, Pie, Radar, and Radial charts
- Interactive tooltips and legends
- Responsive chart containers
- Theme-aware color schemes
- Python-first API for chart creation

## Prerequisites

- Stage 6 complete (React frontend)
- Stage 9 in progress (for Card dependency)

## Dependencies

```json
{
  "recharts": "^2.15.0"
}
```

---

## Task 10.1: Chart Infrastructure Setup

### Description
Set up the foundational chart components and utilities.

### Files to Create

**src/refast/components/shadcn/charts/__init__.py**
```python
"""Chart components powered by Recharts."""

from refast.components.shadcn.charts.base import (
    Chart,
    ChartContainer,
    ChartConfig,
    ChartTooltip,
    ChartTooltipContent,
    ChartLegend,
    ChartLegendContent,
    ChartStyle,
)
from refast.components.shadcn.charts.area import AreaChart, Area
from refast.components.shadcn.charts.bar import BarChart, Bar
from refast.components.shadcn.charts.line import LineChart, Line
from refast.components.shadcn.charts.pie import PieChart, Pie, PieLabel
from refast.components.shadcn.charts.radar import RadarChart, Radar, PolarGrid, PolarAngleAxis
from refast.components.shadcn.charts.radial import RadialBarChart, RadialBar

__all__ = [
    # Base
    "Chart",
    "ChartContainer",
    "ChartConfig",
    "ChartTooltip",
    "ChartTooltipContent",
    "ChartLegend",
    "ChartLegendContent",
    "ChartStyle",
    # Area
    "AreaChart",
    "Area",
    # Bar
    "BarChart",
    "Bar",
    # Line
    "LineChart",
    "Line",
    # Pie
    "PieChart",
    "Pie",
    "PieLabel",
    # Radar
    "RadarChart",
    "Radar",
    "PolarGrid",
    "PolarAngleAxis",
    # Radial
    "RadialBarChart",
    "RadialBar",
]
```

**src/refast/components/shadcn/charts/base.py**
```python
"""Base chart components and utilities."""

from typing import Any, Literal
from pydantic import BaseModel, Field
from refast.components.base import Component


class ChartConfig(BaseModel):
    """Configuration for chart data series."""
    
    label: str
    color: str | None = None
    icon: str | None = None
    
    class Config:
        extra = "allow"


class ChartStyle(Component):
    """
    Style component for chart theming.
    
    Generates CSS custom properties for chart colors.
    """
    
    component_type: str = "ChartStyle"
    
    def __init__(
        self,
        id: str,
        config: dict[str, ChartConfig],
        **kwargs: Any,
    ):
        super().__init__(id=id, **kwargs)
        self.config = config
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "id": self.id,
                "config": {k: v.model_dump() for k, v in self.config.items()},
            },
        }


class ChartContainer(Component):
    """
    Container component for charts.
    
    Provides responsive sizing and theming context.
    
    Example:
        ```python
        ChartContainer(
            config={
                "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
                "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
            },
            AreaChart(
                data=data,
                Area(data_key="desktop", fill="var(--color-desktop)"),
                Area(data_key="mobile", fill="var(--color-mobile)"),
            ),
        )
        ```
    """
    
    component_type: str = "ChartContainer"
    
    def __init__(
        self,
        *children: Component,
        config: dict[str, ChartConfig] | None = None,
        class_name: str = "",
        aspect_ratio: float | None = None,
        min_height: int | str = 200,
        **kwargs: Any,
    ):
        super().__init__(class_name=class_name, **kwargs)
        self.config = config or {}
        self.aspect_ratio = aspect_ratio
        self.min_height = min_height
        self.children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "config": {k: v.model_dump() for k, v in self.config.items()},
                "className": self.class_name,
                "aspectRatio": self.aspect_ratio,
                "minHeight": self.min_height,
            },
            "children": [c.render() for c in self.children],
        }


class ChartTooltip(Component):
    """
    Tooltip component for charts.
    
    Example:
        ```python
        ChartTooltip(
            cursor=True,
            content=ChartTooltipContent(indicator="line"),
        )
        ```
    """
    
    component_type: str = "ChartTooltip"
    
    def __init__(
        self,
        content: "ChartTooltipContent | None" = None,
        cursor: bool = True,
        hide_label: bool = False,
        hide_indicator: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.content = content
        self.cursor = cursor
        self.hide_label = hide_label
        self.hide_indicator = hide_indicator
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "cursor": self.cursor,
                "hideLabel": self.hide_label,
                "hideIndicator": self.hide_indicator,
            },
            "children": [self.content.render()] if self.content else [],
        }


class ChartTooltipContent(Component):
    """
    Content component for chart tooltips.
    
    Args:
        indicator: Type of indicator ("line" | "dot" | "dashed")
        name_key: Key to use for the name
        label_key: Key to use for the label
    """
    
    component_type: str = "ChartTooltipContent"
    
    def __init__(
        self,
        indicator: Literal["line", "dot", "dashed"] = "dot",
        name_key: str | None = None,
        label_key: str | None = None,
        hide_label: bool = False,
        hide_indicator: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.indicator = indicator
        self.name_key = name_key
        self.label_key = label_key
        self.hide_label = hide_label
        self.hide_indicator = hide_indicator
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "indicator": self.indicator,
                "nameKey": self.name_key,
                "labelKey": self.label_key,
                "hideLabel": self.hide_label,
                "hideIndicator": self.hide_indicator,
            },
        }


class ChartLegend(Component):
    """
    Legend component for charts.
    
    Example:
        ```python
        ChartLegend(content=ChartLegendContent())
        ```
    """
    
    component_type: str = "ChartLegend"
    
    def __init__(
        self,
        content: "ChartLegendContent | None" = None,
        vertical_align: Literal["top", "middle", "bottom"] = "bottom",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.content = content
        self.vertical_align = vertical_align
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "verticalAlign": self.vertical_align,
            },
            "children": [self.content.render()] if self.content else [],
        }


class ChartLegendContent(Component):
    """Content component for chart legends."""
    
    component_type: str = "ChartLegendContent"
    
    def __init__(
        self,
        name_key: str | None = None,
        hide_icon: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.name_key = name_key
        self.hide_icon = hide_icon
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "nameKey": self.name_key,
                "hideIcon": self.hide_icon,
            },
        }
```

**src/refast-client/src/components/charts/chart.tsx**
```typescript
import React from 'react';
import {
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  Legend as RechartsLegend,
} from 'recharts';
import { cn } from '../../utils';

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
        <ResponsiveContainer width="100%" height="100%">
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
```

### Tests
- ChartContainer renders with config
- CSS variables are generated correctly
- Tooltip displays data correctly
- Legend renders items correctly

---

## Task 10.2: Area Charts

### Description
Implement area chart components with various styles.

### Python API

```python
from refast.components.charts import (
    ChartContainer,
    ChartConfig,
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    ChartTooltip,
    ChartTooltipContent,
)

# Basic area chart
data = [
    {"month": "January", "desktop": 186},
    {"month": "February", "desktop": 305},
    {"month": "March", "desktop": 237},
    {"month": "April", "desktop": 73},
    {"month": "May", "desktop": 209},
    {"month": "June", "desktop": 214},
]

ChartContainer(
    config={
        "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
    },
    AreaChart(
        data=data,
        CartesianGrid(vertical=False),
        XAxis(data_key="month", tick_line=False, axis_line=False),
        ChartTooltip(cursor=False, content=ChartTooltipContent(indicator="line")),
        Area(
            data_key="desktop",
            type="natural",
            fill="var(--color-desktop)",
            fill_opacity=0.4,
            stroke="var(--color-desktop)",
        ),
    ),
)
```

### Variants

1. **Basic Area Chart** - Simple filled area
2. **Stacked Area Chart** - Multiple areas stacked
3. **Stacked Expanded** - 100% stacked
4. **Gradient Area** - With gradient fill
5. **Step Area** - Step interpolation
6. **Linear Area** - Linear interpolation
7. **Interactive Area** - With date range selector

### Files

**src/refast/components/shadcn/charts/area.py**
```python
"""Area chart components."""

from typing import Any, Literal
from refast.components.base import Component


class AreaChart(Component):
    """
    Area chart component.
    
    Example:
        ```python
        AreaChart(
            data=data,
            margin={"top": 10, "right": 10, "left": 10, "bottom": 0},
            Area(data_key="value", fill="hsl(var(--chart-1))"),
        )
        ```
    """
    
    component_type: str = "AreaChart"
    
    def __init__(
        self,
        *children: Component,
        data: list[dict[str, Any]],
        margin: dict[str, int] | None = None,
        stack_offset: Literal["expand", "none", "wiggle", "silhouette"] | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data = data
        self.margin = margin or {"top": 10, "right": 10, "left": 10, "bottom": 0}
        self.stack_offset = stack_offset
        self.children = children
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "data": self.data,
                "margin": self.margin,
                "stackOffset": self.stack_offset,
            },
            "children": [c.render() for c in self.children],
        }


class Area(Component):
    """
    Area component for AreaChart.
    
    Args:
        data_key: Key from data to use for values
        type: Interpolation type
        fill: Fill color
        fill_opacity: Fill opacity (0-1)
        stroke: Stroke color
        stroke_width: Stroke width
        stacked_id: ID for stacking multiple areas
    """
    
    component_type: str = "Area"
    
    def __init__(
        self,
        data_key: str,
        type: Literal["basis", "linear", "natural", "monotone", "step", "stepBefore", "stepAfter"] = "natural",
        fill: str = "hsl(var(--chart-1))",
        fill_opacity: float = 0.4,
        stroke: str | None = None,
        stroke_width: int = 2,
        stacked_id: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data_key = data_key
        self.type = type
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.stroke = stroke or fill
        self.stroke_width = stroke_width
        self.stacked_id = stacked_id
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "dataKey": self.data_key,
                "type": self.type,
                "fill": self.fill,
                "fillOpacity": self.fill_opacity,
                "stroke": self.stroke,
                "strokeWidth": self.stroke_width,
                "stackId": self.stacked_id,
            },
        }
```

### Tests
- Renders area with data
- Supports gradient fills
- Stacking works correctly
- Tooltip shows on hover

---

## Task 10.3: Bar Charts

### Description
Implement bar chart components with various styles.

### Python API

```python
from refast.components.charts import (
    ChartContainer,
    ChartConfig,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    ChartTooltip,
    ChartTooltipContent,
)

# Basic bar chart
data = [
    {"month": "January", "desktop": 186, "mobile": 80},
    {"month": "February", "desktop": 305, "mobile": 200},
    {"month": "March", "desktop": 237, "mobile": 120},
]

ChartContainer(
    config={
        "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
        "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
    },
    BarChart(
        data=data,
        XAxis(data_key="month"),
        YAxis(),
        ChartTooltip(content=ChartTooltipContent()),
        Bar(data_key="desktop", fill="var(--color-desktop)", radius=4),
        Bar(data_key="mobile", fill="var(--color-mobile)", radius=4),
    ),
)
```

### Variants

1. **Basic Bar Chart** - Vertical bars
2. **Horizontal Bar Chart** - Horizontal layout
3. **Stacked Bar Chart** - Stacked bars
4. **Grouped Bar Chart** - Side-by-side bars
5. **Mixed Bar Chart** - With line overlay
6. **Negative Bar Chart** - With negative values
7. **Bar Chart with Label** - Labels on bars
8. **Interactive Bar Chart** - With click handlers

### Files

**src/refast/components/shadcn/charts/bar.py**

### Tests
- Renders bars correctly
- Horizontal layout works
- Stacking works correctly
- Labels display on bars

---

## Task 10.4: Line Charts

### Description
Implement line chart components.

### Python API

```python
from refast.components.charts import (
    ChartContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    ChartTooltip,
    ChartTooltipContent,
)

data = [
    {"month": "Jan", "desktop": 186, "mobile": 80},
    {"month": "Feb", "desktop": 305, "mobile": 200},
    {"month": "Mar", "desktop": 237, "mobile": 120},
]

ChartContainer(
    config={
        "desktop": ChartConfig(label="Desktop", color="hsl(var(--chart-1))"),
        "mobile": ChartConfig(label="Mobile", color="hsl(var(--chart-2))"),
    },
    LineChart(
        data=data,
        XAxis(data_key="month"),
        YAxis(),
        ChartTooltip(content=ChartTooltipContent()),
        Line(data_key="desktop", stroke="var(--color-desktop)", dot=False),
        Line(data_key="mobile", stroke="var(--color-mobile)", dot=False),
    ),
)
```

### Variants

1. **Basic Line Chart** - Simple lines
2. **Line Chart with Dots** - With data point dots
3. **Multiple Lines** - Multiple series
4. **Step Line** - Step interpolation
5. **Linear Line** - Linear interpolation
6. **Line with Label** - Labels on points
7. **Interactive Line** - Click/hover handlers

### Files

**src/refast/components/shadcn/charts/line.py**

### Tests
- Renders lines correctly
- Different interpolation types work
- Dots display correctly
- Multiple series work

---

## Task 10.5: Pie Charts

### Description
Implement pie and donut chart components.

### Python API

```python
from refast.components.charts import (
    ChartContainer,
    PieChart,
    Pie,
    PieLabel,
    ChartTooltip,
    ChartTooltipContent,
)

data = [
    {"browser": "chrome", "visitors": 275, "fill": "var(--color-chrome)"},
    {"browser": "safari", "visitors": 200, "fill": "var(--color-safari)"},
    {"browser": "firefox", "visitors": 187, "fill": "var(--color-firefox)"},
    {"browser": "edge", "visitors": 173, "fill": "var(--color-edge)"},
    {"browser": "other", "visitors": 90, "fill": "var(--color-other)"},
]

# Donut chart
ChartContainer(
    config={
        "chrome": ChartConfig(label="Chrome", color="hsl(var(--chart-1))"),
        "safari": ChartConfig(label="Safari", color="hsl(var(--chart-2))"),
        "firefox": ChartConfig(label="Firefox", color="hsl(var(--chart-3))"),
        "edge": ChartConfig(label="Edge", color="hsl(var(--chart-4))"),
        "other": ChartConfig(label="Other", color="hsl(var(--chart-5))"),
    },
    PieChart(
        Pie(
            data=data,
            data_key="visitors",
            name_key="browser",
            inner_radius=60,  # Makes it a donut
            outer_radius=80,
            PieLabel(),
        ),
        ChartTooltip(content=ChartTooltipContent(hide_label=True)),
    ),
)
```

### Variants

1. **Basic Pie Chart** - Simple pie
2. **Donut Chart** - With inner radius
3. **Pie with Label** - Labels on slices
4. **Pie with Legend** - With legend
5. **Interactive Pie** - With click handlers
6. **Pie with Custom Colors** - Custom fill per slice

### Files

**src/refast/components/shadcn/charts/pie.py**

### Tests
- Renders pie correctly
- Donut with inner radius works
- Labels position correctly
- Legend works

---

## Task 10.6: Radar Charts

### Description
Implement radar chart components.

### Python API

```python
from refast.components.charts import (
    ChartContainer,
    RadarChart,
    Radar,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    ChartTooltip,
    ChartTooltipContent,
)

data = [
    {"skill": "JavaScript", "level": 90},
    {"skill": "TypeScript", "level": 85},
    {"skill": "Python", "level": 80},
    {"skill": "React", "level": 95},
    {"skill": "Node.js", "level": 75},
]

ChartContainer(
    config={
        "level": ChartConfig(label="Skill Level", color="hsl(var(--chart-1))"),
    },
    RadarChart(
        data=data,
        PolarGrid(),
        PolarAngleAxis(data_key="skill"),
        PolarRadiusAxis(angle=30),
        Radar(
            data_key="level",
            fill="var(--color-level)",
            fill_opacity=0.6,
            stroke="var(--color-level)",
        ),
        ChartTooltip(content=ChartTooltipContent()),
    ),
)
```

### Variants

1. **Basic Radar Chart** - Single series
2. **Multiple Radars** - Overlapping series
3. **Radar with Legend** - With legend
4. **Filled Radar** - With fill opacity

### Files

**src/refast/components/shadcn/charts/radar.py**

### Tests
- Renders radar correctly
- Multiple series overlap correctly
- Angle axis labels correctly

---

## Task 10.7: Radial Charts

### Description
Implement radial bar chart components.

### Python API

```python
from refast.components.charts import (
    ChartContainer,
    RadialBarChart,
    RadialBar,
    PolarAngleAxis,
    ChartTooltip,
    ChartTooltipContent,
)

data = [
    {"browser": "chrome", "visitors": 275, "fill": "var(--color-chrome)"},
    {"browser": "safari", "visitors": 200, "fill": "var(--color-safari)"},
    {"browser": "firefox", "visitors": 187, "fill": "var(--color-firefox)"},
]

ChartContainer(
    config={
        "chrome": ChartConfig(label="Chrome", color="hsl(var(--chart-1))"),
        "safari": ChartConfig(label="Safari", color="hsl(var(--chart-2))"),
        "firefox": ChartConfig(label="Firefox", color="hsl(var(--chart-3))"),
    },
    RadialBarChart(
        data=data,
        inner_radius=30,
        outer_radius=100,
        start_angle=90,
        end_angle=-270,
        RadialBar(
            data_key="visitors",
            background=True,
        ),
        PolarAngleAxis(type="number", domain=[0, 500], tick=False),
        ChartTooltip(content=ChartTooltipContent(name_key="browser")),
    ),
)
```

### Variants

1. **Basic Radial Bar** - Simple radial progress
2. **Radial Bar with Label** - With center label
3. **Multiple Radial Bars** - Stacked radials
4. **Radial with Text** - Text in center

### Files

**src/refast/components/shadcn/charts/radial.py**

### Tests
- Renders radial bars correctly
- Angles calculate correctly
- Center content works

---

## Task 10.8: Chart Utilities

### Description
Implement common chart utilities and axes.

### Components

```python
# Axes
XAxis(
    data_key="month",
    tick_line=False,
    axis_line=False,
    tick_margin=8,
    tick_formatter=lambda v: v[:3],  # Truncate month names
)

YAxis(
    tick_line=False,
    axis_line=False,
    tick_margin=8,
    tick_count=5,
)

# Grid
CartesianGrid(
    stroke_dasharray="3 3",
    vertical=False,
    horizontal=True,
)

# Reference lines
ReferenceLine(
    y=200,
    stroke="hsl(var(--muted))",
    stroke_dasharray="3 3",
    label="Target",
)

# Brush (for zooming)
Brush(
    data_key="month",
    height=30,
    stroke="hsl(var(--border))",
)
```

### Files

**src/refast/components/shadcn/charts/utils.py**

### Tests
- Axes render correctly
- Grid renders correctly
- Reference lines position correctly
- Brush zooming works

---

## File Structure

```
src/refast/components/shadcn/charts/
├── __init__.py
├── base.py          # ChartContainer, ChartTooltip, ChartLegend
├── area.py          # AreaChart, Area
├── bar.py           # BarChart, Bar
├── line.py          # LineChart, Line
├── pie.py           # PieChart, Pie
├── radar.py         # RadarChart, Radar
├── radial.py        # RadialBarChart, RadialBar
└── utils.py         # XAxis, YAxis, CartesianGrid, etc.

src/refast-client/src/components/charts/
├── index.ts
├── chart.tsx        # ChartContainer, tooltips, legends
├── area-chart.tsx
├── bar-chart.tsx
├── line-chart.tsx
├── pie-chart.tsx
├── radar-chart.tsx
├── radial-chart.tsx
└── utils.tsx        # Axes, grids, brushes
```

---

## Theme Integration

### CSS Variables for Charts

Add to `src/refast-client/src/index.css`:

```css
:root {
  --chart-1: 221.2 83.2% 53.3%;
  --chart-2: 212 95% 68%;
  --chart-3: 216 92% 60%;
  --chart-4: 210 98% 78%;
  --chart-5: 212 97% 87%;
}

.dark {
  --chart-1: 220 70% 50%;
  --chart-2: 160 60% 45%;
  --chart-3: 30 80% 55%;
  --chart-4: 280 65% 60%;
  --chart-5: 340 75% 55%;
}
```

---

## Example Usage

### Dashboard with Multiple Charts

```python
from refast.components import Row, Column, Card, CardHeader, CardTitle, CardContent
from refast.components.charts import (
    ChartContainer,
    ChartConfig,
    AreaChart,
    Area,
    BarChart,
    Bar,
    PieChart,
    Pie,
    ChartTooltip,
    ChartTooltipContent,
)

@app.page("/dashboard")
def dashboard(ctx: Context):
    return Column(
        Row(
            Card(
                CardHeader(CardTitle("Revenue Over Time")),
                CardContent(
                    ChartContainer(
                        config={"revenue": ChartConfig(label="Revenue", color="hsl(var(--chart-1))")},
                        AreaChart(
                            data=ctx.state.revenue_data,
                            Area(data_key="revenue", fill="var(--color-revenue)"),
                            ChartTooltip(content=ChartTooltipContent()),
                        ),
                    ),
                ),
            ),
            Card(
                CardHeader(CardTitle("Sales by Category")),
                CardContent(
                    ChartContainer(
                        config={"sales": ChartConfig(label="Sales", color="hsl(var(--chart-2))")},
                        BarChart(
                            data=ctx.state.sales_data,
                            Bar(data_key="sales", fill="var(--color-sales)"),
                            ChartTooltip(content=ChartTooltipContent()),
                        ),
                    ),
                ),
            ),
        ),
    )
```

---

## Testing Strategy

### Unit Tests
- Each chart type renders correctly
- Props are passed correctly to Recharts
- Tooltips display data correctly
- Legends render items correctly

### Integration Tests
- Charts update with new data
- Real-time data streaming works
- Click handlers fire correctly

### Visual Tests
- Charts render at different sizes
- Responsive behavior works
- Theme switching works

---

## Estimated Effort

| Task | Components | Estimated Time |
|------|------------|----------------|
| 10.1 | Infrastructure | 1-2 days |
| 10.2 | Area Charts | 1 day |
| 10.3 | Bar Charts | 1 day |
| 10.4 | Line Charts | 1 day |
| 10.5 | Pie Charts | 1 day |
| 10.6 | Radar Charts | 0.5 days |
| 10.7 | Radial Charts | 0.5 days |
| 10.8 | Utilities | 1 day |
| **Total** | **7 chart types** | **7-8 days** |

---

## Success Criteria

1. All chart types render correctly with Recharts
2. Charts are responsive and work at all sizes
3. Theme colors are applied correctly
4. Tooltips and legends work as expected
5. Python API is intuitive and type-safe
6. Documentation with examples for each chart type
7. Integration with existing Card component
8. Real-time data updates work smoothly
