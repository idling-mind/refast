"""Input components based on shadcn."""

from typing import Any, Literal

from refast.components.base import ChildrenType, Component


class InputWrapper(Component):
    """
    A wrapper component for form controls with label, description, required indicator, and error.

    Use this component to wrap any form control to add consistent styling for labels,
    descriptions, required indicators, and error messages. The built-in inputs wrap themselves
    automatically — use ``InputWrapper`` directly only when building custom controls.

    Example:
        ```python
        from refast.components.shadcn.input import InputWrapper
        from refast.components.shadcn.controls import Slider

        InputWrapper(
            label="Volume",
            description="Adjust the playback volume.",
            required=True,
            error="Volume must be set.",
            children=[
                Slider(value=[75], min=0, max=100),
            ],
        )
        ```

    Args:
        label: Label text displayed above the wrapped control.
        description: Help text displayed below the label.
        required: Shows a required asterisk next to the label.
        error: Error message displayed below the control.
        children: The wrapped control(s).
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "InputWrapper"

    def __init__(
        self,
        label: str | None = None,
        description: str | None = None,
        required: bool = False,
        error: str | None = None,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.description = description
        self.required = required
        self.error = error
        self.add_children(children)

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
    Single-line text input component with label, description, and validation support.

    Example:
        ```python
        Input(
            name="email",
            label="Email Address",
            description="We'll never share your email.",
            type="email",
            placeholder="you@example.com",
            required=True,
            read_only=False,
            error="Please enter a valid email",
            debounce=300,
            on_change=ctx.callback(handle_change),
        )
        ```

    Args:
        name: HTML ``name`` attribute used in form data; omit to skip.
        label: Label text displayed above the input.
        description: Help text displayed below the label.
        type: HTML input type.
        placeholder: Placeholder text shown when the field is empty.
        value: Controlled value. When ``None`` the input starts uncontrolled.
        required: Shows a required asterisk and sets the HTML ``required`` attribute.
        disabled: Disables interaction.
        read_only: Renders the input in read-only mode.
        error: Error message displayed below the input.
        debounce: Milliseconds to delay ``on_change`` after the user stops typing.
        on_change: Callback fired when the value changes.
        on_blur: Callback fired when the input loses focus.
        on_focus: Callback fired when the input gains focus.
        on_keydown: Callback fired on key-down events.
        on_keyup: Callback fired on key-up events.
        on_input: Callback fired on every native input event.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Input"

    def __init__(
        self,
        name: str | None = None,
        label: str | None = None,
        description: str | None = None,
        type: Literal["text", "email", "password", "number", "tel", "url", "search"] = "text",
        placeholder: str = "",
        value: str | None = None,
        default_value: str | None = None,
        required: bool = False,
        disabled: bool = False,
        read_only: bool = False,
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
        self.default_value = default_value
        self.required = required
        self.disabled = disabled
        self.read_only = read_only
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
            "label": self.label,
            "description": self.description,
            "type": self.input_type,
            "placeholder": self.placeholder,
            "required": self.required,
            "disabled": self.disabled,
            "read_only": self.read_only,
            "error": self.error,
            "debounce": self.debounce,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.name is not None:
            props["name"] = self.name

        # Only include value when explicitly set (not None) so the frontend
        # Input starts as uncontrolled.  This allows update_props({"value": ""})
        # to transition from undefined → "" and actually trigger a UI update.
        if self.value is not None:
            props["value"] = self.value
        if self.default_value is not None:
            props["default_value"] = self.default_value

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
    """
    Multi-line text input component.

    Example:
        ```python
        Textarea(
            name="bio",
            label="Biography",
            description="Tell us a little about yourself.",
            placeholder="Write your bio here\u2026",
            rows=5,
            required=True,
            debounce=300,
            on_change=ctx.callback(handle_change),
        )
        ```

    Args:
        name: HTML ``name`` attribute; omit to skip.
        label: Label text displayed above the textarea.
        description: Help text displayed below the label.
        placeholder: Placeholder text.
        value: Controlled value.
        rows: Number of visible text rows.
        required: Shows a required asterisk.
        disabled: Disables interaction.
        error: Error message displayed below.
        debounce: Milliseconds to delay ``on_change``.
        on_change: Callback fired when the value changes.
        on_blur: Callback fired on blur.
        on_focus: Callback fired on focus.
        on_keydown: Callback fired on key-down.
        on_keyup: Callback fired on key-up.
        on_input: Callback fired on every input event.
        id: Component ID.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Textarea"

    def __init__(
        self,
        name: str | None = None,
        label: str | None = None,
        description: str | None = None,
        placeholder: str = "",
        value: str | None = None,
        default_value: str | None = None,
        rows: int = 3,
        required: bool = False,
        disabled: bool = False,
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
        self.placeholder = placeholder
        self.value = value
        self.default_value = default_value
        self.rows = rows
        self.required = required
        self.disabled = disabled
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

        if self.name is not None:
            props["name"] = self.name

        if self.value is not None:
            props["value"] = self.value
        if self.default_value is not None:
            props["default_value"] = self.default_value

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


class Select(Component):
    """
    Dropdown select component.

    Options are plain dicts with ``value`` and ``label`` keys. Add
    ``"disabled": True`` to an option to make it unselectable.

    Example:
        ```python
        Select(
            name="country",
            label="Country",
            description="Select your country of residence.",
            options=[
                {"value": "us", "label": "United States"},
                {"value": "gb", "label": "United Kingdom"},
                {"value": "de", "label": "Germany", "disabled": True},
            ],
            placeholder="Choose a country\u2026",
            required=True,
            on_change=ctx.callback(handle_change),
        )
        ```

    Args:
        options: List of ``{"value": str, "label": str}`` dicts.
            Optionally add ``"disabled": True`` to disable an option.
        name: HTML ``name`` attribute; omit to skip.
        label: Label text displayed above the select.
        description: Help text displayed below the label.
        value: Controlled selected value.
        placeholder: Placeholder option shown when nothing is selected.
        required: Shows a required asterisk.
        disabled: Disables the select.
        error: Error message displayed below the select.
        on_change: Callback fired when the selection changes.
        id: Component ID.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Select"

    def __init__(
        self,
        options: list[dict[str, str]],  # [{"value": "a", "label": "Option A"}, ...]
        name: str | None = None,
        label: str | None = None,
        description: str | None = None,
        value: str | None = None,
        default_value: str | None = None,
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
        self.default_value = default_value
        self.placeholder = placeholder
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
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

        if self.name is not None:
            props["name"] = self.name

        if self.value is not None:
            props["value"] = self.value
        if self.default_value is not None:
            props["default_value"] = self.default_value

        if self.on_change:
            props["on_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Checkbox(Component):
    """
    Single checkbox input component.

    Example:
        ```python
        Checkbox(
            name="agree",
            value="yes",
            label="I agree to the terms of service",
            required=True,
            on_change=ctx.callback(handle_toggle),
        )
        ```

    Args:
        name: HTML ``name`` attribute; omit to skip.
        value: The value submitted when the checkbox is checked.
        label: Label text displayed next to the checkbox.
        description: Help text displayed below the checkbox.
        checked: Controlled checked state.
        required: Shows a required asterisk.
        disabled: Disables interaction.
        error: Error message displayed below the checkbox.
        on_change: Callback fired when the checked state changes.
            Serialized as ``on_checked_change``.
        id: Component ID.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Checkbox"

    def __init__(
        self,
        name: str | None = None,
        value: str | None = None,
        label: str | None = None,
        description: str | None = None,
        checked: bool = False,
        default_checked: bool = False,
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
        self.default_checked = default_checked
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
            "default_checked": self.default_checked,
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
        name: str | None = None,
        children: ChildrenType = None,
        label: str | None = None,
        description: str | None = None,
        value: list[str] | None = None,
        default_value: list[str] | None = None,
        options: list[dict[str, Any]] | None = None,
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
        self.add_children(children)
        self.name = name
        self.label = label
        self.description = description
        self.value = value or []
        self.default_value = default_value
        self.options = options
        self.orientation = orientation
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "label": self.label,
            "description": self.description,
            "value": self.value,
            "default_value": self.default_value,
            "options": self.options,
            "orientation": self.orientation,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.name is not None:
            props["name"] = self.name

        if self.on_change:
            props["on_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class Radio(Component):
    """
    Single radio button component, typically used inside a ``RadioGroup``.

    Example:
        ```python
        Radio(value="small", label="Small", name="size")
        ```

    Args:
        value: The value emitted when this radio is selected (required).
        name: HTML ``name`` attribute shared with other radios in the group.
        label: Label text displayed next to the radio button.
        description: Help text displayed below the radio.
        checked: Controlled checked state.
        required: Shows a required asterisk.
        disabled: Disables this radio button.
        error: Error message displayed below.
        on_change: Callback fired when this radio is selected.
        id: Component ID.
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Radio"

    def __init__(
        self,
        value: str,
        name: str | None = None,
        label: str | None = None,
        description: str | None = None,
        checked: bool = False,
        default_checked: bool = False,
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
        self.default_checked = default_checked
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "value": self.value,
            "label": self.label,
            "description": self.description,
            "checked": self.checked,
            "default_checked": self.default_checked,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.name is not None:
            props["name"] = self.name

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
        name: str | None = None,
        children: ChildrenType = None,
        label: str | None = None,
        description: str | None = None,
        value: str | None = None,
        default_value: str | None = None,
        options: list[dict[str, Any]] | None = None,
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
        self.add_children(children)
        self.name = name
        self.label = label
        self.description = description
        self.value = value
        self.default_value = default_value
        self.options = options
        self.orientation = orientation
        self.required = required
        self.disabled = disabled
        self.error = error
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "label": self.label,
            "description": self.description,
            "value": self.value,
            "default_value": self.default_value,
            "options": self.options,
            "orientation": self.orientation,
            "required": self.required,
            "disabled": self.disabled,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.name is not None:
            props["name"] = self.name

        if self.on_change:
            props["on_value_change"] = self.on_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }
