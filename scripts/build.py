#!/usr/bin/env python3
"""Build script for Refast frontend assets.

This script builds the React frontend client and copies the built assets
to the Python package's static directory.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    # Script is in scripts/build.py, so go up one level
    return Path(__file__).parent.parent


def get_frontend_dir() -> Path:
    """Get the frontend source directory."""
    return get_project_root() / "src" / "refast-client"


def get_static_dir() -> Path:
    """Get the static assets destination directory."""
    return get_project_root() / "src" / "refast" / "static"


def check_node() -> bool:
    """Check if Node.js is available."""
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"Node.js version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    return False


def check_npm() -> bool:
    """Check if npm is available."""
    try:
        result = subprocess.run(
            ["npm", "--version"],
            capture_output=True,
            text=True,
            shell=sys.platform == "win32",
        )
        if result.returncode == 0:
            print(f"npm version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    return False


def install_dependencies(frontend_dir: Path) -> bool:
    """Install npm dependencies."""
    print("Installing npm dependencies...")
    result = subprocess.run(
        ["npm", "install"],
        cwd=frontend_dir,
        capture_output=True,
        text=True,
        shell=sys.platform == "win32",
    )
    if result.returncode != 0:
        print(f"Error installing dependencies:\n{result.stderr}")
        return False
    print("Dependencies installed successfully")
    return True


def build_frontend(frontend_dir: Path) -> bool:
    """Build the frontend."""
    print("Building frontend...")
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=frontend_dir,
        capture_output=True,
        text=True,
        shell=sys.platform == "win32",
    )
    if result.returncode != 0:
        print("Error building frontend:")
        if result.stdout:
            print(f"stdout:\n{result.stdout}")
        if result.stderr:
            print(f"stderr:\n{result.stderr}")
        return False
    print("Frontend built successfully")
    return True


def copy_assets(frontend_dir: Path, static_dir: Path) -> bool:
    """Copy built assets to static directory."""
    dist_dir = frontend_dir / "dist"

    if not dist_dir.exists():
        print(f"Error: dist directory not found at {dist_dir}")
        return False

    # Ensure static directory exists
    static_dir.mkdir(parents=True, exist_ok=True)

    # Clear existing assets (except __init__.py)
    for item in static_dir.iterdir():
        if item.name != "__init__.py" and item.name != "__pycache__":
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    # Copy JS, CSS bundles, manifest, and compressed files
    print(f"Copying assets from {dist_dir} to {static_dir}")

    copied_files = []
    for item in dist_dir.iterdir():
        if item.is_file() and item.suffix in (".js", ".css", ".gz", ".br"):
            shutil.copy2(item, static_dir / item.name)
            copied_files.append(item.name)

    # Copy .vite/manifest.json → static/manifest.json
    manifest_src = dist_dir / ".vite" / "manifest.json"
    if manifest_src.is_file():
        shutil.copy2(manifest_src, static_dir / "manifest.json")
        copied_files.append("manifest.json")

    print(f"Copied files: {', '.join(copied_files)}")
    return True


def print_summary(static_dir: Path) -> None:
    """Print a summary of the built assets."""
    print("\n" + "=" * 50)
    print("Build Summary")
    print("=" * 50)

    total_size = 0
    for item in static_dir.rglob("*"):
        if item.is_file() and item.name not in ("__init__.py",):
            size = item.stat().st_size
            total_size += size
            print(f"  {item.relative_to(static_dir)}: {size / 1024:.2f} KB")

    print("-" * 50)
    print(f"Total size: {total_size / 1024:.2f} KB")
    print("=" * 50)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build Refast frontend assets")
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip npm install step",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean static directory before building",
    )
    args = parser.parse_args()

    project_root = get_project_root()
    frontend_dir = get_frontend_dir()
    static_dir = get_static_dir()

    print(f"Project root: {project_root}")
    print(f"Frontend dir: {frontend_dir}")
    print(f"Static dir: {static_dir}")
    print()

    # Check prerequisites
    if not check_node():
        print("Error: Node.js is not installed or not in PATH")
        return 1

    if not check_npm():
        print("Error: npm is not installed or not in PATH")
        return 1

    # Check frontend directory exists
    if not frontend_dir.exists():
        print(f"Error: Frontend directory not found at {frontend_dir}")
        return 1

    # Clean if requested
    if args.clean:
        print("Cleaning static directory...")
        for item in static_dir.iterdir():
            if item.name not in ("__init__.py", "__pycache__"):
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

    # Install dependencies
    if not args.skip_install:
        if not install_dependencies(frontend_dir):
            return 1

    # Build frontend
    if not build_frontend(frontend_dir):
        return 1

    # Copy assets
    if not copy_assets(frontend_dir, static_dir):
        return 1

    # Print summary
    print_summary(static_dir)

    print("\nBuild completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
