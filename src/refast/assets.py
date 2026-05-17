"""Asset pipeline for Refast: manifest parsing, chunk resolution, and HTML shell rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from refast.app import RefastApp

# Static directory path for the built React client
STATIC_DIR = Path(__file__).parent / "static"

# MIME types that browsers may execute as active content — never serve these
# with their declared type; remap to application/octet-stream.
UNSAFE_CONTENT_TYPES: frozenset[str] = frozenset(
    {
        "text/html",
        "text/xml",
        "application/xhtml+xml",
        "application/xml",
        "application/javascript",
        "application/x-javascript",
        "text/javascript",
        "image/svg+xml",
    }
)

# All known lazy feature-chunk names (must match vite manualChunks keys)
ALL_FEATURE_CHUNKS = frozenset(
    {
        "charts",
        "markdown",
        "mermaid",
        "katex",
        "icons",
        "navigation",
        "overlay",
        "controls",
    }
)


def _load_manifest() -> dict[str, Any]:
    """Load the Vite build manifest from static/manifest.json.

    Returns an empty dict if the file doesn't exist (pre-built assets
    may not include a manifest in development).
    """
    manifest_path = STATIC_DIR / "manifest.json"
    if manifest_path.is_file():
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def _chunk_feature(file_name: str, entry: dict[str, Any]) -> str | None:
    """Infer which feature bucket a manifest entry belongs to.

    Returns ``None`` for non-feature (shared/vendor/core) chunks.
    """
    name = entry.get("name")
    if isinstance(name, str) and name in ALL_FEATURE_CHUNKS:
        return name

    src = str(entry.get("src", ""))
    if "src/components/charts/" in src:
        return "charts"
    if src.endswith("/shadcn/navigation.tsx"):
        return "navigation"
    if src.endswith("/shadcn/overlay.tsx"):
        return "overlay"
    if src.endswith("/shadcn/controls.tsx"):
        return "controls"
    if src.endswith("/shadcn/icon.tsx"):
        return "icons"
    if "markdown" in src:
        return "markdown"

    for feature in ALL_FEATURE_CHUNKS:
        if file_name.startswith(f"refast-{feature}-"):
            return feature
    return None


def _get_chunk_files(manifest: dict[str, Any], preloaded_features: list[str] | None) -> list[str]:
    """Derive the list of JS chunk filenames to include from the manifest.

    Args:
        manifest: Parsed Vite manifest.json contents.
        preloaded_features: Which feature chunks should be hinted with
            ``modulepreload``. ``None`` means no feature chunks are preloaded.

    Returns:
        List of JS filenames (relative to /static/) in load order.
        The entry chunk (``refast-client.js``) is always first.
    """
    if not manifest:
        return ["refast-client.js"]

    allowed = set(preloaded_features or [])

    entry_key: str | None = None
    entry_file = "refast-client.js"
    for key, entry in manifest.items():
        if entry.get("isEntry") is True:
            entry_key = key
            entry_file = str(entry.get("file", entry_file))
            break

    if entry_key is None:
        return [entry_file]

    result: list[str] = []
    seen_files: set[str] = set()
    visited_keys: set[str] = set()

    def _add_file(file_name: str) -> None:
        if file_name.endswith(".js") and file_name not in seen_files:
            seen_files.add(file_name)
            result.append(file_name)

    def _walk(key: str) -> None:
        if key in visited_keys:
            return
        visited_keys.add(key)

        entry = manifest.get(key, {})
        file_name = str(entry.get("file", ""))
        if not file_name:
            return

        feature = _chunk_feature(file_name, entry)
        if feature is not None and feature not in allowed:
            return

        _add_file(file_name)
        for imported_key in entry.get("imports", []):
            if isinstance(imported_key, str):
                _walk(imported_key)

    _add_file(entry_file)
    for imported_key in manifest.get(entry_key, {}).get("imports", []):
        if isinstance(imported_key, str):
            _walk(imported_key)

    return result


def render_html_shell(app: RefastApp) -> str:
    """Render the full HTML shell for a Refast page.

    Resolves the asset chunks from the build manifest, injects feature
    preload hints, extension loader scripts, theme overrides, and custom
    head/body tags configured on *app*.

    Args:
        app: The :class:`~refast.app.RefastApp` instance.

    Returns:
        A complete ``<!DOCTYPE html>`` string ready to send as an HTTP response.
    """
    # Check if React client CSS exists
    client_css_path = STATIC_DIR / "refast-client.css"
    has_client_css = client_css_path.exists()

    # Resolve chunk files from the build manifest
    manifest = _load_manifest()
    lazy_features = (
        set(app.lazy_features)
        if app.lazy_features is not None
        else set(ALL_FEATURE_CHUNKS)
    )
    startup_features = sorted(
        set(app.preloaded_features or []) | (set(ALL_FEATURE_CHUNKS) - lazy_features)
    )
    chunk_files = _get_chunk_files(manifest, startup_features)

    # Build script tags — entry is type="module", chunks are modulepreload
    client_css = (
        '<link rel="stylesheet" href="/static/refast-client.css">' if has_client_css else ""
    )

    # The entry module + feature chunks
    script_tags: list[str] = []
    preload_tags: list[str] = []
    for f in chunk_files:
        path = f"/static/{f}"
        if f == "refast-client.js":
            script_tags.append(f'<script type="module" src="{path}"></script>')
        else:
            preload_tags.append(f'<link rel="modulepreload" href="{path}">')

    # Collect extension assets and metadata
    extension_styles = []
    extension_script_map: dict[str, list[str]] = {}
    extension_component_map: dict[str, str] = {}
    for ext in app._extensions.values():
        extension_styles.extend(
            f'<link rel="stylesheet" href="{url}">' for url in ext.get_style_urls()
        )
        extension_script_map[ext.name] = ext.get_script_urls()
        for component in ext.components:
            component_type = getattr(component, "component_type", component.__name__)
            extension_component_map[component_type] = ext.name

    extension_names = set(extension_script_map.keys())
    lazy_extensions = (
        set(app.lazy_extensions)
        if app.lazy_extensions is not None
        else set(extension_names)
    )
    startup_extensions = sorted(
        (set(app.preloaded_extensions or []) | (extension_names - lazy_extensions))
        & extension_names
    )

    scripts_html = "\n    ".join(script_tags)
    preloads_html = "\n    ".join(preload_tags)
    preload_config_html = (
        "<script>window.__REFAST_PRELOADED_FEATURES__ = "
        f"{json.dumps(startup_features)};"
        "window.__REFAST_STARTUP_FEATURES__ = "
        f"{json.dumps(startup_features)};"
        "window.__REFAST_LAZY_FEATURES__ = "
        f"{json.dumps(sorted(lazy_features))};"
        "window.__REFAST_EXTENSIONS_READY__ = "
        f"{str(not bool(extension_script_map)).lower()};"
        "window.__REFAST_EXTENSION_SCRIPT_MAP__ = "
        f"{json.dumps(extension_script_map)};"
        "window.__REFAST_EXTENSION_COMPONENT_MAP__ = "
        f"{json.dumps(extension_component_map)};"
        "window.__REFAST_EXTENSION_LOADED__ = "
        "window.__REFAST_EXTENSION_LOADED__ || {};"
        "</script>"
    )

    ext_styles_html = "\n    ".join(extension_styles)

    # Extensions are IIFE scripts that need window.RefastClient.
    # We inject a runtime loader that can preload startup extensions and
    # lazily load the rest on demand by component type.
    ext_loader_html = ""
    if extension_script_map:
        script_map_json = json.dumps(extension_script_map)
        component_map_json = json.dumps(extension_component_map)
        startup_extensions_json = json.dumps(startup_extensions)
        ext_loader_html = f"""<script type="module">
        window.__REFAST_EXTENSIONS_READY__ = false;
        window.__REFAST_EXTENSION_SCRIPT_MAP__ = {script_map_json};
        window.__REFAST_EXTENSION_COMPONENT_MAP__ = {component_map_json};
        window.__REFAST_EXTENSION_LOADED__ = window.__REFAST_EXTENSION_LOADED__ || {{}};

        const startupExtensions = {startup_extensions_json};
        const extensionPromises = {{}};

        function loadScript(url, extName) {{
            return new Promise((resolve) => {{
                const existing = document.querySelector('script[data-refast-ext="' + extName + '"][src="' + url + '"]');
                if (existing) {{
                    if (existing.dataset.refastLoaded === '1') {{
                        resolve(true);
                        return;
                    }}

                    const onLoad = () => resolve(true);
                    const onError = () => resolve(false);
                    existing.addEventListener('load', onLoad, {{ once: true }});
                    existing.addEventListener('error', onError, {{ once: true }});
                    return;
                }}
                const s = document.createElement('script');
                s.src = url;
                s.async = true;
                s.setAttribute('data-refast-ext', extName);
                s.onload = () => {{
                    s.dataset.refastLoaded = '1';
                    resolve(true);
                }};
                s.onerror = () => resolve(false);
                document.body.appendChild(s);
            }});
        }}

        window.__REFAST_LOAD_EXTENSION__ = function(name) {{
            if (window.__REFAST_EXTENSION_LOADED__[name]) {{
                window.dispatchEvent(new CustomEvent('refast:extension-loaded', {{ detail: {{ name }} }}));
                return Promise.resolve();
            }}

            if (extensionPromises[name]) {{
                return extensionPromises[name];
            }}

            const urls = (window.__REFAST_EXTENSION_SCRIPT_MAP__ || {{}})[name] || [];
            extensionPromises[name] = Promise.all(urls.map((url) => loadScript(url, name))).then((results) => {{
                const loaded = results.every(Boolean);
                if (loaded) {{
                    window.__REFAST_EXTENSION_LOADED__[name] = true;
                    window.dispatchEvent(new CustomEvent('refast:extension-loaded', {{ detail: {{ name }} }}));
                    return;
                }}

                delete extensionPromises[name];
            }});
            return extensionPromises[name];
        }};

        function loadStartupExtensions() {{
            if (startupExtensions.length === 0) {{
                window.__REFAST_EXTENSIONS_READY__ = true;
                window.dispatchEvent(new CustomEvent('refast:extensions-ready'));
                return;
            }}

            Promise.all(startupExtensions.map((name) => window.__REFAST_LOAD_EXTENSION__(name))).finally(() => {{
                window.__REFAST_EXTENSIONS_READY__ = true;
                window.dispatchEvent(new CustomEvent('refast:extensions-ready'));
            }});
        }}

        if (window.RefastClient) {{
            loadStartupExtensions();
        }} else {{
            window.addEventListener('refast:ready', loadStartupExtensions, {{ once: true }});
        }}
    </script>"""  # noqa: E501

    # --- Theme CSS variable overrides ---
    theme_style = ""
    if app.theme is not None:
        css_vars = app.theme.to_css_variables()
        if css_vars:
            theme_style = f"<style data-refast-theme>\n{css_vars}\n</style>"

    # --- Favicon ---
    favicon_tag = ""
    if app.favicon:
        favicon_tag = f'<link rel="icon" href="{app.favicon}">'

    # --- Extra <head> tags ---
    head_tags_html = "\n    ".join(app._head_tags) if app._head_tags else ""

    # --- Custom CSS (after extension CSS so user overrides win) ---
    custom_css_parts: list[str] = []
    for entry in app._custom_css:
        if entry.startswith("http") or entry.startswith("/"):
            custom_css_parts.append(f'<link rel="stylesheet" href="{entry}">')
        else:
            custom_css_parts.append(f"<style>{entry}</style>")
    custom_css_html = "\n    ".join(custom_css_parts)

    # --- Custom JS (after client + extension scripts so globals exist) ---
    custom_js_parts: list[str] = []
    for entry in app._custom_js:
        if entry.startswith("http") or entry.startswith("/"):
            custom_js_parts.append(f'<script src="{entry}"></script>')
        else:
            custom_js_parts.append(f"<script>{entry}</script>")
    custom_js_html = "\n    ".join(custom_js_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app.title}</title>
    {favicon_tag}
    {client_css}
    {preloads_html}
    {theme_style}
    {ext_styles_html}
    {custom_css_html}
    {head_tags_html}
    <style>
        @keyframes refast-spin {{ to {{ transform: rotate(360deg); }} }}
        #refast-loading-overlay {{
            position: fixed;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #ffffff;
            z-index: 9999;
        }}
        @media (prefers-color-scheme: dark) {{
            #refast-loading-overlay {{ background: #09090b; }}
        }}
        #refast-loading-spinner {{
            width: 2rem;
            height: 2rem;
            border-radius: 50%;
            border: 4px solid #e2e8f0;
            border-top-color: #3b82f6;
            animation: refast-spin 0.7s linear infinite;
        }}
        @media (prefers-color-scheme: dark) {{
            #refast-loading-spinner {{ border-color: #27272a; border-top-color: #3b82f6; }}
        }}
    </style>
</head>
<body>
    <div id="refast-loading-overlay" aria-label="Loading" role="status">
        <div id="refast-loading-spinner"></div>
    </div>
    <div id="refast-root"></div>
    {preload_config_html}
    {scripts_html}
    {ext_loader_html}
    {custom_js_html}
</body>
</html>"""
