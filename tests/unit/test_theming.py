"""Tests for RefastApp theming and customization features.

Covers custom_css, custom_js, head_tags, favicon, Theme integration,
and the add_css / add_js / add_head_tag helper methods.
"""


from refast import RefastApp
from refast.theme import Theme, ThemeColors

# ---------------------------------------------------------------------------
# Constructor parameter tests
# ---------------------------------------------------------------------------


class TestAppThemeParam:
    """Tests for the theme parameter on RefastApp."""

    def test_default_theme_is_none(self):
        app = RefastApp()
        assert app.theme is None

    def test_accepts_theme_instance(self):
        theme = Theme(light=ThemeColors(primary="1 2% 3%"))
        app = RefastApp(theme=theme)
        assert app.theme is theme

    def test_theme_can_be_replaced(self):
        t1 = Theme(light=ThemeColors(primary="1 2% 3%"))
        t2 = Theme(light=ThemeColors(primary="4 5% 6%"))
        app = RefastApp(theme=t1)
        app.theme = t2
        assert app.theme is t2


class TestAppFavicon:
    """Tests for the favicon parameter."""

    def test_default_favicon_is_none(self):
        app = RefastApp()
        assert app.favicon is None

    def test_accepts_favicon_string(self):
        app = RefastApp(favicon="/static/favicon.ico")
        assert app.favicon == "/static/favicon.ico"


class TestAppCustomCss:
    """Tests for custom_css parameter and add_css()."""

    def test_default_empty(self):
        app = RefastApp()
        assert app._custom_css == []

    def test_string_normalised_to_list(self):
        app = RefastApp(custom_css="body { color: red; }")
        assert app._custom_css == ["body { color: red; }"]

    def test_list_preserved(self):
        entries = ["body { color: red; }", "https://example.com/style.css"]
        app = RefastApp(custom_css=entries)
        assert app._custom_css == entries

    def test_add_css_appends(self):
        app = RefastApp()
        app.add_css("body { margin: 0; }")
        app.add_css("https://cdn.example.com/lib.css")
        assert len(app._custom_css) == 2
        assert "body { margin: 0; }" in app._custom_css
        assert "https://cdn.example.com/lib.css" in app._custom_css


class TestAppCustomJs:
    """Tests for custom_js parameter and add_js()."""

    def test_default_empty(self):
        app = RefastApp()
        assert app._custom_js == []

    def test_string_normalised_to_list(self):
        app = RefastApp(custom_js="console.log('hi');")
        assert app._custom_js == ["console.log('hi');"]

    def test_list_preserved(self):
        entries = ["alert('a');", "https://cdn.example.com/lib.js"]
        app = RefastApp(custom_js=entries)
        assert app._custom_js == entries

    def test_add_js_appends(self):
        app = RefastApp()
        app.add_js("console.log('ready');")
        assert len(app._custom_js) == 1


class TestAppHeadTags:
    """Tests for head_tags parameter and add_head_tag()."""

    def test_default_empty(self):
        app = RefastApp()
        assert app._head_tags == []

    def test_accepts_list(self):
        tags = [
            '<meta name="robots" content="noindex">',
            '<link rel="preconnect" href="https://fonts.gstatic.com">',
        ]
        app = RefastApp(head_tags=tags)
        assert app._head_tags == tags

    def test_add_head_tag_appends(self):
        app = RefastApp()
        app.add_head_tag('<meta name="author" content="me">')
        assert len(app._head_tags) == 1
        assert '<meta name="author" content="me">' in app._head_tags


# ---------------------------------------------------------------------------
# HTML shell rendering tests
# ---------------------------------------------------------------------------


class TestRenderHtmlShellTheming:
    """Tests that _render_html_shell correctly injects theming / customization."""

    def _render(self, app: RefastApp) -> str:
        """Helper: register a dummy page and render the HTML shell."""
        from refast.router import RefastRouter

        class FakeComponent:
            def render(self):
                return {"type": "Text", "id": "t", "props": {}, "children": ["hi"]}

        class FakeRequest:
            headers = {}
            query_params = {}
            url = type("U", (), {"path": "/"})()

        router = RefastRouter(app)
        from refast.context import Context

        ctx = Context(request=FakeRequest(), app=app)
        return router._render_html_shell(FakeComponent(), ctx)

    # --- Favicon ---

    def test_no_favicon_by_default(self):
        html = self._render(RefastApp())
        assert 'rel="icon"' not in html

    def test_favicon_injected(self):
        html = self._render(RefastApp(favicon="/static/favicon.png"))
        assert '<link rel="icon" href="/static/favicon.png">' in html

    # --- Theme ---

    def test_no_theme_no_style_block(self):
        html = self._render(RefastApp())
        assert "data-refast-theme" not in html

    def test_theme_injects_css_vars(self):
        theme = Theme(
            light=ThemeColors(primary="100 50% 50%"),
            dark=ThemeColors(primary="200 60% 40%"),
        )
        html = self._render(RefastApp(theme=theme))
        assert "data-refast-theme" in html
        assert "--primary: 100 50% 50%;" in html
        assert "--primary: 200 60% 40%;" in html

    def test_theme_font_family_in_html(self):
        theme = Theme(font_family="'Comic Sans MS', cursive")
        html = self._render(RefastApp(theme=theme))
        assert "font-family: 'Comic Sans MS', cursive;" in html

    def test_theme_radius_in_html(self):
        theme = Theme(radius="1rem")
        html = self._render(RefastApp(theme=theme))
        assert "--radius: 1rem;" in html

    # --- Custom CSS ---

    def test_inline_css_injected(self):
        html = self._render(RefastApp(custom_css="body { color: red; }"))
        assert "<style>body { color: red; }</style>" in html

    def test_external_css_url_injected(self):
        url = "https://fonts.googleapis.com/css2?family=Inter"
        html = self._render(RefastApp(custom_css=url))
        assert f'<link rel="stylesheet" href="{url}">' in html

    def test_relative_css_url_injected(self):
        html = self._render(RefastApp(custom_css="/static/extra.css"))
        assert '<link rel="stylesheet" href="/static/extra.css">' in html

    # --- Custom JS ---

    def test_inline_js_injected(self):
        html = self._render(RefastApp(custom_js="console.log('hi');"))
        assert "<script>console.log('hi');</script>" in html

    def test_external_js_url_injected(self):
        url = "https://cdn.example.com/lib.js"
        html = self._render(RefastApp(custom_js=url))
        assert f'<script src="{url}"></script>' in html

    def test_relative_js_url_injected(self):
        html = self._render(RefastApp(custom_js="/static/extra.js"))
        assert '<script src="/static/extra.js"></script>' in html

    # --- Head tags ---

    def test_head_tag_injected(self):
        tag = '<meta name="description" content="My app">'
        html = self._render(RefastApp(head_tags=[tag]))
        assert tag in html
        # Should be in <head>
        head_section = html.split("<head>")[1].split("</head>")[0]
        assert tag in head_section

    def test_multiple_head_tags(self):
        tags = [
            '<meta name="a" content="1">',
            '<meta name="b" content="2">',
        ]
        html = self._render(RefastApp(head_tags=tags))
        for tag in tags:
            assert tag in html

    # --- Ordering ---

    def test_custom_css_after_theme(self):
        """Custom CSS should appear after theme CSS for override priority."""
        theme = Theme(light=ThemeColors(primary="1 2% 3%"))
        html = self._render(RefastApp(theme=theme, custom_css="body { margin: 0; }"))
        theme_pos = html.index("data-refast-theme")
        custom_pos = html.index("body { margin: 0; }")
        assert custom_pos > theme_pos

    def test_custom_js_in_body(self):
        """Custom JS should be in <body>, not <head>."""
        html = self._render(RefastApp(custom_js="alert(1);"))
        body_section = html.split("<body>")[1].split("</body>")[0]
        assert "alert(1);" in body_section

    # --- Combined ---

    def test_all_customizations_together(self):
        theme = Theme(
            light=ThemeColors(primary="10 20% 30%"),
            font_family="Inter",
            radius="0.5rem",
        )
        app = RefastApp(
            title="Test",
            theme=theme,
            favicon="/fav.ico",
            custom_css=["body { margin: 0; }", "https://example.com/a.css"],
            custom_js=["console.log('a');", "https://example.com/b.js"],
            head_tags=['<meta name="x" content="y">'],
        )
        html = self._render(app)
        assert "<title>Test</title>" in html
        assert "data-refast-theme" in html
        assert "--primary: 10 20% 30%;" in html
        assert "font-family: Inter;" in html
        assert "--radius: 0.5rem;" in html
        assert '<link rel="icon" href="/fav.ico">' in html
        assert "<style>body { margin: 0; }</style>" in html
        assert '<link rel="stylesheet" href="https://example.com/a.css">' in html
        assert "<script>console.log('a');</script>" in html
        assert '<script src="https://example.com/b.js"></script>' in html
        assert '<meta name="x" content="y">' in html
