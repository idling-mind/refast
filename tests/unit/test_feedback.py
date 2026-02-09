"""Tests for feedback components."""

from refast.components.shadcn.feedback import (
    Alert,
    ConnectionStatus,
    Progress,
    Skeleton,
    Spinner,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestAlert:
    """Tests for Alert component."""

    def test_alert_renders(self):
        """Test Alert renders correctly."""
        alert = Alert(title="Error", message="Something went wrong")
        rendered = alert.render()
        assert rendered["type"] == "Alert"
        assert rendered["props"]["title"] == "Error"
        assert rendered["props"]["message"] == "Something went wrong"

    def test_alert_variant(self):
        """Test Alert variant prop."""
        alert = Alert(variant="destructive")
        rendered = alert.render()
        assert rendered["props"]["variant"] == "destructive"

    def test_alert_dismissible(self):
        """Test Alert dismissible prop."""
        cb = MockCallback()
        alert = Alert(dismissible=True, on_dismiss=cb)
        rendered = alert.render()
        assert rendered["props"]["dismissible"] is True
        assert rendered["props"]["on_dismiss"] == {"callbackId": "cb-123"}


class TestSpinner:
    """Tests for Spinner component."""

    def test_spinner_renders(self):
        """Test Spinner renders correctly."""
        spinner = Spinner()
        rendered = spinner.render()
        assert rendered["type"] == "Spinner"
        assert rendered["props"]["size"] == "md"

    def test_spinner_size(self):
        """Test Spinner size prop."""
        spinner = Spinner(size="lg")
        rendered = spinner.render()
        assert rendered["props"]["size"] == "lg"


class TestProgress:
    """Tests for Progress component."""

    def test_progress_renders(self):
        """Test Progress renders correctly."""
        progress = Progress(value=50)
        rendered = progress.render()
        assert rendered["type"] == "Progress"
        assert rendered["props"]["value"] == 50
        assert rendered["props"]["max"] == 100

    def test_progress_with_label(self):
        """Test Progress with label."""
        progress = Progress(value=75, label="Uploading...")
        rendered = progress.render()
        assert rendered["props"]["label"] == "Uploading..."

    def test_progress_show_value(self):
        """Test Progress showValue prop."""
        progress = Progress(value=30, show_value=True)
        rendered = progress.render()
        assert rendered["props"]["show_value"] is True

    def test_progress_custom_styles(self):
        """Test Progress with custom styles."""
        progress = Progress(
            value=60, foreground_color="primary", track_color="secondary", striped="animated"
        )
        rendered = progress.render()
        assert rendered["props"]["foreground_color"] == "primary"
        assert rendered["props"]["track_color"] == "secondary"
        assert rendered["props"]["striped"] == "animated"


class TestSkeleton:
    """Tests for Skeleton component."""

    def test_skeleton_renders(self):
        """Test Skeleton renders correctly."""
        skeleton = Skeleton()
        rendered = skeleton.render()
        assert rendered["type"] == "Skeleton"
        assert rendered["props"]["variant"] == "text"

    def test_skeleton_dimensions(self):
        """Test Skeleton dimensions."""
        skeleton = Skeleton(width=200, height=100)
        rendered = skeleton.render()
        assert rendered["props"]["width"] == 200
        assert rendered["props"]["height"] == 100

    def test_skeleton_variant(self):
        """Test Skeleton variant prop."""
        skeleton = Skeleton(variant="circular")
        rendered = skeleton.render()
        assert rendered["props"]["variant"] == "circular"


class MockJsCallback:
    """Mock JS callback for testing."""

    def __init__(self, code: str):
        self.code = code

    def serialize(self):
        return {"jsFunction": self.code, "boundArgs": {}}


class TestConnectionStatus:
    """Tests for ConnectionStatus component."""

    def test_connection_status_default_props(self):
        """Test ConnectionStatus with default props."""
        component = ConnectionStatus()
        rendered = component.render()

        assert rendered["type"] == "ConnectionStatus"
        assert rendered["props"]["children_connected"] == []
        assert rendered["props"]["children_disconnected"] == []
        assert rendered["props"]["position"] == "bottom-right"
        assert rendered["props"]["debounce_ms"] == 500

    def test_connection_status_with_children_disconnected(self):
        """Test ConnectionStatus with children_disconnected."""
        component = ConnectionStatus(
            children_disconnected=[Alert(title="Disconnected", variant="destructive")]
        )
        rendered = component.render()

        assert len(rendered["props"]["children_disconnected"]) == 1
        assert rendered["props"]["children_disconnected"][0]["type"] == "Alert"
        assert rendered["props"]["children_disconnected"][0]["props"]["title"] == "Disconnected"

    def test_connection_status_with_children_connected(self):
        """Test ConnectionStatus with children_connected."""
        component = ConnectionStatus(
            children_connected=[Alert(title="Connected", variant="success")]
        )
        rendered = component.render()

        assert len(rendered["props"]["children_connected"]) == 1
        assert rendered["props"]["children_connected"][0]["type"] == "Alert"
        assert rendered["props"]["children_connected"][0]["props"]["title"] == "Connected"

    def test_connection_status_with_both_children(self):
        """Test ConnectionStatus with both connected and disconnected children."""
        component = ConnectionStatus(
            children_connected=[Alert(title="Online", variant="success")],
            children_disconnected=[Alert(title="Offline", variant="destructive")],
        )
        rendered = component.render()

        assert len(rendered["props"]["children_connected"]) == 1
        assert len(rendered["props"]["children_disconnected"]) == 1
        assert rendered["props"]["children_connected"][0]["props"]["title"] == "Online"
        assert rendered["props"]["children_disconnected"][0]["props"]["title"] == "Offline"

    def test_connection_status_with_python_callbacks(self):
        """Test ConnectionStatus with Python callbacks."""
        on_disconnect = MockCallback()
        on_reconnect = MockCallback()

        component = ConnectionStatus(
            on_disconnect=on_disconnect,
            on_reconnect=on_reconnect,
        )
        rendered = component.render()

        assert rendered["props"]["on_disconnect"]["callbackId"] == "cb-123"
        assert rendered["props"]["on_reconnect"]["callbackId"] == "cb-123"

    def test_connection_status_with_js_callbacks(self):
        """Test ConnectionStatus with JavaScript callbacks."""
        js_on_disconnect = MockJsCallback("console.log('disconnected')")
        js_on_reconnect = MockJsCallback("console.log('reconnected')")

        component = ConnectionStatus(
            js_on_disconnect=js_on_disconnect,
            js_on_reconnect=js_on_reconnect,
        )
        rendered = component.render()

        assert rendered["props"]["js_on_disconnect"]["jsFunction"] == "console.log('disconnected')"
        assert rendered["props"]["js_on_reconnect"]["jsFunction"] == "console.log('reconnected')"

    def test_connection_status_custom_position(self):
        """Test ConnectionStatus with custom position."""
        component = ConnectionStatus(position="top-left")
        rendered = component.render()

        assert rendered["props"]["position"] == "top-left"

    def test_connection_status_inline_position(self):
        """Test ConnectionStatus with inline position."""
        component = ConnectionStatus(
            position="inline",
            children_connected=[Alert(title="Online")],
        )
        rendered = component.render()

        assert rendered["props"]["position"] == "inline"
        assert len(rendered["props"]["children_connected"]) == 1

    def test_connection_status_custom_debounce(self):
        """Test ConnectionStatus with custom debounce."""
        component = ConnectionStatus(debounce_ms=1000)
        rendered = component.render()

        assert rendered["props"]["debounce_ms"] == 1000

    def test_connection_status_all_positions(self):
        """Test ConnectionStatus with all valid positions."""
        positions = ["top-left", "top-right", "bottom-left", "bottom-right", "inline"]

        for pos in positions:
            component = ConnectionStatus(position=pos)
            rendered = component.render()
            assert rendered["props"]["position"] == pos

    def test_connection_status_class_name(self):
        """Test ConnectionStatus with custom class name."""
        component = ConnectionStatus(class_name="my-custom-class")
        rendered = component.render()

        assert rendered["props"]["class_name"] == "my-custom-class"

    def test_connection_status_children_are_empty_lists(self):
        """Test ConnectionStatus renders empty lists for children by default."""
        component = ConnectionStatus()
        rendered = component.render()

        # Both should be empty lists, not None
        assert rendered["props"]["children_connected"] == []
        assert rendered["props"]["children_disconnected"] == []
        # Main children should be empty (we don't use _children)
        assert rendered["children"] == []
