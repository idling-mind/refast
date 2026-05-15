"""Markdown Features Example - Mermaid diagrams and LaTeX math.

This example demonstrates:
- Rendering Mermaid diagrams inside Markdown with enable_mermaid=True
- Rendering LaTeX math expressions with enable_latex=True
- Both libraries are loaded on demand (not bundled in the main JS)

Run this file with:
    python app.py

Then open http://localhost:8000 in your browser.
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Markdown,
    Row,
    ThemeSwitcher,
)

ui = RefastApp(title="Markdown Features")

# ---------------------------------------------------------------------------
# Content blocks
# ---------------------------------------------------------------------------

MERMAID_MD = """\
# Mermaid Diagrams

Refast renders fenced ` ```mermaid ` blocks as interactive SVG diagrams.
The Mermaid library (~2.5 MB) is loaded **only** when `enable_mermaid=True`.

## Flowchart

```mermaid
flowchart TD
    A([Start]) --> B{User logged in?}
    B -- Yes --> C[Show Dashboard]
    B -- No  --> D[Show Login Page]
    C --> E([End])
    D --> E
```

## Sequence diagram

```mermaid
sequenceDiagram
    participant Browser
    participant Server
    Browser->>Server: GET /
    Server-->>Browser: 200 HTML
    Browser->>Server: WS connect
    Server-->>Browser: Component tree
    Browser->>Server: Button click event
    Server-->>Browser: State update
```

## Entity relationship diagram

```mermaid
erDiagram
    USER {
        int id PK
        string name
        string email
    }
    POST {
        int id PK
        string title
        text   body
        int    user_id FK
    }
    USER ||--o{ POST : "writes"
```
"""

LATEX_MD = r"""
# LaTeX / KaTeX Math

Refast renders inline math with `$...$` and display math with `$$...$$`.
KaTeX (~1.8 MB) is loaded **only** when `enable_latex=True`.

## Inline math

Einstein's famous equation $E = mc^2$ and Euler's identity $e^{i\pi} + 1 = 0$.

## Display math — Gaussian integral

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

## Maxwell's equations (differential form)

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
\qquad
\nabla \cdot \mathbf{B} = 0
$$

$$
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
\qquad
\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
$$

## Quadratic formula

The roots of $ax^2 + bx + c = 0$ are:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

## Matrix

$$
\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix},
\quad
\det(\mathbf{A}) = ad - bc
$$
"""


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------


@ui.page("/")
def index(ctx: Context):
    return Container(
        class_name="p-6 max-w-7xl mx-auto",
        children=[
            ThemeSwitcher(),
            Card(
                class_name="mb-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Markdown · Mermaid + LaTeX"),
                            CardDescription(
                                "Both libraries are lazy-loaded — only fetched when the "
                                "corresponding prop is enabled."
                            ),
                        ]
                    ),
                ]
            ),
            Row(
                class_name="gap-4",
                children=[
                    Column(
                        class_name="flex-1",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("Mermaid diagrams"),
                                            CardDescription("enable_mermaid=True"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Markdown(
                                                content=MERMAID_MD,
                                                enable_mermaid=True,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    Column(
                        class_name="flex-1",
                        children=[
                            Card(
                                children=[
                                    CardHeader(
                                        children=[
                                            CardTitle("LaTeX math"),
                                            CardDescription("enable_latex=True"),
                                        ]
                                    ),
                                    CardContent(
                                        children=[
                                            Markdown(
                                                content=LATEX_MD,
                                                enable_latex=True,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
