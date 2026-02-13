"""Test example to verify ctx.update_prop() works with input value props."""

import asyncio

from fastapi import FastAPI

from refast import RefastApp
from refast.components import Button, Container, Flex, Heading, Input, Select, Textarea

ui = RefastApp(title="Test Update Prop Value")


@ui.page("/")
def home(ctx):
    async def set_input_value(event):
        """Set the input value using ctx.update_props()."""
        await ctx.update_props("my-input", {"value": "Updated via update_props!"})
        await asyncio.sleep(5)
        await ctx.update_props("my-input", {"value": "Final Value after 5 seconds!"})
    
    async def clear_input_value(event):
        """Clear the input value using ctx.update_props()."""
        await ctx.update_props("my-input", {"value": ""})
    
    async def set_textarea_value(event):
        """Set the textarea value using ctx.update_props()."""
        await ctx.update_props("my-textarea", {"value": "This is a multi-line\ntext that was set\nvia update_props!"})
    
    async def set_select_value(event):
        """Set the select value using ctx.update_props()."""
        await ctx.update_props("my-select", {"value": "option2"})

    return Container(
        children=[
            Heading("Test ctx.update_props() with Input Values", level=1),
            
            Heading("Input Test", level=2, class_name="mt-4"),
            Input(
                id="my-input",
                name="test-input",
                label="Test Input",
                placeholder="Type something...",
            ),
            Flex(
                children=[
                    Button("Set Value", on_click=ctx.callback(set_input_value)),
                    Button("Clear Value", on_click=ctx.callback(clear_input_value), variant="secondary"),
                ],
                direction="row",
                gap="2",
                class_name="mt-2"
            ),
            
            Heading("Textarea Test", level=2, class_name="mt-6"),
            Textarea(
                id="my-textarea",
                name="test-textarea",
                label="Test Textarea",
                placeholder="Type something...",
                rows=4,
            ),
            Button("Set Value", on_click=ctx.callback(set_textarea_value), class_name="mt-2"),
            
            Heading("Select Test", level=2, class_name="mt-6"),
            Select(
                id="my-select",
                name="test-select",
                label="Test Select",
                options=[
                    {"value": "option1", "label": "Option 1"},
                    {"value": "option2", "label": "Option 2"},
                    {"value": "option3", "label": "Option 3"},
                ],
                placeholder="Select an option...",
            ),
            Button("Set to Option 2", on_click=ctx.callback(set_select_value), class_name="mt-2"),
        ],
        class_name="p-8 max-w-2xl"
    )

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8765)