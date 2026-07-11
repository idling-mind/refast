"""Unit tests for the FileUploader component."""

import pytest

from refast import Context, RefastApp
from refast.components.shadcn.file_uploader import FileUploader


@pytest.fixture
def ctx():
    app = RefastApp()
    return Context(app=app)


class TestFileUploaderDefaults:
    def test_component_type(self):
        fu = FileUploader()
        assert fu.render()["type"] == "FileUploader"

    def test_has_id(self):
        fu = FileUploader()
        rendered = fu.render()
        assert "id" in rendered
        assert rendered["id"] is not None

    def test_custom_id(self):
        fu = FileUploader(id="my-uploader")
        assert fu.render()["id"] == "my-uploader"

    def test_children_is_empty_list(self):
        fu = FileUploader()
        assert fu.render()["children"] == []

    def test_default_label(self):
        fu = FileUploader()
        assert fu.render()["props"]["label"] == "Upload file"

    def test_default_variant(self):
        fu = FileUploader()
        assert fu.render()["props"]["variant"] == "dropzone"

    def test_default_multiple_false(self):
        fu = FileUploader()
        assert fu.render()["props"]["multiple"] is False

    def test_default_disabled_false(self):
        fu = FileUploader()
        assert fu.render()["props"]["disabled"] is False

    def test_default_required_false(self):
        fu = FileUploader()
        assert fu.render()["props"]["required"] is False

    def test_default_drag_drop_true(self):
        fu = FileUploader()
        assert fu.render()["props"]["drag_drop"] is True

    def test_default_upload_url(self):
        fu = FileUploader()
        assert fu.render()["props"]["upload_url"] == "/api/upload"

    def test_no_callbacks_by_default(self):
        fu = FileUploader()
        props = fu.render()["props"]
        for key in (
            "on_select",
            "on_upload_start",
            "on_upload_complete",
            "on_upload_error",
            "on_remove",
        ):
            assert key not in props

    def test_optional_props_absent_by_default(self):
        props = FileUploader().render()["props"]
        assert "accept" not in props
        assert "max_size" not in props
        assert "max_files" not in props
        assert "description" not in props or props.get("description") is None
        assert "error" not in props or props.get("error") is None


class TestFileUploaderProps:
    def test_label(self):
        fu = FileUploader(label="Drop here")
        assert fu.render()["props"]["label"] == "Drop here"

    def test_description(self):
        fu = FileUploader(description="Max 5 MB")
        assert fu.render()["props"]["description"] == "Max 5 MB"

    def test_variant_button(self):
        fu = FileUploader(variant="button")
        assert fu.render()["props"]["variant"] == "button"

    def test_disabled(self):
        fu = FileUploader(disabled=True)
        assert fu.render()["props"]["disabled"] is True

    def test_required(self):
        fu = FileUploader(required=True)
        assert fu.render()["props"]["required"] is True

    def test_error(self):
        fu = FileUploader(error="Something went wrong")
        assert fu.render()["props"]["error"] == "Something went wrong"

    def test_accept(self):
        fu = FileUploader(accept="image/*")
        assert fu.render()["props"]["accept"] == "image/*"

    def test_multiple(self):
        fu = FileUploader(multiple=True)
        assert fu.render()["props"]["multiple"] is True

    def test_max_size(self):
        fu = FileUploader(max_size=5_242_880)
        assert fu.render()["props"]["max_size"] == 5_242_880

    def test_max_files(self):
        fu = FileUploader(max_files=3)
        assert fu.render()["props"]["max_files"] == 3

    def test_drag_drop_false(self):
        fu = FileUploader(drag_drop=False)
        assert fu.render()["props"]["drag_drop"] is False

    def test_custom_upload_url(self):
        fu = FileUploader(upload_url="/myapp/api/upload")
        assert fu.render()["props"]["upload_url"] == "/myapp/api/upload"

    def test_class_name(self):
        fu = FileUploader(class_name="mt-4")
        assert fu.render()["props"]["class_name"] == "mt-4"


class TestFileUploaderCallbacks:
    def _make_callback(self, ctx):
        async def handler(ctx):
            pass

        return ctx.callback(handler)

    def test_on_select_serialized(self, ctx):
        cb = self._make_callback(ctx)
        fu = FileUploader(on_select=cb)
        props = fu.render()["props"]
        assert "on_select" in props
        assert "callbackId" in props["on_select"]

    def test_on_upload_start_serialized(self, ctx):
        cb = self._make_callback(ctx)
        fu = FileUploader(on_upload_start=cb)
        props = fu.render()["props"]
        assert "on_upload_start" in props
        assert "callbackId" in props["on_upload_start"]

    def test_on_upload_complete_serialized(self, ctx):
        cb = self._make_callback(ctx)
        fu = FileUploader(on_upload_complete=cb)
        props = fu.render()["props"]
        assert "on_upload_complete" in props
        assert "callbackId" in props["on_upload_complete"]

    def test_on_upload_error_serialized(self, ctx):
        cb = self._make_callback(ctx)
        fu = FileUploader(on_upload_error=cb)
        props = fu.render()["props"]
        assert "on_upload_error" in props
        assert "callbackId" in props["on_upload_error"]

    def test_on_remove_serialized(self, ctx):
        cb = self._make_callback(ctx)
        fu = FileUploader(on_remove=cb)
        props = fu.render()["props"]
        assert "on_remove" in props
        assert "callbackId" in props["on_remove"]

    def test_all_callbacks_have_different_ids(self, ctx):
        async def h1(ctx):
            pass

        async def h2(ctx):
            pass

        async def h3(ctx):
            pass

        async def h4(ctx):
            pass

        async def h5(ctx):
            pass

        fu = FileUploader(
            on_select=ctx.callback(h1),
            on_upload_start=ctx.callback(h2),
            on_upload_complete=ctx.callback(h3),
            on_upload_error=ctx.callback(h4),
            on_remove=ctx.callback(h5),
        )
        props = fu.render()["props"]
        ids = [
            props["on_select"]["callbackId"],
            props["on_upload_start"]["callbackId"],
            props["on_upload_complete"]["callbackId"],
            props["on_upload_error"]["callbackId"],
            props["on_remove"]["callbackId"],
        ]
        assert len(ids) == len(set(ids)), "Callback IDs must be unique"

    def test_callback_with_bound_args(self, ctx):
        async def handler(ctx, folder_id: int):
            pass

        cb = ctx.callback(handler, folder_id=42)
        fu = FileUploader(on_upload_complete=cb)
        props = fu.render()["props"]
        assert props["on_upload_complete"]["boundArgs"]["folder_id"] == 42

    def test_file_uploader_name(self):
        fu = FileUploader(name="attachments")
        assert fu.render()["props"]["name"] == "attachments"
