"""Advanced form control components based on shadcn/ui."""

from typing import Any, Literal

from refast.components.base import Component


class Switch(Component):
    """
    Toggle switch component.

    Example:
        ```python
        Switch(
            id="airplane-mode",
            checked=True,
            on_change=ctx.callback(handle_change),
        )
        ```
    """

    component_type: str = "Switch"

    def __init__(
        self,
        checked: bool | None = None,
        default_checked: bool = False,
        disabled: bool = False,
        name: str | None = None,
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.checked = checked
        self.default_checked = default_checked
        self.disabled = disabled
        self.name = name
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        props = {
            "disabled": self.disabled,
            "name": self.name,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_change:
            props["on_checked_change"] = self.on_change.serialize()

        if self.checked is not None:
            props["checked"] = self.checked
        if self.default_checked:
            props["default_checked"] = self.default_checked

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Slider(Component):
    """
    Slider input for selecting a value from a range.

    Example:
        ```python
        Slider(
            value=[50],
            min=0,
            max=100,
            step=1,
            on_value_change=ctx.callback(handle_change),
        )
        ```
    """

    component_type: str = "Slider"

    def __init__(
        self,
        value: list[float] | None = None,
        default_value: list[float] | None = None,
        min: float = 0,
        max: float = 100,
        step: float = 1,
        disabled: bool = False,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        on_value_change: Any = None,
        on_value_commit: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.default_value = default_value or [0]
        self.min = min
        self.max = max
        self.step = step
        self.disabled = disabled
        self.orientation = orientation
        self.on_value_change = on_value_change
        self.on_value_commit = on_value_commit

    def render(self) -> dict[str, Any]:
        props = {
            "default_value": self.default_value,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "disabled": self.disabled,
            "orientation": self.orientation,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_value_change:
            props["on_value_change"] = self.on_value_change.serialize()

        if self.on_value_commit:
            props["on_value_commit"] = self.on_value_commit.serialize()

        if self.value is not None:
            props["value"] = self.value

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class Toggle(Component):
    """
    A two-state button that can be on or off.

    Example:
        ```python
        Toggle(
            "Bold",
            icon="Bold",
            pressed=True,
            on_pressed_change=ctx.callback(handle_toggle),
        )
        ```
    """

    component_type: str = "Toggle"

    def __init__(
        self,
        label: str = "",
        icon: str | None = None,
        pressed: bool | None = None,
        default_pressed: bool = False,
        disabled: bool = False,
        variant: Literal["default", "outline"] = "default",
        size: Literal["sm", "default", "lg"] = "default",
        on_pressed_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.pressed = pressed
        self.default_pressed = default_pressed
        self.disabled = disabled
        self.variant = variant
        self.size = size
        self.on_pressed_change = on_pressed_change

    def render(self) -> dict[str, Any]:
        props = {
            "label": self.label,
            "icon": self.icon,
            "disabled": self.disabled,
            "variant": self.variant,
            "size": self.size,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.pressed is not None:
            props["pressed"] = self.pressed
        if self.default_pressed:
            props["default_pressed"] = self.default_pressed
        if self.on_pressed_change:
            props["on_pressed_change"] = self.on_pressed_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class ToggleGroup(Component):
    """
    A set of two-state buttons that can be toggled on or off.

    Example:
        ```python
        ToggleGroup(
            type="multiple",
            default_value={"bold": True, "italic": False},
            children=[
                ToggleGroupItem("Bold", icon="Bold", name="bold"),
                ToggleGroupItem("Italic", icon="Italic", name="italic"),
            ],
            on_value_change=ctx.callback(handle_change),
        )
        ```
    """

    component_type: str = "ToggleGroup"

    def __init__(
        self,
        type: Literal["single", "multiple"] = "single",
        value: str | list[str] | dict[str, bool] | None = None,
        default_value: str | list[str] | dict[str, bool] | None = None,
        disabled: bool = False,
        variant: Literal["default", "outline"] = "default",
        size: Literal["sm", "default", "lg"] = "default",
        on_value_change: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.toggle_type = type
        self.value = value
        self.default_value = default_value
        self.disabled = disabled
        self.variant = variant
        self.size = size
        self.on_value_change = on_value_change
        if children:
            self._children = children

    def _convert_dict_to_list(self, val: dict[str, bool] | Any) -> list[str] | Any:
        if isinstance(val, dict):
            return [k for k, v in val.items() if v]
        return val

    def render(self) -> dict[str, Any]:
        props = {
            "type": self.toggle_type,
            "default_value": self._convert_dict_to_list(self.default_value),
            "disabled": self.disabled,
            "variant": self.variant,
            "size": self.size,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.value is not None:
            props["value"] = self._convert_dict_to_list(self.value)
        if self.on_value_change:
            props["on_value_change"] = self.on_value_change.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class ToggleGroupItem(Component):
    """
    An item within a ToggleGroup.

    Example:
        ```python
        ToggleGroupItem("Bold", icon="Bold", name="bold")
        ```
    """

    component_type: str = "ToggleGroupItem"

    def __init__(
        self,
        label: str = "",
        icon: str | None = None,
        value: str | None = None,
        name: str | None = None,
        disabled: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.label = label
        self.icon = icon
        self.value = value or name or ""
        self.disabled = disabled

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "label": self.label,
                "icon": self.icon,
                "value": self.value,
                "disabled": self.disabled,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Calendar(Component):
    """
    A date picker calendar component.

    Example:
        ```python
        Calendar(
            mode="single",
            selected=date(2024, 1, 15),
            on_select=ctx.callback(handle_select),
        )
        ```
    """

    component_type: str = "Calendar"

    def __init__(
        self,
        mode: Literal["single", "multiple", "range"] = "single",
        selected: Any = None,  # date, list[date], or DateRange
        default_month: Any = None,  # date
        disabled: bool = False,
        show_outside_days: bool = True,
        on_select: Any = None,
        on_month_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.mode = mode
        self.selected = selected
        self.default_month = default_month
        self.disabled = disabled
        self.show_outside_days = show_outside_days
        self.on_select = on_select
        self.on_month_change = on_month_change

    def _serialize_date(self, d: Any) -> str | list[str] | dict[str, str] | None:
        """Serialize date objects to ISO strings."""
        if d is None:
            return None
        if hasattr(d, "isoformat"):
            return d.isoformat()
        if isinstance(d, list):
            return [self._serialize_date(item) for item in d]
        if isinstance(d, dict):
            return {k: self._serialize_date(v) for k, v in d.items()}
        return str(d)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "mode": self.mode,
                "selected": self._serialize_date(self.selected),
                "default_month": self._serialize_date(self.default_month),
                "disabled": self.disabled,
                "show_outside_days": self.show_outside_days,
                "on_select": self.on_select.serialize() if self.on_select else None,
                "on_month_change": self.on_month_change.serialize() if self.on_month_change else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class DatePicker(Component):
    """
    A date picker with input and calendar popup.

    Example:
        ```python
        DatePicker(
            value=date(2024, 1, 15),
            placeholder="Pick a date",
            on_change=ctx.callback(handle_date_change),
        )
        ```
    """

    component_type: str = "DatePicker"

    def __init__(
        self,
        value: Any = None,  # date
        placeholder: str = "Pick a date",
        disabled: bool = False,
        format: str = "PPP",  # date-fns format
        on_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.value = value
        self.placeholder = placeholder
        self.disabled = disabled
        self.format = format
        self.on_change = on_change

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "value": self.value.isoformat() if hasattr(self.value, "isoformat") else self.value,
                "placeholder": self.placeholder,
                "disabled": self.disabled,
                "format": self.format,
                "on_change": self.on_change.serialize() if self.on_change else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Combobox(Component):
    """
    An autocomplete input with dropdown.

    Example:
        ```python
        Combobox(
            options=[
                {"value": "next", "label": "Next.js"},
                {"value": "react", "label": "React"},
            ],
            placeholder="Select framework...",
            multiselect=True,
            on_select=ctx.callback(handle_select),
        )
        ```
    """

    component_type: str = "Combobox"

    def __init__(
        self,
        options: list[dict[str, str]] | None = None,
        value: str | list[str] = "",
        placeholder: str = "Select...",
        search_placeholder: str = "Search...",
        empty_text: str = "No results found.",
        multiselect: bool = False,
        disabled: bool = False,
        on_select: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.options = options or []
        self.value = value
        self.placeholder = placeholder
        self.search_placeholder = search_placeholder
        self.empty_text = empty_text
        self.multiselect = multiselect
        self.disabled = disabled
        self.on_select = on_select

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "options": self.options,
                "value": self.value,
                "placeholder": self.placeholder,
                "search_placeholder": self.search_placeholder,
                "empty_text": self.empty_text,
                "multiselect": self.multiselect,
                "disabled": self.disabled,
                "on_select": self.on_select.serialize() if self.on_select else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class InputOTP(Component):
    """
    An input for one-time passwords.

    Example:
        ```python
        InputOTP(
            max_length=6,
            on_complete=ctx.callback(handle_complete),
        )
        ```
    """

    component_type: str = "InputOTP"

    def __init__(
        self,
        max_length: int = 6,
        value: str = "",
        disabled: bool = False,
        pattern: str | None = None,  # Regex pattern for each character
        on_change: Any = None,
        on_complete: Any = None,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.max_length = max_length
        self.value = value
        self.disabled = disabled
        self.pattern = pattern
        self.on_change = on_change
        self.on_complete = on_complete
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "max_length": self.max_length,
                "value": self.value,
                "disabled": self.disabled,
                "pattern": self.pattern,
                "on_change": self.on_change.serialize() if self.on_change else None,
                "on_complete": self.on_complete.serialize() if self.on_complete else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class InputOTPGroup(Component):
    """
    A group of OTP slots.

    Example:
        ```python
        InputOTPGroup(
            children=[
                InputOTPSlot(index=0),
                InputOTPSlot(index=1),
                InputOTPSlot(index=2),
            ]
        )
        ```
    """

    component_type: str = "InputOTPGroup"

    def __init__(
        self,
        children: list["Component"] | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        if children:
            self._children = children

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }


class InputOTPSlot(Component):
    """
    A single slot in an OTP input.

    Example:
        ```python
        InputOTPSlot(index=0)
        ```
    """

    component_type: str = "InputOTPSlot"

    def __init__(
        self,
        index: int = 0,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.index = index

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "index": self.index,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class InputOTPSeparator(Component):
    """
    A separator between OTP groups.

    Example:
        ```python
        InputOTPSeparator()
        ```
    """

    component_type: str = "InputOTPSeparator"

    def __init__(
        self,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }

