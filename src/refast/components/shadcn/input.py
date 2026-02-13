"""Input components based on shadcn."""

from typing import Any, Literal

from refast.components.base import Component


class InputWrapper(Component):
    """
    A wrapper component for form controls with label, description, required indicator, and error.

    Use this component to wrap any form control to add consistent styling for labels,
    descriptions, required indicators, and error messages.

    Example:
        ```python
        InputWrapper(
            label="Custom Field",
            description="This is a custom field with a wrapper",
            required=True,
            error="This field has an error",
            children=[
                Slider(value=[50], min=0, max=100),
            ],
        )
        ```
    """

    component_type: str = "InputWrapper"

    def __init__(
        self,
        label: str | None = None,
        description: str | None = None,
        required: bool = False,
        error: str | None = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.description = description
        self.required = required
        self.error = error
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "label": self.label,
                "description": self.description,
                "required": self.required,
                "error": self.error,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class Input(Component):
    """
    Text input component.

    Example:
        ```python
        Input(
            name="email",
            label="Email Address",
            description="We'll never share your email.",
            type="email",
            placeholder="you@example.com",
            required=True,
            error="Please enter a valid email",
            on_change=ctx.callback(handle_change),
        )
        ```
    """

    component_type: str = "Input"

    def __init__(
        self,
        name: str,
        label: str | None = None,
        description: str | None = None,
        type: Literal["text", "email", "password", "number", "tel", "url", "search"] = "text",
        placeholder: str = "",
        value: str | None = None,
        required: bool = False,
        disabled: bool = False,
        readonly: bool = False,
        error: str | None = None,
        debounce: int = 0,
        on_change: Any = None,
        on_blur: Any = None,
        on_focus: Any = None,
        on_keydown: Any = None,
        on_keyup: Any = None,
        on_input: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.description = description
        self.input_type = type
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self.disabled = disabled
        self.readonly = readonly
        self.error = error
        self.debounce = debounce
        self.on_change = on_change
        self.on_blur = on_blur
        self.on_focus = on_focus
        self.on_keydown = on_keydown
        self.on_keyup = on_keyup
        self.on_input = on_input

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "type": self.input_type,
            "placeholder": self.placeholder,
            "required": self.required,
            "disabled": self.disabled,
            "read_only": self.readonly,
            "error": self.error,
            "debounce": self.debounce,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        # Only include value when explicitly set (not None) so the frontend
        # Input starts as uncontrolled.  This allows update_props({"value": ""})
        # to transition from undefined → "" and actually trigger a UI update.
        if self.value is not None:
            props["value"] = self.value

        if self.on_change:
            props["on_change"] = self.on_change.serialize()
        if self.on_blur:
            props["on_blur"] = self.on_blur.serialize()
        if self.on_focus:
            props["on_focus"] = self.on_focus.serialize()
        if self.on_keydown:
            props["on_keydown"] = self.on_keydown.serialize()
        if self.on_keyup:
            props["on_keyup"] = self.on_keyup.serialize()
        if self.on_input:
            props["on_input"] = self.on_input.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Textarea(Component):
    """Multi-line text input."""

    component_type: str = "Textarea"

    def __init__(
        self,
        name: str,
        label: str | None = None,
        description: str | None = None,
        placeholder: str = "",
        value: str | None = None,
        rows: int = 3,
        required: bool = False,
        disabled: bool = False,
        error: str | None = None,
        debounce: int = 0,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.description = description
        self.placeholder = placeholder
        self.value = value
        self.rows = rows
        self.required = required
        self.disabled = disabled
        self.error = error
        self.debounce = debounce
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "placeholder": self.placeholder,
            "rows": self.rows,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "debounce": self.debounce,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.value is not None:
            props["value"] = self.value

        if self.on_change:
            props["on_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Select(Component):
    """Dropdown select component."""

    component_type: str = "Select"

    def __init__(
        self,
        name: str,
        options: list[dict[str, str]],  # [{"value": "a", "label": "Option A"}, ...]
        label: str | None = None,
        description: str | None = None,
        value: str | None = None,
        placeholder: str = "Select...",
        required: bool = False,
        disabled: bool = False,
        error: str | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.options = options
        self.label = label
        self.description = description
        self.value = value
        self.placeholder = placeholder
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "options": self.options,
            "label": self.label,
            "description": self.description,
            "placeholder": self.placeholder,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.value is not None:
            props["value"] = self.value

        if self.on_change:
            props["on_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Checkbox(Component):
    """Checkbox input component."""

    component_type: str = "Checkbox"

    def __init__(
        self,
        name: str | None = None,
        value: str | None = None,
        label: str | None = None,
        description: str | None = None,
        checked: bool = False,
        required: bool = False,
        disabled: bool = False,
        error: str | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.value = value
        self.label = label
        self.description = description
        self.checked = checked
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "value": self.value,
            "label": self.label,
            "description": self.description,
            "checked": self.checked,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_change:
            props["on_checked_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class CheckboxGroup(Component):
    """
    Checkbox group component for selecting multiple options.

    Example:
        ```python
        CheckboxGroup(
            name="fruits",
            label="Select your favorite fruits",
            description="Choose as many as you like",
            value=["apple"],
            required=True,
            error="Please select at least one fruit",
            on_change=ctx.callback(handle_change),
            children=[
                Checkbox(value="apple", label="Apple"),
                Checkbox(value="banana", label="Banana"),
                Checkbox(value="orange", label="Orange", disabled=True),
            ],
        )
        ```

    Args:
        name: The name for the checkbox group (used for form submission).
        label: Label text for the entire group.
        description: Description text displayed below the label.
        children: Checkbox components as children.
        value: List of currently selected values.
        orientation: Layout orientation - "vertical" or "horizontal".
        required: Whether the field is required (shows asterisk).
        disabled: Whether the entire group is disabled.
        error: Error message to display.
        on_change: Callback when selection changes (receives list of selected values).
    """

    component_type: str = "CheckboxGroup"

    def __init__(
        self,
        name: str,
        children: list[Component | str] | None = None,
        label: str | None = None,
        description: str | None = None,
        value: list[str] | None = None,
        orientation: Literal["vertical", "horizontal"] = "vertical",
        required: bool = False,
        disabled: bool = False,
        error: str | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.name = name
        self.label = label
        self.description = description
        self.value = value or []
        self.orientation = orientation
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "value": self.value,
            "orientation": self.orientation,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_change:
            props["on_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class Radio(Component):
    """Radio button component."""

    component_type: str = "Radio"

    def __init__(
        self,
        name: str,
        value: str,
        label: str | None = None,
        description: str | None = None,
        checked: bool = False,
        required: bool = False,
        disabled: bool = False,
        error: str | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.value = value
        self.label = label
        self.description = description
        self.checked = checked
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "value": self.value,
            "label": self.label,
            "description": self.description,
            "checked": self.checked,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_change:
            props["on_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class RadioGroup(Component):
    """
    Radio group component for selecting a single option from multiple choices.

    Example:
        ```python
        RadioGroup(
            name="gender",
            label="Select your gender",
            description="This information is optional",
            value="male",
            orientation="vertical",
            required=True,
            error="Please select an option",
            on_change=ctx.callback(handle_change),
            children=[
                Radio(value="male", label="Male"),
                Radio(value="female", label="Female"),
                Radio(value="other", label="Other"),
            ],
        )
        ```

    Args:
        name: The name for the radio group (used for form submission).
        label: Label text for the entire group.
        description: Description text displayed below the label.
        children: Radio components as children.
        value: Currently selected value.
        orientation: Layout orientation - "vertical" or "horizontal".
        required: Whether the field is required (shows asterisk).
        disabled: Whether the entire group is disabled.
        error: Error message to display.
        on_change: Callback when selection changes (receives selected value).
    """

    component_type: str = "RadioGroup"

    def __init__(
        self,
        name: str,
        children: list[Component | str] | None = None,
        label: str | None = None,
        description: str | None = None,
        value: str | None = None,
        orientation: Literal["vertical", "horizontal"] = "vertical",
        required: bool = False,
        disabled: bool = False,
        error: str | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children
        self.name = name
        self.label = label
        self.description = description
        self.value = value
        self.orientation = orientation
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "value": self.value,
            "orientation": self.orientation,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_change:
            props["on_value_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }
