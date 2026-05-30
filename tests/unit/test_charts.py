"""Tests for chart components."""

from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    Bar,
    BarChart,
    Brush,
    CartesianGrid,
    Cell,
    ChartContainer,
    ComposedChart,
    ErrorBar,
    Funnel,
    FunnelChart,
    Label,
    LabelList,
    Line,
    LineChart,
    Pie,
    PieChart,
    ReferenceArea,
    ReferenceDot,
    ReferenceLine,
    Sankey,
    Scatter,
    ScatterChart,
    Treemap,
    XAxis,
    YAxis,
    ZAxis,
)
from refast.context import Callback


def test_chart_container_props():
    """Test ChartContainer initialization and rendering with new props."""

    def handle_resize(ctx):
        pass

    cb = Callback(id="test-callback", func=handle_resize)

    container = ChartContainer(
        width=500,
        height=300,
        min_height=100,
        min_width=50,
        max_height=600,
        aspect=2.0,
        debounce=100,
        initial_dimension={"width": 400, "height": 200},
        on_resize=cb,
        class_name="my-chart",
    )

    rendered = container.render()
    props = rendered["props"]

    assert props["width"] == 500
    assert props["height"] == 300
    assert props["min_height"] == 100
    assert props["min_width"] == 50
    assert props["max_height"] == 600
    assert props["aspect"] == 2.0
    assert props["debounce"] == 100
    assert props["initialDimension"] == {"width": 400, "height": 200}
    assert props["onResize"] == cb.serialize()
    assert props["class_name"] == "my-chart"


class TestAreaChart:
    """Tests for AreaChart and Area components."""

    def test_area_chart_basic(self):
        """Test basic AreaChart creation."""
        data = [{"month": "Jan", "value": 100}]
        chart = AreaChart(data=data)

        rendered = chart.render()
        assert rendered["type"] == "AreaChart"
        assert rendered["props"]["data"] == data
        assert rendered["props"]["layout"] == "horizontal"

    def test_area_chart_with_callbacks(self):
        """Test AreaChart with event handlers."""
        data = [{"month": "Jan", "value": 100}]
        cb = Callback(id="test-cb", func=lambda ctx: None)

        chart = AreaChart(
            data=data,
            layout="vertical",
            sync_id="sync1",
            sync_method="value",
            on_click=cb,
            on_mouse_enter=cb,
        )

        rendered = chart.render()
        assert rendered["props"]["layout"] == "vertical"
        assert rendered["props"]["syncId"] == "sync1"
        assert rendered["props"]["syncMethod"] == "value"
        assert rendered["props"]["on_click"] == cb.serialize()
        assert rendered["props"]["on_mouse_enter"] == cb.serialize()

    def test_area_component_full_props(self):
        """Test Area component with all props."""
        area = Area(
            data_key="value",
            type="monotone",
            fill="#8884d8",
            fill_opacity=0.6,
            stroke="#8884d8",
            stacked_id="stack1",
            connect_nulls=True,
            dot=True,
            active_dot={"r": 8},
            label=True,
            legend_type="circle",
            name="Test Area",
            unit="$",
            x_axis_id="x1",
            y_axis_id="y1",
            is_animation_active=True,
            animation_begin=100,
            animation_duration=1000,
            animation_easing="ease-in-out",
            hide=False,
        )

        rendered = area.render()
        assert rendered["props"]["data_key"] == "value"
        assert rendered["props"]["type"] == "monotone"
        assert rendered["props"]["connectNulls"] is True
        assert rendered["props"]["legend_type"] == "circle"
        assert rendered["props"]["name"] == "Test Area"
        assert rendered["props"]["x_axis_id"] == "x1"
        assert rendered["props"]["y_axis_id"] == "y1"
        assert rendered["props"]["animation_duration"] == 1000


class TestBarChart:
    """Tests for BarChart and Bar components."""

    def test_bar_chart_with_sync(self):
        """Test BarChart with sync props."""
        data = [{"name": "A", "value": 100}]
        chart = BarChart(
            data=data,
            sync_id="charts",
            sync_method="index",
            reverse_stack_order=True,
            max_bar_size=50,
        )

        rendered = chart.render()
        assert rendered["props"]["syncId"] == "charts"
        assert rendered["props"]["syncMethod"] == "index"
        assert rendered["props"]["reverseStackOrder"] is True
        assert rendered["props"]["maxBarSize"] == 50

    def test_bar_component_full_props(self):
        """Test Bar component with all props."""
        bar = Bar(
            data_key="value",
            fill="#8884d8",
            radius=[4, 4, 0, 0],
            x_axis_id="x1",
            y_axis_id="y1",
            min_point_size=5,
            max_bar_size=100,
            name="Sales",
            unit="$",
            label=True,
            active_bar={"fill": "red"},
            animation_duration=500,
            hide=False,
        )

        rendered = bar.render()
        assert rendered["props"]["radius"] == [4, 4, 0, 0]
        assert rendered["props"]["x_axis_id"] == "x1"
        assert rendered["props"]["minPointSize"] == 5
        assert rendered["props"]["name"] == "Sales"
        assert rendered["props"]["activeBar"] == {"fill": "red"}


class TestLineChart:
    """Tests for LineChart and Line components."""

    def test_line_chart_with_callbacks(self):
        """Test LineChart with event callbacks."""
        data = [{"x": 1, "y": 10}]
        cb = Callback(id="cb", func=lambda ctx: None)

        chart = LineChart(
            data=data,
            layout="vertical",
            sync_id="line-sync",
            on_click=cb,
            on_mouse_move=cb,
        )

        rendered = chart.render()
        assert rendered["props"]["layout"] == "vertical"
        assert rendered["props"]["syncId"] == "line-sync"
        assert rendered["props"]["on_click"] == cb.serialize()
        assert rendered["props"]["on_mouse_move"] == cb.serialize()

    def test_line_component_full_props(self):
        """Test Line component with all props."""
        line = Line(
            data_key="value",
            type="linear",
            stroke="#82ca9d",
            stroke_width=3,
            dot={"r": 5},
            active_dot={"r": 8},
            connect_nulls=True,
            x_axis_id="x1",
            legend_type="square",
            name="Revenue",
            stroke_dasharray="5 5",
            animation_begin=200,
        )

        rendered = line.render()
        assert rendered["props"]["type"] == "linear"
        assert rendered["props"]["stroke_width"] == 3
        assert rendered["props"]["connectNulls"] is True
        assert rendered["props"]["stroke_dasharray"] == "5 5"


class TestPieChart:
    """Tests for PieChart and Pie components."""

    def test_pie_chart_with_callbacks(self):
        """Test PieChart with event handlers."""
        cb = Callback(id="cb", func=lambda ctx: None)
        chart = PieChart(
            on_click=cb,
            on_mouse_enter=cb,
        )

        rendered = chart.render()
        assert rendered["props"]["on_click"] == cb.serialize()
        assert rendered["props"]["on_mouse_enter"] == cb.serialize()

    def test_pie_component_full_props(self):
        """Test Pie component with all props."""
        data = [{"name": "A", "value": 100}]
        pie = Pie(
            data=data,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            inner_radius=60,
            outer_radius=80,
            start_angle=90,
            end_angle=-270,
            padding_angle=5,
            corner_radius=4,
            min_angle=10,
            label_line=True,
            legend_type="rect",
            animation_duration=800,
        )

        rendered = pie.render()
        assert rendered["props"]["start_angle"] == 90
        assert rendered["props"]["end_angle"] == -270
        assert rendered["props"]["paddingAngle"] == 5
        assert rendered["props"]["cornerRadius"] == 4
        assert rendered["props"]["minAngle"] == 10


class TestScatterChart:
    """Tests for ScatterChart and Scatter components."""

    def test_scatter_chart_basic(self):
        """Test basic ScatterChart creation."""
        data = [{"x": 100, "y": 200, "z": 50}]
        chart = ScatterChart(data=data, margin={"top": 20, "right": 20})

        rendered = chart.render()
        assert rendered["type"] == "ScatterChart"
        assert rendered["props"]["data"] == data

    def test_scatter_chart_with_callbacks(self):
        """Test ScatterChart with event handlers."""
        cb = Callback(id="cb", func=lambda ctx: None)
        chart = ScatterChart(
            sync_id="scatter-sync",
            on_click=cb,
            on_mouse_enter=cb,
        )

        rendered = chart.render()
        assert rendered["props"]["syncId"] == "scatter-sync"
        assert rendered["props"]["on_click"] == cb.serialize()

    def test_scatter_component_full_props(self):
        """Test Scatter component with all props."""
        data = [{"x": 100, "y": 200}]
        scatter = Scatter(
            data=data,
            x_axis_id="x1",
            y_axis_id="y1",
            z_axis_id="z1",
            line=True,
            line_type="fitting",
            shape="diamond",
            name="Points",
            fill="#ff7300",
            animation_duration=1000,
        )

        rendered = scatter.render()
        assert rendered["props"]["data"] == data
        assert rendered["props"]["x_axis_id"] == "x1"
        assert rendered["props"]["zAxisId"] == "z1"
        assert rendered["props"]["line"] is True
        assert rendered["props"]["lineType"] == "fitting"
        assert rendered["props"]["shape"] == "diamond"

    def test_z_axis_component(self):
        """Test ZAxis component."""
        z_axis = ZAxis(
            z_axis_id="z1",
            data_key="z",
            type="number",
            range=[10, 100],
            name="Size",
            unit="px",
        )

        rendered = z_axis.render()
        assert rendered["type"] == "ZAxis"
        assert rendered["props"]["zAxisId"] == "z1"
        assert rendered["props"]["range"] == [10, 100]
        assert rendered["props"]["name"] == "Size"


class TestComposedChart:
    """Tests for ComposedChart."""

    def test_composed_chart_basic(self):
        """Test basic ComposedChart creation."""
        data = [{"name": "A", "bar": 100, "line": 50, "area": 200}]
        chart = ComposedChart(
            data=data,
            bar_category_gap="20%",
            bar_gap=4,
        )

        rendered = chart.render()
        assert rendered["type"] == "ComposedChart"
        assert rendered["props"]["data"] == data
        assert rendered["props"]["bar_category_gap"] == "20%"

    def test_composed_chart_with_children(self):
        """Test ComposedChart with children."""
        data = [{"name": "A", "bar": 100, "line": 50}]
        chart = ComposedChart(
            data=data,
            children=[
                Bar(data_key="bar"),
                Line(data_key="line"),
            ],
        )

        rendered = chart.render()
        assert len(rendered["children"]) == 2
        assert rendered["children"][0]["type"] == "Bar"
        assert rendered["children"][1]["type"] == "Line"


class TestFunnelChart:
    """Tests for FunnelChart and Funnel components."""

    def test_funnel_chart_basic(self):
        """Test basic FunnelChart creation."""
        chart = FunnelChart(margin={"top": 5, "bottom": 5})

        rendered = chart.render()
        assert rendered["type"] == "FunnelChart"

    def test_funnel_component_full_props(self):
        """Test Funnel component with all props."""
        data = [
            {"name": "Visit", "value": 4000},
            {"name": "Cart", "value": 3000},
            {"name": "Purchase", "value": 1000},
        ]
        funnel = Funnel(
            data=data,
            data_key="value",
            name_key="name",
            label=True,
            last_shape_type="rectangle",
            reversed=False,
            animation_duration=1000,
        )

        rendered = funnel.render()
        assert rendered["type"] == "Funnel"
        # Data is enriched with auto-fill colors
        assert len(rendered["props"]["data"]) == 3
        assert rendered["props"]["data"][0]["name"] == "Visit"
        assert rendered["props"]["data"][0]["value"] == 4000
        assert "fill" in rendered["props"]["data"][0]
        assert rendered["props"]["lastShapeType"] == "rectangle"


class TestTreemap:
    """Tests for Treemap component."""

    def test_treemap_basic(self):
        """Test basic Treemap creation."""
        data = [
            {"name": "A", "size": 100},
            {"name": "B", "size": 200},
        ]
        treemap = Treemap(
            data=data,
            data_key="size",
            name_key="name",
            aspect_ratio=1.5,
            stroke="#fff",
        )

        rendered = treemap.render()
        assert rendered["type"] == "Treemap"
        assert rendered["props"]["data"] == data
        assert rendered["props"]["aspectRatio"] == 1.5

    def test_treemap_with_callbacks(self):
        """Test Treemap with event handlers."""
        data = [{"name": "A", "value": 100}]
        cb = Callback(id="cb", func=lambda ctx: None)

        treemap = Treemap(
            data=data,
            on_click=cb,
            on_mouse_enter=cb,
        )

        rendered = treemap.render()
        assert rendered["props"]["on_click"] == cb.serialize()


class TestSankey:
    """Tests for Sankey component."""

    def test_sankey_basic(self):
        """Test basic Sankey creation."""
        data = {
            "nodes": [{"name": "A"}, {"name": "B"}],
            "links": [{"source": 0, "target": 1, "value": 100}],
        }
        sankey = Sankey(
            data=data,
            node_padding=10,
            node_width=15,
            link_curvature=0.5,
        )

        rendered = sankey.render()
        assert rendered["type"] == "Sankey"
        assert rendered["props"]["data"] == data
        assert rendered["props"]["nodePadding"] == 10
        assert rendered["props"]["nodeWidth"] == 15
        assert rendered["props"]["linkCurvature"] == 0.5


class TestAxisComponents:
    """Tests for XAxis and YAxis components."""

    def test_x_axis_full_props(self):
        """Test XAxis with all props."""
        x_axis = XAxis(
            data_key="month",
            orientation="bottom",
            type="category",
            x_axis_id="x1",
            allow_decimals=False,
            allow_data_overflow=True,
            scale="band",
            domain=["auto", "auto"],
            tick_count=5,
            tick_size=8,
            interval="preserveEnd",
            padding={"left": 10, "right": 10},
            mirror=False,
            reversed=False,
            angle=-45,
            min_tick_gap=10,
        )

        rendered = x_axis.render()
        assert rendered["props"]["x_axis_id"] == "x1"
        assert rendered["props"]["allow_decimals"] is False
        assert rendered["props"]["allow_data_overflow"] is True
        assert rendered["props"]["tick_count"] == 5
        assert rendered["props"]["angle"] == -45

    def test_y_axis_full_props(self):
        """Test YAxis with all props."""
        y_axis = YAxis(
            data_key="value",
            orientation="right",
            type="number",
            y_axis_id="y1",
            width="auto",
            domain=[0, "dataMax + 100"],
            ticks=[0, 100, 200, 300],
            label={"value": "Sales", "angle": -90},
            unit="$",
        )

        rendered = y_axis.render()
        assert rendered["props"]["y_axis_id"] == "y1"
        assert rendered["props"]["orientation"] == "right"
        assert rendered["props"]["ticks"] == [0, 100, 200, 300]
        assert rendered["props"]["unit"] == "$"


class TestReferenceComponents:
    """Tests for reference and annotation components."""

    def test_reference_line_full_props(self):
        """Test ReferenceLine with all props."""
        ref_line = ReferenceLine(
            y=100,
            stroke="red",
            stroke_dasharray="3 3",
            stroke_width=2,
            label="Average",
            x_axis_id="x1",
            y_axis_id="y1",
            if_overflow="extendDomain",
            position="middle",
        )

        rendered = ref_line.render()
        assert rendered["props"]["y"] == 100
        assert rendered["props"]["stroke_width"] == 2
        assert rendered["props"]["x_axis_id"] == "x1"
        assert rendered["props"]["ifOverflow"] == "extendDomain"
        assert rendered["props"]["position"] == "middle"

    def test_reference_area_full_props(self):
        """Test ReferenceArea with all props."""
        ref_area = ReferenceArea(
            x1="Jan",
            x2="Mar",
            y1=0,
            y2=100,
            fill="#8884d8",
            fill_opacity=0.3,
            stroke="#8884d8",
            label="Q1",
        )

        rendered = ref_area.render()
        assert rendered["type"] == "ReferenceArea"
        assert rendered["props"]["x1"] == "Jan"
        assert rendered["props"]["x2"] == "Mar"
        assert rendered["props"]["fill_opacity"] == 0.3

    def test_reference_dot_full_props(self):
        """Test ReferenceDot with all props."""
        ref_dot = ReferenceDot(
            x=100,
            y=200,
            r=8,
            fill="red",
            stroke="white",
            stroke_width=2,
            label="Peak",
        )

        rendered = ref_dot.render()
        assert rendered["type"] == "ReferenceDot"
        assert rendered["props"]["x"] == 100
        assert rendered["props"]["r"] == 8

    def test_cell_component(self):
        """Test Cell component."""
        cell = Cell(fill="#8884d8", stroke="#fff")

        rendered = cell.render()
        assert rendered["type"] == "Cell"
        assert rendered["props"]["fill"] == "#8884d8"

    def test_label_list_component(self):
        """Test LabelList component."""
        label_list = LabelList(
            data_key="value",
            position="top",
            offset=10,
            fill="#333",
            font_size=12,
        )

        rendered = label_list.render()
        assert rendered["type"] == "LabelList"
        assert rendered["props"]["position"] == "top"
        assert rendered["props"]["offset"] == 10

    def test_label_component(self):
        """Test Label component."""
        label = Label(
            value="Total Sales",
            position="center",
            angle=-90,
            fill="#666",
        )

        rendered = label.render()
        assert rendered["type"] == "ChartLabel"
        assert rendered["props"]["value"] == "Total Sales"
        assert rendered["props"]["angle"] == -90

    def test_error_bar_component(self):
        """Test ErrorBar component."""
        error_bar = ErrorBar(
            data_key="error",
            width=5,
            direction="y",
            stroke="#ff0000",
            stroke_width=2,
        )

        rendered = error_bar.render()
        assert rendered["type"] == "ErrorBar"
        assert rendered["props"]["data_key"] == "error"
        assert rendered["props"]["direction"] == "y"


# ---------------------------------------------------------------------------
# New API: simplified colors, label/color on series, auto-fill in data
# ---------------------------------------------------------------------------

from refast.components.shadcn.charts import (  # noqa: E402
    ChartConfig,
    ChartContainer,
    RadialBarChart,
    RadialBar,
    Radar,
    Scatter,
)


class TestChartConfigColorShorthand:
    """ChartConfig accepts int color shorthand."""

    def test_int_color_converted_to_css_var(self):
        cfg = ChartConfig(label="Desktop", color=1)
        assert cfg.color == "hsl(var(--chart-1))"

    def test_int_color_large_index(self):
        cfg = ChartConfig(label="X", color=8)
        assert cfg.color == "hsl(var(--chart-8))"

    def test_string_color_unchanged(self):
        cfg = ChartConfig(label="X", color="#ff5500")
        assert cfg.color == "#ff5500"

    def test_string_hsl_unchanged(self):
        cfg = ChartConfig(label="X", color="hsl(var(--chart-3))")
        assert cfg.color == "hsl(var(--chart-3))"

    def test_none_color_stays_none(self):
        cfg = ChartConfig(label="X")
        assert cfg.color is None


class TestChartContainerNormalizeConfig:
    """ChartContainer accepts plain dict and str values in config."""

    def test_plain_dict_config(self):
        container = ChartContainer(
            config={"desktop": {"label": "Desktop", "color": "#ff5500"}}
        )
        cfg = container.config["desktop"]
        assert isinstance(cfg, ChartConfig)
        assert cfg.label == "Desktop"
        assert cfg.color == "#ff5500"

    def test_str_config(self):
        container = ChartContainer(config={"desktop": "Desktop Users"})
        cfg = container.config["desktop"]
        assert isinstance(cfg, ChartConfig)
        assert cfg.label == "Desktop Users"
        assert cfg.color is None

    def test_chartconfig_passthrough(self):
        orig = ChartConfig(label="Desktop", color=2)
        container = ChartContainer(config={"desktop": orig})
        assert container.config["desktop"] is orig


class TestChartContainerAutoConfig:
    """ChartContainer builds config automatically from series children."""

    def test_auto_color_assigned_by_order(self):
        data = [{"month": "Jan", "desktop": 100, "mobile": 50}]
        container = ChartContainer(
            children=AreaChart(
                data=data,
                children=[
                    Area(data_key="desktop", label="Desktop"),
                    Area(data_key="mobile", label="Mobile"),
                ],
            )
        )
        rendered = container.render()
        config = rendered["props"]["config"]
        assert config["desktop"]["color"] == "hsl(var(--chart-1))"
        assert config["mobile"]["color"] == "hsl(var(--chart-2))"
        assert config["desktop"]["label"] == "Desktop"
        assert config["mobile"]["label"] == "Mobile"

    def test_label_defaults_to_data_key(self):
        """Series without label falls back to data_key as label."""
        data = [{"month": "Jan", "revenue": 100}]
        container = ChartContainer(children=BarChart(data=data, children=[Bar(data_key="revenue")]))
        rendered = container.render()
        assert rendered["props"]["config"]["revenue"]["label"] == "revenue"

    def test_explicit_color_on_series(self):
        data = [{"month": "Jan", "revenue": 100}]
        container = ChartContainer(
            children=BarChart(data=data, children=[Bar(data_key="revenue", label="Revenue", color=3)])
        )
        rendered = container.render()
        assert rendered["props"]["config"]["revenue"]["color"] == "hsl(var(--chart-3))"

    def test_explicit_hex_color_on_series(self):
        data = [{"month": "Jan", "revenue": 100}]
        container = ChartContainer(
            children=BarChart(
                data=data, children=[Bar(data_key="revenue", label="Revenue", color="#abcdef")]
            )
        )
        rendered = container.render()
        assert rendered["props"]["config"]["revenue"]["color"] == "#abcdef"

    def test_explicit_config_overrides_auto(self):
        """Explicit config= takes precedence over series-derived config."""
        data = [{"month": "Jan", "desktop": 100}]
        explicit = ChartConfig(label="My Desktop", color="#123456")
        container = ChartContainer(
            config={"desktop": explicit},
            children=AreaChart(
                data=data, children=[Area(data_key="desktop", label="Desktop")]
            ),
        )
        rendered = container.render()
        cfg = rendered["props"]["config"]["desktop"]
        assert cfg["label"] == "My Desktop"
        assert cfg["color"] == "#123456"

    def test_auto_color_cycles_at_8(self):
        """Colors cycle through 8-palette slots."""
        data = [{"x": i} for i in range(10)]
        series = [Bar(data_key=f"s{i}", label=f"S{i}") for i in range(9)]
        container = ChartContainer(children=BarChart(data=data, children=series))
        rendered = container.render()
        config = rendered["props"]["config"]
        assert config["s0"]["color"] == "hsl(var(--chart-1))"
        assert config["s7"]["color"] == "hsl(var(--chart-8))"
        assert config["s8"]["color"] == "hsl(var(--chart-1))"  # wraps


class TestSeriesAutoFill:
    """Series components auto-derive fill/stroke from data_key."""

    def test_area_default_fill(self):
        area = Area(data_key="desktop")
        assert area.fill == "var(--color-desktop)"
        assert area.stroke == "var(--color-desktop)"

    def test_area_explicit_fill_respected(self):
        area = Area(data_key="desktop", fill="#ff0000")
        assert area.fill == "#ff0000"

    def test_bar_default_fill(self):
        bar = Bar(data_key="revenue")
        assert bar.fill == "var(--color-revenue)"

    def test_line_default_stroke(self):
        line = Line(data_key="orders")
        assert line.stroke == "var(--color-orders)"

    def test_radar_default_fill(self):
        radar = Radar(data_key="speed")
        assert radar.fill == "var(--color-speed)"
        assert radar.stroke == "var(--color-speed)"

    def test_scatter_default_fill_from_name(self):
        scatter = Scatter(name="Series A")
        assert scatter.series_key == "series_a"
        assert scatter.fill == "var(--color-series_a)"

    def test_scatter_series_key_normalized(self):
        scatter = Scatter(name="My-Series B")
        assert scatter.series_key == "my_series_b"


class TestAutoFillInData:
    """Pie, Funnel, RadialBarChart auto-inject fill into data items."""

    def test_pie_auto_fill(self):
        data = [{"browser": "chrome", "visitors": 100}, {"browser": "safari", "visitors": 80}]
        pie = Pie(data=data, data_key="visitors", name_key="browser")
        assert pie.data[0]["fill"] == "hsl(var(--chart-1))"
        assert pie.data[1]["fill"] == "hsl(var(--chart-2))"
        # original data not mutated
        assert "fill" not in data[0]

    def test_pie_respects_existing_fill(self):
        data = [{"browser": "chrome", "visitors": 100, "fill": "#custom"}]
        pie = Pie(data=data, data_key="visitors", name_key="browser")
        assert pie.data[0]["fill"] == "#custom"

    def test_funnel_auto_fill(self):
        data = [{"name": "Visit", "value": 1000}, {"name": "Cart", "value": 500}]
        funnel = Funnel(data=data, data_key="value")
        assert funnel.data[0]["fill"] == "hsl(var(--chart-1))"
        assert funnel.data[1]["fill"] == "hsl(var(--chart-2))"

    def test_radial_auto_fill(self):
        data = [{"activity": "a", "value": 50}, {"activity": "b", "value": 80}]
        chart = RadialBarChart(data=data, children=[RadialBar(data_key="value")])
        assert chart.data[0]["fill"] == "hsl(var(--chart-1))"
        assert chart.data[1]["fill"] == "hsl(var(--chart-2))"

    def test_radial_respects_existing_fill(self):
        data = [{"activity": "a", "value": 50, "fill": "red"}]
        chart = RadialBarChart(data=data, children=[RadialBar(data_key="value")])
        assert chart.data[0]["fill"] == "red"


class TestCartesianGrid:
    """Tests for CartesianGrid component."""

    def test_cartesian_grid_full_props(self):
        """Test CartesianGrid with all props."""
        grid = CartesianGrid(
            stroke_dasharray="3 3",
            vertical=True,
            horizontal=True,
            horizontal_fill=["#fff", "#f5f5f5"],
            vertical_fill=["#fff", "#f0f0f0"],
            fill="#fafafa",
            fill_opacity=0.5,
            stroke="#ccc",
            sync_with_ticks=True,
        )

        rendered = grid.render()
        assert rendered["props"]["stroke_dasharray"] == "3 3"
        assert rendered["props"]["horizontalFill"] == ["#fff", "#f5f5f5"]
        assert rendered["props"]["syncWithTicks"] is True


class TestBrush:
    """Tests for Brush component."""

    def test_brush_full_props(self):
        """Test Brush with all props."""
        cb = Callback(id="cb", func=lambda ctx: None)
        brush = Brush(
            data_key="name",
            height=40,
            stroke="#8884d8",
            traveller_width=10,
            gap=1,
            start_index=0,
            end_index=5,
            fill="#ddd",
            always_show_text=True,
            on_change=cb,
        )

        rendered = brush.render()
        assert rendered["props"]["height"] == 40
        assert rendered["props"]["travellerWidth"] == 10
        assert rendered["props"]["startIndex"] == 0
        assert rendered["props"]["endIndex"] == 5
        assert rendered["props"]["alwaysShowText"] is True
        assert rendered["props"]["on_change"] == cb.serialize()
