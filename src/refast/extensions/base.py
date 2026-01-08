"""Base Extension class for Refast extensions."""

from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.components.base import Component


class Extension(ABC):
    """
    Base class for Refast extensions.

    Extensions allow third-party packages to provide custom React components
    to Refast applications. Each extension defines:
    - Metadata (name, version, description)
    - Static assets (JavaScript and CSS files)
    - Python component classes

    Example:
        ```python
        from pathlib import Path
        from refast.extensions import Extension
        from .components import MapContainer, Marker, TileLayer

        class LeafletExtension(Extension):
            name = "refast-leaflet"
            version = "0.1.0"
            description = "Interactive maps for Refast using Leaflet"

            scripts = ["refast-leaflet.js"]
            styles = ["refast-leaflet.css"]

            @property
            def static_path(self) -> Path:
                return Path(__file__).parent / "static"

            @property
            def components(self) -> list:
                return [MapContainer, Marker, TileLayer]
        ```

    To register an extension with a Refast app:
        ```python
        from refast import RefastApp
        from refast_leaflet import LeafletExtension

        ui = RefastApp(extensions=[LeafletExtension()])
        ```

    Or for auto-discovery via entry points, add to pyproject.toml:
        ```toml
        [project.entry-points."refast.extensions"]
        refast_leaflet = "refast_leaflet:LeafletExtension"
        ```
    """

    # Required: Unique extension name (e.g., "refast-leaflet")
    name: str

    # Optional metadata
    version: str = "0.0.0"
    description: str = ""

    # Static assets to inject into HTML (relative to static_path)
    scripts: list[str] = []  # JavaScript files
    styles: list[str] = []  # CSS files

    def __init__(self) -> None:
        """Initialize the extension."""
        if not hasattr(self, "name") or not self.name:
            raise ValueError(
                f"Extension class {self.__class__.__name__} must define a 'name' attribute"
            )

    @property
    def static_path(self) -> Path | None:
        """
        Path to the directory containing static assets.

        Override this property to return the path where your extension's
        JavaScript and CSS files are located.

        Returns:
            Path to static directory, or None if no static assets.
        """
        return None

    @property
    def components(self) -> list[type["Component"]]:
        """
        List of Python component classes provided by this extension.

        Override this property to return the component classes that
        this extension provides.

        Returns:
            List of Component subclasses.
        """
        return []

    def on_register(self, app: "RefastApp") -> None:
        """
        Called when the extension is registered with an app.

        Override this method to perform custom initialization,
        such as registering event handlers or modifying app configuration.

        Args:
            app: The RefastApp instance this extension is being registered with.
        """
        pass

    def get_script_urls(self) -> list[str]:
        """
        Get the URLs for this extension's JavaScript files.

        Returns:
            List of URL paths for script tags.
        """
        return [f"/static/ext/{self.name}/{script}" for script in self.scripts]

    def get_style_urls(self) -> list[str]:
        """
        Get the URLs for this extension's CSS files.

        Returns:
            List of URL paths for link tags.
        """
        return [f"/static/ext/{self.name}/{style}" for style in self.styles]

    def get_static_file_path(self, filename: str) -> Path | None:
        """
        Get the full path to a static file.

        Args:
            filename: The filename relative to static_path.

        Returns:
            Full path to the file, or None if not found.
        """
        if self.static_path is None:
            return None
        file_path = self.static_path / filename
        if file_path.exists() and file_path.is_file():
            return file_path
        return None

    def validate(self) -> list[str]:
        """
        Validate the extension configuration.

        Returns:
            List of validation error messages (empty if valid).
        """
        errors: list[str] = []

        if not self.name:
            errors.append("Extension name is required")

        # Check that static files exist if specified
        if self.scripts or self.styles:
            if self.static_path is None:
                errors.append(
                    f"Extension '{self.name}' specifies scripts/styles but no static_path"
                )
            elif not self.static_path.exists():
                errors.append(
                    f"Extension '{self.name}' static_path does not exist: {self.static_path}"
                )
            else:
                for script in self.scripts:
                    if not (self.static_path / script).exists():
                        errors.append(
                            f"Extension '{self.name}' script not found: {script}"
                        )
                for style in self.styles:
                    if not (self.static_path / style).exists():
                        errors.append(
                            f"Extension '{self.name}' style not found: {style}"
                        )

        return errors

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} version={self.version!r}>"
