"""Form components."""

from typing import Any

from refast.components.base import ChildrenType, Component


class Form(Component):
    """
    Form container component.

    Example:
        ```python
        Form(
            on_submit=ctx.callback(handle_submit),
            children=[
                FormField(
                    label="Email",
                    children=[Input(name="email", type="email")]
                ),
                Button("Submit", type="submit"),
            ]
        )
        ```
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
    """Form field wrapper with label and error handling."""

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
    """Form label component."""

    component_type: str = "Label"

    def __init__(
        self,
        text: str,
        html_for: str | None = None,
        required: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text
        self.html_for = html_for
        self.required = required

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "html_for": self.html_for,
                "required": self.required,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.text],
        }
