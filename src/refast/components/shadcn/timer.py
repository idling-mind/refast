"""Timer component — fires a server callback at a regular interval."""

from typing import Any

from refast.components.base import Component


class Timer(Component):
    """
    An invisible component that repeatedly triggers a server callback at a
    fixed interval.  Place it anywhere in your component tree; it renders
    nothing in the browser.

    Example:
        ```python
        import refast as rf
        from refast.components import Timer

        app = rf.RefastApp()

        @app.page("/")
        def home(ctx):
            return rf.Container(
                Timer(
                    interval=2000,
                    enabled=True,
                    on_tick=ctx.callback(handle_tick),
                ),
            )

        async def handle_tick(ctx):
            # called every 2 seconds
            await ctx.refresh()
        ```

    Args:
        interval: Milliseconds between ticks.  Must be >= 100.  Defaults to
            ``1000`` (one second).
        enabled: When ``False`` the timer is paused and no callbacks are
            fired.  Defaults to ``True``.
        on_tick: Server callback invoked on each tick.  Receives ``ctx`` as
            its only positional argument.
    """

    component_type: str = "Timer"

    def __init__(
        self,
        interval: int = 1000,
        enabled: bool = True,
        on_tick: Any = None,
        id: str | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        if interval < 100:
            raise ValueError("interval must be >= 100 ms")
        super().__init__(id=id, extra_props=extra_props)
        self.interval = interval
        self.enabled = enabled
        self.on_tick = on_tick

    def render(self) -> dict[str, Any]:
        props: dict[str, Any] = {
            "interval": self.interval,
            "enabled": self.enabled,
        }

        if self.on_tick:
            props["on_tick"] = self.on_tick.serialize()

        props.update(self._serialize_extra_props())

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": [],
        }
