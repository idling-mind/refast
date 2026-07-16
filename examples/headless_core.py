import asyncio
from pathlib import Path
from typing import Any

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import Container, Text
from refast.components.base import Component
from refast.components.registry import register_component
from refast.extensions import Extension


# 1. Define the Python class for the Custom Component
@register_component("CustomButton", package="custom-button", module="CustomButton")
class CustomButton(Component):
    component_type = "CustomButton"

    def __init__(
        self,
        label: str = "Click me",
        on_click: Any = None,
        class_name: str = "",
        id: str | None = None,
    ):
        super().__init__(id=id, class_name=class_name)
        self.label = label
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        props = {
            "label": self.label,
            "class_name": self.class_name,
        }
        if self.on_click:
            props["on_click"] = (
                self.on_click.serialize() if hasattr(self.on_click, "serialize") else self.on_click
            )

        return {
            "type": self.component_type,
            "id": self.id,
            "props": props,
            "children": self._render_children(),
        }


# 2. Define the Extension that registers the custom React component
class CustomButtonExtension(Extension):
    name = "custom-button"
    version = "0.1.0"
    description = "A custom button component for the headless core Refast app showcase"

    scripts = ["custom_button.js"]

    @property
    def static_path(self) -> Path:
        return Path(__file__).parent / "core_static"

    @property
    def components(self) -> list:
        return [CustomButton]


# 3. Create RefastApp in 'core' headless client mode
ui = RefastApp(
    title="Headless Core Client Showcase",
    debug=True,
    client_mode="core",  # Loads refast-client-core.js instead of refast-client.js
    extensions=[CustomButtonExtension()],  # Inject custom component assets
)


# 4. Define Python Callback
async def handle_button_click(ctx: Context):
    """Callback fired from the custom button extension."""
    ctx.state.set("clicks", ctx.state.get("clicks", 0) + 1)
    clicks = ctx.state.get("clicks")

    # Show a toast via the core ToastManager
    await ctx.show_toast(f"Button Clicked! ({clicks} times)")

    # Update state and display text on page
    message = f"Hello from the Refast backend! You clicked the custom extension button {clicks} times."
    await ctx.update_text("status_message", message)


# 5. Define Page using ONLY core components and extensions
@ui.page("/")
def headless_home(ctx: Context):
    return Container(
        [
            Container(
                [
                    Text("Refast Core Headless Mode", class_name="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight"),
                    Text(
                        "This app is running in client_mode='core'. The initial JS bundle (refast-client-core.js) "
                        "weighed only ~2.25kB gzipped because all standard UI components (like Card, Input, Tables) "
                        "were split and omitted. Only the core runtime and basic primitives (Container, Text, Toaster) "
                        "are loaded.",
                        class_name="text-slate-600 dark:text-slate-400 text-sm max-w-xl text-center leading-relaxed",
                    ),
                    # Custom button registered from our extension
                    CustomButton(
                        label="Trigger Backend Action",
                        on_click=ctx.callback(handle_button_click),
                        class_name="mt-4",
                    ),
                    # Core Text element displaying status updates
                    Text(
                        "Click the button above to communicate with FastAPI.",
                        id="status_message",
                        class_name="text-sm font-medium text-slate-500 mt-6 bg-slate-100 dark:bg-slate-800 px-4 py-2 rounded-full",
                    ),
                ],
                class_name="flex flex-col items-center justify-center space-y-6 text-center",
            )
        ],
        class_name="min-h-screen w-screen flex flex-col items-center justify-center p-8 bg-gradient-to-tr from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900 transition-colors duration-300",
    )


# 6. Include Router in FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    print("Starting Refast Headless Core example app...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
