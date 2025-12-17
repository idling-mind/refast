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
        self.on_change = on_change
        self.on_blur = on_blur
        self.on_focus = on_focus

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "label": self.label,
                "type": self.input_type,
                "placeholder": self.placeholder,
                "value": self.value,
                "required": self.required,
                "disabled": self.disabled,
                "readOnly": self.readonly,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "onBlur": self.on_blur.serialize() if self.on_blur else None,
                "onFocus": self.on_focus.serialize() if self.on_focus else None,
                "className": self.class_name,
                **self.extra_props,
            },
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
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "label": self.label,
                "placeholder": self.placeholder,
                "value": self.value,
                "rows": self.rows,
                "required": self.required,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "options": self.options,
                "label": self.label,
                "value": self.value,
                "placeholder": self.placeholder,
                "required": self.required,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }


class Checkbox(Component):
    """Checkbox input component."""

    component_type: str = "Checkbox"

    def __init__(
        self,
        name: str | None = None,
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
        self.label = label
        self.checked = checked
        self.disabled = disabled
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "label": self.label,
                "checked": self.checked,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
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
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "name": self.name,
                "value": self.value,
                "label": self.label,
                "checked": self.checked,
                "disabled": self.disabled,
                "onChange": self.on_change.serialize() if self.on_change else None,
                "className": self.class_name,
                **self.extra_props,
            },
            "children": [],
        }
