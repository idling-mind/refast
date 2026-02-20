"""Tests for control components (Stage 9)."""

from refast.components.shadcn.controls import (
    Calendar,
    DatePicker,
    Slider,
    Switch,
    Toggle,
    ToggleGroup,
    ToggleGroupItem,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestSwitch:
    """Tests for Switch component."""

    def test_switch_renders(self):
        """Test Switch renders correctly."""
        switch = Switch(name="notifications")
        rendered = switch.render()
        assert rendered["type"] == "Switch"
        assert rendered["props"]["name"] == "notifications"

    def test_switch_with_checked(self):
        """Test Switch with checked state."""
        switch = Switch(name="dark_mode", checked=True)
        rendered = switch.render()
        assert rendered["props"]["checked"] is True

    def test_switch_disabled(self):
        """Test Switch disabled state."""
        switch = Switch(name="test", disabled=True)
        rendered = switch.render()
        assert rendered["props"]["disabled"] is True

    def test_switch_with_label(self):
        """Test Switch with checked and name."""
        switch = Switch(name="dark_mode", checked=True)
        rendered = switch.render()
        assert rendered["props"]["name"] == "dark_mode"
        assert rendered["props"]["checked"] is True

    def test_switch_with_callback(self):
        """Test Switch with on_change callback."""
        cb = MockCallback()
        switch = Switch(name="test", on_change=cb)
        rendered = switch.render()
        assert rendered["props"]["on_checked_change"] == {"callbackId": "cb-123"}


class TestSlider:
    """Tests for Slider component."""

    def test_slider_renders(self):
        """Test Slider renders correctly."""
        slider = Slider(name="volume")
        rendered = slider.render()
        assert rendered["type"] == "Slider"
        assert rendered["props"]["name"] == "volume"

    def test_slider_with_range(self):
        """Test Slider with min/max values."""
        slider = Slider(name="brightness", min=0, max=255, step=5)
        rendered = slider.render()
        assert rendered["props"]["min"] == 0
        assert rendered["props"]["max"] == 255
        assert rendered["props"]["step"] == 5

    def test_slider_with_value(self):
        """Test Slider with initial value."""
        slider = Slider(name="test", value=[50])
        rendered = slider.render()
        assert rendered["props"]["value"] == [50]

    def test_slider_disabled(self):
        """Test Slider disabled state."""
        slider = Slider(name="test", disabled=True)
        rendered = slider.render()
        assert rendered["props"]["disabled"] is True

    def test_slider_orientation(self):
        """Test Slider orientation."""
        slider = Slider(name="test", orientation="vertical")
        rendered = slider.render()
        assert rendered["props"]["orientation"] == "vertical"

    def test_slider_with_callback(self):
        """Test Slider with onValueChange callback."""
        cb = MockCallback()
        slider = Slider(name="test", on_value_change=cb)
        rendered = slider.render()
        assert rendered["props"]["on_value_change"] == {"callbackId": "cb-123"}


class TestToggle:
    """Tests for Toggle component."""

    def test_toggle_renders(self):
        """Test Toggle renders correctly."""
        toggle = Toggle(label="Bold")
        rendered = toggle.render()
        assert rendered["type"] == "Toggle"
        assert rendered["props"]["label"] == "Bold"

    def test_toggle_pressed(self):
        """Test Toggle pressed state."""
        toggle = Toggle(label="Italic", pressed=True)
        rendered = toggle.render()
        assert rendered["props"]["pressed"] is True

    def test_toggle_disabled(self):
        """Test Toggle disabled state."""
        toggle = Toggle(label="Test", disabled=True)
        rendered = toggle.render()
        assert rendered["props"]["disabled"] is True

    def test_toggle_variant(self):
        """Test Toggle variants."""
        toggle = Toggle(label="Test", variant="outline")
        rendered = toggle.render()
        assert rendered["props"]["variant"] == "outline"

    def test_toggle_size(self):
        """Test Toggle sizes."""
        toggle = Toggle(label="Test", size="sm")
        rendered = toggle.render()
        assert rendered["props"]["size"] == "sm"

    def test_toggle_with_callback(self):
        """Test Toggle with onPressedChange callback."""
        cb = MockCallback()
        toggle = Toggle(label="Test", on_pressed_change=cb)
        rendered = toggle.render()
        assert rendered["props"]["on_pressed_change"] == {"callbackId": "cb-123"}


class TestToggleGroup:
    """Tests for ToggleGroup component."""

    def test_toggle_group_renders(self):
        """Test ToggleGroup renders correctly."""
        group = ToggleGroup(type="single")
        rendered = group.render()
        assert rendered["type"] == "ToggleGroup"
        assert rendered["props"]["type"] == "single"

    def test_toggle_group_multiple(self):
        """Test ToggleGroup with multiple selection."""
        group = ToggleGroup(type="multiple")
        rendered = group.render()
        assert rendered["props"]["type"] == "multiple"

    def test_toggle_group_with_children(self):
        """Test ToggleGroup with ToggleGroupItem children."""
        item1 = ToggleGroupItem(value="left", label="Left")
        item2 = ToggleGroupItem(value="center", label="Center")
        group = ToggleGroup(type="single", children=[item1, item2])
        rendered = group.render()
        assert len(rendered["children"]) == 2

    def test_toggle_group_default_value(self):
        """Test ToggleGroup with default value."""
        group = ToggleGroup(type="single", default_value="center")
        rendered = group.render()
        assert rendered["props"]["default_value"] == "center"


class TestToggleGroupItem:
    """Tests for ToggleGroupItem component."""

    def test_toggle_group_item_renders(self):
        """Test ToggleGroupItem renders correctly."""
        item = ToggleGroupItem(value="bold", label="B")
        rendered = item.render()
        assert rendered["type"] == "ToggleGroupItem"
        assert rendered["props"]["value"] == "bold"
        assert rendered["props"]["label"] == "B"

    def test_toggle_group_item_disabled(self):
        """Test ToggleGroupItem disabled state."""
        item = ToggleGroupItem(value="test", label="T", disabled=True)
        rendered = item.render()
        assert rendered["props"]["disabled"] is True


class TestDatePicker:
    """Tests for DatePicker component."""

    def test_date_picker_renders(self):
        """Test DatePicker renders correctly."""
        picker = DatePicker(name="birthday")
        rendered = picker.render()
        assert rendered["type"] == "DatePicker"
        assert rendered["props"]["name"] == "birthday"

    def test_date_picker_with_value(self):
        """Test DatePicker with value."""
        picker = DatePicker(name="test", value="2024-01-15")
        rendered = picker.render()
        assert rendered["props"]["value"] == "2024-01-15"

    def test_date_picker_placeholder(self):
        """Test DatePicker with placeholder."""
        picker = DatePicker(name="test", placeholder="Select date")
        rendered = picker.render()
        assert rendered["props"]["placeholder"] == "Select date"

    def test_date_picker_disabled(self):
        """Test DatePicker disabled state."""
        picker = DatePicker(name="test", disabled=True)
        rendered = picker.render()
        assert rendered["props"]["disabled"] is True

    def test_date_picker_format(self):
        """Test DatePicker with custom format."""
        picker = DatePicker(name="test", format="dd/MM/yyyy")
        rendered = picker.render()
        assert rendered["props"]["format"] == "dd/MM/yyyy"

    def test_date_picker_with_callback(self):
        """Test DatePicker with onChange callback."""
        cb = MockCallback()
        picker = DatePicker(name="test", on_change=cb)
        rendered = picker.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}

    def test_date_picker_mode_multiple(self):
        """Test DatePicker in multiple mode."""
        picker = DatePicker(name="test", mode="multiple")
        rendered = picker.render()
        assert rendered["props"]["mode"] == "multiple"

    def test_date_picker_with_multiple_values(self):
        """Test DatePicker serializes multiple selected dates."""
        picker = DatePicker(name="test", mode="multiple", value=["2026-02-17", "2026-02-25"])
        rendered = picker.render()
        assert rendered["props"]["value"] == ["2026-02-17", "2026-02-25"]


class TestCalendar:
    """Tests for Calendar component."""

    def test_calendar_renders(self):
        """Test Calendar renders correctly."""
        calendar = Calendar()
        rendered = calendar.render()
        assert rendered["type"] == "Calendar"

    def test_calendar_mode_single(self):
        """Test Calendar in single selection mode."""
        calendar = Calendar(mode="single")
        rendered = calendar.render()
        assert rendered["props"]["mode"] == "single"

    def test_calendar_mode_multiple(self):
        """Test Calendar in multiple selection mode."""
        calendar = Calendar(mode="multiple")
        rendered = calendar.render()
        assert rendered["props"]["mode"] == "multiple"

    def test_calendar_mode_range(self):
        """Test Calendar in range selection mode."""
        calendar = Calendar(mode="range")
        rendered = calendar.render()
        assert rendered["props"]["mode"] == "range"

    def test_calendar_disabled(self):
        """Test Calendar disabled state."""
        calendar = Calendar(disabled=True)
        rendered = calendar.render()
        assert rendered["props"]["disabled"] is True

    def test_calendar_show_outside_days(self):
        """Test Calendar showing outside days."""
        calendar = Calendar(show_outside_days=True)
        rendered = calendar.render()
        assert rendered["props"]["show_outside_days"] is True

    def test_calendar_with_callback(self):
        """Test Calendar with onSelect callback."""
        cb = MockCallback()
        calendar = Calendar(on_select=cb)
        rendered = calendar.render()
        assert rendered["props"]["on_select"] == {"callbackId": "cb-123"}
