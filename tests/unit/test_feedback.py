"""Tests for feedback components."""


from refast.components.shadcn.feedback import (
    Alert,
    Dialog,
    Modal,
    Progress,
    Skeleton,
    Spinner,
    Toast,
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
        assert rendered["props"]["onDismiss"] == {"callbackId": "cb-123"}


class TestToast:
    """Tests for Toast component."""

    def test_toast_renders(self):
        """Test Toast renders correctly."""
        toast = Toast(title="Success", message="Operation completed")
        rendered = toast.render()
        assert rendered["type"] == "Toast"
        assert rendered["props"]["title"] == "Success"
        assert rendered["props"]["duration"] == 3000

    def test_toast_variant(self):
        """Test Toast variant prop."""
        toast = Toast(variant="success")
        rendered = toast.render()
        assert rendered["props"]["variant"] == "success"

    def test_toast_duration(self):
        """Test Toast duration prop."""
        toast = Toast(duration=5000)
        rendered = toast.render()
        assert rendered["props"]["duration"] == 5000


class TestModal:
    """Tests for Modal component."""

    def test_modal_renders(self):
        """Test Modal renders correctly."""
        modal = Modal(title="Confirm", open=True)
        rendered = modal.render()
        assert rendered["type"] == "Modal"
        assert rendered["props"]["title"] == "Confirm"
        assert rendered["props"]["open"] is True

    def test_modal_size(self):
        """Test Modal size prop."""
        modal = Modal(size="lg")
        rendered = modal.render()
        assert rendered["props"]["size"] == "lg"

    def test_modal_with_callback(self):
        """Test Modal with on_close callback."""
        cb = MockCallback()
        modal = Modal(on_close=cb)
        rendered = modal.render()
        assert rendered["props"]["onClose"] == {"callbackId": "cb-123"}


class TestDialog:
    """Tests for Dialog component."""

    def test_dialog_renders(self):
        """Test Dialog renders correctly."""
        dialog = Dialog(title="Delete Item", description="Are you sure?")
        rendered = dialog.render()
        assert rendered["type"] == "Dialog"
        assert rendered["props"]["title"] == "Delete Item"
        assert rendered["props"]["description"] == "Are you sure?"

    def test_dialog_open(self):
        """Test Dialog open state."""
        dialog = Dialog(open=True)
        rendered = dialog.render()
        assert rendered["props"]["open"] is True

    def test_dialog_with_callback(self):
        """Test Dialog with on_open_change callback."""
        cb = MockCallback()
        dialog = Dialog(on_open_change=cb)
        rendered = dialog.render()
        assert rendered["props"]["onOpenChange"] == {"callbackId": "cb-123"}


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
        assert rendered["props"]["showValue"] is True


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
