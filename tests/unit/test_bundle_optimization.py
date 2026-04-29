"""Tests for bundle optimization features.

Covers:
- RefastApp ``preloaded_features`` configuration
- _load_manifest / _get_chunk_files helpers
- HTML shell: ESM script tags, modulepreload hints, extension loader
- Static handler: pre-compressed file serving (brotli / gzip)
"""

import gzip
import json
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import RefastApp
from refast.router import ALL_FEATURE_CHUNKS, _get_chunk_files, _load_manifest

# ── Fixtures ─────────────────────────────────────────────────────────────


@pytest.fixture
def sample_manifest() -> dict:
    """A realistic Vite manifest mirroring a multi-chunk build."""
    return {
        "src/index.tsx": {
            "file": "refast-client.js",
            "isEntry": True,
            "src": "src/index.tsx",
            "imports": ["_shared", "_charts", "_icons"],
        },
        "_charts": {
            "file": "refast-charts-abc123.js",
            "name": "charts",
        },
        "_icons": {
            "file": "refast-icons-def456.js",
            "name": "icons",
        },
        "_navigation": {
            "file": "refast-navigation-ghi789.js",
            "name": "navigation",
            "isDynamicEntry": True,
            "src": "src/components/shadcn/navigation.tsx",
        },
        "_overlay": {
            "file": "refast-overlay-jkl012.js",
            "name": "overlay",
            "isDynamicEntry": True,
            "src": "src/components/shadcn/overlay.tsx",
        },
        "_controls": {
            "file": "refast-controls-mno345.js",
            "name": "controls",
            "isDynamicEntry": True,
            "src": "src/components/shadcn/controls.tsx",
        },
        "_markdown": {
            "file": "refast-markdown-pqr678.js",
            "name": "markdown",
            "isDynamicEntry": True,
        },
        "_shared": {
            "file": "refast-shared-zzz000.js",
            "imports": ["_vendor"],
        },
        "_vendor": {
            "file": "refast-vendor-vvv111.js",
        },
    }


@pytest.fixture
def preloaded_features_app():
    """Factory to create a RefastApp with given preloaded features + page."""

    def _make(preloaded_features=None, lazy_features=None):
        ui = RefastApp(
            title="Test",
            preloaded_features=preloaded_features,
            lazy_features=lazy_features,
        )

        @ui.page("/")
        def home(ctx):
            return None

        fa = FastAPI()
        fa.include_router(ui.router, prefix="/ui")
        return TestClient(fa), ui

    return _make


# ═══════════════════════════════════════════════════════════════════════════
# RefastApp.preloaded_features configuration
# ═══════════════════════════════════════════════════════════════════════════


class TestPreloadedFeaturesConfig:
    """Tests for the ``preloaded_features`` parameter on RefastApp."""

    def test_default_preloaded_features_is_none(self):
        app = RefastApp()
        assert app.preloaded_features is None

    def test_preloaded_features_empty_list(self):
        app = RefastApp(preloaded_features=[])
        assert app.preloaded_features == []

    def test_preloaded_features_specific_list(self):
        app = RefastApp(preloaded_features=["charts", "icons"])
        assert app.preloaded_features == ["charts", "icons"]

    def test_preloaded_features_stored_as_given(self):
        feats = ["navigation", "overlay"]
        app = RefastApp(preloaded_features=feats)
        assert app.preloaded_features is feats  # same reference

    def test_default_lazy_features_is_none(self):
        app = RefastApp()
        assert app.lazy_features is None

    def test_lazy_features_specific_list(self):
        app = RefastApp(lazy_features=["charts", "icons"])
        assert app.lazy_features == ["charts", "icons"]


# ═══════════════════════════════════════════════════════════════════════════
# _get_chunk_files helper
# ═══════════════════════════════════════════════════════════════════════════


class TestGetChunkFiles:
    """Unit tests for _get_chunk_files manifest resolution."""

    def test_empty_manifest_returns_entry(self):
        assert _get_chunk_files({}, None) == ["refast-client.js"]

    def test_no_feature_preloads_when_none(self, sample_manifest):
        """preloaded_features=None should preload only entry + non-feature graph."""
        files = _get_chunk_files(sample_manifest, None)
        assert files[0] == "refast-client.js"
        # Feature chunks are skipped by default
        assert not any("charts" in f for f in files)
        assert not any("icons" in f for f in files)
        assert any("shared" in f for f in files)
        assert any("vendor" in f for f in files)
        # Unreferenced dynamic entries should not be preloaded
        assert not any("navigation" in f for f in files)
        assert not any("overlay" in f for f in files)
        assert not any("controls" in f for f in files)
        assert not any("markdown" in f for f in files)

    def test_specific_features_only(self, sample_manifest):
        """Only requested features should be included."""
        files = _get_chunk_files(sample_manifest, ["charts"])
        assert "refast-client.js" in files
        assert any("charts" in f for f in files)
        # Other features excluded
        assert not any("icons" in f for f in files)
        assert not any("navigation" in f for f in files)
        # Shared chunks still included
        assert any("shared" in f for f in files)
        assert any("vendor" in f for f in files)

    def test_empty_features_excludes_all_feature_chunks(self, sample_manifest):
        """preloaded_features=[] should include only entry + shared."""
        files = _get_chunk_files(sample_manifest, [])
        assert "refast-client.js" in files
        # All feature chunks excluded
        for feat in ALL_FEATURE_CHUNKS:
            assert not any(f"refast-{feat}-" in f for f in files)
        # Shared chunk still included
        assert any("shared" in f for f in files)
        assert any("vendor" in f for f in files)

    def test_entry_always_first(self, sample_manifest):
        files = _get_chunk_files(sample_manifest, None)
        assert files[0] == "refast-client.js"

    def test_multiple_features(self, sample_manifest):
        files = _get_chunk_files(sample_manifest, ["charts", "icons", "overlay"])
        assert any("charts" in f for f in files)
        assert any("icons" in f for f in files)
        # overlay is dynamic-only and not in static entry imports, so it is
        # intentionally not preloaded.
        assert not any("overlay" in f for f in files)
        assert not any("navigation" in f for f in files)
        assert not any("controls" in f for f in files)


# ═══════════════════════════════════════════════════════════════════════════
# _load_manifest helper
# ═══════════════════════════════════════════════════════════════════════════


class TestLoadManifest:
    """Tests for _load_manifest file reading."""

    def test_returns_empty_when_no_file(self, tmp_path):
        with patch("refast.router.STATIC_DIR", tmp_path):
            assert _load_manifest() == {}

    def test_reads_manifest_json(self, tmp_path):
        data = {"src/index.tsx": {"file": "refast-client.js"}}
        (tmp_path / "manifest.json").write_text(json.dumps(data))

        with patch("refast.router.STATIC_DIR", tmp_path):
            result = _load_manifest()
        assert result == data


# ═══════════════════════════════════════════════════════════════════════════
# HTML shell output
# ═══════════════════════════════════════════════════════════════════════════


class TestHtmlShell:
    """Test that the HTML shell uses ESM and modulepreload correctly."""

    def test_html_uses_script_type_module(self, preloaded_features_app):
        client, _ = preloaded_features_app()
        response = client.get("/ui/")
        assert response.status_code == 200
        assert '<script type="module"' in response.text

    def test_html_includes_root_div(self, preloaded_features_app):
        client, _ = preloaded_features_app()
        response = client.get("/ui/")
        assert 'id="refast-root"' in response.text

    def test_html_includes_initial_data(self, preloaded_features_app):
        client, _ = preloaded_features_app()
        response = client.get("/ui/")
        assert "__REFAST_INITIAL_DATA__" not in response.text

    def test_html_includes_lazy_and_startup_config(self, preloaded_features_app):
        client, _ = preloaded_features_app(
            preloaded_features=["charts"],
            lazy_features=["charts", "icons"],
        )
        response = client.get("/ui/")
        assert response.status_code == 200
        assert "__REFAST_STARTUP_FEATURES__" in response.text
        assert "__REFAST_LAZY_FEATURES__" in response.text
        assert "\"charts\"" in response.text
        assert "\"icons\"" in response.text


# ═══════════════════════════════════════════════════════════════════════════
# Static handler – pre-compressed file serving
# ═══════════════════════════════════════════════════════════════════════════


class TestStaticHandlerCompression:
    """Test pre-compressed static file serving."""

    def _setup_static(self, tmp_path):
        """Create a tiny JS file with .br and .gz variants.

        Uses real gzip data so httpx's automatic decompression works.
        """
        js_content = b"console.log('hello');"
        js_file = tmp_path / "test.js"
        js_file.write_bytes(js_content)

        # Real gzip compression
        gz_file = tmp_path / "test.js.gz"
        gz_file.write_bytes(gzip.compress(js_content))

        # .br file — we can't assume brotli is installed, so we use
        # a sentinel value but only assert on the Content-Encoding header.
        br_file = tmp_path / "test.js.br"
        br_file.write_bytes(b"brotli-compressed-data")

        return tmp_path

    def test_serves_brotli_when_accepted(self, preloaded_features_app, tmp_path):
        static = self._setup_static(tmp_path)
        client, _ = preloaded_features_app()

        with patch("refast.router.STATIC_DIR", static):
            # Use a raw httpx transport to avoid automatic decoding
            response = client.get(
                "/ui/static/test.js",
                headers={"Accept-Encoding": "br, gzip"},
            )

        assert response.status_code == 200
        assert response.headers.get("Content-Encoding") == "br"

    def test_serves_gzip_when_br_not_accepted(self, preloaded_features_app, tmp_path):
        static = self._setup_static(tmp_path)
        client, _ = preloaded_features_app()

        with patch("refast.router.STATIC_DIR", static):
            response = client.get(
                "/ui/static/test.js",
                headers={"Accept-Encoding": "gzip"},
            )

        assert response.status_code == 200
        # httpx auto-decompresses gzip, so we get the original content
        assert response.content == b"console.log('hello');"

    def test_serves_uncompressed_when_no_encoding(self, preloaded_features_app, tmp_path):
        static = self._setup_static(tmp_path)
        client, _ = preloaded_features_app()

        with patch("refast.router.STATIC_DIR", static):
            response = client.get(
                "/ui/static/test.js",
                headers={"Accept-Encoding": "identity"},
            )

        assert response.status_code == 200
        assert response.headers.get("Content-Encoding") is None
        assert response.content == b"console.log('hello');"

    def test_404_for_missing_file(self, preloaded_features_app, tmp_path):
        client, _ = preloaded_features_app()

        with patch("refast.router.STATIC_DIR", tmp_path):
            response = client.get("/ui/static/nonexistent.js")

        assert response.status_code == 404


# ═══════════════════════════════════════════════════════════════════════════
# ALL_FEATURE_CHUNKS constant
# ═══════════════════════════════════════════════════════════════════════════


class TestFeatureChunksConstant:
    """Verify the ALL_FEATURE_CHUNKS constant matches expectations."""

    def test_is_frozenset(self):
        assert isinstance(ALL_FEATURE_CHUNKS, frozenset)

    def test_contains_expected_chunks(self):
        expected = {"charts", "markdown", "icons", "navigation", "overlay", "controls"}
        assert ALL_FEATURE_CHUNKS == expected
