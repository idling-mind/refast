"""Form components."""

from typing import Any

from refast.components.base import ChildrenType, Component


class Form(Component):
    """
    Form container component that intercepts the submit event and routes it to a server callback.

    Refast intercepts the native ``submit`` event; ``method`` and ``enctype`` are therefore
    not configurable — all data is sent over the WebSocket.

    Example:
        ```python
        from refast.components.shadcn.form import Form, FormField
        from refast.components.shadcn.input import Input
        from refast.components.shadcn.button import Button

        Form(
            on_submit=ctx.callback(handle_submit),
            children=[
                FormField(
                    label="Email",
                    required=True,
                    children=[Input(name="email", type="email")],
                ),
                Button("Submit", type="submit"),
            ],
        )
        ```

    Args:
        children: Form content — typically ``FormField`` components and a submit ``Button``.
        on_submit: Callback fired when the form is submitted.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Form"

    def __init__(
        self,
        children: ChildrenType = None,
        on_submit: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
        self.on_submit = on_submit

    def render(self) -> dict[str, Any]:
        props = {
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_submit:
            props["on_submit"] = self.on_submit.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class FormField(Component):
    """
    Form field wrapper that pairs an input with a label, hint text, and validation error.

    Example:
        ```python
        from refast.components.shadcn.form import FormField
        from refast.components.shadcn.input import Input

        FormField(
            label="Password",
            hint="At least 8 characters, one number, one symbol.",
            required=True,
            error="Password is too short.",
            children=[Input(name="password", type="password")],
        )
        ```

    Args:
        children: The input component(s) to wrap.
        label: Field label text.
        error: Validation error message displayed below the field.
        hint: Hint text displayed below the label.
        required: Shows a required asterisk next to the label.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "FormField"

    def __init__(
        self,
        children: ChildrenType = None,
        label: str | None = None,
        error: str | None = None,
        hint: str | None = None,
        required: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)
        self.label = label
        self.error = error
        self.hint = hint
        self.required = required

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "label": self.label,
                "error": self.error,
                "hint": self.hint,
                "required": self.required,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Label(Component):
    """
    Standalone form label element.

    Most inputs include a built-in ``label`` prop — use ``Label`` only when you need a
    label element that is decoupled from the control it describes.

    Example:
        ```python
        from refast.components.shadcn.form import Label

        Label(text="API Key", html_for="api-key-input", required=True)
        ```

    Args:
        text: Label text content.
        html_for: Associates the label with a control's ``id`` (rendered as ``htmlFor``).
        required: Shows a required asterisk.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Label"

    def __init__(
        self,
        text: str,
        html_for: str | None = None,
        required: bool = False,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text
        self.html_for = html_for
        self.required = required
        self.style = style

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "html_for": self.html_for,
                "required": self.required,
                "class_name": self.class_name,
                "style": self.style,
                **self._serialize_extra_props(),
            },
            "children": [self.text],
        }
