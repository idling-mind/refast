# Real-time Dashboard Example

This example demonstrates how to build a real-time dashboard that updates automatically without user interaction.

## Features Demonstrated

- **Server-Sent Updates**: The server pushes updates to the client using WebSockets.
- **Background Tasks**: Uses `asyncio` to run a background task that generates data.
- **Global State**: Maintains shared state across all connected clients.
- **Client-Specific State**: Maintains unique state (Client ID, update counter) for each connected client.
- **Dynamic UI**: Updates the entire dashboard UI periodically with mixed global and client-specific data.

## How it Works

1.  A global `dashboard_data` dictionary holds the current state.
2.  A background task `update_dashboard_task` runs every 2 seconds.
3.  The task updates the global data and then iterates through all active WebSocket connections.
4.  For each connection, it updates client-specific state (counter) and calls `ctx.replace()` to push the new UI structure.

## Running the Example

1.  Ensure you have the environment set up.
2.  Run the app:

```bash
cd examples/realtime_dashboard
python app.py
```

3.  Open http://localhost:8000 in your browser.
4.  Open multiple tabs to see them all update in sync!
