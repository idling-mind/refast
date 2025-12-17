"""State management for Refast."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class State(Generic[T]):
    """
    State container with optional type validation.

    Can be used with a Pydantic model for typed state:

    Example:
        ```python
        class AppState(BaseModel):
            count: int = 0
            user: str | None = None

        @ui.page("/")
        def home(ctx: Context[AppState]):
            ctx.state.count += 1
            return Text(f"Count: {ctx.state.count}")
        ```

    Or as a simple dict:
        ```python
        ctx.state["count"] = 0
        ```
    """

    def __init__(self, initial: T | dict[str, Any] | None = None):
        if isinstance(initial, BaseModel):
            self._data = initial.model_dump()
            self._model_class = type(initial)
        elif isinstance(initial, dict):
            self._data = initial.copy()
            self._model_class = None
        else:
            self._data = {}
            self._model_class = None

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value with optional default."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a value."""
        self._data[key] = value

    def update(self, data: dict[str, Any]) -> None:
        """Update multiple values."""
        self._data.update(data)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return self._data.copy()

    def validate(self) -> bool:
        """Validate against the model if one was provided."""
        if self._model_class:
            try:
                self._model_class(**self._data)
                return True
            except Exception:
                return False
        return True
