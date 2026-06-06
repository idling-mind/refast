import asyncio
import os
import platform
import socket
import sys
import threading
import time
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
import psutil
import webview

from refast import Context, RefastApp
from refast.components import (
    Alert,
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Grid,
    Icon,
    IconButton,
    Input,
    Progress,
    Row,
    Switch,
    Text,
    ThemeSwitcher,
    Tooltip,
)
from refast.theme import catppuccin_theme

# Global references for window management
window = None
port = 8000
is_maximized = False
is_fullscreen = False
is_frameless = False

# Create the Refast App
ui = RefastApp(
    title="Refast Desktop Showcase",
    theme=catppuccin_theme,
)


# Helper: Find a free port starting from a default
def find_free_port(start_port=8000):
    p = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                p += 1


# Helper: Get current system resource stats
def get_system_stats():
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        drive = "C:\\" if os.name == "nt" else "/"
        disk = psutil.disk_usage(drive).percent
        return cpu, ram, disk
    except Exception:
        return 0.0, 0.0, 0.0


# Background loop to push system metrics updates to the UI
async def periodic_stats_updater():
    while True:
        try:
            for ctx in ui.active_contexts:
                # Only update if the user has auto-refresh enabled in their local session/state
                if ctx.state.get("auto_refresh", True):
                    cpu, ram, disk = get_system_stats()

                    # Update CPU progress and label text
                    await ctx.update_props("cpu-progress", {"value": int(cpu)})
                    await ctx.update_text("cpu-text", f"{cpu}%")

                    # Update RAM progress and label text
                    await ctx.update_props("ram-progress", {"value": int(ram)})
                    await ctx.update_text("ram-text", f"{ram}%")

                    # Update Disk progress and label text
                    await ctx.update_props("disk-progress", {"value": int(disk)})
                    await ctx.update_text("disk-text", f"{disk}%")
        except Exception as e:
            # Silently catch update errors (e.g. during disconnects)
            pass
        await asyncio.sleep(2.0)


# Lifespan manager for FastAPI to manage background tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(periodic_stats_updater())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# Window Action Callbacks
async def minimize_window(ctx: Context):
    if window:
        window.minimize()
        await ctx.show_toast("Window minimized to taskbar", variant="info")


async def toggle_maximize(ctx: Context):
    global is_maximized
    if window:
        if is_maximized:
            window.restore()
            is_maximized = False
            await ctx.show_toast("Window restored to default size", variant="info")
        else:
            window.maximize()
            is_maximized = True
            await ctx.show_toast("Window maximized", variant="info")


async def toggle_fullscreen(ctx: Context):
    global is_fullscreen
    if window:
        window.toggle_fullscreen()
        is_fullscreen = not is_fullscreen
        status = "Entered Fullscreen" if is_fullscreen else "Exited Fullscreen"
        await ctx.show_toast(status, variant="info")


async def close_window(ctx: Context):
    if window:
        await ctx.show_toast("Closing application...", variant="warning")
        await asyncio.sleep(0.5)
        window.destroy()


# Rename Title Callback
async def rename_window_title(ctx: Context, title_input: str):
    if not title_input:
        await ctx.show_toast("Please type a window title", variant="error")
        return
    if window:
        window.set_title(title_input)
        await ctx.show_toast(f"Window title updated to: '{title_input}'", variant="success")


# Window Preset Size Callback
async def resize_window_preset(ctx: Context, size_preset: str):
    if window:
        if size_preset == "small":
            window.resize(800, 600)
            await ctx.show_toast("Resized to 800 x 600", variant="success")
        elif size_preset == "medium":
            window.resize(1024, 768)
            await ctx.show_toast("Resized to 1024 x 768", variant="success")
        elif size_preset == "large":
            window.resize(1280, 720)
            await ctx.show_toast("Resized to 1280 x 720", variant="success")


# Toggle Frameless Window state by recreating the window dynamically
async def toggle_frameless_state(ctx: Context, checked: bool = None):
    global window, is_frameless, is_maximized, is_fullscreen
    
    # Determine the new target state (use checked bool if from switch, else toggle)
    new_state = checked if checked is not None else not is_frameless
    
    # Write to local storage to persist the choice
    ctx.store.local["is_frameless"] = new_state
    
    # Update backend global state
    is_frameless = new_state
    
    if window:
        # Fetch current window placement properties to preserve them
        width = window.width
        height = window.height
        x = window.x
        y = window.y
        title = window.title
        url = window.get_current_url() or f"http://127.0.0.1:{port}"
        
        # Reset maximized and fullscreen tracking since we are initializing a clean window
        is_maximized = False
        is_fullscreen = False
        
        old_window = window
        print(f"[*] Recreating window: frameless={is_frameless}, title='{title}', url='{url}'")
        
        # Create a new window instance with the new frame style
        window = webview.create_window(
            title=title,
            url=url,
            width=width,
            height=height,
            x=x,
            y=y,
            frameless=is_frameless,
            min_size=(800, 600),
        )
        
        # Destroy the previous window instance
        old_window.destroy()


# Native Dialog Callbacks
async def trigger_open_file(ctx: Context):
    if not window:
        return
    await ctx.show_toast("Opening native file dialog...", variant="info")
    file_types = ("All files (*.*)", "Python files (*.py)", "Text files (*.txt)")
    result = window.create_file_dialog(webview.OPEN_DIALOG, file_types=file_types)

    if result:
        file_path = result[0]
        try:
            size_kb = os.path.getsize(file_path) / 1024
            display_text = f"Selected File: {os.path.basename(file_path)} ({size_kb:.2f} KB)\nFull Path: {file_path}"
            await ctx.update_text("file-dialog-result", display_text)
            await ctx.show_toast("File loaded!", variant="success")
        except Exception as e:
            await ctx.show_toast(f"Error accessing file info: {e}", variant="error")
    else:
        await ctx.show_toast("File selection cancelled", variant="warning")


async def trigger_select_folder(ctx: Context):
    if not window:
        return
    await ctx.show_toast("Opening native folder dialog...", variant="info")
    result = window.create_file_dialog(webview.FOLDER_DIALOG)

    if result:
        folder_path = result[0]
        try:
            # Count the files inside
            all_items = os.listdir(folder_path)
            file_count = len([f for f in all_items if os.path.isfile(os.path.join(folder_path, f))])
            display_text = f"Selected Folder: {folder_path}\nFiles Count: {file_count} files"
            ctx.state.set("selected_folder", folder_path)
            await ctx.update_text("folder-dialog-result", display_text)
            # Enable the Open in Explorer button
            await ctx.update_props("open-explorer-btn", {"disabled": False})
            await ctx.show_toast("Folder selected!", variant="success")
        except Exception as e:
            await ctx.show_toast(f"Error reading directory contents: {e}", variant="error")
    else:
        await ctx.show_toast("Folder selection cancelled", variant="warning")


async def trigger_save_file(ctx: Context):
    if not window:
        return
    await ctx.show_toast("Opening native save dialog...", variant="info")
    file_types = ("Text files (*.txt)", "JSON files (*.json)", "All files (*.*)")
    result = window.create_file_dialog(
        webview.SAVE_DIALOG, file_types=file_types, save_filename="refast_export.txt"
    )

    if result:
        save_path = result[0] if isinstance(result, (list, tuple)) else result
        display_text = f"Target Save Location: {save_path}"
        await ctx.update_text("save-dialog-result", display_text)
        await ctx.show_toast("Save destination selected!", variant="success")
    else:
        await ctx.show_toast("Save cancelled", variant="warning")


async def trigger_open_explorer(ctx: Context):
    folder_path = ctx.state.get("selected_folder")
    if folder_path and os.path.exists(folder_path):
        try:
            os.startfile(folder_path)
            await ctx.show_toast("Opened folder in Explorer", variant="success")
        except Exception as e:
            await ctx.show_toast(f"Failed to open explorer: {e}", variant="error")
    else:
        await ctx.show_toast("Please select a folder first", variant="error")


# Computer Function Callbacks
async def trigger_sound_beep(ctx: Context):
    try:
        if os.name == "nt":
            import winsound

            # Play system warning alert and a hardware beep
            winsound.MessageBeep()
            winsound.Beep(1200, 300)
            await ctx.show_toast("Motherboard audio alert triggered!", variant="success")
        else:
            print("\a", end="")  # Fallback ASCII system bell
            await ctx.show_toast("Fallback system bell triggered!", variant="success")
    except Exception as e:
        await ctx.show_toast(f"Beep action failed: {e}", variant="error")


async def toggle_auto_refresh_state(ctx: Context):
    current = ctx.state.get("auto_refresh", True)
    ctx.state.set("auto_refresh", not current)
    status_msg = "Auto-refresh enabled" if not current else "Auto-refresh disabled"
    await ctx.show_toast(status_msg, variant="info")


# Define UI Page
@ui.page("/")
def index_page(ctx: Context):
    # Retrieve system properties for static specs
    cpu_cores_logical = psutil.cpu_count(logical=True)
    cpu_cores_physical = psutil.cpu_count(logical=False)
    total_ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
    os_name = f"{platform.system()} {platform.release()}"
    python_ver = platform.python_version()

    # Initial stats fetch
    init_cpu, init_ram, init_disk = get_system_stats()
    
    # Read frameless configuration choice from persistent local storage
    init_frameless = ctx.store.local.get("is_frameless", False)

    # Build Header Bar with Title and Custom Window Controls (iconbuttons)
    # Adding 'pywebview-drag-region' to class_name makes it draggable in frameless mode!
    header = Card(
        class_name="mb-6 bg-slate-900 border-slate-800 text-slate-100 pywebview-drag-region",
        children=[
            CardContent(
                class_name="py-3 px-6 flex flex-row justify-between items-center",
                children=[
                    Row(
                        gap=3,
                        align="center",
                        children=[
                            Icon("monitor", size=22, class_name="text-purple-400"),
                            Column(
                                gap=0,
                                children=[
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Text("Refast Desktop Environment", class_name="font-bold text-lg"),
                                            Badge("Frameless Mode", variant="outline", class_name="text-xs bg-purple-950/30 text-purple-300 border-purple-800") if init_frameless else Container(),
                                        ]
                                    ),
                                    Text("PyWebView native window bridge showcase (Drag header to move window)", class_name="text-xs text-muted-foreground"),
                                ],
                            ),
                        ],
                    ),
                    Row(
                        gap=1,
                        children=[
                            Tooltip(
                                content="Minimize Window",
                                children=IconButton(
                                    icon="minus",
                                    variant="ghost",
                                    size="sm",
                                    class_name="hover:bg-slate-800 hover:text-slate-200",
                                    on_click=ctx.callback(minimize_window),
                                ),
                            ),
                            Tooltip(
                                content="Maximize / Restore",
                                children=IconButton(
                                    icon="square",
                                    variant="ghost",
                                    size="sm",
                                    class_name="hover:bg-slate-800 hover:text-slate-200",
                                    on_click=ctx.callback(toggle_maximize),
                                ),
                            ),
                            Tooltip(
                                content="Toggle Fullscreen",
                                children=IconButton(
                                    icon="maximize-2",
                                    variant="ghost",
                                    size="sm",
                                    class_name="hover:bg-slate-800 hover:text-slate-200",
                                    on_click=ctx.callback(toggle_fullscreen),
                                ),
                            ),
                            Tooltip(
                                content="Close App",
                                children=IconButton(
                                    icon="x",
                                    variant="ghost",
                                    size="sm",
                                    class_name="hover:bg-red-950 hover:text-red-400",
                                    on_click=ctx.callback(close_window),
                                ),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    # 1. System Info Specs Card
    sys_specs_card = Card(
        class_name="bg-card shadow-lg",
        children=[
            CardHeader(
                children=[
                    CardTitle("Computer Specifications"),
                    CardDescription("Static system parameters read from platform/sys"),
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=4,
                        children=[
                            Row(
                                justify="between",
                                children=[
                                    Text("Operating System", class_name="text-muted-foreground font-medium"),
                                    Badge(os_name, variant="secondary"),
                                ],
                            ),
                            Row(
                                justify="between",
                                children=[
                                    Text("Processor Cores", class_name="text-muted-foreground font-medium"),
                                    Badge(f"{cpu_cores_physical} Cores (Logical: {cpu_cores_logical})", variant="secondary"),
                                ],
                            ),
                            Row(
                                justify="between",
                                children=[
                                    Text("Installed Memory", class_name="text-muted-foreground font-medium"),
                                    Badge(f"{total_ram_gb} GB", variant="secondary"),
                                ],
                            ),
                            Row(
                                justify="between",
                                children=[
                                    Text("Python Engine", class_name="text-muted-foreground font-medium"),
                                    Badge(f"v{python_ver}", variant="secondary"),
                                ],
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    # 2. System Health Metrics Card
    sys_health_card = Card(
        class_name="bg-card shadow-lg",
        children=[
            CardHeader(
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Column(
                                gap=1,
                                children=[
                                    CardTitle("System Diagnostics"),
                                    CardDescription("Dynamic CPU, RAM, and primary Drive diagnostics"),
                                ]
                            ),
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Text("Auto-Refresh", class_name="text-xs text-muted-foreground font-medium"),
                                    Switch(
                                        id="auto-refresh-switch",
                                        checked=ctx.state.get("auto_refresh", True),
                                        on_checked_change=ctx.callback(toggle_auto_refresh_state),
                                    ),
                                ],
                            ),
                        ],
                    )
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=5,
                        children=[
                            # CPU Usage bar
                            Column(
                                gap=2,
                                children=[
                                    Row(
                                        justify="between",
                                        children=[
                                            Text("Processor Activity (CPU)", class_name="font-semibold text-sm"),
                                            Text(f"{init_cpu}%", id="cpu-text", class_name="font-mono text-sm"),
                                        ],
                                    ),
                                    Progress(
                                        id="cpu-progress",
                                        value=int(init_cpu),
                                        max=100,
                                        foreground_color="primary",
                                        striped="animated",
                                    ),
                                ],
                            ),
                            # Memory Usage bar
                            Column(
                                gap=2,
                                children=[
                                    Row(
                                        justify="between",
                                        children=[
                                            Text("RAM Memory Load", class_name="font-semibold text-sm"),
                                            Text(f"{init_ram}%", id="ram-text", class_name="font-mono text-sm"),
                                        ],
                                    ),
                                    Progress(
                                        id="ram-progress",
                                        value=int(init_ram),
                                        max=100,
                                        foreground_color="accent",
                                    ),
                                ],
                            ),
                            # Disk Usage bar
                            Column(
                                gap=2,
                                children=[
                                    Row(
                                        justify="between",
                                        children=[
                                            Text("Disk Space Usage", class_name="font-semibold text-sm"),
                                            Text(f"{init_disk}%", id="disk-text", class_name="font-mono text-sm"),
                                        ],
                                    ),
                                    Progress(
                                        id="disk-progress",
                                        value=int(init_disk),
                                        max=100,
                                        foreground_color="destructive",
                                    ),
                                ],
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    # 3. Native dialog card
    dialog_card = Card(
        class_name="bg-card shadow-lg",
        children=[
            CardHeader(
                children=[
                    CardTitle("OS File & Directory Integrations"),
                    CardDescription("Invoke native dialog screens and map files to local apps"),
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=4,
                        children=[
                            # File selector
                            Row(
                                gap=4,
                                align="center",
                                children=[
                                    Button("Select File", icon="file", on_click=ctx.callback(trigger_open_file)),
                                    Text("No file chosen yet...", id="file-dialog-result", class_name="text-xs text-muted-foreground flex-1 break-all"),
                                ],
                            ),
                            # Folder selector
                            Row(
                                gap=4,
                                align="center",
                                children=[
                                    Button("Select Folder", icon="folder", on_click=ctx.callback(trigger_select_folder)),
                                    Text("No folder chosen yet...", id="folder-dialog-result", class_name="text-xs text-muted-foreground flex-1 break-all"),
                                ],
                            ),
                            # Action: Open explorer
                            Row(
                                gap=4,
                                children=[
                                    Button(
                                        "Open Selected Folder in File Explorer",
                                        id="open-explorer-btn",
                                        icon="external-link",
                                        variant="outline",
                                        disabled=True,  # enabled after folder is selected
                                        on_click=ctx.callback(trigger_open_explorer),
                                    )
                                ],
                            ),
                            # Save Dialog
                            Row(
                                gap=4,
                                align="center",
                                children=[
                                    Button("Save File Dialog", icon="save", variant="secondary", on_click=ctx.callback(trigger_save_file)),
                                    Text("Awaiting save location...", id="save-dialog-result", class_name="text-xs text-muted-foreground flex-1 break-all"),
                                ],
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    # 4. System utilities card
    utils_card = Card(
        class_name="bg-card shadow-lg",
        children=[
            CardHeader(
                children=[
                    CardTitle("Desktop System Tools"),
                    CardDescription("Interact with physical hardware and active GUI parameters"),
                ]
            ),
            CardContent(
                children=[
                    Column(
                        gap=6,
                        children=[
                            # Sound Beep Trigger
                            Column(
                                gap=2,
                                children=[
                                    Text("Hardware/Motherboard Beep", class_name="font-semibold text-sm"),
                                    Text("Uses winsound on Windows to play a physical beep", class_name="text-xs text-muted-foreground mb-1"),
                                    Button(
                                        "Trigger Motherboard Beep Sound",
                                        icon="volume-2",
                                        variant="default",
                                        on_click=ctx.callback(trigger_sound_beep),
                                    ),
                                ],
                            ),
                            # Rename window
                            Column(
                                gap=2,
                                children=[
                                    Text("Rename GUI Window Title", class_name="font-semibold text-sm"),
                                    Text("Dynamically update the parent window's text bar", class_name="text-xs text-muted-foreground mb-1"),
                                    Row(
                                        gap=2,
                                        children=[
                                            Input(
                                                placeholder="Enter new window name...",
                                                class_name="flex-1",
                                                on_change=ctx.save_prop("title_input"),
                                            ),
                                            Button(
                                                "Apply",
                                                variant="outline",
                                                on_click=ctx.callback(rename_window_title, props=["title_input"]),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # Window Resizing Presets
                            Column(
                                gap=2,
                                children=[
                                    Text("Window Dimensions Preset", class_name="font-semibold text-sm"),
                                    Text("Resize the application window layout instantly", class_name="text-xs text-muted-foreground mb-2"),
                                    Row(
                                        gap=2,
                                        children=[
                                            Button(
                                                "800 x 600",
                                                variant="outline",
                                                size="sm",
                                                on_click=ctx.callback(resize_window_preset, size_preset="small"),
                                            ),
                                            Button(
                                                "1024 x 768",
                                                variant="outline",
                                                size="sm",
                                                on_click=ctx.callback(resize_window_preset, size_preset="medium"),
                                            ),
                                            Button(
                                                "1280 x 720",
                                                variant="outline",
                                                size="sm",
                                                on_click=ctx.callback(resize_window_preset, size_preset="large"),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            # Dynamic Frameless Switch
                            Row(
                                justify="between",
                                align="center",
                                children=[
                                    Column(
                                        gap=1,
                                        children=[
                                            Text("Frameless Window Border", class_name="font-semibold text-sm"),
                                            Text("Toggle OS border/title bar (recreates window)", class_name="text-xs text-muted-foreground"),
                                        ]
                                    ),
                                    Switch(
                                        id="frameless-switch",
                                        checked=init_frameless,
                                        on_checked_change=ctx.callback(toggle_frameless_state),
                                    ),
                                ],
                                class_name="border-t border-slate-800 pt-4"
                            ),
                        ],
                    )
                ]
            ),
        ],
    )

    # Footer Card
    footer = Card(
        class_name="mt-6 bg-slate-900 border-slate-800 text-slate-100",
        children=[
            CardContent(
                class_name="py-4 px-6 flex flex-row justify-between items-center",
                children=[
                    Text("Refast-PyWebView Desktop Integration Sample", class_name="text-sm text-slate-400"),
                    Row(
                        gap=4,
                        align="center",
                        children=[
                            ThemeSwitcher(default_theme="dark"),
                        ],
                    ),
                ],
            )
        ],
    )

    # Assemble complete dashboard page
    return Container(
        class_name="min-h-screen p-6 bg-background flex flex-col justify-between",
        children=[
            header,
            Grid(
                columns=2,
                gap=6,
                class_name="flex-grow",
                children=[
                    # Column 1
                    Column(gap=6, children=[sys_specs_card, sys_health_card]),
                    # Column 2
                    Column(gap=6, children=[dialog_card, utils_card]),
                ],
            ),
            footer,
        ],
    )


# Setup FastAPI Server Application
app = FastAPI(title="Refast Desktop App Server", lifespan=lifespan)
app.include_router(ui.router)


def run_server(server_port):
    uvicorn.run(app, host="127.0.0.1", port=server_port, log_level="warning")


if __name__ == "__main__":
    port = find_free_port(8000)
    print(f"[*] Starting background Refast/FastAPI server on port {port}...")
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    # Give uvicorn a short moment to bind and launch
    time.sleep(1.5)

    print("[*] Launching pywebview native client...")
    # Open the pywebview window loaded with the FastAPI server URL
    window = webview.create_window(
        title="Refast Desktop Showcase",
        url=f"http://127.0.0.1:{port}",
        width=1000,
        height=750,
        min_size=(800, 600),
        frameless=is_frameless,
    )

    # Start the native window main loop
    webview.start()
    print("[*] Application terminated.")
