"""Tests for layout components."""

from refast.components.base import Text
from refast.components.shadcn.layout import (
    Center,
    Column,
    Divider,
    Flex,
    Grid,
    Row,
    Spacer,
    Stack,
)


class TestRow:
    """Tests for Row component."""

    def test_row_renders(self):
        """Test Row renders correctly."""
        row = Row(children=[Text("A"), Text("B")], gap=4)
        rendered = row.render()
        assert rendered["type"] == "Row"
        assert rendered["props"]["gap"] == 4
        assert len(rendered["children"]) == 2

    def test_row_justify(self):
        """Test Row justify prop."""
        row = Row(justify="between")
        rendered = row.render()
        assert rendered["props"]["justify"] == "between"

    def test_row_align(self):
        """Test Row align prop."""
        row = Row(align="center")
        rendered = row.render()
        assert rendered["props"]["align"] == "center"

    def test_row_wrap(self):
        """Test Row wrap prop."""
        row = Row(wrap=True)
        rendered = row.render()
        assert rendered["props"]["wrap"] is True


class TestColumn:
    """Tests for Column component."""

    def test_column_renders(self):
        """Test Column renders correctly."""
        col = Column(gap=2, justify="center")
        rendered = col.render()
        assert rendered["type"] == "Column"
        assert rendered["props"]["justify"] == "center"
        assert rendered["props"]["gap"] == 2

    def test_column_default_align(self):
        """Test Column default align is stretch."""
        col = Column()
        rendered = col.render()
        assert rendered["props"]["align"] == "stretch"


class TestStack:
    """Tests for Stack component."""

    def test_stack_renders(self):
        """Test Stack renders correctly."""
        stack = Stack(spacing=8, direction="horizontal")
        rendered = stack.render()
        assert rendered["type"] == "Stack"
        assert rendered["props"]["spacing"] == 8
        assert rendered["props"]["direction"] == "horizontal"

    def test_stack_default_vertical(self):
        """Test Stack defaults to vertical."""
        stack = Stack()
        rendered = stack.render()
        assert rendered["props"]["direction"] == "vertical"


class TestGrid:
    """Tests for Grid component."""

    def test_grid_renders(self):
        """Test Grid renders correctly."""
        grid = Grid(columns=3, gap=4)
        rendered = grid.render()
        assert rendered["type"] == "Grid"
        assert rendered["props"]["columns"] == 3
        assert rendered["props"]["gap"] == 4

    def test_grid_with_rows(self):
        """Test Grid with rows prop."""
        grid = Grid(columns=2, rows=3)
        rendered = grid.render()
        assert rendered["props"]["rows"] == 3


class TestFlex:
    """Tests for Flex component."""

    def test_flex_renders(self):
        """Test Flex renders correctly."""
        flex = Flex(direction="column", justify="center", align="start")
        rendered = flex.render()
        assert rendered["type"] == "Flex"
        assert rendered["props"]["direction"] == "column"
        assert rendered["props"]["justify"] == "center"
        assert rendered["props"]["align"] == "start"

    def test_flex_wrap(self):
        """Test Flex wrap prop."""
        flex = Flex(wrap="wrap")
        rendered = flex.render()
        assert rendered["props"]["wrap"] == "wrap"


class TestCenter:
    """Tests for Center component."""

    def test_center_renders(self):
        """Test Center renders correctly."""
        center = Center(children=[Text("Centered")])
        rendered = center.render()
        assert rendered["type"] == "Center"
        assert len(rendered["children"]) == 1


class TestSpacer:
    """Tests for Spacer component."""

    def test_spacer_renders(self):
        """Test Spacer renders correctly."""
        spacer = Spacer(size=20)
        rendered = spacer.render()
        assert rendered["type"] == "Spacer"
        assert rendered["props"]["size"] == 20

    def test_spacer_no_children(self):
        """Test Spacer has no children."""
        spacer = Spacer()
        rendered = spacer.render()
        assert rendered["children"] == []


class TestDivider:
    """Tests for Divider component."""

    def test_divider_renders(self):
        """Test Divider renders correctly."""
        divider = Divider()
        rendered = divider.render()
        assert rendered["type"] == "Divider"
        assert rendered["props"]["orientation"] == "horizontal"

    def test_divider_vertical(self):
        """Test Divider vertical orientation."""
        divider = Divider(orientation="vertical")
        rendered = divider.render()
        assert rendered["props"]["orientation"] == "vertical"



