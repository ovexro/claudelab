"""Agent character sprites and animation states for ClaudeLab.

Each agent is a small ASCII character (3-5 lines tall) with multiple animation
frames per activity state.  Frames are stored as lists of strings (one per row).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Sitting agent (at desk) -- variants for left/right hand typing
# ---------------------------------------------------------------------------

SITTING_IDLE: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
]

SITTING_TYPING_FRAMES: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|\\ ",
        " _/ \\ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\_ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " _/ \\_ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
]

# ---------------------------------------------------------------------------
# Standing agent -- for whiteboard, coffee machine, carrying blocks
# ---------------------------------------------------------------------------

STANDING_NEUTRAL: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
]

STANDING_POINTING: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|--",
        " / \\ ",
    ],
    [
        "  \u25c9 / ",
        " /|/  ",
        " / \\  ",
    ],
]

STANDING_EXAMINING: list[list[str]] = [
    [
        "  \u25c9o ",
        " /|\\ ",
        " / \\ ",
    ],
    [
        "  \u25c9 o",
        " /|\\ ",
        " / \\ ",
    ],
]

# ---------------------------------------------------------------------------
# Walking agent -- for carrying blocks, going to coffee
# ---------------------------------------------------------------------------

WALKING_FRAMES: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|\\ ",
        " /   ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        "   \\ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " | | ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
]

CARRYING_FRAMES: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|\\ \u2590\u2588\u258c",
        " /   ",
    ],
    [
        "  \u25c9  ",
        " /|\\ \u2590\u2588\u258c",
        "   \\ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ \u2590\u2588\u258c",
        " | | ",
    ],
    [
        "  \u25c9  ",
        " /|\\ \u2590\u2588\u258c",
        " / \\ ",
    ],
]

# ---------------------------------------------------------------------------
# Leaning back (idle/relaxed)
# ---------------------------------------------------------------------------

LEANING_FRAMES: list[list[str]] = [
    [
        "  \u25c9  ",
        "  |\\  ",
        " / \\ ",
    ],
    [
        "  \u25c9  ",
        "  |\\ ",
        " / \\ ",
    ],
]

# ---------------------------------------------------------------------------
# Drinking coffee
# ---------------------------------------------------------------------------

DRINKING_FRAMES: list[list[str]] = [
    [
        "  \u25c9\u2510",
        " /|  ",
        " / \\ ",
    ],
    [
        "  \u25c9/ ",
        " /|  ",
        " / \\ ",
    ],
    [
        "  \u25c9\u2510",
        " /|  ",
        " / \\ ",
    ],
]

# ---------------------------------------------------------------------------
# Pushing buttons at control panel
# ---------------------------------------------------------------------------

BUTTON_PUSH_FRAMES: list[list[str]] = [
    [
        "  \u25c9  ",
        " /|\\-",
        " / \\ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
    [
        "  \u25c9  ",
        "-/|\\ ",
        " / \\ ",
    ],
    [
        "  \u25c9  ",
        " /|\\ ",
        " / \\ ",
    ],
]

# ---------------------------------------------------------------------------
# Thought bubbles (displayed above agent head)
# ---------------------------------------------------------------------------

THOUGHT_BUBBLES: list[list[str]] = [
    [
        "  .o( ... )",
    ],
    [
        "  .o(  ?  )",
    ],
    [
        "  .o(  !  )",
    ],
    [
        "  .o( >>> )",
    ],
    [
        "  .o( <*> )",
    ],
    [
        "  .o( ~~~ )",
    ],
]

# ---------------------------------------------------------------------------
# Lightbulb animation (above head during thinking)
# ---------------------------------------------------------------------------

LIGHTBULB_FRAMES: list[list[str]] = [
    ["     "],
    ["  .  "],
    ["  o  "],
    [" (!) "],
    [" (*) "],
    [" (*) "],
    [" (!) "],
    ["  o  "],
]


def get_agent_frames(activity: str, variant: int = 0) -> list[list[str]]:
    """Return the animation frames for a given activity.

    Parameters
    ----------
    activity:
        One of "thinking", "coding", "debugging", "running",
        "building", "idle".
    variant:
        Selects among multiple agent roles within a scene.

    Returns
    -------
    A list of frames, each frame a list of row strings.
    """
    match activity:
        case "thinking":
            return SITTING_IDLE if variant == 0 else STANDING_NEUTRAL
        case "coding":
            return SITTING_TYPING_FRAMES
        case "debugging":
            if variant == 0:
                return STANDING_POINTING
            return STANDING_EXAMINING
        case "running":
            return BUTTON_PUSH_FRAMES
        case "building":
            return CARRYING_FRAMES
        case "idle":
            if variant == 0:
                return DRINKING_FRAMES
            return LEANING_FRAMES
        case _:
            return STANDING_NEUTRAL
