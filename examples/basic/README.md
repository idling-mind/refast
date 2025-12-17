# Basic Refast Example

This is a simple example demonstrating the basic features of Refast.

## Features Demonstrated

- Basic page routing
- Component rendering (Container, Text, Button)
- Callback handling
- State management

## Running the Example

1. Install dependencies:

```bash
cd examples/basic
uv pip install -e ../..
```

2. Run the app:

```bash
uvicorn app:app --reload
```

3. Open your browser to `http://localhost:8000`

## How It Works

The example creates a simple counter application:

- A text display shows the current count
- An "Increment" button increases the count
- A "Reset" button sets the count back to 0

When you click a button, a WebSocket message is sent to the server, which updates the state and sends back updated components.
