"""Tests for State class."""

import pytest
from pydantic import BaseModel
from refast.state import State


class TestStateBasic:
    """Tests for basic State operations."""
    
    def test_state_creation(self):
        """Test State can be created."""
        state = State()
        assert state is not None
    
    def test_state_empty_by_default(self):
        """Test State is empty by default."""
        state = State()
        assert state.to_dict() == {}
    
    def test_state_with_initial_dict(self):
        """Test State with initial dictionary."""
        state = State({"count": 0, "name": "test"})
        assert state["count"] == 0
        assert state["name"] == "test"


class TestStateDictOperations:
    """Tests for dict-like State operations."""
    
    def test_state_setitem(self):
        """Test State __setitem__."""
        state = State()
        state["count"] = 0
        assert state["count"] == 0
    
    def test_state_getitem(self):
        """Test State __getitem__."""
        state = State({"key": "value"})
        assert state["key"] == "value"
    
    def test_state_getitem_keyerror(self):
        """Test State __getitem__ raises KeyError for missing key."""
        state = State()
        with pytest.raises(KeyError):
            _ = state["missing"]
    
    def test_state_contains(self):
        """Test State __contains__."""
        state = State({"key": "value"})
        assert "key" in state
        assert "missing" not in state
    
    def test_state_get_with_default(self):
        """Test State get() with default."""
        state = State()
        assert state.get("missing", 42) == 42
    
    def test_state_get_without_default(self):
        """Test State get() without default returns None."""
        state = State()
        assert state.get("missing") is None
    
    def test_state_get_existing(self):
        """Test State get() for existing key."""
        state = State({"key": "value"})
        assert state.get("key") == "value"
    
    def test_state_set(self):
        """Test State set() method."""
        state = State()
        state.set("key", "value")
        assert state["key"] == "value"
    
    def test_state_update(self):
        """Test State update() method."""
        state = State({"a": 1})
        state.update({"b": 2, "c": 3})
        assert state["a"] == 1
        assert state["b"] == 2
        assert state["c"] == 3
    
    def test_state_to_dict(self):
        """Test State to_dict() returns copy."""
        state = State({"a": 1, "b": 2})
        d = state.to_dict()
        assert d == {"a": 1, "b": 2}
        
        # Modifying the copy shouldn't affect the state
        d["c"] = 3
        assert "c" not in state


class TestStateWithPydantic:
    """Tests for State with Pydantic models."""
    
    def test_state_with_pydantic_model(self):
        """Test State with Pydantic model."""
        class AppState(BaseModel):
            count: int = 0
            name: str = ""
        
        state = State(AppState())
        assert state["count"] == 0
        assert state["name"] == ""
    
    def test_state_pydantic_model_values(self):
        """Test State with Pydantic model custom values."""
        class AppState(BaseModel):
            count: int = 0
            name: str = ""
        
        state = State(AppState(count=5, name="test"))
        assert state["count"] == 5
        assert state["name"] == "test"
    
    def test_state_pydantic_model_mutable(self):
        """Test State from Pydantic model is mutable."""
        class AppState(BaseModel):
            count: int = 0
        
        state = State(AppState())
        state["count"] = 10
        assert state["count"] == 10
    
    def test_state_validate_success(self):
        """Test State validate() with valid data."""
        class AppState(BaseModel):
            count: int = 0
        
        state = State(AppState())
        state["count"] = 5
        assert state.validate() is True
    
    def test_state_validate_failure(self):
        """Test State validate() with invalid data."""
        class AppState(BaseModel):
            count: int = 0
        
        state = State(AppState())
        state["count"] = "not an int"
        assert state.validate() is False
    
    def test_state_validate_without_model(self):
        """Test State validate() without model always returns True."""
        state = State({"anything": "goes"})
        assert state.validate() is True
    
    def test_state_validate_empty(self):
        """Test State validate() on empty state."""
        state = State()
        assert state.validate() is True


class TestStateInitialCopy:
    """Tests for State initial value copying."""
    
    def test_state_copies_initial_dict(self):
        """Test State copies initial dict."""
        initial = {"a": 1}
        state = State(initial)
        
        # Modifying original shouldn't affect state
        initial["b"] = 2
        assert "b" not in state
    
    def test_state_none_initial(self):
        """Test State with None initial."""
        state = State(None)
        assert state.to_dict() == {}
