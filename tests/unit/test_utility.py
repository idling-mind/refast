"""Tests for utility components (Stage 9)."""

from refast.components.shadcn.utility import (
    AspectRatio,
    Carousel,
    CarouselItem,
    Collapsible,
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
    ScrollArea,
    Separator,
    ThemeSwitcher,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestSeparator:
    """Tests for Separator component."""

    def test_separator_renders(self):
        """Test Separator renders correctly."""
        sep = Separator()
        rendered = sep.render()
        assert rendered["type"] == "Separator"

    def test_separator_horizontal(self):
        """Test horizontal separator (default)."""
        sep = Separator(orientation="horizontal")
        rendered = sep.render()
        assert rendered["props"]["orientation"] == "horizontal"

    def test_separator_vertical(self):
        """Test vertical separator."""
        sep = Separator(orientation="vertical")
        rendered = sep.render()
        assert rendered["props"]["orientation"] == "vertical"

    def test_separator_decorative(self):
        """Test decorative separator."""
        sep = Separator(decorative=True)
        rendered = sep.render()
        assert rendered["props"]["decorative"] is True


class TestAspectRatio:
    """Tests for AspectRatio component."""

    def test_aspect_ratio_renders(self):
        """Test AspectRatio renders correctly."""
        ratio = AspectRatio()
        rendered = ratio.render()
        assert rendered["type"] == "AspectRatio"

    def test_aspect_ratio_16_9(self):
        """Test AspectRatio with 16:9."""
        ratio = AspectRatio(ratio=16 / 9)
        rendered = ratio.render()
        assert abs(rendered["props"]["ratio"] - (16 / 9)) < 0.001

    def test_aspect_ratio_4_3(self):
        """Test AspectRatio with 4:3."""
        ratio = AspectRatio(ratio=4 / 3)
        rendered = ratio.render()
        assert abs(rendered["props"]["ratio"] - (4 / 3)) < 0.001

    def test_aspect_ratio_1_1(self):
        """Test AspectRatio with 1:1 (square)."""
        ratio = AspectRatio(ratio=1)
        rendered = ratio.render()
        assert rendered["props"]["ratio"] == 1


class TestScrollArea:
    """Tests for ScrollArea component."""

    def test_scroll_area_renders(self):
        """Test ScrollArea renders correctly."""
        area = ScrollArea()
        rendered = area.render()
        assert rendered["type"] == "ScrollArea"

    def test_scroll_area_type_auto(self):
        """Test ScrollArea with auto scrollbar."""
        area = ScrollArea(type="auto")
        rendered = area.render()
        assert rendered["props"]["type"] == "auto"

    def test_scroll_area_type_always(self):
        """Test ScrollArea with always visible scrollbar."""
        area = ScrollArea(type="always")
        rendered = area.render()
        assert rendered["props"]["type"] == "always"

    def test_scroll_area_type_hover(self):
        """Test ScrollArea with scrollbar on hover."""
        area = ScrollArea(type="hover")
        rendered = area.render()
        assert rendered["props"]["type"] == "hover"

    def test_scroll_area_hide_delay(self):
        """Test ScrollArea with custom hide delay."""
        area = ScrollArea(scroll_hide_delay=1000)
        rendered = area.render()
        assert rendered["props"]["scroll_hide_delay"] == 1000


class TestCollapsible:
    """Tests for Collapsible component."""

    def test_collapsible_renders(self):
        """Test Collapsible renders correctly."""
        collapse = Collapsible()
        rendered = collapse.render()
        assert rendered["type"] == "Collapsible"

    def test_collapsible_open_state(self):
        """Test Collapsible open state."""
        collapse = Collapsible(open=True)
        rendered = collapse.render()
        assert rendered["props"]["open"] is True

    def test_collapsible_default_open(self):
        """Test Collapsible default open state."""
        collapse = Collapsible(default_open=True)
        rendered = collapse.render()
        assert rendered["props"]["default_open"] is True

    def test_collapsible_disabled(self):
        """Test Collapsible disabled state."""
        collapse = Collapsible(disabled=True)
        rendered = collapse.render()
        assert rendered["props"]["disabled"] is True

    def test_collapsible_with_callback(self):
        """Test Collapsible with onOpenChange callback."""
        cb = MockCallback()
        collapse = Collapsible(on_open_change=cb)
        rendered = collapse.render()
        assert rendered["props"]["on_open_change"] == {"callbackId": "cb-123"}


class TestCarousel:
    """Tests for Carousel component."""

    def test_carousel_renders(self):
        """Test Carousel renders correctly."""
        carousel = Carousel()
        rendered = carousel.render()
        assert rendered["type"] == "Carousel"

    def test_carousel_orientation(self):
        """Test Carousel orientation."""
        carousel = Carousel(orientation="vertical")
        rendered = carousel.render()
        assert rendered["props"]["orientation"] == "vertical"

    def test_carousel_loop(self):
        """Test Carousel with loop enabled."""
        carousel = Carousel(loop=True)
        rendered = carousel.render()
        assert rendered["props"]["loop"] is True

    def test_carousel_with_items(self):
        """Test Carousel with CarouselItems."""
        item1 = CarouselItem()
        item2 = CarouselItem()
        carousel = Carousel(children=[item1, item2])
        rendered = carousel.render()
        assert len(rendered["children"]) == 2


class TestCarouselItem:
    """Tests for CarouselItem component."""

    def test_carousel_item_renders(self):
        """Test CarouselItem renders correctly."""
        item = CarouselItem()
        rendered = item.render()
        assert rendered["type"] == "CarouselItem"


class TestResizablePanelGroup:
    """Tests for ResizablePanelGroup component."""

    def test_resizable_panel_group_renders(self):
        """Test ResizablePanelGroup renders correctly."""
        group = ResizablePanelGroup()
        rendered = group.render()
        assert rendered["type"] == "ResizablePanelGroup"

    def test_resizable_panel_group_direction_horizontal(self):
        """Test ResizablePanelGroup horizontal direction."""
        group = ResizablePanelGroup(direction="horizontal")
        rendered = group.render()
        assert rendered["props"]["direction"] == "horizontal"

    def test_resizable_panel_group_direction_vertical(self):
        """Test ResizablePanelGroup vertical direction."""
        group = ResizablePanelGroup(direction="vertical")
        rendered = group.render()
        assert rendered["props"]["direction"] == "vertical"


class TestResizablePanel:
    """Tests for ResizablePanel component."""

    def test_resizable_panel_renders(self):
        """Test ResizablePanel renders correctly."""
        panel = ResizablePanel()
        rendered = panel.render()
        assert rendered["type"] == "ResizablePanel"

    def test_resizable_panel_default_size(self):
        """Test ResizablePanel with default size."""
        panel = ResizablePanel(default_size=30)
        rendered = panel.render()
        assert rendered["props"]["default_size"] == 30

    def test_resizable_panel_min_max_size(self):
        """Test ResizablePanel with min/max size."""
        panel = ResizablePanel(min_size=10, max_size=80)
        rendered = panel.render()
        assert rendered["props"]["min_size"] == 10
        assert rendered["props"]["max_size"] == 80


class TestResizableHandle:
    """Tests for ResizableHandle component."""

    def test_resizable_handle_renders(self):
        """Test ResizableHandle renders correctly."""
        handle = ResizableHandle()
        rendered = handle.render()
        assert rendered["type"] == "ResizableHandle"

    def test_resizable_handle_with_handle_visual(self):
        """Test ResizableHandle with visual handle."""
        handle = ResizableHandle(with_handle=True)
        rendered = handle.render()
        assert rendered["props"]["with_handle"] is True


class TestThemeSwitcher:
    """Tests for ThemeSwitcher component."""

    def test_theme_switcher_renders(self):
        """Test ThemeSwitcher renders correctly."""
        switcher = ThemeSwitcher()
        rendered = switcher.render()
        assert rendered["type"] == "ThemeSwitcher"

    def test_theme_switcher_default_theme_system(self):
        """Test ThemeSwitcher with default system theme."""
        switcher = ThemeSwitcher()
        rendered = switcher.render()
        assert rendered["props"]["default_theme"] == "system"

    def test_theme_switcher_default_theme_light(self):
        """Test ThemeSwitcher with light default theme."""
        switcher = ThemeSwitcher(default_theme="light")
        rendered = switcher.render()
        assert rendered["props"]["default_theme"] == "light"

    def test_theme_switcher_default_theme_dark(self):
        """Test ThemeSwitcher with dark default theme."""
        switcher = ThemeSwitcher(default_theme="dark")
        rendered = switcher.render()
        assert rendered["props"]["default_theme"] == "dark"

    def test_theme_switcher_storage_key(self):
        """Test ThemeSwitcher with custom storage key."""
        switcher = ThemeSwitcher(storage_key="my-app-theme")
        rendered = switcher.render()
        assert rendered["props"]["storage_key"] == "my-app-theme"

    def test_theme_switcher_toggle_mode(self):
        """Test ThemeSwitcher in toggle mode."""
        switcher = ThemeSwitcher(mode="toggle")
        rendered = switcher.render()
        assert rendered["props"]["mode"] == "toggle"

    def test_theme_switcher_dropdown_mode(self):
        """Test ThemeSwitcher in dropdown mode."""
        switcher = ThemeSwitcher(mode="dropdown")
        rendered = switcher.render()
        assert rendered["props"]["mode"] == "dropdown"

    def test_theme_switcher_show_system_option(self):
        """Test ThemeSwitcher with show_system_option."""
        switcher = ThemeSwitcher(show_system_option=False)
        rendered = switcher.render()
        assert rendered["props"]["show_system_option"] is False

    def test_theme_switcher_with_callback(self):
        """Test ThemeSwitcher with on_change callback."""
        cb = MockCallback()
        switcher = ThemeSwitcher(on_change=cb)
        rendered = switcher.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}

    def test_theme_switcher_class_name(self):
        """Test ThemeSwitcher with custom class name."""
        switcher = ThemeSwitcher(class_name="my-theme-switcher")
        rendered = switcher.render()
        assert rendered["props"]["class_name"] == "my-theme-switcher"

    def test_theme_switcher_with_id(self):
        """Test ThemeSwitcher with custom id."""
        switcher = ThemeSwitcher(id="theme-toggle")
        rendered = switcher.render()
        assert rendered["id"] == "theme-toggle"
