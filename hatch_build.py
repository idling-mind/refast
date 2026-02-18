"""Custom hatch build hook that builds the React frontend and copies assets to the Python package.

This hook runs automatically during `uv build` / `hatch build` so that the
published wheel and sdist always contain the compiled frontend bundle
(refast-client.js + refast-client.css) without requiring a separate manual step.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class FrontendBuildHook(BuildHookInterface):
    """Build the React frontend and copy assets into src/refast/static/."""

    PLUGIN_NAME = "frontend"

    # ------------------------------------------------------------------ #
    # Paths
    # ------------------------------------------------------------------ #

    @property
    def _frontend_dir(self) -> Path:
        return Path(self.root) / "src" / "refast-client"

    @property
    def _static_dir(self) -> Path:
        return Path(self.root) / "src" / "refast" / "static"

    @property
    def _dist_dir(self) -> Path:
        return self._frontend_dir / "dist"

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _run(self, cmd: list[str], *, cwd: Path | None = None) -> None:
        """Run a subprocess, raising on failure."""
        self.app.display_info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            shell=sys.platform == "win32",
        )
        if result.returncode != 0:
            self.app.display_error(result.stdout)
            self.app.display_error(result.stderr)
            msg = f"Command failed with exit code {result.returncode}: {' '.join(cmd)}"
            raise RuntimeError(msg)

    def _node_available(self) -> bool:
        """Check whether node and npm are on PATH."""
        for binary in ("node", "npm"):
            try:
                subprocess.run(
                    [binary, "--version"],
                    capture_output=True,
                    shell=sys.platform == "win32",
                )
            except FileNotFoundError:
                return False
        return True

    def _assets_exist(self) -> bool:
        """Return True if the compiled JS + CSS already exist in static/."""
        js = self._static_dir / "refast-client.js"
        css = self._static_dir / "refast-client.css"
        return js.is_file() and css.is_file()

    def _copy_assets(self) -> None:
        """Copy only the runtime assets (JS + CSS) from dist/ → static/."""
        self._static_dir.mkdir(parents=True, exist_ok=True)

        # Remove old generated assets (keep __init__.py and __pycache__)
        keep = {"__init__.py", "__pycache__"}
        for item in self._static_dir.iterdir():
            if item.name in keep:
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        # Copy only the files we actually need – JS and CSS bundles.
        # (skip .d.ts declaration files, __tests__ dirs, etc.)
        copied: list[str] = []
        for item in self._dist_dir.iterdir():
            if item.suffix in (".js", ".css"):
                shutil.copy2(item, self._static_dir / item.name)
                copied.append(item.name)

        self.app.display_info(f"Copied to static/: {', '.join(copied)}")

    # ------------------------------------------------------------------ #
    # Hook interface
    # ------------------------------------------------------------------ #

    def initialize(self, version: str, build_data: dict) -> None:  # noqa: ARG002
        """Run the frontend build before the Python package build."""
        # If the frontend source doesn't exist (e.g. sdist consumer), skip.
        if not self._frontend_dir.is_dir():
            self.app.display_warning(
                "Frontend source not found – skipping frontend build. "
                "Pre-built assets in static/ will be used if present."
            )
            return

        # Allow opting out via environment variable (e.g. REFAST_SKIP_FRONTEND_BUILD=1)
        if os.environ.get("REFAST_SKIP_FRONTEND_BUILD", "").strip() in ("1", "true", "yes"):
            self.app.display_info("Skipping frontend build (REFAST_SKIP_FRONTEND_BUILD is set)")
            return

        # If Node.js is not available, fall back to pre-built assets.
        if not self._node_available():
            if self._assets_exist():
                self.app.display_warning(
                    "Node.js not found – using existing pre-built assets in static/"
                )
                return
            msg = (
                "Node.js is required to build the frontend but was not found on PATH. "
                "Install Node.js >= 18 or set REFAST_SKIP_FRONTEND_BUILD=1 to skip."
            )
            raise RuntimeError(msg)

        # 1. npm ci (deterministic install from lockfile)
        lockfile = self._frontend_dir / "package-lock.json"
        install_cmd = "ci" if lockfile.exists() else "install"
        self._run(["npm", install_cmd], cwd=self._frontend_dir)

        # 2. npm run build
        self._run(["npm", "run", "build"], cwd=self._frontend_dir)

        # 3. Copy JS + CSS into static/
        if not self._dist_dir.is_dir():
            msg = f"Frontend build did not produce a dist/ directory at {self._dist_dir}"
            raise RuntimeError(msg)

        self._copy_assets()

        # Mark the generated files as artifacts so hatchling includes them
        # even though they are .gitignored.
        build_data["artifacts"].extend([
            "src/refast/static/refast-client.js",
            "src/refast/static/refast-client.css",
        ])

    def clean(self, versions: list[str]) -> None:  # noqa: ARG002
        """Remove generated assets from static/."""
        keep = {"__init__.py", "__pycache__"}
        if self._static_dir.is_dir():
            for item in self._static_dir.iterdir():
                if item.name in keep:
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            self.app.display_info("Cleaned static/ directory")
