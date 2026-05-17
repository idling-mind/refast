"""URL Parameters Example.

This example demonstrates all URL parameter features added to Refast:

- Path parameters:
    /books/{id:int}      → ctx.path_params["id"]  (auto-coerced to int)
    /genre/{slug}        → ctx.path_params["slug"] (string)
- Query parameters:
    /search?q=...&genre=...&page=2  → ctx.query_params["q"], etc.
- ctx.url property — full current URL including query string
- ctx.load() for navigating with path params and query strings
- Browser back / forward preserves the full URL (including query string)

Run with:
    uvicorn examples.url_params.app:app --reload --port 8000
"""

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
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
    Heading,
    Input,
    Row,
    Select,
    Separator,
    Text,
)

# ---------------------------------------------------------------------------
# App & data
# ---------------------------------------------------------------------------

ui = RefastApp(title="Bookstore — URL Params Demo")

BOOKS = [
    {
        "id": 1,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "author_slug": "david-thomas",
        "genre": "programming",
        "year": 1999,
        "description": "A classic guide on software craftsmanship and practical development habits.",
        "rating": 4.8,
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "author_slug": "robert-martin",
        "genre": "programming",
        "year": 2008,
        "description": "Principles, patterns, and practices of writing clean, readable code.",
        "rating": 4.6,
    },
    {
        "id": 3,
        "title": "Design Patterns",
        "author": "Gang of Four",
        "author_slug": "gang-of-four",
        "genre": "programming",
        "year": 1994,
        "description": "The seminal catalog of reusable object-oriented design patterns.",
        "rating": 4.5,
    },
    {
        "id": 4,
        "title": "Refactoring",
        "author": "Martin Fowler",
        "author_slug": "martin-fowler",
        "genre": "programming",
        "year": 1999,
        "description": "Improving the design of existing code through safe, incremental transformations.",
        "rating": 4.7,
    },
    {
        "id": 5,
        "title": "The Mythical Man-Month",
        "author": "Fred Brooks",
        "author_slug": "fred-brooks",
        "genre": "programming",
        "year": 1975,
        "description": "Essays on software engineering and project management, still relevant today.",
        "rating": 4.4,
    },
    {
        "id": 6,
        "title": "Structure and Interpretation of Computer Programs",
        "author": "Harold Abelson",
        "author_slug": "harold-abelson",
        "genre": "programming",
        "year": 1996,
        "description": "The legendary MIT textbook on programming and computational thinking.",
        "rating": 4.6,
    },
    {
        "id": 7,
        "title": "Dune",
        "author": "Frank Herbert",
        "author_slug": "frank-herbert",
        "genre": "sci-fi",
        "year": 1965,
        "description": "A sweeping epic set in a distant future amidst a feudal interstellar empire.",
        "rating": 4.9,
    },
    {
        "id": 8,
        "title": "Neuromancer",
        "author": "William Gibson",
        "author_slug": "william-gibson",
        "genre": "sci-fi",
        "year": 1984,
        "description": "The novel that defined the cyberpunk genre.",
        "rating": 4.3,
    },
    {
        "id": 9,
        "title": "The Left Hand of Darkness",
        "author": "Ursula K. Le Guin",
        "author_slug": "ursula-le-guin",
        "genre": "sci-fi",
        "year": 1969,
        "description": "A revolutionary exploration of gender and society on a distant ice world.",
        "rating": 4.5,
    },
    {
        "id": 10,
        "title": "Foundation",
        "author": "Isaac Asimov",
        "author_slug": "isaac-asimov",
        "genre": "sci-fi",
        "year": 1951,
        "description": "A mathematician devises a plan to preserve civilization across millennia.",
        "rating": 4.7,
    },
    {
        "id": 11,
        "title": "The Martian",
        "author": "Andy Weir",
        "author_slug": "andy-weir",
        "genre": "sci-fi",
        "year": 2011,
        "description": "An astronaut stranded on Mars must use science and ingenuity to survive.",
        "rating": 4.6,
    },
    {
        "id": 12,
        "title": "Blindsight",
        "author": "Peter Watts",
        "author_slug": "peter-watts",
        "genre": "sci-fi",
        "year": 2006,
        "description": "Hard SF first-contact thriller that questions the nature of consciousness.",
        "rating": 4.4,
    },
    {
        "id": 13,
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "author_slug": "daniel-kahneman",
        "genre": "psychology",
        "year": 2011,
        "description": "Explores the two systems that drive the way we think.",
        "rating": 4.7,
    },
    {
        "id": 14,
        "title": "Atomic Habits",
        "author": "James Clear",
        "author_slug": "james-clear",
        "genre": "psychology",
        "year": 2018,
        "description": "A proven framework for improving every day, 1% at a time.",
        "rating": 4.8,
    },
    {
        "id": 15,
        "title": "Influence",
        "author": "Robert Cialdini",
        "author_slug": "robert-cialdini",
        "genre": "psychology",
        "year": 1984,
        "description": "The definitive guide to the psychology of persuasion and compliance.",
        "rating": 4.6,
    },
    {
        "id": 16,
        "title": "Flow",
        "author": "Mihaly Csikszentmihalyi",
        "author_slug": "mihaly-csikszentmihalyi",
        "genre": "psychology",
        "year": 1990,
        "description": "The psychology of optimal experience and peak states of absorption.",
        "rating": 4.4,
    },
    {
        "id": 17,
        "title": "Man's Search for Meaning",
        "author": "Viktor Frankl",
        "author_slug": "viktor-frankl",
        "genre": "psychology",
        "year": 1946,
        "description": "A psychiatrist's account of surviving the Holocaust and finding purpose.",
        "rating": 4.9,
    },
    {
        "id": 18,
        "title": "The Power of Habit",
        "author": "Charles Duhigg",
        "author_slug": "charles-duhigg",
        "genre": "psychology",
        "year": 2012,
        "description": "Explores the science behind why habits exist and how they can be changed.",
        "rating": 4.5,
    },
    {
        "id": 19,
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "author_slug": "yuval-harari",
        "genre": "history",
        "year": 2011,
        "description": "A brief history of humankind from Stone Age foragers to 21st-century empires.",
        "rating": 4.8,
    },
    {
        "id": 20,
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "author_slug": "jared-diamond",
        "genre": "history",
        "year": 1997,
        "description": "Why did some civilizations conquer others? An environmental and geographic answer.",
        "rating": 4.5,
    },
    {
        "id": 21,
        "title": "The Silk Roads",
        "author": "Peter Frankopan",
        "author_slug": "peter-frankopan",
        "genre": "history",
        "year": 2015,
        "description": "A new world history centered on the trade routes connecting East and West.",
        "rating": 4.4,
    },
    {
        "id": 22,
        "title": "SPQR: A History of Ancient Rome",
        "author": "Mary Beard",
        "author_slug": "mary-beard",
        "genre": "history",
        "year": 2015,
        "description": "An authoritative and witty account of how Rome became a world power.",
        "rating": 4.3,
    },
]

GENRES = ["programming", "sci-fi", "psychology", "history"]

GENRE_LABELS = {
    "programming": "Programming",
    "sci-fi": "Sci-Fi",
    "psychology": "Psychology",
    "history": "History",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _url_pill(ctx: Context) -> Container:
    """Small pill that displays the current URL — shows ctx.url in action."""
    return Container(
        class_name="inline-flex items-center gap-2 rounded-full bg-muted px-3 py-1",
        children=[
            Text("ctx.url:", class_name="text-xs text-muted-foreground font-mono"),
            Text(ctx.url, class_name="text-xs font-mono text-primary font-semibold"),
        ],
    )


def _navbar(ctx: Context) -> Card:
    return Card(
        class_name="mb-6 sticky top-0 z-10",
        children=[
            CardContent(
                class_name="px-6 py-3",
                children=[
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Button(
                                "📚 Bookstore",
                                variant="ghost",
                                class_name="font-bold text-lg",
                                on_click=ctx.callback(nav_home),
                            ),
                            Row(
                                gap=2,
                                align="center",
                                children=[
                                    Button(
                                        "Browse",
                                        variant="ghost",
                                        size="sm",
                                        on_click=ctx.callback(nav_home),
                                    ),
                                    Button(
                                        "Search",
                                        variant="ghost",
                                        size="sm",
                                        on_click=ctx.callback(nav_search),
                                    ),
                                    _url_pill(ctx),
                                ],
                            ),
                        ],
                    )
                ],
            )
        ],
    )


def _book_card(ctx: Context, book: dict, *, compact: bool = False) -> Card:
    """Render a book summary card linking to the detail page."""
    genre_color = {"programming": "default", "sci-fi": "secondary", "psychology": "outline"}
    return Card(
        class_name="hover:shadow-md transition-shadow cursor-pointer",
        children=[
            CardHeader(
                class_name="pb-2",
                children=[
                    Row(
                        justify="between",
                        align="start",
                        children=[
                            CardTitle(
                                book["title"],
                                class_name="text-base leading-snug",
                            ),
                            Badge(
                                children=[GENRE_LABELS.get(book["genre"], book["genre"])],
                                variant=genre_color.get(book["genre"], "outline"),
                            ),
                        ],
                    ),
                    CardDescription(f"by {book['author']} · {book['year']}"),
                ],
            ),
            CardContent(
                children=[
                    *([] if compact else [Text(book["description"], class_name="text-sm text-muted-foreground mb-3")]),
                    Row(
                        justify="between",
                        align="center",
                        children=[
                            Text(f"⭐ {book['rating']}", class_name="text-sm font-medium"),
                            Row(
                                gap=2,
                                children=[
                                    Button(
                                        "View",
                                        variant="outline",
                                        size="sm",
                                        on_click=ctx.callback(nav_book, book_id=book["id"]),
                                    ),
                                    Button(
                                        book["author"].split()[0],
                                        variant="ghost",
                                        size="sm",
                                        on_click=ctx.callback(
                                            nav_author, slug=book["author_slug"]
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Callbacks — navigation
# ---------------------------------------------------------------------------


async def nav_home(ctx: Context):
    await ctx.load("/")


async def nav_search(ctx: Context):
    await ctx.load("/search")


async def nav_book(ctx: Context, book_id: int):
    """Navigate to a book detail page — path param demo."""
    await ctx.load(f"/books/{book_id}")


async def nav_author(ctx: Context, slug: str):
    """Navigate to an author page — string path param demo."""
    await ctx.load(f"/authors/{slug}")


async def nav_genre(ctx: Context, slug: str):
    """Navigate to a genre page."""
    await ctx.load(f"/genre/{slug}")


async def do_search(ctx: Context):
    """Build a search URL from state and navigate — query param demo."""
    q = ctx.state.get("search_q", "")
    genre = ctx.state.get("search_genre", "")
    page = ctx.state.get("search_page", 1)

    parts = []
    if q:
        parts.append(f"q={q}")
    if genre:
        parts.append(f"genre={genre}")
    if page and int(page) > 1:
        parts.append(f"page={page}")

    qs = "&".join(parts)
    url = f"/search?{qs}" if qs else "/search"
    await ctx.load(url)


async def search_next_page(ctx: Context, current_page: int):
    q = ctx.query_params.get("q", "")
    genre = ctx.query_params.get("genre", "")
    next_page = current_page + 1
    parts = [f"page={next_page}"]
    if q:
        parts.append(f"q={q}")
    if genre:
        parts.append(f"genre={genre}")
    await ctx.load("/search?" + "&".join(parts))


async def search_prev_page(ctx: Context, current_page: int):
    q = ctx.query_params.get("q", "")
    genre = ctx.query_params.get("genre", "")
    prev_page = max(1, current_page - 1)
    parts = [f"page={prev_page}"]
    if q:
        parts.append(f"q={q}")
    if genre:
        parts.append(f"genre={genre}")
    await ctx.load("/search?" + "&".join(parts))


async def on_search_q_change(ctx: Context, value: str = ""):
    ctx.state.set("search_q", value)


async def on_search_genre_change(ctx: Context, value: str = ""):
    ctx.state.set("search_genre", value)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


@ui.page("/")
def home(ctx: Context):
    """Homepage — lists all books by genre."""
    return Container(
        class_name="max-w-5xl mx-auto p-4",
        children=[
            _navbar(ctx),
            Heading("Browse the Catalog", level=1, class_name="mb-2"),
            Text(
                "Click a genre badge or a book to explore URL parameter routing.",
                class_name="text-muted-foreground mb-6",
            ),
            # Genre quick-links — each navigates with a path param
            Row(
                gap=2,
                class_name="mb-6",
                children=[
                    Text("Jump to:", class_name="text-sm font-medium self-center"),
                    *[
                        Button(
                            GENRE_LABELS[g],
                            variant="outline",
                            size="sm",
                            on_click=ctx.callback(nav_genre, slug=g),
                        )
                        for g in GENRES
                    ],
                    Button(
                        "🔍 Search with filters",
                        variant="default",
                        size="sm",
                        on_click=ctx.callback(nav_search),
                    ),
                ],
            ),
            Grid(
                columns=2,
                gap=4,
                children=[_book_card(ctx, b) for b in BOOKS],
            ),
        ],
    )


@ui.page("/books/{id:int}")
def book_detail(ctx: Context):
    """Book detail page.

    Demonstrates:
        - ctx.path_params["id"]  — auto-coerced to int
        - ctx.url                — full current path shown in breadcrumb
    """
    book_id: int = ctx.path_params["id"]  # already an int thanks to {id:int}
    book = next((b for b in BOOKS if b["id"] == book_id), None)

    if book is None:
        return Container(
            class_name="max-w-5xl mx-auto p-4",
            children=[
                _navbar(ctx),
                Card(
                    children=[
                        CardContent(
                            class_name="p-8 text-center",
                            children=[
                                Heading("Book not found", level=2, class_name="mb-2"),
                                Text(
                                    f"No book with id={book_id} (ctx.path_params['id'] = {book_id!r}, type={type(book_id).__name__})",
                                    class_name="text-muted-foreground mb-4",
                                ),
                                Button("Go home", on_click=ctx.callback(nav_home)),
                            ],
                        )
                    ]
                ),
            ],
        )

    related = [b for b in BOOKS if b["genre"] == book["genre"] and b["id"] != book["id"]]

    return Container(
        class_name="max-w-4xl mx-auto p-4",
        children=[
            _navbar(ctx),
            # Breadcrumb-style path info
            Row(
                gap=2,
                align="center",
                class_name="mb-4 text-sm text-muted-foreground",
                children=[
                    Button("Home", variant="link", class_name="p-0 h-auto text-sm", on_click=ctx.callback(nav_home)),
                    Text("/"),
                    Button(
                        GENRE_LABELS.get(book["genre"], book["genre"]),
                        variant="link",
                        class_name="p-0 h-auto text-sm",
                        on_click=ctx.callback(nav_genre, slug=book["genre"]),
                    ),
                    Text("/"),
                    Text(book["title"], class_name="text-foreground font-medium"),
                ],
            ),
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            Row(
                                justify="between",
                                align="start",
                                children=[
                                    Column(
                                        gap=1,
                                        children=[
                                            CardTitle(book["title"], class_name="text-2xl"),
                                            CardDescription(f"{book['year']} · ⭐ {book['rating']}"),
                                        ],
                                    ),
                                    Badge(
                                        children=[GENRE_LABELS.get(book["genre"], book["genre"])],
                                        variant="secondary",
                                    ),
                                ],
                            )
                        ]
                    ),
                    CardContent(
                        children=[
                            Text(book["description"], class_name="mb-6"),
                            Separator(class_name="my-4"),
                            # URL params debug panel
                            Card(
                                class_name="bg-muted/40",
                                children=[
                                    CardHeader(children=[CardTitle("URL Parameter Values", class_name="text-sm")]),
                                    CardContent(
                                        class_name="font-mono text-sm space-y-1",
                                        children=[
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text("ctx.url", class_name="text-muted-foreground"),
                                                    Text("="),
                                                    Text(f'"{ctx.url}"', class_name="text-primary"),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text("ctx.path_params", class_name="text-muted-foreground"),
                                                    Text("="),
                                                    Text(str(ctx.path_params), class_name="text-primary"),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text('ctx.path_params["id"]', class_name="text-muted-foreground"),
                                                    Text("="),
                                                    Text(
                                                        f"{book_id!r}  (type: {type(book_id).__name__})",
                                                        class_name="text-green-600 dark:text-green-400",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            Separator(class_name="my-4"),
                            Button(
                                f"About {book['author'].split()[0]}",
                                variant="outline",
                                on_click=ctx.callback(nav_author, slug=book["author_slug"]),
                            ),
                        ]
                    ),
                ],
            ),
            # Related books
            *(
                [
                    Heading("More in this genre", level=3, class_name="mb-3"),
                    Grid(
                        columns=2,
                        gap=3,
                        children=[_book_card(ctx, b, compact=True) for b in related],
                    ),
                ]
                if related
                else []
            ),
        ],
    )


@ui.page("/authors/{slug}")
def author_page(ctx: Context):
    """Author page.

    Demonstrates:
        - ctx.path_params["slug"]  — plain string path param
    """
    slug: str = ctx.path_params["slug"]
    author_books = [b for b in BOOKS if b["author_slug"] == slug]
    author_name = author_books[0]["author"] if author_books else slug.replace("-", " ").title()

    return Container(
        class_name="max-w-4xl mx-auto p-4",
        children=[
            _navbar(ctx),
            Card(
                class_name="mb-6",
                children=[
                    CardHeader(
                        children=[
                            CardTitle(author_name, class_name="text-2xl"),
                            CardDescription(f"{len(author_books)} book(s) in the catalog"),
                        ]
                    ),
                    CardContent(
                        children=[
                            # URL params debug panel
                            Card(
                                class_name="bg-muted/40 mb-4",
                                children=[
                                    CardHeader(children=[CardTitle("URL Parameter Values", class_name="text-sm")]),
                                    CardContent(
                                        class_name="font-mono text-sm space-y-1",
                                        children=[
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text("ctx.url", class_name="text-muted-foreground"),
                                                    Text("="),
                                                    Text(f'"{ctx.url}"', class_name="text-primary"),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text("ctx.path_params", class_name="text-muted-foreground"),
                                                    Text("="),
                                                    Text(str(ctx.path_params), class_name="text-primary"),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                children=[
                                                    Text('ctx.path_params["slug"]', class_name="text-muted-foreground"),
                                                    Text("="),
                                                    Text(f'"{slug}"', class_name="text-green-600 dark:text-green-400"),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ]
                    ),
                ],
            ),
            Heading("Books by this Author", level=3, class_name="mb-3"),
            Grid(
                columns=2,
                gap=4,
                children=[_book_card(ctx, b) for b in author_books],
            ) if author_books else Text(
                "No books found for this author slug.",
                class_name="text-muted-foreground",
            ),
        ],
    )


@ui.page("/genre/{slug}")
def genre_page(ctx: Context):
    """Genre page — string path param."""
    slug: str = ctx.path_params["slug"]
    genre_books = [b for b in BOOKS if b["genre"] == slug]
    label = GENRE_LABELS.get(slug, slug.title())

    return Container(
        class_name="max-w-4xl mx-auto p-4",
        children=[
            _navbar(ctx),
            Row(
                justify="between",
                align="center",
                class_name="mb-6",
                children=[
                    Column(
                        gap=1,
                        children=[
                            Heading(f"{label} Books", level=1),
                            Text(f"{len(genre_books)} titles in this genre", class_name="text-muted-foreground"),
                        ],
                    ),
                    Button("Search within genre", variant="outline", on_click=ctx.callback(nav_search_genre, slug=slug)),
                ],
            ),
            # Path param info
            Card(
                class_name="bg-muted/40 mb-6",
                children=[
                    CardContent(
                        class_name="font-mono text-sm py-3",
                        children=[
                            Row(
                                gap=4,
                                children=[
                                    Text('ctx.path_params["slug"]', class_name="text-muted-foreground"),
                                    Text("→"),
                                    Text(f'"{slug}"', class_name="text-primary font-semibold"),
                                    Text(f"  ({len(genre_books)} matches)", class_name="text-muted-foreground"),
                                ],
                            )
                        ],
                    )
                ],
            ),
            Grid(
                columns=2,
                gap=4,
                children=[_book_card(ctx, b) for b in genre_books],
            ) if genre_books else Text(
                f'No books found for genre "{slug}".',
                class_name="text-muted-foreground",
            ),
        ],
    )


async def nav_search_genre(ctx: Context, slug: str):
    await ctx.load(f"/search?genre={slug}")


@ui.page("/search")
def search_page(ctx: Context):
    """Search page.

    Demonstrates:
        - ctx.query_params["q"]      — search term from ?q=...
        - ctx.query_params["genre"]  — genre filter from ?genre=...
        - ctx.query_params["page"]   — pagination from ?page=2
        - ctx.url                    — full URL with query string
    """
    # Read query params — everything comes from the URL
    q: str = ctx.query_params.get("q", "")
    genre: str = ctx.query_params.get("genre", "")
    page: int = int(ctx.query_params.get("page", "1"))

    # Seed search form state from URL params (so the form reflects the URL)
    if not ctx.state.get("_search_seeded"):
        ctx.state.set("search_q", q)
        ctx.state.set("search_genre", genre)
        ctx.state.set("_search_seeded", True)

    # Filter books
    results = BOOKS
    if q:
        ql = q.lower()
        results = [
            b for b in results
            if ql in b["title"].lower() or ql in b["author"].lower() or ql in b["description"].lower()
        ]
    if genre:
        results = [b for b in results if b["genre"] == genre]

    # Pagination
    per_page = 3
    total = len(results)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    paged = results[(page - 1) * per_page : page * per_page]

    return Container(
        class_name="max-w-4xl mx-auto p-4",
        children=[
            _navbar(ctx),
            Heading("Search", level=1, class_name="mb-4"),
            # Search form
            Card(
                class_name="mb-6",
                children=[
                    CardContent(
                        class_name="pt-4",
                        children=[
                            Row(
                                gap=3,
                                align="end",
                                children=[
                                    Column(
                                        gap=1,
                                        class_name="flex-1",
                                        children=[
                                            Text("Keyword", class_name="text-sm font-medium"),
                                            Input(
                                                placeholder="Title, author, or description…",
                                                value=ctx.state.get("search_q", q),
                                                on_change=ctx.callback(on_search_q_change, debounce=0),
                                            ),
                                        ],
                                    ),
                                    Column(
                                        gap=1,
                                        children=[
                                            Text("Genre", class_name="text-sm font-medium"),
                                            Select(
                                                options=[
                                                    {"value": "", "label": "All genres"},
                                                    *[
                                                        {"value": g, "label": GENRE_LABELS[g]}
                                                        for g in GENRES
                                                    ],
                                                ],
                                                value=ctx.state.get("search_genre", genre),
                                                on_change=ctx.callback(on_search_genre_change),
                                            ),
                                        ],
                                    ),
                                    Button(
                                        "Search",
                                        on_click=ctx.callback(do_search),
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            # URL params debug panel
            Card(
                class_name="bg-muted/40 mb-6",
                children=[
                    CardHeader(children=[CardTitle("URL Parameter Values", class_name="text-sm")]),
                    CardContent(
                        class_name="font-mono text-sm space-y-1",
                        children=[
                            Row(
                                gap=2,
                                children=[
                                    Text("ctx.url", class_name="text-muted-foreground w-52"),
                                    Text("="),
                                    Text(f'"{ctx.url}"', class_name="text-primary"),
                                ],
                            ),
                            Row(
                                gap=2,
                                children=[
                                    Text("ctx.query_params", class_name="text-muted-foreground w-52"),
                                    Text("="),
                                    Text(str(ctx.query_params), class_name="text-primary"),
                                ],
                            ),
                            Row(
                                gap=2,
                                children=[
                                    Text('ctx.query_params["q"]', class_name="text-muted-foreground w-52"),
                                    Text("="),
                                    Text(f'"{q}"' if q else '""', class_name="text-green-600 dark:text-green-400"),
                                ],
                            ),
                            Row(
                                gap=2,
                                children=[
                                    Text('ctx.query_params["genre"]', class_name="text-muted-foreground w-52"),
                                    Text("="),
                                    Text(f'"{genre}"' if genre else '""', class_name="text-green-600 dark:text-green-400"),
                                ],
                            ),
                            Row(
                                gap=2,
                                children=[
                                    Text('ctx.query_params["page"]', class_name="text-muted-foreground w-52"),
                                    Text("="),
                                    Text(f'"{ctx.query_params.get("page", "1")}"', class_name="text-green-600 dark:text-green-400"),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Results
            Text(
                f"{total} result(s)"
                + (f' for \u201c{q}\u201d' if q else "")
                + (f" in {GENRE_LABELS.get(genre, genre)}" if genre else ""),
                class_name="text-sm text-muted-foreground mb-4",
            ),
            *(
                [
                    Grid(
                        columns=1,
                        gap=3,
                        children=[_book_card(ctx, b) for b in paged],
                    ),
                    # Pagination
                    Row(
                        justify="between",
                        align="center",
                        class_name="mt-6",
                        children=[
                            Button(
                                "← Previous",
                                variant="outline",
                                disabled=page <= 1,
                                on_click=ctx.callback(search_prev_page, current_page=page),
                            ),
                            Text(f"Page {page} of {total_pages}", class_name="text-sm text-muted-foreground"),
                            Button(
                                "Next →",
                                variant="outline",
                                disabled=page >= total_pages,
                                on_click=ctx.callback(search_next_page, current_page=page),
                            ),
                        ],
                    ),
                ]
                if paged
                else [
                    Card(
                        children=[
                            CardContent(
                                class_name="p-8 text-center",
                                children=[
                                    Text("No books match your search.", class_name="text-muted-foreground"),
                                ],
                            )
                        ]
                    )
                ]
            ),
        ],
    )


# ---------------------------------------------------------------------------
# FastAPI mount
# ---------------------------------------------------------------------------

app = FastAPI()
app.include_router(ui.router)
