"""Office layout, furniture, and decorations for ClaudeLab.

The office is rendered as a persistent background.  Furniture pieces are
returned as (row_offset, col_offset, lines) tuples so the renderer can
composite them onto the frame buffer.
"""

from __future__ import annotations

import datetime

# ---------------------------------------------------------------------------
# Furniture pieces
# ---------------------------------------------------------------------------

DESK_WITH_MONITOR: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2502\u2593\u2593\u2591\u2591\u2593\u2593\u2591\u2591\u2502",
    "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
    "\u2502\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502",
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2514\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2518",
]

DESK_SMALL: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2514\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2534\u2500\u2500\u2518",
]

MONITOR_FRAMES: list[list[str]] = [
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502\u2593\u2593\u2591\u2591\u2593\u2593\u2591\u2591\u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502\u2591\u2591\u2593\u2593\u2591\u2591\u2593\u2593\u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502\u2593\u2591\u2593\u2591\u2593\u2591\u2593\u2591\u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
]

WHITEBOARD: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2502  WHITEBOARD        \u2502",
    "\u2502  \u250c\u2500\u2500\u2510  \u250c\u2500\u2510        \u2502",
    "\u2502  \u2502  \u2514\u2500\u2500\u2518  \u2502        \u2502",
    "\u2502  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2518        \u2502",
    "\u2502     \u2191              \u2502",
    "\u2502   flow \u2192 logic     \u2502",
    "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
]

WHITEBOARD_DEBUG: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2502  BUG TRACKER       \u2502",
    "\u2502  [x] parse error   \u2502",
    "\u2502  [ ] null ref      \u2502",
    "\u2502  [ ] off-by-one    \u2502",
    "\u2502  \u250c\u2500\u2510\u2500>\u250c\u2500\u2510\u2500>\u250c\u2500\u2510    \u2502",
    "\u2502  \u2502A\u2502  \u2502B\u2502  \u2502C\u2502    \u2502",
    "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
]

SERVER_RACK: list[list[str]] = [
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502\u2588\u2588 \u25cf \u25cf \u25cb\u2502",
        "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524",
        "\u2502\u2588\u2588 \u25cb \u25cf \u25cf\u2502",
        "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524",
        "\u2502\u2588\u2588 \u25cf \u25cb \u25cf\u2502",
        "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524",
        "\u2502\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502\u2588\u2588 \u25cb \u25cf \u25cf\u2502",
        "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524",
        "\u2502\u2588\u2588 \u25cf \u25cf \u25cb\u2502",
        "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524",
        "\u2502\u2588\u2588 \u25cb \u25cf \u25cf\u2502",
        "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524",
        "\u2502\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2593\u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
    ],
]

CONTROL_PANEL: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2502 (\u25cf) (\u25cb) (\u25cf) \u2502",
    "\u2502 [\u2588\u2588] [\u2591\u2591] \u2502",
    "\u2502 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \u2502",
    "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
]

CONTROL_PANEL_ACTIVE: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2502 (\u25cf) (\u25cf) (\u25cf) \u2502",
    "\u2502 [\u2588\u2588] [\u2588\u2588] \u2502",
    "\u2502 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 \u2502",
    "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
]

COFFEE_MACHINE: list[list[str]] = [
    [
        "  \u250c\u2500\u2500\u2500\u2510  ",
        "  \u2502 C \u2502  ",
        "\u250c\u2500\u2534\u2500\u2500\u2500\u2534\u2500\u2510",
        "\u2502 \u2592\u2592\u2592\u2592\u2592 \u2502",
        "\u2502  \u2592\u2592\u2592  \u2502",
        "\u2502 \u250c\u2510   \u2502",
        "\u2502 \u2514\u2518   \u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
    ],
    [
        "  \u250c\u2500\u2500\u2500\u2510  ",
        "  \u2502 C \u2502  ",
        "\u250c\u2500\u2534\u2500\u2500\u2500\u2534\u2500\u2510",
        "\u2502 \u2593\u2593\u2593\u2593\u2593 \u2502",
        "\u2502  \u2593\u2593\u2593  \u2502",
        "\u2502 \u250c\u2510~  \u2502",
        "\u2502 \u2514\u2518   \u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
    ],
]

PLANT_FRAMES: list[list[str]] = [
    [
        "  \\|/  ",
        "  /|\\  ",
        " \\|/|  ",
        " [\u2593\u2593\u2593] ",
    ],
    [
        "  \\|/  ",
        "  /|\\  ",
        "  |\\|/ ",
        " [\u2593\u2593\u2593] ",
    ],
]

CLOCK_FRAMES: list[list[str]] = [
    [
        "\u250c\u2500\u2500\u2500\u2510",
        "\u2502 | \u2502",
        "\u2502    \u2502",
        "\u2514\u2500\u2500\u2500\u2518",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2510",
        "\u2502  / \u2502",
        "\u2502    \u2502",
        "\u2514\u2500\u2500\u2500\u2518",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2510",
        "\u2502 -- \u2502",
        "\u2502    \u2502",
        "\u2514\u2500\u2500\u2500\u2518",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2510",
        "\u2502  \\ \u2502",
        "\u2502    \u2502",
        "\u2514\u2500\u2500\u2500\u2518",
    ],
]

CONVEYOR_BELT: list[str] = [
    "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550",
]

ASSEMBLY_PLATFORM: list[str] = [
    "\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584\u2584",
    "\u2588  BUILD   \u2588",
    "\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580\u2580",
]


# ---------------------------------------------------------------------------
# Day/night window
# ---------------------------------------------------------------------------

def get_window(width: int = 14) -> list[str]:
    """Return a window piece whose appearance depends on the real time."""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 18:
        # Day
        fill = "\u2591"
        label = " day "
    elif 18 <= hour < 21:
        # Dusk
        fill = "\u2592"
        label = "dusk "
    elif 21 <= hour or hour < 5:
        # Night
        fill = "\u2593"
        label = "night"
    else:
        # Dawn
        fill = "\u2592"
        label = "dawn "

    inner = width - 2
    return [
        "\u250c" + "\u2500" * inner + "\u2510",
        "\u2502" + fill * inner + "\u2502",
        "\u2502" + fill * ((inner - len(label)) // 2) + label + fill * ((inner - len(label) + 1) // 2) + "\u2502",
        "\u2502" + fill * inner + "\u2502",
        "\u2514" + "\u2500" * inner + "\u2518",
    ]


# ---------------------------------------------------------------------------
# Full office layout helper
# ---------------------------------------------------------------------------

def build_office_bg(width: int, height: int) -> list[str]:
    """Return a list of *height* strings (each *width* chars) forming the
    static office background.  Callers composite animated elements on top.

    The layout adapts to the available terminal size.
    """
    # Start with empty room
    rows: list[list[str]] = [[" "] * width for _ in range(height)]

    # --- ceiling ---
    if height > 2:
        for c in range(width):
            rows[0][c] = "\u2500"
        rows[0][0] = "\u250c"
        rows[0][width - 1] = "\u2510"

    # --- floor ---
    floor_row = height - 1
    if floor_row > 0:
        for c in range(width):
            rows[floor_row][c] = "\u2500"
        rows[floor_row][0] = "\u2514"
        rows[floor_row][width - 1] = "\u2518"

    # --- walls ---
    for r in range(1, floor_row):
        rows[r][0] = "\u2502"
        rows[r][width - 1] = "\u2502"

    # Convert to strings
    return ["".join(row) for row in rows]


def stamp(canvas: list[str], piece: list[str], row: int, col: int) -> list[str]:
    """Non-destructively stamp *piece* onto *canvas* at (row, col).

    Returns a new list of row strings with the piece composited.
    Characters from *piece* overwrite the canvas; spaces in *piece*
    are treated as transparent.
    """
    out = list(canvas)
    for dy, line in enumerate(piece):
        r = row + dy
        if r < 0 or r >= len(out):
            continue
        row_chars = list(out[r])
        for dx, ch in enumerate(line):
            c = col + dx
            if c < 0 or c >= len(row_chars):
                continue
            if ch != " ":
                row_chars[c] = ch
        out[r] = "".join(row_chars)
    return out
