"""Input components based on shadcn."""

from typing import Any, Literal

from refast.components.base import Component


class Input(Component):
    """
    Text input component.

    Example:
        ```python
        Input(
            name="email",
            label="Email Address",
            type="email",
            placeholder="you@example.com",
            on_change=ctx.callback(handle_change),
        )
        ```
    """

    component_type: str = "Input"

    def __init__(
        self,
        name: str,
        label: str | None = None,
        type: Literal["text", "email", "password", "number", "tel", "url", "search"] = "text",
        placeholder: str = "",
        value: str = "",
        required: bool = False,
        disabled: bool = False,
        readonly: bool = False,
        debounce: int = 0,
        on_change: Any = None,
        on_blur: Any = None,
        on_focus: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.input_type = type
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self.disabled = disabled
        self.readonly = readonly
        self.debounce = debounce
        self.on_change = on_change
        self.on_blur = on_blur
        self.on_focus = on_focus

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "type": self.input_type,
            "placeholder": self.placeholder,
            "value": self.value,
            "required": self.required,
            "disabled": self.disabled,
            "read_only": self.readonly,
            "debounce": self.debounce,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_change:
            props["on_change"] = self.on_change.serialize()
        if self.on_blur:
            props["on_blur"] = self.on_blur.serialize()
        if self.on_focus:
            props["on_focus"] = self.on_focus.serialize()

        # Input usually doesn't need uncontrolled/controlled dichotomy as much unless it's live-validated
        # But if value is None, we could treat it as uncontrolled. The current __init__ defaults value to ""
        # so it is always controlled by default. This is fine for Input.

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
        placeholder: str = "",
        value: str = "",
        rows: int = 3,
        required: bool = False,
        disabled: bool = False,
        debounce: int = 0,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.label = label
        self.placeholder = placeholder
        self.value = value
        self.rows = rows
        self.required = required
        self.disabled = disabled
        self.debounce = debounce
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "placeholder": self.placeholder,
            "value": self.value,
            "rows": self.rows,
            "required": self.required,
            "disabled": self.disabled,
            "debounce": self.debounce,
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


class Select(Component):
    """Dropdown select component."""

    component_type: str = "Select"

    def __init__(
        self,
        name: str,
        options: list[dict[str, str]],  # [{"value": "a", "label": "Option A"}, ...]
        label: str | None = None,
        value: str = "",
        placeholder: str = "Select...",
        required: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.options = options
        self.label = label
        self.value = value
        self.placeholder = placeholder
        self.required = required
        self.disabled = disabled
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "options": self.options,
            "label": self.label,
            "value": self.value,
            "placeholder": self.placeholder,
            "required": self.required,
            "disabled": self.disabled,
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


class Checkbox(Component):
    """Checkbox input component."""

    component_type: str = "Checkbox"

    def __init__(
        self,
        name: str | None = None,
        value: str | None = None,
        label: str | None = None,
        checked: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.value = value
        self.label = label
        self.checked = checked
        self.disabled = disabled
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "value": self.value,
            "label": self.label,
            "checked": self.checked,
            "disabled": self.disabled,
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
            value=["apple"],
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
        children: Checkbox components as children.
        value: List of currently selected values.
        orientation: Layout orientation - "vertical" or "horizontal".
        disabled: Whether the entire group is disabled.
        on_change: Callback when selection changes (receives list of selected values).
    """

    component_type: str = "CheckboxGroup"

    def __init__(
        self,
        name: str,
        children: list[Component | str] | None = None,
        label: str | None = None,
        value: list[str] | None = None,
        orientation: Literal["vertical", "horizontal"] = "vertical",
        disabled: bool = False,
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
        self.value = value or []
        self.orientation = orientation
        self.disabled = disabled
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "value": self.value,
            "orientation": self.orientation,
            "disabled": self.disabled,
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
        checked: bool = False,
        disabled: bool = False,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.name = name
        self.value = value
        self.label = label
        self.checked = checked
        self.disabled = disabled
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "value": self.value,
            "label": self.label,
            "checked": self.checked,
            "disabled": self.disabled,
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
            value="male",
            orientation="vertical",
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
        children: Radio components as children.
        value: Currently selected value.
        orientation: Layout orientation - "vertical" or "horizontal".
        disabled: Whether the entire group is disabled.
        on_change: Callback when selection changes (receives selected value).
    """

    component_type: str = "RadioGroup"

    def __init__(
        self,
        name: str,
        children: list[Component | str] | None = None,
        label: str | None = None,
        value: str | None = None,
        orientation: Literal["vertical", "horizontal"] = "vertical",
        disabled: bool = False,
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
        self.value = value
        self.orientation = orientation
        self.disabled = disabled
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "name": self.name,
            "label": self.label,
            "value": self.value,
            "orientation": self.orientation,
            "disabled": self.disabled,
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

