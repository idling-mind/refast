# Input Component Features Example

This example demonstrates the enhanced Input component features:

## Features Showcased

### 1. Label with Required Indicator
- Input fields can have a `label` prop that displays above the input
- When `required=True`, a red asterisk (*) is automatically shown next to the label

### 2. Description Text
- The `description` prop adds helpful hint text below the label
- Appears in muted text color
- Useful for providing context or instructions

### 3. Error States
- The `error` prop displays validation errors
- When error is present:
  - Input border becomes red
  - Placeholder text becomes red
  - Error message displays below the input in red text
  - Error message replaces the description text

### 4. Enhanced Event Handlers
New keyboard and input events are now supported:
- `on_keydown` - Fired when a key is pressed down
- `on_keyup` - Fired when a key is released
- `on_input` - Fired on every input change

### 5. Form Validation Example
The example includes:
- Real-time email validation
- Password strength checking
- Required field indicators
- Submit handler with validation

## Running the Example

```bash
cd examples/input_features
python app.py
```

Then open http://127.0.0.1:8000 in your browser.

## Key Behaviors

1. **Username** - Required field with description
2. **Email** - Real-time validation with error display
3. **Password** - Keyboard event demo (press Enter to see message)
4. **Phone** - Optional field example (no required asterisk)

Try filling out the form to see all features in action!
