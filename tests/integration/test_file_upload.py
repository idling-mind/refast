"""Integration tests for the file upload/download HTTP endpoints."""

import io
import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import RefastApp
from refast.utils.temp_file_store import DiskFileStore, MemoryFileStore


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def memory_app() -> RefastApp:
    return RefastApp(title="Upload Test", file_store=MemoryFileStore(max_size_bytes=1024))


@pytest.fixture
def memory_client(memory_app: RefastApp) -> TestClient:
    fastapi = FastAPI()
    fastapi.include_router(memory_app.router, prefix="")
    return TestClient(fastapi)


@pytest.fixture
def disk_app(tmp_path) -> RefastApp:
    store = DiskFileStore(max_size_bytes=1024, directory=str(tmp_path))
    return RefastApp(title="Disk Upload Test", file_store=store)


@pytest.fixture
def disk_client(disk_app: RefastApp) -> TestClient:
    fastapi = FastAPI()
    fastapi.include_router(disk_app.router, prefix="")
    return TestClient(fastapi)


def _multipart(filename: str, content: bytes, content_type: str = "text/plain"):
    """Return a files dict suitable for requests' multipart upload."""
    return [("files", (filename, io.BytesIO(content), content_type))]


# ─── POST /api/upload ─────────────────────────────────────────────────────────


class TestUploadEndpoint:
    def test_upload_single_file_returns_200(self, memory_client):
        resp = memory_client.post(
            "/api/upload",
            files=_multipart("hello.txt", b"hello world"),
        )
        assert resp.status_code == 200

    def test_upload_response_structure(self, memory_client):
        resp = memory_client.post(
            "/api/upload",
            files=_multipart("hello.txt", b"hello world"),
        )
        body = resp.json()
        assert "files" in body
        assert len(body["files"]) == 1
        f = body["files"][0]
        assert "id" in f
        assert f["name"] == "hello.txt"
        assert f["size"] == 11
        assert "content_type" in f

    def test_upload_multiple_files(self, memory_client):
        resp = memory_client.post(
            "/api/upload",
            files=[
                ("files", ("a.txt", io.BytesIO(b"aaa"), "text/plain")),
                ("files", ("b.txt", io.BytesIO(b"bbbb"), "text/plain")),
            ],
        )
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["files"]) == 2
        names = {f["name"] for f in body["files"]}
        assert names == {"a.txt", "b.txt"}

    def test_upload_file_exceeds_size_returns_413(self, memory_client):
        big = b"x" * 2048  # > 1024 byte limit
        resp = memory_client.post(
            "/api/upload",
            files=_multipart("big.bin", big),
        )
        assert resp.status_code == 413

    def test_upload_413_body_contains_error(self, memory_client):
        resp = memory_client.post(
            "/api/upload",
            files=_multipart("big.bin", b"x" * 2048),
        )
        body = resp.json()
        assert "error" in body

    def test_upload_stores_file_in_memory_store(self, memory_app, memory_client):
        resp = memory_client.post(
            "/api/upload",
            files=_multipart("stored.txt", b"stored content"),
        )
        file_id = resp.json()["files"][0]["id"]
        # Retrieve from store directly to verify storage
        import asyncio

        data = asyncio.run(memory_app.file_store.get_file(file_id))
        assert data == b"stored content"

    def test_upload_stores_file_on_disk(self, disk_app, disk_client, tmp_path):
        resp = disk_client.post(
            "/api/upload",
            files=_multipart("disk.bin", b"on disk"),
        )
        assert resp.status_code == 200
        file_id = resp.json()["files"][0]["id"]
        assert (tmp_path / file_id).exists()


# ─── GET /api/file/{file_id} ─────────────────────────────────────────────────


class TestFileEndpoint:
    def _upload(self, client, content: bytes, filename: str = "f.bin") -> str:
        resp = client.post("/api/upload", files=_multipart(filename, content))
        assert resp.status_code == 200
        return resp.json()["files"][0]["id"]

    def test_download_returns_200(self, memory_client):
        fid = self._upload(memory_client, b"data")
        resp = memory_client.get(f"/api/file/{fid}")
        assert resp.status_code == 200

    def test_download_content(self, memory_client):
        fid = self._upload(memory_client, b"exact bytes")
        resp = memory_client.get(f"/api/file/{fid}")
        assert resp.content == b"exact bytes"

    def test_download_content_disposition_attachment(self, memory_client):
        fid = self._upload(memory_client, b"dl", "report.pdf")
        resp = memory_client.get(f"/api/file/{fid}")
        cd = resp.headers.get("content-disposition", "")
        assert "attachment" in cd
        assert "report.pdf" in cd

    def test_unknown_id_returns_404(self, memory_client):
        resp = memory_client.get("/api/file/no-such-uuid")
        assert resp.status_code == 404

    def test_404_body_has_error_key(self, memory_client):
        resp = memory_client.get("/api/file/no-such-uuid")
        assert "error" in resp.json()

    def test_download_correct_content_type(self, memory_client):
        fid = self._upload(memory_client, b"\x89PNG", "img.png")
        # The upload stores with the uploaded content-type; we check it's set
        resp = memory_client.get(f"/api/file/{fid}")
        assert resp.status_code == 200

    def test_expired_file_returns_404(self, memory_app, memory_client):
        import asyncio
        import time

        fid = self._upload(memory_client, b"temp")
        # Force expiry in the store
        data, meta, _ = memory_app.file_store._files[fid]
        memory_app.file_store._files[fid] = (data, meta, time.monotonic() - 1)
        resp = memory_client.get(f"/api/file/{fid}")
        assert resp.status_code == 404


# ─── ctx.create_file_url & ctx.trigger_download ──────────────────────────────


class TestContextFileMethods:
    @pytest.mark.asyncio
    async def test_create_file_url_returns_path(self):
        app = RefastApp()
        from refast.context import Context

        ctx = Context(app=app)
        url = await ctx.create_file_url(b"bytes", "test.bin")
        assert url.startswith("/api/file/")
        # UUID portion: remove prefix and check it's 36 chars
        uid = url.removeprefix("/api/file/")
        assert len(uid) == 36

    @pytest.mark.asyncio
    async def test_create_file_url_stores_file(self):
        app = RefastApp()
        from refast.context import Context

        ctx = Context(app=app)
        content = b"my file content"
        url = await ctx.create_file_url(content, "out.bin")
        file_id = url.removeprefix("/api/file/")
        stored = await app.file_store.get_file(file_id)
        assert stored == content

    @pytest.mark.asyncio
    async def test_create_file_url_inline_flag(self):
        app = RefastApp()
        from refast.context import Context

        ctx = Context(app=app)
        url = await ctx.create_file_url(b"img", "img.png", "image/png", inline=True)
        file_id = url.removeprefix("/api/file/")
        info = await app.file_store.get_file_info(file_id)
        assert info is not None
        assert info.inline is True

    @pytest.mark.asyncio
    async def test_trigger_download_sends_js_exec(self):
        """trigger_download must send a js_exec WS message."""
        from unittest.mock import AsyncMock, MagicMock

        app = RefastApp()
        from refast.context import Context

        ws = MagicMock()
        ws.send_json = AsyncMock()
        ctx = Context(websocket=ws, app=app)

        await ctx.trigger_download("/api/file/some-id", "report.csv")

        ws.send_json.assert_called_once()
        call_args = ws.send_json.call_args[0][0]
        assert call_args["type"] == "js_exec"
        assert "args" in call_args
        assert call_args["args"]["url"] == "/api/file/some-id"
        assert call_args["args"]["filename"] == "report.csv"

    @pytest.mark.asyncio
    async def test_trigger_download_js_contains_anchor_trick(self):
        from unittest.mock import AsyncMock, MagicMock

        app = RefastApp()
        from refast.context import Context

        ws = MagicMock()
        ws.send_json = AsyncMock()
        ctx = Context(websocket=ws, app=app)
        await ctx.trigger_download("/some/url", "file.zip")

        code = ws.send_json.call_args[0][0]["code"]
        assert "createElement" in code
        assert "a.click" in code

    @pytest.mark.asyncio
    async def test_create_file_url_raises_without_app(self):
        from refast.context import Context

        ctx = Context()
        with pytest.raises(RuntimeError, match="no associated app"):
            await ctx.create_file_url(b"x", "x.bin")
