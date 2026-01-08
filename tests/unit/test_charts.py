"""Tests for chart components."""

from refast.components.shadcn.charts import (
    Area,
    AreaChart,
    Bar,
    BarChart,
    Brush,
    CartesianGrid,
    Cell,
    ChartConfig,
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
    PolarAngleAxis,
    PolarGrid,
    PolarRadiusAxis,
    Radar,
    RadarChart,
    RadialBar,
    RadialBarChart,
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
from refast.events.types import Callback


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
    assert props["minHeight"] == 100
    assert props["minWidth"] == 50
    assert props["maxHeight"] == 600
    assert props["aspect"] == 2.0
    assert props["debounce"] == 100
    assert props["initialDimension"] == {"width": 400, "height": 200}
    assert props["onResize"] == cb.serialize()
    assert props["className"] == "my-chart"


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
        assert rendered["props"]["onClick"] == cb.serialize()
        assert rendered["props"]["onMouseEnter"] == cb.serialize()

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
        assert rendered["props"]["dataKey"] == "value"
        assert rendered["props"]["type"] == "monotone"
        assert rendered["props"]["connectNulls"] is True
        assert rendered["props"]["legendType"] == "circle"
        assert rendered["props"]["name"] == "Test Area"
        assert rendered["props"]["xAxisId"] == "x1"
        assert rendered["props"]["yAxisId"] == "y1"
        assert rendered["props"]["animationDuration"] == 1000


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
        assert rendered["props"]["xAxisId"] == "x1"
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
        assert rendered["props"]["onClick"] == cb.serialize()
        assert rendered["props"]["onMouseMove"] == cb.serialize()

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
        assert rendered["props"]["strokeWidth"] == 3
        assert rendered["props"]["connectNulls"] is True
        assert rendered["props"]["strokeDasharray"] == "5 5"


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
        assert rendered["props"]["onClick"] == cb.serialize()
        assert rendered["props"]["onMouseEnter"] == cb.serialize()

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
        assert rendered["props"]["startAngle"] == 90
        assert rendered["props"]["endAngle"] == -270
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
        assert rendered["props"]["onClick"] == cb.serialize()

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
        assert rendered["props"]["xAxisId"] == "x1"
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
        assert rendered["props"]["barCategoryGap"] == "20%"

    def test_composed_chart_with_children(self):
        """Test ComposedChart with children."""
        data = [{"name": "A", "bar": 100, "line": 50}]
        chart = ComposedChart(
            Bar(data_key="bar"),
            Line(data_key="line"),
            data=data,
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
        assert rendered["props"]["data"] == data
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
        assert rendered["props"]["onClick"] == cb.serialize()


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
        assert rendered["props"]["xAxisId"] == "x1"
        assert rendered["props"]["allowDecimals"] is False
        assert rendered["props"]["allowDataOverflow"] is True
        assert rendered["props"]["tickCount"] == 5
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
        assert rendered["props"]["yAxisId"] == "y1"
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
        assert rendered["props"]["strokeWidth"] == 2
        assert rendered["props"]["xAxisId"] == "x1"
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
        assert rendered["props"]["fillOpacity"] == 0.3

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
        assert rendered["props"]["dataKey"] == "error"
        assert rendered["props"]["direction"] == "y"


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
        assert rendered["props"]["strokeDasharray"] == "3 3"
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
        assert rendered["props"]["onChange"] == cb.serialize()
