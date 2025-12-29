"""Test that package imports work correctly."""



def test_import_refast():
    """Test that refast package can be imported."""
    import refast

    assert hasattr(refast, "__version__")


def test_import_refastapp():
    """Test that RefastApp can be imported."""
    from refast import RefastApp

    assert RefastApp is not None


def test_import_context():
    """Test that Context can be imported."""
    from refast import Context

    assert Context is not None


def test_import_state():
    """Test that State can be imported."""
    from refast import State

    assert State is not None


def test_version():
    """Test version is set correctly."""
    from refast import __version__

    assert __version__ == "0.1.0"
