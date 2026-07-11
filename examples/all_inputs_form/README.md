# Refast Form Submission Showcase

This example demonstrates how to build a unified form containing all Refast input components, including both basic inputs and the advanced components with new `name` prop support.

## Components Showcased

1. **Text Inputs**:
   - `Input`
   - `Textarea`

2. **Choice Controls**:
   - `Select`
   - `RadioGroup` / `Radio`

3. **Checkboxes & Multi-select**:
   - `Checkbox`
   - `Switch`
   - `Combobox` (multi-select)

4. **Advanced Controls (New `name` Prop Support)**:
   - `Slider`
   - `Toggle`
   - `ToggleGroup` (multi-select)
   - `Calendar` (multiple dates selection)
   - `DatePicker`
   - `InputOTP`
   - `FileUploader` (multiple files)

## How It Works

All controls are wrapped inside a single `<Form>` container component. The form intercepts the submit event on the client-side, aggregates all values from the inputs (supporting both single-value fields and multi-value/array fields like `ToggleGroup` or `Calendar` and lists of files in `FileUploader`), and transmits them to the server-side callback:

```python
async def handle_submit(ctx: Context, **kwargs):
    # kwargs receives the key-value dictionary of all named controls!
    print(kwargs)
```

## Running the Example

Make sure dependencies are installed and run the application using Python:

```bash
uv run python examples/all_inputs_form/app.py
```

Open your browser to `http://localhost:8000` to view the form showcase!
