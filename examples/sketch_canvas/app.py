"""Test example for refast-sketch-canvas extension."""

from fastapi import FastAPI
from refast import RefastApp, Context
from refast.components import Container, Text, Button, Row, Column
from refast_sketch_canvas import SketchCanvas

ui = RefastApp(title="Sketch Canvas Test")


@ui.page("/")
def home(ctx: Context):
    return Container(
        class_name="p-8 max-w-2xl mx-auto",
        children=[
            Text("Sketch Canvas Demo", class_name="text-2xl font-bold mb-4"),
            Text("Draw something below:", class_name="mb-2"),
            SketchCanvas(
                id="canvas",
                width="100%",
                height="400px",
                stroke_color="blue",
                stroke_width=4,
                canvas_color="#f5f5f5",
                class_name="border rounded-lg",
            ),
        ]
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
