"""Tests for data display components."""

from refast.components.base import Text
from refast.components.shadcn.data_display import (
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
    Avatar,
    Badge,
    DataTable,
    List,
    TabItem,
    Table,
    TableBody,
    TableHeader,
    Tabs,
    Tooltip,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestTable:
    """Tests for Table component."""

    def test_table_renders(self):
        """Test Table renders correctly."""
        children = [TableHeader(children=["Head"]), TableBody(children=["Body"])]
        table = Table(children=children)
        rendered = table.render()
        assert rendered["type"] == "Table"
        assert len(rendered["children"]) == 2
        assert rendered["children"][0]["type"] == "TableHeader"

    def test_table_striped(self):
        """Test Table striped prop."""
        table = Table(children=[], striped=True)
        rendered = table.render()
        assert rendered["props"]["striped"] is True

    def test_table_hoverable(self):
        """Test Table hoverable prop."""
        table = Table(children=[], hoverable=False)
        rendered = table.render()
        assert rendered["props"]["hoverable"] is False


class TestDataTable:
    """Tests for DataTable component."""

    def test_data_table_renders(self):
        """Test DataTable renders correctly."""
        dt = DataTable(columns=[], data=[], page_size=20)
        rendered = dt.render()
        assert rendered["type"] == "DataTable"
        assert rendered["props"]["pageSize"] == 20

    def test_data_table_features(self):
        """Test DataTable feature flags."""
        dt = DataTable(
            columns=[],
            data=[],
            sortable=False,
            filterable=False,
            paginated=False,
        )
        rendered = dt.render()
        assert rendered["props"]["sortable"] is False
        assert rendered["props"]["filterable"] is False
        assert rendered["props"]["paginated"] is False

    def test_data_table_with_callback(self):
        """Test DataTable with on_row_click callback."""
        cb = MockCallback()
        dt = DataTable(columns=[], data=[], on_row_click=cb)
        rendered = dt.render()
        assert rendered["props"]["onRowClick"] == {"callbackId": "cb-123"}


class TestList:
    """Tests for List component."""

    def test_list_renders(self):
        """Test List renders correctly."""
        lst = List(children=[Text("Item 1"), Text("Item 2")])
        rendered = lst.render()
        assert rendered["type"] == "List"
        assert len(rendered["children"]) == 2

    def test_list_ordered(self):
        """Test List ordered prop."""
        lst = List(ordered=True)
        rendered = lst.render()
        assert rendered["props"]["ordered"] is True


class TestBadge:
    """Tests for Badge component."""

    def test_badge_renders(self):
        """Test Badge renders correctly."""
        badge = Badge(children=["New"])
        rendered = badge.render()
        assert rendered["type"] == "Badge"
        assert rendered["children"] == ["New"]

    def test_badge_variant(self):
        """Test Badge variant prop."""
        badge = Badge(children=["Error"], variant="destructive")
        rendered = badge.render()
        assert rendered["props"]["variant"] == "destructive"


class TestAvatar:
    """Tests for Avatar component."""

    def test_avatar_renders(self):
        """Test Avatar renders correctly."""
        avatar = Avatar(src="/image.jpg", alt="User")
        rendered = avatar.render()
        assert rendered["type"] == "Avatar"
        assert rendered["props"]["src"] == "/image.jpg"
        assert rendered["props"]["alt"] == "User"

    def test_avatar_fallback(self):
        """Test Avatar fallback prop."""
        avatar = Avatar(fallback="JD")
        rendered = avatar.render()
        assert rendered["props"]["fallback"] == "JD"

    def test_avatar_size(self):
        """Test Avatar size prop."""
        avatar = Avatar(size="lg")
        rendered = avatar.render()
        assert rendered["props"]["size"] == "lg"


class TestTooltip:
    """Tests for Tooltip component."""

    def test_tooltip_renders(self):
        """Test Tooltip renders correctly."""
        tooltip = Tooltip(content="Help text", children=[Text("Hover me")])
        rendered = tooltip.render()
        assert rendered["type"] == "Tooltip"
        assert rendered["props"]["content"] == "Help text"

    def test_tooltip_side(self):
        """Test Tooltip side prop."""
        tooltip = Tooltip(content="Text", side="bottom")
        rendered = tooltip.render()
        assert rendered["props"]["side"] == "bottom"


class TestTabs:
    """Tests for Tabs component."""

    def test_tabs_renders(self):
        """Test Tabs renders correctly."""
        tabs = Tabs(default_value="tab1")
        rendered = tabs.render()
        assert rendered["type"] == "Tabs"
        assert rendered["props"]["defaultValue"] == "tab1"

    def test_tabs_controlled(self):
        """Test Tabs controlled mode."""
        cb = MockCallback()
        tabs = Tabs(value="tab2", on_value_change=cb)
        rendered = tabs.render()
        assert rendered["props"]["value"] == "tab2"
        assert rendered["props"]["onValueChange"] == {"callbackId": "cb-123"}


class TestTabItem:
    """Tests for TabItem component."""

    def test_tab_item_renders(self):
        """Test TabItem renders correctly."""
        item = TabItem(value="tab1", label="Tab 1", children=[Text("Content")])
        rendered = item.render()
        assert rendered["type"] == "TabItem"
        assert rendered["props"]["value"] == "tab1"
        assert rendered["props"]["label"] == "Tab 1"

    def test_tab_item_disabled(self):
        """Test TabItem disabled prop."""
        item = TabItem(value="tab1", label="Tab 1", disabled=True)
        rendered = item.render()
        assert rendered["props"]["disabled"] is True


class TestAccordion:
    """Tests for Accordion component."""

    def test_accordion_renders(self):
        """Test Accordion renders correctly."""
        children = [
            AccordionItem(
                value="item-1",
                children=[
                    AccordionTrigger(children=["Trigger"]),
                    AccordionContent(children=["Content"]),
                ],
            )
        ]
        accordion = Accordion(children=children)
        rendered = accordion.render()
        assert rendered["type"] == "Accordion"
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["type"] == "AccordionItem"

    def test_accordion_type(self):
        """Test Accordion type prop."""
        accordion = Accordion(children=[], type="multiple")
        rendered = accordion.render()
        assert rendered["props"]["type"] == "multiple"

    def test_accordion_collapsible(self):
        """Test Accordion collapsible prop."""
        accordion = Accordion(children=[], collapsible=False)
        rendered = accordion.render()
        assert rendered["props"]["collapsible"] is False

    def test_accordion_default_value(self):
        """Test Accordion defaultValue prop."""
        accordion = Accordion(children=[], default_value="section-1")
        rendered = accordion.render()
        assert rendered["props"]["defaultValue"] == "section-1"
