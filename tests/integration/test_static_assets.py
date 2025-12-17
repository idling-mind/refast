"""Tests for static file serving and asset bundling."""

import pytest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast import RefastApp, Context
from refast.components import Text
from refast.router import STATIC_DIR


class TestStaticFileServing:
    """Test static file serving."""

    @pytest.fixture
    def ui_app(self):
        """Create a Refast app."""
        ui = RefastApp()

        @ui.page("/")
        def home(ctx: Context):
            return Text("Home")

        return ui

    @pytest.fixture
    def client(self, ui_app):
        """Create test client."""
        app = FastAPI()
        app.include_router(ui_app.router)
        return TestClient(app)

    def test_static_dir_exists(self):
        """Test that static directory exists."""
        assert STATIC_DIR.exists()
        assert STATIC_DIR.is_dir()

    def test_static_dir_has_init(self):
        """Test that static directory has __init__.py."""
        init_file = STATIC_DIR / "__init__.py"
        assert init_file.exists()

    def test_missing_static_file_returns_404(self, client):
        """Test that missing static files return 404."""
        response = client.get("/static/nonexistent.js")
        assert response.status_code == 404


class TestBuildScript:
    """Test build script functionality."""

    def test_build_script_exists(self):
        """Test that build script exists."""
        # tests/integration/test_static_assets.py -> go up 3 levels to get project root
        project_root = Path(__file__).parent.parent.parent
        build_script = project_root / "scripts" / "build.py"
        assert build_script.exists(), f"Expected {build_script} to exist"

    def test_build_script_is_valid_python(self):
        """Test that build script is valid Python."""
        project_root = Path(__file__).parent.parent.parent
        build_script = project_root / "scripts" / "build.py"
        
        with open(build_script) as f:
            content = f.read()
        
        # This will raise SyntaxError if invalid
        compile(content, str(build_script), "exec")

    def test_build_script_has_main(self):
        """Test that build script has main function."""
        project_root = Path(__file__).parent.parent.parent
        build_script = project_root / "scripts" / "build.py"
        
        with open(build_script) as f:
            content = f.read()
        
        assert "def main(" in content
        assert "if __name__" in content
