import logging
import re

from refast import components as rc

logger = logging.getLogger(__name__)

def render_markdown_with_demo_apps(content: str, locals: dict):
    """Renders markdown content with embedded demo apps.

    The markdown can include special markers to indicate where the demo apps should be rendered.
    Example usage in markdown:

    ```markdown
    # Demo App

    {{ demo_app }}

    Other content...
    ```
    The `demo_app` variable in the `locals` dictionary should be a function that returns a
    Refast component.

    Args:
        content (str): The markdown content to render.
        locals (dict): A dictionary of local variables that may include demo app variables.

    Returns:
        A Refast component that renders the markdown content with embedded demo apps.
    """
    splits = re.split(r"(\{\{.*?\}\})", content)
    components = []
    for part in splits:
        match = re.match(r"\{\{(.*?)\}\}", part)
        if match:
            var_name = match.group(1).strip()
            if var_name in locals:
                components.append(
                    rc.Container(
                        children = [locals[var_name]],
                        class_name="border rounded p-4 mb-4 overflow-auto",
                    )
                )
            else:
                logger.error(f"Demo app variable '{var_name}' not found in locals")
                components.append(
                    rc.Alert(
                        "Demo app not found",
                        message=f"Variable '{var_name}' could not be found.",
                        variant="destructive",
                    )
                )  # Show as-is if not found
        else:
            components.append(rc.Markdown(part))
    return rc.Column(components, class_name="w-full min-w-0")
