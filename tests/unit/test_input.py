"""Tests for input components."""

import pytest

from refast.components.shadcn.input import Input, Textarea, Select, Checkbox, Radio


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

    def test_input_disabled(self):
        """Test Input disabled prop."""
        inp = Input(name="test", disabled=True)
        rendered = inp.render()
        assert rendered["props"]["disabled"] is True

    def test_input_readonly(self):
        """Test Input readonly prop."""
        inp = Input(name="test", readonly=True)
        rendered = inp.render()
        assert rendered["props"]["readOnly"] is True

    def test_input_with_callbacks(self):
        """Test Input with callbacks."""
        cb = MockCallback()
        inp = Input(name="test", on_change=cb, on_blur=cb, on_focus=cb)
        rendered = inp.render()
        assert rendered["props"]["onChange"] == {"callbackId": "cb-123"}
        assert rendered["props"]["onBlur"] == {"callbackId": "cb-123"}
        assert rendered["props"]["onFocus"] == {"callbackId": "cb-123"}


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
        assert rendered["props"]["onChange"] == {"callbackId": "cb-123"}


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
        assert rendered["props"]["onChange"] == {"callbackId": "cb-123"}


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
        assert rendered["props"]["onChange"] == {"callbackId": "cb-123"}


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
        assert rendered["props"]["onChange"] == {"callbackId": "cb-123"}
