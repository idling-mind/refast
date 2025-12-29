"""Tests for form components."""


from refast.components.shadcn.form import Form, FormField, Label
from refast.components.shadcn.input import Input


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestForm:
    """Tests for Form component."""

    def test_form_renders(self):
        """Test Form renders correctly."""
        form = Form(children=[Input(name="email")])
        rendered = form.render()
        assert rendered["type"] == "Form"
        assert len(rendered["children"]) == 1

    def test_form_with_callback(self):
        """Test Form with on_submit callback."""
        cb = MockCallback()
        form = Form(on_submit=cb)
        rendered = form.render()
        assert rendered["props"]["onSubmit"] == {"callbackId": "cb-123"}


class TestFormField:
    """Tests for FormField component."""

    def test_form_field_renders(self):
        """Test FormField renders correctly."""
        field = FormField(label="Email", children=[Input(name="email")])
        rendered = field.render()
        assert rendered["type"] == "FormField"
        assert rendered["props"]["label"] == "Email"

    def test_form_field_with_error(self):
        """Test FormField with error message."""
        field = FormField(label="Email", error="Invalid email")
        rendered = field.render()
        assert rendered["props"]["error"] == "Invalid email"

    def test_form_field_with_hint(self):
        """Test FormField with hint text."""
        field = FormField(label="Password", hint="At least 8 characters")
        rendered = field.render()
        assert rendered["props"]["hint"] == "At least 8 characters"

    def test_form_field_required(self):
        """Test FormField required prop."""
        field = FormField(label="Name", required=True)
        rendered = field.render()
        assert rendered["props"]["required"] is True


class TestLabel:
    """Tests for Label component."""

    def test_label_renders(self):
        """Test Label renders correctly."""
        label = Label(text="Email Address")
        rendered = label.render()
        assert rendered["type"] == "Label"
        assert rendered["children"] == ["Email Address"]

    def test_label_with_for(self):
        """Test Label with htmlFor prop."""
        label = Label(text="Email", html_for="email-input")
        rendered = label.render()
        assert rendered["props"]["htmlFor"] == "email-input"

    def test_label_required(self):
        """Test Label required indicator."""
        label = Label(text="Name", required=True)
        rendered = label.render()
        assert rendered["props"]["required"] is True
