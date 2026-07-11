"""FileUploader component."""

from typing import Any, Literal

from refast.components.base import Component


class FileUploader(Component):
    """
    A file upload component with drag-and-drop support.

    Supports two visual variants: a large dashed drop-zone (``"dropzone"``)
    or a compact button (``"button"``).  In both variants drag-and-drop can
    be enabled/disabled independently via *drag_drop*.

    Files are uploaded via a multipart ``POST`` to *upload_url* (which must
    be served by the same Refast router, or a compatible endpoint).  Per-file
    progress bars are displayed automatically via XHR ``onprogress`` events
    inside the component — no server callback is required for progress tracking.

    Example:
        ```python
        async def handle_upload(ctx: Context, files: list[dict]):
            for f in files:
                data = await ctx.app.file_store.get_file(f["id"])
                # process data …
            await ctx.show_toast(f"Uploaded {len(files)} file(s)", variant="success")

        async def handle_error(ctx: Context, error: str, file: dict):
            await ctx.show_toast(f"Error: {error}", variant="error")

        FileUploader(
            label="Drop files here",
            description="PNG, JPG up to 5 MB",
            accept="image/*",
            multiple=True,
            max_size=5 * 1024 * 1024,
            on_upload_complete=ctx.callback(handle_upload),
            on_upload_error=ctx.callback(handle_error),
        )
        ```

    Args:
        label: Heading text inside the drop-zone or the button label.
        description: Secondary text shown below *label*.
        variant: Visual style — ``"dropzone"`` (large zone) or ``"button"``
            (compact button that opens the file picker).
        disabled: When ``True`` the component is non-interactive.
        required: Shows a required asterisk next to the label.
        error: Server-set error message displayed below the component.
        accept: MIME type filter passed to the ``<input>`` element,
            e.g. ``"image/*"`` or ``".pdf,.docx"``.
        multiple: Allow selecting/dropping multiple files at once.
        max_size: Maximum allowed file size **in bytes** (client-side guard).
            Files exceeding this are rejected before upload starts.
        max_files: Maximum number of files accepted in one interaction.
            Only meaningful when *multiple* is ``True``.
        drag_drop: Enable drag-and-drop onto the component. ``True`` by
            default for both variants.
        upload_url: URL the component POSTs files to.  Override when the
            Refast router is mounted under a custom prefix.
        on_select: Fired when the user picks files **before** upload begins.
            ``eventData``: ``{ files: [{ name, size, type }] }``
        on_upload_start: Fired when the HTTP upload starts.
            ``eventData``: ``{ files: [{ name, size, type }] }``
        on_upload_complete: Fired when **all** files have been uploaded.
            ``eventData``: ``{ files: [{ id, name, size, content_type }] }``
        on_upload_error: Fired on a network or server error.
            ``eventData``: ``{ error: str, file: { name } }``
        on_remove: Fired when the user removes a file from the list.
            ``eventData``: ``{ file: { name, size, type } }``
        id: Component ID (auto-generated if omitted).
        class_name: Additional Tailwind CSS classes applied to the root element.
    """

    component_type: str = "FileUploader"

    def __init__(
        self,
        label: str = "Upload file",
        description: str | None = None,
        variant: Literal["dropzone", "button"] = "dropzone",
        disabled: bool = False,
        required: bool = False,
        error: str | None = None,
        accept: str | None = None,
        multiple: bool = False,
        max_size: int | None = None,
        max_files: int | None = None,
        drag_drop: bool = True,
        upload_url: str = "/api/upload",
        on_select: Any = None,
        on_upload_start: Any = None,
        on_upload_complete: Any = None,
        on_upload_error: Any = None,
        on_remove: Any = None,
        name: str | None = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.label = label
        self.description = description
        self.variant = variant
        self.disabled = disabled
        self.required = required
        self.error = error
        self.accept = accept
        self.multiple = multiple
        self.max_size = max_size
        self.max_files = max_files
        self.drag_drop = drag_drop
        self.upload_url = upload_url
        self.on_select = on_select
        self.on_upload_start = on_upload_start
        self.on_upload_complete = on_upload_complete
        self.on_upload_error = on_upload_error
        self.on_remove = on_remove
        self.name = name

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "label": self.label,
            "description": self.description,
            "variant": self.variant,
            "disabled": self.disabled,
            "required": self.required,
            "error": self.error,
            "multiple": self.multiple,
            "drag_drop": self.drag_drop,
            "upload_url": self.upload_url,
            "name": self.name,
            "class_name": self.class_name,
            **self._serialize_extra_props(),
        }

        if self.accept is not None:
            props["accept"] = self.accept
        if self.max_size is not None:
            props["max_size"] = self.max_size
        if self.max_files is not None:
            props["max_files"] = self.max_files

        if self.on_select is not None:
            props["on_select"] = self.on_select.serialize()
        if self.on_upload_start is not None:
            props["on_upload_start"] = self.on_upload_start.serialize()
        if self.on_upload_complete is not None:
            props["on_upload_complete"] = self.on_upload_complete.serialize()
        if self.on_upload_error is not None:
            props["on_upload_error"] = self.on_upload_error.serialize()
        if self.on_remove is not None:
            props["on_remove"] = self.on_remove.serialize()

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }
