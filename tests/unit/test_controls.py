"""Tests for control components (Stage 9)."""

from refast.components.shadcn.controls import (
    Calendar,
    Combobox,
    DatePicker,
    InputOTP,
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
        """Test Switch with on_checked_change callback."""
        cb = MockCallback()
        switch = Switch(name="test", on_checked_change=cb)
        rendered = switch.render()
        assert rendered["props"]["on_checked_change"] == {"callbackId": "cb-123"}


class TestSlider:
    """Tests for Slider component."""

    def test_slider_renders(self):
        """Test Slider renders correctly."""
        slider = Slider(label="volume")
        rendered = slider.render()
        assert rendered["type"] == "Slider"
        assert rendered["props"]["label"] == "volume"

    def test_slider_with_range(self):
        """Test Slider with min/max values."""
        slider = Slider(label="brightness", min=0, max=255, step=5)
        rendered = slider.render()
        assert rendered["props"]["min"] == 0
        assert rendered["props"]["max"] == 255
        assert rendered["props"]["step"] == 5

    def test_slider_with_value(self):
        """Test Slider with initial value."""
        slider = Slider(label="test", value=[50])
        rendered = slider.render()
        assert rendered["props"]["value"] == [50]

    def test_slider_disabled(self):
        """Test Slider disabled state."""
        slider = Slider(label="test", disabled=True)
        rendered = slider.render()
        assert rendered["props"]["disabled"] is True

    def test_slider_orientation(self):
        """Test Slider orientation."""
        slider = Slider(label="test", orientation="vertical")
        rendered = slider.render()
        assert rendered["props"]["orientation"] == "vertical"

    def test_slider_with_callback(self):
        """Test Slider with on_value_change callback."""
        cb = MockCallback()
        slider = Slider(label="test", on_value_change=cb)
        rendered = slider.render()
        assert rendered["props"]["on_value_change"] == {"callbackId": "cb-123"}

    def test_slider_show_value(self):
        """Test Slider show value option."""
        slider = Slider(label="test", show_value=True)
        rendered = slider.render()
        assert rendered["props"]["show_value"] is True

    def test_slider_with_name(self):
        """Test Slider with name argument."""
        slider = Slider(label="test", name="volume_slider")
        rendered = slider.render()
        assert rendered["props"]["name"] == "volume_slider"


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
        """Test Toggle with on_pressed_change callback."""
        cb = MockCallback()
        toggle = Toggle(label="Test", on_pressed_change=cb)
        rendered = toggle.render()
        assert rendered["props"]["on_pressed_change"] == {"callbackId": "cb-123"}

    def test_toggle_with_name(self):
        """Test Toggle with name argument."""
        toggle = Toggle(label="Test", name="toggle_bold")
        rendered = toggle.render()
        assert rendered["props"]["name"] == "toggle_bold"


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

    def test_toggle_group_with_name(self):
        """Test ToggleGroup with name argument."""
        group = ToggleGroup(type="single", name="alignment")
        rendered = group.render()
        assert rendered["props"]["name"] == "alignment"


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
        picker = DatePicker(label="birthday")
        rendered = picker.render()
        assert rendered["type"] == "DatePicker"
        assert rendered["props"]["label"] == "birthday"

    def test_date_picker_with_value(self):
        """Test DatePicker with value."""
        picker = DatePicker(label="test", value="2024-01-15")
        rendered = picker.render()
        assert rendered["props"]["value"] == "2024-01-15"

    def test_date_picker_placeholder(self):
        """Test DatePicker with placeholder."""
        picker = DatePicker(label="test", placeholder="Select date")
        rendered = picker.render()
        assert rendered["props"]["placeholder"] == "Select date"

    def test_date_picker_disabled(self):
        """Test DatePicker disabled state."""
        picker = DatePicker(label="test", disabled=True)
        rendered = picker.render()
        assert rendered["props"]["disabled"] is True

    def test_date_picker_format(self):
        """Test DatePicker with custom format."""
        picker = DatePicker(label="test", format="dd/MM/yyyy")
        rendered = picker.render()
        assert rendered["props"]["format"] == "dd/MM/yyyy"

    def test_date_picker_with_callback(self):
        """Test DatePicker with onChange callback."""
        cb = MockCallback()
        picker = DatePicker(label="test", on_change=cb)
        rendered = picker.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}

    def test_date_picker_mode_multiple(self):
        """Test DatePicker in multiple mode."""
        picker = DatePicker(label="test", mode="multiple")
        rendered = picker.render()
        assert rendered["props"]["mode"] == "multiple"

    def test_date_picker_with_multiple_values(self):
        """Test DatePicker serializes multiple selected dates."""
        picker = DatePicker(label="test", mode="multiple", value=["2026-02-17", "2026-02-25"])
        rendered = picker.render()
        assert rendered["props"]["value"] == ["2026-02-17", "2026-02-25"]

    def test_date_picker_with_name(self):
        """Test DatePicker with name argument."""
        picker = DatePicker(label="test", name="start_date")
        rendered = picker.render()
        assert rendered["props"]["name"] == "start_date"


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

    def test_calendar_with_name(self):
        """Test Calendar with name argument."""
        calendar = Calendar(name="booking_calendar")
        rendered = calendar.render()
        assert rendered["props"]["name"] == "booking_calendar"


class TestCombobox:
    """Tests for Combobox component."""

    def test_combobox_renders(self):
        """Test Combobox renders correctly."""
        combobox = Combobox(options=[{"value": "react", "label": "React"}])
        rendered = combobox.render()

        assert rendered["type"] == "Combobox"
        assert rendered["props"]["options"] == [{"value": "react", "label": "React"}]

    def test_combobox_with_rich_option_metadata(self):
        """Test Combobox preserves rich option metadata in serialization."""
        combobox = Combobox(
            options=[
                {
                    "value": "qwen-local",
                    "label": "Qwen-local",
                    "description": "vllm - Qwen/Qwen3-4B-Instruct-2507",
                    "icon": "bot",
                    "color": "#3b82f6",
                    "search_text": "llm local qwen",
                    "disabled": False,
                }
            ]
        )
        rendered = combobox.render()
        option = rendered["props"]["options"][0]

        assert option["description"] == "vllm - Qwen/Qwen3-4B-Instruct-2507"
        assert option["icon"] == "bot"
        assert option["color"] == "#3b82f6"
        assert option["search_text"] == "llm local qwen"
        assert option["disabled"] is False

    def test_combobox_multiselect_value(self):
        """Test Combobox supports multiselect values."""
        combobox = Combobox(
            options=[{"value": "react", "label": "React"}],
            multiselect=True,
            value=["react"],
        )
        rendered = combobox.render()

        assert rendered["props"]["multiselect"] is True
        assert rendered["props"]["value"] == ["react"]

    def test_combobox_with_callback(self):
        """Test Combobox serializes on_select callback."""
        cb = MockCallback()
        combobox = Combobox(options=[{"value": "react", "label": "React"}], on_select=cb)
        rendered = combobox.render()

        assert rendered["props"]["on_select"] == {"callbackId": "cb-123"}

    def test_combobox_with_name(self):
        """Test Combobox with name argument."""
        combobox = Combobox(options=[{"value": "react", "label": "React"}], name="framework")
        rendered = combobox.render()

        assert rendered["props"]["name"] == "framework"

    def test_combobox_creatable(self):
        """Test Combobox with creatable argument."""
        combobox = Combobox(options=[{"value": "react", "label": "React"}], creatable=True)
        rendered = combobox.render()

        assert rendered["props"]["creatable"] is True



class TestInputOTP:
    """Tests for InputOTP component."""

    def test_input_otp_renders(self):
        """Test InputOTP renders correctly."""
        otp = InputOTP(max_length=6)
        rendered = otp.render()
        assert rendered["type"] == "InputOTP"
        assert rendered["props"]["max_length"] == 6

    def test_input_otp_with_name(self):
        """Test InputOTP with name argument."""
        otp = InputOTP(max_length=6, name="otp_code")
        rendered = otp.render()
        assert rendered["props"]["name"] == "otp_code"
