"""Tests for input components."""

from refast.components.shadcn.input import (
    Checkbox,
    CheckboxGroup,
    Input,
    Radio,
    RadioGroup,
    Select,
    Textarea,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestInput:
    """Tests for Input component."""

    def test_input_renders(self):
        """Test Input renders correctly."""
        inp = Input(name="email", type="email", placeholder="Enter email")
        rendered = inp.render()
        assert rendered["type"] == "Input"
        assert rendered["props"]["name"] == "email"
        assert rendered["props"]["type"] == "email"
        assert rendered["props"]["placeholder"] == "Enter email"

    def test_input_with_label(self):
        """Test Input with label."""
        inp = Input(name="name", label="Full Name")
        rendered = inp.render()
        assert rendered["props"]["label"] == "Full Name"

    def test_input_with_description(self):
        """Test Input with description."""
        inp = Input(name="email", description="We'll never share your email")
        rendered = inp.render()
        assert rendered["props"]["description"] == "We'll never share your email"

    def test_input_with_label_and_description(self):
        """Test Input with both label and description."""
        inp = Input(
            name="email",
            label="Email Address",
            description="Enter your email address"
        )
        rendered = inp.render()
        assert rendered["props"]["label"] == "Email Address"
        assert rendered["props"]["description"] == "Enter your email address"

    def test_input_with_value(self):
        """Test Input with value."""
        inp = Input(name="test", value="initial")
        rendered = inp.render()
        assert rendered["props"]["value"] == "initial"

    def test_input_required(self):
        """Test Input required prop."""
        inp = Input(name="test", required=True)
        rendered = inp.render()
        assert rendered["props"]["required"] is True

    def test_input_required_with_label(self):
        """Test Input required prop with label (for asterisk display)."""
        inp = Input(name="test", label="Required Field", required=True)
        rendered = inp.render()
        assert rendered["props"]["required"] is True
        assert rendered["props"]["label"] == "Required Field"

    def test_input_disabled(self):
        """Test Input disabled prop."""
        inp = Input(name="test", disabled=True)
        rendered = inp.render()
        assert rendered["props"]["disabled"] is True

    def test_input_readonly(self):
        """Test Input readonly prop."""
        inp = Input(name="test", readonly=True)
        rendered = inp.render()
        assert rendered["props"]["read_only"] is True

    def test_input_with_error(self):
        """Test Input with error message."""
        inp = Input(name="email", error="Invalid email address")
        rendered = inp.render()
        assert rendered["props"]["error"] == "Invalid email address"

    def test_input_with_error_and_description(self):
        """Test Input with both error and description (error takes precedence)."""
        inp = Input(
            name="email",
            description="Enter your email",
            error="Invalid email address"
        )
        rendered = inp.render()
        assert rendered["props"]["description"] == "Enter your email"
        assert rendered["props"]["error"] == "Invalid email address"

    def test_input_with_callbacks(self):
        """Test Input with callbacks."""
        cb = MockCallback()
        inp = Input(name="test", on_change=cb, on_blur=cb, on_focus=cb)
        rendered = inp.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_blur"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_focus"] == {"callbackId": "cb-123"}

    def test_input_with_keyboard_events(self):
        """Test Input with keyboard event callbacks."""
        cb = MockCallback()
        inp = Input(
            name="test",
            on_keydown=cb,
            on_keyup=cb
        )
        rendered = inp.render()
        assert rendered["props"]["on_keydown"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_keyup"] == {"callbackId": "cb-123"}

    def test_input_with_input_event(self):
        """Test Input with onInput event callback."""
        cb = MockCallback()
        inp = Input(name="test", on_input=cb)
        rendered = inp.render()
        assert rendered["props"]["on_input"] == {"callbackId": "cb-123"}

    def test_input_with_all_events(self):
        """Test Input with all event callbacks."""
        cb = MockCallback()
        inp = Input(
            name="test",
            on_change=cb,
            on_blur=cb,
            on_focus=cb,
            on_keydown=cb,
            on_keyup=cb,
            on_input=cb
        )
        rendered = inp.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_blur"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_focus"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_keydown"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_keyup"] == {"callbackId": "cb-123"}
        assert rendered["props"]["on_input"] == {"callbackId": "cb-123"}

    def test_input_with_debounce(self):
        """Test Input debounce prop."""
        inp = Input(name="search", debounce=300)
        rendered = inp.render()
        assert rendered["props"]["debounce"] == 300

    def test_input_complete_example(self):
        """Test Input with all features combined."""
        cb = MockCallback()
        inp = Input(
            name="email",
            label="Email Address",
            description="We'll never share your email",
            type="email",
            placeholder="you@example.com",
            value="",
            required=True,
            error="",
            debounce=300,
            on_change=cb,
            on_keydown=cb
        )
        rendered = inp.render()
        assert rendered["props"]["name"] == "email"
        assert rendered["props"]["label"] == "Email Address"
        assert rendered["props"]["description"] == "We'll never share your email"
        assert rendered["props"]["type"] == "email"
        assert rendered["props"]["required"] is True
        assert rendered["props"]["debounce"] == 300


class TestTextarea:
    """Tests for Textarea component."""

    def test_textarea_renders(self):
        """Test Textarea renders correctly."""
        ta = Textarea(name="bio", placeholder="Tell us about yourself", rows=5)
        rendered = ta.render()
        assert rendered["type"] == "Textarea"
        assert rendered["props"]["name"] == "bio"
        assert rendered["props"]["rows"] == 5

    def test_textarea_with_callback(self):
        """Test Textarea with on_change callback."""
        cb = MockCallback()
        ta = Textarea(name="test", on_change=cb)
        rendered = ta.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}

    def test_textarea_with_debounce(self):
        """Test Textarea debounce prop."""
        ta = Textarea(name="bio", debounce=150)
        rendered = ta.render()
        assert rendered["props"]["debounce"] == 150


class TestSelect:
    """Tests for Select component."""

    def test_select_renders(self):
        """Test Select renders correctly."""
        options = [
            {"value": "a", "label": "Option A"},
            {"value": "b", "label": "Option B"},
        ]
        sel = Select(name="choice", options=options, placeholder="Choose...")
        rendered = sel.render()
        assert rendered["type"] == "Select"
        assert rendered["props"]["name"] == "choice"
        assert rendered["props"]["options"] == options
        assert rendered["props"]["placeholder"] == "Choose..."

    def test_select_with_value(self):
        """Test Select with selected value."""
        options = [{"value": "a", "label": "A"}]
        sel = Select(name="test", options=options, value="a")
        rendered = sel.render()
        assert rendered["props"]["value"] == "a"

    def test_select_with_callback(self):
        """Test Select with on_change callback."""
        cb = MockCallback()
        sel = Select(name="test", options=[], on_change=cb)
        rendered = sel.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}


class TestCheckbox:
    """Tests for Checkbox component."""

    def test_checkbox_renders(self):
        """Test Checkbox renders correctly."""
        cb = Checkbox(name="agree", label="I agree")
        rendered = cb.render()
        assert rendered["type"] == "Checkbox"
        assert rendered["props"]["name"] == "agree"
        assert rendered["props"]["label"] == "I agree"

    def test_checkbox_checked(self):
        """Test Checkbox checked state."""
        cb = Checkbox(checked=True)
        rendered = cb.render()
        assert rendered["props"]["checked"] is True

    def test_checkbox_with_callback(self):
        """Test Checkbox with on_change callback."""
        mock = MockCallback()
        cb = Checkbox(on_change=mock)
        rendered = cb.render()
        assert rendered["props"]["on_checked_change"] == {"callbackId": "cb-123"}


class TestRadio:
    """Tests for Radio component."""

    def test_radio_renders(self):
        """Test Radio renders correctly."""
        radio = Radio(name="size", value="small", label="Small")
        rendered = radio.render()
        assert rendered["type"] == "Radio"
        assert rendered["props"]["name"] == "size"
        assert rendered["props"]["value"] == "small"
        assert rendered["props"]["label"] == "Small"

    def test_radio_checked(self):
        """Test Radio checked state."""
        radio = Radio(name="size", value="large", checked=True)
        rendered = radio.render()
        assert rendered["props"]["checked"] is True

    def test_radio_with_callback(self):
        """Test Radio with on_change callback."""
        cb = MockCallback()
        radio = Radio(name="test", value="a", on_change=cb)
        rendered = radio.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}


class TestCheckboxGroup:
    """Tests for CheckboxGroup component."""

    def test_checkbox_group_renders(self):
        """Test CheckboxGroup renders correctly."""
        children = [
            Checkbox(value="apple", label="Apple"),
            Checkbox(value="banana", label="Banana"),
            Checkbox(value="orange", label="Orange"),
        ]
        cbg = CheckboxGroup(name="fruits", children=children)
        rendered = cbg.render()
        assert rendered["type"] == "CheckboxGroup"
        assert rendered["props"]["name"] == "fruits"
        assert len(rendered["children"]) == 3

    def test_checkbox_group_with_label(self):
        """Test CheckboxGroup with label."""
        cbg = CheckboxGroup(
            name="fruits",
            label="Select fruits",
            children=[Checkbox(value="apple", label="Apple")],
        )
        rendered = cbg.render()
        assert rendered["props"]["label"] == "Select fruits"

    def test_checkbox_group_with_selected_values(self):
        """Test CheckboxGroup with pre-selected values."""
        children = [
            Checkbox(value="a", label="A"),
            Checkbox(value="b", label="B"),
            Checkbox(value="c", label="C"),
        ]
        cbg = CheckboxGroup(name="letters", children=children, value=["a", "c"])
        rendered = cbg.render()
        assert rendered["props"]["value"] == ["a", "c"]

    def test_checkbox_group_empty_value(self):
        """Test CheckboxGroup with no selection defaults to empty list."""
        cbg = CheckboxGroup(name="test")
        rendered = cbg.render()
        assert rendered["props"]["value"] == []

    def test_checkbox_group_orientation(self):
        """Test CheckboxGroup orientation options."""
        cbg_v = CheckboxGroup(name="test", orientation="vertical")
        rendered_v = cbg_v.render()
        assert rendered_v["props"]["orientation"] == "vertical"

        cbg_h = CheckboxGroup(name="test", orientation="horizontal")
        rendered_h = cbg_h.render()
        assert rendered_h["props"]["orientation"] == "horizontal"

    def test_checkbox_group_disabled(self):
        """Test CheckboxGroup disabled state."""
        cbg = CheckboxGroup(name="test", disabled=True)
        rendered = cbg.render()
        assert rendered["props"]["disabled"] is True

    def test_checkbox_group_with_callback(self):
        """Test CheckboxGroup with on_change callback."""
        cb = MockCallback()
        cbg = CheckboxGroup(name="test", on_change=cb)
        rendered = cbg.render()
        assert rendered["props"]["on_change"] == {"callbackId": "cb-123"}


class TestRadioGroup:
    """Tests for RadioGroup component."""

    def test_radio_group_renders(self):
        """Test RadioGroup renders correctly."""
        children = [
            Radio(name="gender", value="male", label="Male"),
            Radio(name="gender", value="female", label="Female"),
            Radio(name="gender", value="other", label="Other"),
        ]
        rg = RadioGroup(name="gender", children=children)
        rendered = rg.render()
        assert rendered["type"] == "RadioGroup"
        assert rendered["props"]["name"] == "gender"
        assert len(rendered["children"]) == 3

    def test_radio_group_with_label(self):
        """Test RadioGroup with label."""
        rg = RadioGroup(
            name="gender",
            label="Select gender",
            children=[Radio(name="gender", value="male", label="Male")],
        )
        rendered = rg.render()
        assert rendered["props"]["label"] == "Select gender"

    def test_radio_group_with_selected_value(self):
        """Test RadioGroup with pre-selected value."""
        children = [
            Radio(name="choice", value="a", label="A"),
            Radio(name="choice", value="b", label="B"),
        ]
        rg = RadioGroup(name="choice", children=children, value="b")
        rendered = rg.render()
        assert rendered["props"]["value"] == "b"

    def test_radio_group_no_value(self):
        """Test RadioGroup with no selection."""
        rg = RadioGroup(name="test")
        rendered = rg.render()
        assert rendered["props"]["value"] is None

    def test_radio_group_orientation(self):
        """Test RadioGroup orientation options."""
        rg_v = RadioGroup(name="test", orientation="vertical")
        rendered_v = rg_v.render()
        assert rendered_v["props"]["orientation"] == "vertical"

        rg_h = RadioGroup(name="test", orientation="horizontal")
        rendered_h = rg_h.render()
        assert rendered_h["props"]["orientation"] == "horizontal"

    def test_radio_group_disabled(self):
        """Test RadioGroup disabled state."""
        rg = RadioGroup(name="test", disabled=True)
        rendered = rg.render()
        assert rendered["props"]["disabled"] is True

    def test_radio_group_with_callback(self):
        """Test RadioGroup with on_change callback."""
        cb = MockCallback()
        rg = RadioGroup(name="test", on_change=cb)
        rendered = rg.render()
        assert rendered["props"]["on_value_change"] == {"callbackId": "cb-123"}



