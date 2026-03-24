"""Advanced form control components based on shadcn/ui."""

from typing import Any, Literal

from refast.components.base import ChildrenType, Component


class Switch(Component):
    """
    Toggle switch component.

    Example:
        ```python
        Switch(
            id="airplane-mode",
            checked=True,
            on_checked_change=ctx.callback(handle_change),
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
        on_checked_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.checked = checked
        self.default_checked = default_checked
        self.disabled = disabled
        self.name = name
        self.on_checked_change = on_checked_change

    def render(self) -> dict[str, Any]:
        props = {
            "disabled": self.disabled,
            "name": self.name,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.on_checked_change:
            props["on_checked_change"] = self.on_checked_change.serialize()

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
            label="Volume",
            description="Adjust the volume level",
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
        label: str | None = None,
        description: str | None = None,
        required: bool = False,
        error: str | None = None,
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
        self.label = label
        self.description = description
        self.required = required
        self.error = error
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
            "label": self.label,
            "description": self.description,
            "required": self.required,
            "error": self.error,
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
        size: Literal["sm", "md", "lg"] = "md",
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
        size: Literal["sm", "md", "lg"] = "md",
        on_value_change: Any = None,
        children: ChildrenType = None,
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
        self.add_children(children)

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
    Inline calendar component for date selection.

    Supports single, multiple, and range selection modes. Renders directly in the page
    without a popover trigger. For a trigger-based picker use ``DatePicker``.

    Example:
        ```python
        from refast.components.shadcn.controls import Calendar
        from datetime import date

        # Single date selection
        Calendar(
            mode="single",
            selected=date(2026, 4, 15),
            on_select=ctx.callback(handle_select),
        )

        # Date range with dropdown navigation and boundaries
        Calendar(
            mode="range",
            caption_layout="dropdown",
            min_date=date(2024, 1, 1),
            max_date=date(2026, 12, 31),
            on_select=ctx.callback(handle_range_select),
        )
        ```

    Args:
        mode: Selection mode — ``"single"``, ``"multiple"``, or ``"range"``.
        caption_layout: Calendar header style — ``"label"``, ``"dropdown"`` (month + year
            dropdowns), ``"dropdown-months"``, or ``"dropdown-years"``.
        selected: Controlled selected date(s). Pass a ``date`` for single/multiple mode,
            or a ``dict`` with ``"from"`` and ``"to"`` keys for range mode.
        default_month: Initial month to display.
        disabled: Disables all interaction.
        show_outside_days: Show days from adjacent months in the grid.
        show_week_number: Show week numbers in the calendar grid.
        min_date: Earliest selectable date (``date`` or ISO 8601 string).
        max_date: Latest selectable date (``date`` or ISO 8601 string).
        number_of_months: Number of months displayed simultaneously.
        on_select: Callback fired when the selection changes.
        on_month_change: Callback fired when the displayed month changes.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Calendar"

    def __init__(
        self,
        mode: Literal["single", "multiple", "range"] = "single",
        caption_layout: Literal["label", "dropdown", "dropdown-months", "dropdown-years"] = "label",
        selected: Any = None,  # date, list[date], or DateRange
        default_month: Any = None,  # date
        disabled: bool = False,
        show_outside_days: bool = True,
        show_week_number: bool = False,
        min_date: Any = None,  # date or ISO string - dates before this are disabled
        max_date: Any = None,  # date or ISO string - dates after this are disabled
        number_of_months: int | None = None,
        on_select: Any = None,
        on_month_change: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.mode = mode
        self.caption_layout = caption_layout
        self.selected = selected
        self.default_month = default_month
        self.disabled = disabled
        self.show_outside_days = show_outside_days
        self.show_week_number = show_week_number
        self.min_date = min_date
        self.max_date = max_date
        self.number_of_months = number_of_months
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
        props: dict[str, Any] = {
            "mode": self.mode,
            "caption_layout": self.caption_layout,
            "selected": self._serialize_date(self.selected),
            "default_month": self._serialize_date(self.default_month),
            "disabled": self.disabled,
            "show_outside_days": self.show_outside_days,
            "show_week_number": self.show_week_number,
            "min_date": self._serialize_date(self.min_date),
            "max_date": self._serialize_date(self.max_date),
            "number_of_months": self.number_of_months,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        if self.on_select:
            props["on_select"] = self.on_select.serialize()
        if self.on_month_change:
            props["on_month_change"] = self.on_month_change.serialize()
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class DatePicker(Component):
    """
    Date picker with a button trigger that opens a calendar popover.

    Supports single, multiple, and range date selection. Date values can be Python
    ``date``/``datetime`` objects or ISO 8601 strings. Range mode expects a ``dict``
    with ``"from"`` and ``"to"`` keys.

    Example:
        ```python
        from refast.components.shadcn.controls import DatePicker
        from datetime import date

        # Single date picker with label and validation
        DatePicker(
            label="Appointment date",
            description="Select the date of your appointment.",
            value=date(2026, 4, 15),
            placeholder="Pick a date",
            required=True,
            on_change=ctx.callback(handle_date_change),
        )

        # Date range picker with month/year navigation dropdowns
        DatePicker(
            label="Report period",
            mode="range",
            caption_layout="dropdown",
            placeholder="Select date range",
            min_date=date(2024, 1, 1),
            max_date=date(2026, 12, 31),
            on_change=ctx.callback(handle_range_change),
        )
        ```

    Args:
        value: Controlled selected value. Pass a ``date`` for single mode, a
            ``list[date]`` for multiple mode, or a ``dict`` with ``"from"``/``"to"``
            keys for range mode.
        placeholder: Button text shown when no date is selected.
        disabled: Disables the picker.
        format: ``date-fns`` format string used for the button label (default ``"PPP"``
            renders as ``"April 15, 2026"`` in en-US locale).
        mode: Selection mode — ``"single"``, ``"multiple"``, or ``"range"``.
        caption_layout: Calendar header style — ``"label"``, ``"dropdown"`` (month +
            year dropdowns), ``"dropdown-months"``, or ``"dropdown-years"``.
        min_date: Earliest selectable date (``date`` or ISO 8601 string).
        max_date: Latest selectable date (``date`` or ISO 8601 string).
        number_of_months: Number of calendar months shown simultaneously.
        label: Label text displayed above the picker.
        description: Help text displayed below the label.
        required: Shows a required asterisk.
        error: Error message displayed below the picker.
        on_change: Callback fired when the selection changes.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "DatePicker"

    def __init__(
        self,
        value: Any = None,  # date, list[date], or {"from": date, "to": date} for range
        placeholder: str = "Pick a date",
        disabled: bool = False,
        format: str = "PPP",  # date-fns format
        mode: Literal["single", "multiple", "range"] = "single",
        caption_layout: Literal["label", "dropdown", "dropdown-months", "dropdown-years"] = "label",
        min_date: Any = None,  # date or ISO string
        max_date: Any = None,  # date or ISO string
        number_of_months: int | None = None,
        label: str | None = None,
        description: str | None = None,
        required: bool = False,
        error: str | None = None,
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
        self.mode = mode
        self.caption_layout = caption_layout
        self.min_date = min_date
        self.max_date = max_date
        self.number_of_months = number_of_months
        self.label = label
        self.description = description
        self.required = required
        self.error = error
        self.on_change = on_change

    def _serialize_date_value(self, d: Any) -> str | list[str] | dict[str, str | None] | None:
        """Serialize date value to ISO string, list of ISO strings, or range object."""
        if d is None:
            return None
        if hasattr(d, "isoformat"):
            return d.isoformat()
        if isinstance(d, list):
            return [item.isoformat() if hasattr(item, "isoformat") else str(item) for item in d]
        if isinstance(d, dict):
            # Range mode: {"from": date, "to": date}
            return {
                "from": d.get("from").isoformat()
                if d.get("from") and hasattr(d.get("from"), "isoformat")
                else d.get("from"),
                "to": d.get("to").isoformat()
                if d.get("to") and hasattr(d.get("to"), "isoformat")
                else d.get("to"),
            }
        return str(d)

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "value": self._serialize_date_value(self.value),
            "placeholder": self.placeholder,
            "disabled": self.disabled,
            "format": self.format,
            "mode": self.mode,
            "caption_layout": self.caption_layout,
            "min_date": self.min_date.isoformat()
            if hasattr(self.min_date, "isoformat")
            else self.min_date,
            "max_date": self.max_date.isoformat()
            if hasattr(self.max_date, "isoformat")
            else self.max_date,
            "number_of_months": self.number_of_months,
            "label": self.label,
            "description": self.description,
            "required": self.required,
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


class Combobox(Component):
    """
    Searchable select with type-ahead filtering and optional multi-select.

    Options are plain dicts with ``value`` and ``label`` keys. In single-select mode
    the ``on_select`` callback receives the selected ``str`` value; in multi-select mode
    it receives a ``list[str]`` of all selected values.

    Example:
        ```python
        from refast.components.shadcn.controls import Combobox

        # Single-select
        Combobox(
            label="Framework",
            description="Select your primary framework.",
            options=[
                {"value": "next",   "label": "Next.js"},
                {"value": "react",  "label": "React"},
                {"value": "vue",    "label": "Vue"},
            ],
            placeholder="Select framework…",
            search_placeholder="Search frameworks…",
            empty_text="No frameworks found.",
            required=True,
            on_select=ctx.callback(handle_select),
        )

        # Multi-select with pre-selected values
        Combobox(
            label="Tags",
            options=[
                {"value": "python", "label": "Python"},
                {"value": "ts",     "label": "TypeScript"},
            ],
            multiselect=True,
            value=["python"],
            on_select=ctx.callback(handle_tags),
        )
        ```

    Args:
        options: List of ``{"value": str, "label": str}`` dicts.
        value: Controlled selected value(s). Pass a ``str`` for single-select or a
            ``list[str]`` for multi-select.
        placeholder: Trigger button text when nothing is selected.
        search_placeholder: Placeholder inside the search input.
        empty_text: Text shown when no options match the current search.
        multiselect: Allow selecting multiple values simultaneously.
        disabled: Disables the combobox.
        label: Label text displayed above the combobox.
        description: Help text displayed below the label.
        required: Shows a required asterisk.
        error: Error message displayed below the combobox.
        on_select: Callback fired when the selection changes.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "Combobox"

    def __init__(
        self,
        options: list[dict[str, str]] | None = None,
        value: str | list[str] | None = None,
        placeholder: str = "Select...",
        search_placeholder: str = "Search...",
        empty_text: str = "No results found.",
        multiselect: bool = False,
        disabled: bool = False,
        label: str | None = None,
        description: str | None = None,
        required: bool = False,
        error: str | None = None,
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
        self.label = label
        self.description = description
        self.required = required
        self.error = error
        self.on_select = on_select

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "options": self.options,
            **({"value": self.value} if self.value is not None else {}),
            "placeholder": self.placeholder,
            "search_placeholder": self.search_placeholder,
            "empty_text": self.empty_text,
            "multiselect": self.multiselect,
            "disabled": self.disabled,
            "label": self.label,
            "description": self.description,
            "required": self.required,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        if self.on_select:
            props["on_select"] = self.on_select.serialize()
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }


class InputOTP(Component):
    """
    One-time password input composed from individual slot primitives.

    The simplest usage passes only ``max_length`` and lets the component auto-generate
    its layout. For a custom layout (e.g. two groups of three separated by a dash),
    compose ``InputOTPGroup``, ``InputOTPSlot``, and ``InputOTPSeparator`` as children.

    Example:
        ```python
        from refast.components.shadcn.controls import (
            InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator,
        )

        # Simple 6-digit OTP (auto-layout)
        InputOTP(
            label="Verification Code",
            description="Enter the 6-digit code sent to your email.",
            max_length=6,
            required=True,
            on_complete=ctx.callback(handle_complete),
        )

        # Custom layout: two groups of 3 separated by a dash
        InputOTP(
            max_length=6,
            on_complete=ctx.callback(handle_complete),
            children=[
                InputOTPGroup(children=[
                    InputOTPSlot(index=0),
                    InputOTPSlot(index=1),
                    InputOTPSlot(index=2),
                ]),
                InputOTPSeparator(),
                InputOTPGroup(children=[
                    InputOTPSlot(index=3),
                    InputOTPSlot(index=4),
                    InputOTPSlot(index=5),
                ]),
            ],
        )
        ```

    Args:
        max_length: Total number of OTP characters.
        value: Controlled OTP value string.
        disabled: Disables the input.
        pattern: Optional regex pattern to validate each character (e.g. ``"[0-9]"``).
        label: Label text displayed above the input.
        description: Help text displayed below the label.
        required: Shows a required asterisk.
        error: Error message displayed below the input.
        on_change: Callback fired on every character change.
        on_complete: Callback fired when all slots are filled.
        children: Custom layout using ``InputOTPGroup``, ``InputOTPSlot``, and
            ``InputOTPSeparator``. If omitted, an auto-layout is generated.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "InputOTP"

    def __init__(
        self,
        max_length: int = 6,
        value: str | None = None,
        disabled: bool = False,
        pattern: str | None = None,  # Regex pattern for each character
        label: str | None = None,
        description: str | None = None,
        required: bool = False,
        error: str | None = None,
        on_change: Any = None,
        on_complete: Any = None,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.max_length = max_length
        self.value = value
        self.disabled = disabled
        self.pattern = pattern
        self.label = label
        self.description = description
        self.required = required
        self.error = error
        self.on_change = on_change
        self.on_complete = on_complete
        self.add_children(children)

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "max_length": self.max_length,
            **({"value": self.value} if self.value is not None else {}),
            "disabled": self.disabled,
            "pattern": self.pattern,
            "label": self.label,
            "description": self.description,
            "required": self.required,
            "error": self.error,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }
        if self.on_change:
            props["on_change"] = self.on_change.serialize()
        if self.on_complete:
            props["on_complete"] = self.on_complete.serialize()
        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


class InputOTPGroup(Component):
    """
    A group of contiguous OTP slots within an ``InputOTP``.

    Group multiple ``InputOTPSlot`` components together and optionally separate groups
    with ``InputOTPSeparator``.

    Example:
        ```python
        from refast.components.shadcn.controls import InputOTPGroup, InputOTPSlot

        InputOTPGroup(
            children=[
                InputOTPSlot(index=0),
                InputOTPSlot(index=1),
                InputOTPSlot(index=2),
            ],
        )
        ```

    Args:
        children: ``InputOTPSlot`` components in this group.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
    """

    component_type: str = "InputOTPGroup"

    def __init__(
        self,
        children: ChildrenType = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.add_children(children)

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
    A single character slot in an ``InputOTP``.

    The ``index`` must match the slot's zero-based position within the parent
    ``InputOTP`` (not within its group).

    Example:
        ```python
        from refast.components.shadcn.controls import InputOTPSlot

        InputOTPSlot(index=0)
        ```

    Args:
        index: Zero-based slot index within the parent ``InputOTP``.
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
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
    A visual separator rendered between ``InputOTPGroup`` components.

    Renders a dash (``—``) character to visually divide slot groups. Accepts no content
    props.

    Example:
        ```python
        from refast.components.shadcn.controls import InputOTPSeparator

        InputOTPSeparator()
        ```

    Args:
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes.
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
