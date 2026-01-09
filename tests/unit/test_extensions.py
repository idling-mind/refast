"""Tests for the Refast extension system."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from refast import RefastApp
from refast.extensions import Extension
from refast.components.base import Component


# =============================================================================
# Test Fixtures
# =============================================================================


class MockComponent(Component):
    """Mock component for testing."""

    component_type = "MockComponent"

    def __init__(self, value: str = "", **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {"value": self.value},
            "children": [],
        }


class SampleExtension(Extension):
    """Test extension for testing."""

    name = "test-extension"
    version = "1.0.0"
    description = "A test extension"
    scripts = ["test.js"]
    styles = ["test.css"]

    def __init__(self, static_dir: Path | None = None):
        super().__init__()
        self._static_dir = static_dir

    @property
    def static_path(self) -> Path | None:
        return self._static_dir

    @property
    def components(self) -> list:
        return [MockComponent]


class MinimalExtension(Extension):
    """Minimal extension with just a name."""

    name = "minimal-ext"


# =============================================================================
# Extension Base Class Tests
# =============================================================================


class TestExtensionBase:
    """Tests for the Extension base class."""

    def test_extension_requires_name(self):
        """Extension must have a name."""

        class NoNameExtension(Extension):
            pass

        with pytest.raises(ValueError, match="must define a 'name' attribute"):
            NoNameExtension()

    def test_extension_with_name(self):
        """Extension with name should initialize."""
        ext = MinimalExtension()
        assert ext.name == "minimal-ext"
        assert ext.version == "0.0.0"
        assert ext.description == ""

    def test_extension_metadata(self):
        """Extension should have correct metadata."""
        ext = SampleExtension()
        assert ext.name == "test-extension"
        assert ext.version == "1.0.0"
        assert ext.description == "A test extension"

    def test_extension_scripts_and_styles(self):
        """Extension should list scripts and styles."""
        ext = SampleExtension()
        assert ext.scripts == ["test.js"]
        assert ext.styles == ["test.css"]

    def test_extension_components(self):
        """Extension should list components."""
        ext = SampleExtension()
        assert MockComponent in ext.components

    def test_extension_static_path_default(self):
        """Extension static_path defaults to None."""
        ext = MinimalExtension()
        assert ext.static_path is None

    def test_extension_repr(self):
        """Extension should have readable repr."""
        ext = SampleExtension()
        assert "SampleExtension" in repr(ext)
        assert "test-extension" in repr(ext)
        assert "1.0.0" in repr(ext)


class TestExtensionUrls:
    """Tests for extension URL generation."""

    def test_get_script_urls(self):
        """get_script_urls should return correct paths."""
        ext = SampleExtension()
        urls = ext.get_script_urls()
        assert urls == ["/static/ext/test-extension/test.js"]

    def test_get_style_urls(self):
        """get_style_urls should return correct paths."""
        ext = SampleExtension()
        urls = ext.get_style_urls()
        assert urls == ["/static/ext/test-extension/test.css"]

    def test_get_urls_with_multiple_files(self):
        """Should handle multiple scripts/styles."""

        class MultiFileExtension(Extension):
            name = "multi-ext"
            scripts = ["a.js", "b.js", "c.js"]
            styles = ["x.css", "y.css"]

        ext = MultiFileExtension()
        assert len(ext.get_script_urls()) == 3
        assert len(ext.get_style_urls()) == 2

    def test_get_urls_empty(self):
        """Should handle no scripts/styles."""
        ext = MinimalExtension()
        assert ext.get_script_urls() == []
        assert ext.get_style_urls() == []


class TestExtensionStaticFiles:
    """Tests for static file handling."""

    def test_get_static_file_path_no_static_path(self):
        """Should return None if no static_path."""
        ext = MinimalExtension()
        assert ext.get_static_file_path("test.js") is None

    def test_get_static_file_path_file_exists(self):
        """Should return path if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir)
            (static_dir / "test.js").write_text("// test")

            ext = SampleExtension(static_dir=static_dir)
            path = ext.get_static_file_path("test.js")

            assert path is not None
            assert path.exists()
            assert path.name == "test.js"

    def test_get_static_file_path_file_not_exists(self):
        """Should return None if file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir)
            ext = SampleExtension(static_dir=static_dir)
            path = ext.get_static_file_path("nonexistent.js")
            assert path is None


class TestExtensionValidation:
    """Tests for extension validation."""

    def test_validate_no_errors(self):
        """Minimal extension should validate without errors."""
        ext = MinimalExtension()
        errors = ext.validate()
        assert errors == []

    def test_validate_scripts_without_static_path(self):
        """Should error if scripts specified but no static_path."""

        class BadExtension(Extension):
            name = "bad-ext"
            scripts = ["test.js"]

        ext = BadExtension()
        errors = ext.validate()
        assert len(errors) == 1
        assert "no static_path" in errors[0]

    def test_validate_static_path_not_exists(self):
        """Should error if static_path doesn't exist."""
        ext = SampleExtension(static_dir=Path("/nonexistent/path"))
        errors = ext.validate()
        assert len(errors) == 1
        assert "does not exist" in errors[0]

    def test_validate_missing_script_file(self):
        """Should error if script file doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir)
            # Create directory but not the script file
            ext = SampleExtension(static_dir=static_dir)
            errors = ext.validate()
            assert any("test.js" in e and "not found" in e for e in errors)

    def test_validate_all_files_exist(self):
        """Should pass if all files exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir)
            (static_dir / "test.js").write_text("// test")
            (static_dir / "test.css").write_text("/* test */")

            ext = SampleExtension(static_dir=static_dir)
            errors = ext.validate()
            assert errors == []


# =============================================================================
# RefastApp Extension Integration Tests
# =============================================================================


class TestRefastAppExtensions:
    """Tests for RefastApp extension registration."""

    def test_app_starts_with_no_extensions(self):
        """App should start with empty extensions dict."""
        app = RefastApp(auto_discover_extensions=False)
        assert app.extensions == {}

    def test_register_extension(self):
        """Should register an extension."""
        app = RefastApp(auto_discover_extensions=False)
        ext = MinimalExtension()

        app.register_extension(ext)

        assert "minimal-ext" in app.extensions
        assert app.extensions["minimal-ext"] is ext

    def test_register_extension_via_constructor(self):
        """Should register extensions via constructor."""
        ext = MinimalExtension()
        app = RefastApp(
            extensions=[ext],
            auto_discover_extensions=False,
        )

        assert "minimal-ext" in app.extensions

    def test_register_duplicate_extension_raises(self):
        """Should raise if registering same extension twice."""
        app = RefastApp(auto_discover_extensions=False)
        ext = MinimalExtension()

        app.register_extension(ext)

        with pytest.raises(ValueError, match="already registered"):
            app.register_extension(ext)

    def test_register_non_extension_raises(self):
        """Should raise if registering non-Extension."""
        app = RefastApp(auto_discover_extensions=False)

        with pytest.raises(TypeError, match="Expected Extension instance"):
            app.register_extension("not an extension")  # type: ignore

    def test_get_extension(self):
        """Should get extension by name."""
        app = RefastApp(auto_discover_extensions=False)
        ext = MinimalExtension()
        app.register_extension(ext)

        result = app.get_extension("minimal-ext")
        assert result is ext

    def test_get_extension_not_found(self):
        """Should return None for unknown extension."""
        app = RefastApp(auto_discover_extensions=False)
        result = app.get_extension("unknown")
        assert result is None

    def test_on_register_hook_called(self):
        """on_register hook should be called."""

        class HookExtension(Extension):
            name = "hook-ext"
            registered_with = None

            def on_register(self, app):
                HookExtension.registered_with = app

        app = RefastApp(auto_discover_extensions=False)
        ext = HookExtension()
        app.register_extension(ext)

        assert HookExtension.registered_with is app


class TestExtensionDiscovery:
    """Tests for extension auto-discovery."""

    def test_discover_extensions_no_entry_points(self):
        """Should handle no entry points gracefully."""
        with patch("importlib.metadata.entry_points") as mock_eps:
            mock_eps.return_value = []
            app = RefastApp(auto_discover_extensions=True)
            assert app.extensions == {}

    def test_discover_extensions_with_entry_point(self):
        """Should load extensions from entry points."""

        class DiscoveredExtension(Extension):
            name = "discovered-ext"

        mock_ep = MagicMock()
        mock_ep.name = "discovered-ext"
        mock_ep.load.return_value = DiscoveredExtension

        with patch("importlib.metadata.entry_points") as mock_eps:
            mock_eps.return_value = [mock_ep]
            app = RefastApp(auto_discover_extensions=True)

            assert "discovered-ext" in app.extensions

    def test_discover_extensions_handles_load_error(self):
        """Should handle extension load errors gracefully."""
        mock_ep = MagicMock()
        mock_ep.name = "broken-ext"
        mock_ep.load.side_effect = ImportError("Module not found")

        with patch("importlib.metadata.entry_points") as mock_eps:
            mock_eps.return_value = [mock_ep]
            # Should not raise
            app = RefastApp(auto_discover_extensions=True)
            assert "broken-ext" not in app.extensions


# =============================================================================
# Router Integration Tests
# =============================================================================


class TestRouterExtensionIntegration:
    """Tests for router extension handling."""

    def test_extension_assets_in_html(self):
        """Extension assets should be included in HTML."""
        from refast.router import RefastRouter
        from refast.context import Context
        from refast.components import Container

        app = RefastApp(auto_discover_extensions=False)
        ext = SampleExtension()
        app.register_extension(ext)

        router = RefastRouter(app)

        # Create a mock context
        ctx = MagicMock(spec=Context)

        # Render HTML
        component = Container()
        html = router._render_html_shell(component, ctx)

        # Check extension assets are included
        assert '/static/ext/test-extension/test.js' in html
        assert '/static/ext/test-extension/test.css' in html

    def test_extension_assets_order(self):
        """Extension assets should come after core assets."""
        from refast.router import RefastRouter
        from refast.context import Context
        from refast.components import Container

        app = RefastApp(auto_discover_extensions=False)
        ext = SampleExtension()
        app.register_extension(ext)

        router = RefastRouter(app)
        ctx = MagicMock(spec=Context)
        component = Container()
        html = router._render_html_shell(component, ctx)

        # Extension JS should come after refast-client.js
        # (refast-client.js in body, extension scripts after)
        core_js_pos = html.find("refast-client.js")
        ext_js_pos = html.find("test-extension/test.js")

        # Extension CSS should come after refast-client.css
        core_css_pos = html.find("refast-client.css")
        ext_css_pos = html.find("test-extension/test.css")

        # Core assets first, then extensions
        if core_js_pos != -1 and ext_js_pos != -1:
            assert core_js_pos < ext_js_pos
        if core_css_pos != -1 and ext_css_pos != -1:
            assert core_css_pos < ext_css_pos


class TestExtensionStaticRouting:
    """Tests for extension static file routing."""

    @pytest.mark.asyncio
    async def test_serve_extension_static_file(self):
        """Should serve static files from extension."""
        from refast.router import RefastRouter

        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir)
            (static_dir / "test.js").write_text("console.log('test');")

            app = RefastApp(auto_discover_extensions=False)
            ext = SampleExtension(static_dir=static_dir)
            app.register_extension(ext)

            router = RefastRouter(app)

            # Call the handler
            response = await router._extension_static_handler(
                "test-extension", "test.js"
            )

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_serve_extension_static_unknown_extension(self):
        """Should return 404 for unknown extension."""
        from refast.router import RefastRouter

        app = RefastApp(auto_discover_extensions=False)
        router = RefastRouter(app)

        response = await router._extension_static_handler(
            "unknown-extension", "test.js"
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_serve_extension_static_unknown_file(self):
        """Should return 404 for unknown file."""
        from refast.router import RefastRouter

        with tempfile.TemporaryDirectory() as tmpdir:
            static_dir = Path(tmpdir)

            app = RefastApp(auto_discover_extensions=False)
            ext = SampleExtension(static_dir=static_dir)
            app.register_extension(ext)

            router = RefastRouter(app)

            response = await router._extension_static_handler(
                "test-extension", "nonexistent.js"
            )

            assert response.status_code == 404



