"""Tests for navigation components (Stage 9)."""

from refast.components.shadcn.navigation import (
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbSeparator,
    Command,
    CommandInput,
    CommandItem,
    Menubar,
    MenubarItem,
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestBreadcrumb:
    """Tests for Breadcrumb component."""

    def test_breadcrumb_renders(self):
        """Test Breadcrumb renders correctly."""
        breadcrumb = Breadcrumb()
        rendered = breadcrumb.render()
        assert rendered["type"] == "Breadcrumb"

    def test_breadcrumb_with_separator(self):
        """Test Breadcrumb with custom separator."""
        breadcrumb = Breadcrumb(separator=">")
        rendered = breadcrumb.render()
        assert rendered["props"]["separator"] == ">"

    def test_breadcrumb_with_children(self):
        """Test Breadcrumb with BreadcrumbItem children."""
        item1 = BreadcrumbItem(children=[BreadcrumbLink(label="Home", href="/")])
        item2 = BreadcrumbItem(children=[BreadcrumbLink(label="Products", href="/products")])
        breadcrumb = Breadcrumb(children=[item1, item2])
        rendered = breadcrumb.render()
        assert len(rendered["children"]) == 2


class TestBreadcrumbItem:
    """Tests for BreadcrumbItem component."""

    def test_breadcrumb_item_renders(self):
        """Test BreadcrumbItem renders correctly."""
        item = BreadcrumbItem()
        rendered = item.render()
        assert rendered["type"] == "BreadcrumbItem"


class TestBreadcrumbLink:
    """Tests for BreadcrumbLink component."""

    def test_breadcrumb_link_renders(self):
        """Test BreadcrumbLink renders correctly."""
        link = BreadcrumbLink(label="Home", href="/")
        rendered = link.render()
        assert rendered["type"] == "BreadcrumbLink"
        assert rendered["children"] == ["Home"]
        assert rendered["props"]["href"] == "/"

    def test_breadcrumb_link_current(self):
        """Test BreadcrumbLink as current page."""
        link = BreadcrumbLink(label="Products", current=True)
        rendered = link.render()
        assert rendered["props"]["current"] is True


class TestBreadcrumbSeparator:
    """Tests for BreadcrumbSeparator component."""

    def test_breadcrumb_separator_renders(self):
        """Test BreadcrumbSeparator renders correctly."""
        sep = BreadcrumbSeparator()
        rendered = sep.render()
        assert rendered["type"] == "BreadcrumbSeparator"


class TestNavigationMenu:
    """Tests for NavigationMenu component."""

    def test_navigation_menu_renders(self):
        """Test NavigationMenu renders correctly."""
        menu = NavigationMenu()
        rendered = menu.render()
        assert rendered["type"] == "NavigationMenu"

    def test_navigation_menu_orientation(self):
        """Test NavigationMenu orientation."""
        menu = NavigationMenu(orientation="vertical")
        rendered = menu.render()
        assert rendered["props"]["orientation"] == "vertical"

    def test_navigation_menu_with_items(self):
        """Test NavigationMenu with items."""
        item1 = NavigationMenuItem(label="Home")
        item2 = NavigationMenuItem(label="About")
        menu = NavigationMenu(children=[item1, item2])
        rendered = menu.render()
        assert len(rendered["children"]) == 2


class TestNavigationMenuItem:
    """Tests for NavigationMenuItem component."""

    def test_navigation_menu_item_renders(self):
        """Test NavigationMenuItem renders correctly."""
        item = NavigationMenuItem(label="Products")
        rendered = item.render()
        assert rendered["type"] == "NavigationMenuItem"
        assert rendered["props"]["label"] == "Products"


class TestNavigationMenuLink:
    """Tests for NavigationMenuLink component."""

    def test_navigation_menu_link_renders(self):
        """Test NavigationMenuLink renders correctly."""
        link = NavigationMenuLink(href="/about", label="About")
        rendered = link.render()
        assert rendered["type"] == "NavigationMenuLink"
        assert rendered["props"]["href"] == "/about"
        assert rendered["children"] == ["About"]

    def test_navigation_menu_link_active(self):
        """Test NavigationMenuLink active state."""
        link = NavigationMenuLink(href="/", label="Home", active=True)
        rendered = link.render()
        assert rendered["props"]["active"] is True


class TestMenubar:
    """Tests for Menubar component."""

    def test_menubar_renders(self):
        """Test Menubar renders correctly."""
        menubar = Menubar()
        rendered = menubar.render()
        assert rendered["type"] == "Menubar"

    def test_menubar_with_items(self):
        """Test Menubar with MenubarItems."""
        item1 = MenubarItem(label="File")
        item2 = MenubarItem(label="Edit")
        menubar = Menubar(children=[item1, item2])
        rendered = menubar.render()
        assert len(rendered["children"]) == 2


class TestMenubarItem:
    """Tests for MenubarItem component."""

    def test_menubar_item_renders(self):
        """Test MenubarItem renders correctly."""
        item = MenubarItem(label="File")
        rendered = item.render()
        assert rendered["type"] == "MenubarItem"
        assert rendered["children"][0] == "File"

    def test_menubar_item_disabled(self):
        """Test MenubarItem disabled state."""
        item = MenubarItem(label="Edit", disabled=True)
        rendered = item.render()
        assert rendered["props"]["disabled"] is True

    def test_menubar_item_with_callback(self):
        """Test MenubarItem with onSelect callback."""
        cb = MockCallback()
        item = MenubarItem(label="Save", on_select=cb)
        rendered = item.render()
        assert rendered["props"]["on_select"] == {"callbackId": "cb-123"}


class TestCommand:
    """Tests for Command component."""

    def test_command_renders(self):
        """Test Command renders correctly."""
        command = Command()
        rendered = command.render()
        assert rendered["type"] == "Command"

    def test_command_with_placeholder(self):
        """Test Command with placeholder."""
        command = Command(placeholder="Search...")
        rendered = command.render()
        assert rendered["props"]["placeholder"] == "Search..."


class TestCommandInput:
    """Tests for CommandInput component."""

    def test_command_input_renders(self):
        """Test CommandInput renders correctly."""
        input = CommandInput(placeholder="Type a command...")
        rendered = input.render()
        assert rendered["type"] == "CommandInput"
        assert rendered["props"]["placeholder"] == "Type a command..."


class TestCommandItem:
    """Tests for CommandItem component."""

    def test_command_item_renders(self):
        """Test CommandItem renders correctly."""
        item = CommandItem(value="settings", label="Settings")
        rendered = item.render()
        assert rendered["type"] == "CommandItem"
        assert rendered["props"]["value"] == "settings"
        assert rendered["children"][0] == "Settings"

    def test_command_item_disabled(self):
        """Test CommandItem disabled state."""
        item = CommandItem(value="locked", label="Locked", disabled=True)
        rendered = item.render()
        assert rendered["props"]["disabled"] is True

    def test_command_item_with_callback(self):
        """Test CommandItem with onSelect callback."""
        cb = MockCallback()
        item = CommandItem(value="action", label="Action", on_select=cb)
        rendered = item.render()
        assert rendered["props"]["on_select"] == {"callbackId": "cb-123"}



