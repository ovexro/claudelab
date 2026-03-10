"""Color palette and theme management for ClaudeLab."""

import curses

# Color pair IDs
PAIR_DEFAULT = 0
PAIR_TITLE = 1
PAIR_STATUS = 2
PAIR_AGENT_BODY = 3
PAIR_AGENT_HEAD = 4
PAIR_DESK = 5
PAIR_MONITOR = 6
PAIR_MONITOR_TEXT = 7
PAIR_WALL = 8
PAIR_FLOOR = 9
PAIR_PLANT = 10
PAIR_COFFEE = 11
PAIR_WARNING = 12
PAIR_SUCCESS = 13
PAIR_THOUGHT = 14
PAIR_SERVER_ON = 15
PAIR_SERVER_OFF = 16
PAIR_WHITEBOARD = 17
PAIR_GEAR = 18
PAIR_BLOCK_PY = 19
PAIR_BLOCK_JS = 20
PAIR_BLOCK_TS = 21
PAIR_CLOCK = 22
PAIR_DIM = 23
PAIR_ACCENT = 24
PAIR_NIGHT_SKY = 25
PAIR_DAY_SKY = 26
PAIR_PROGRESS = 27
PAIR_LABEL = 28

THEME_DARK = "dark"
THEME_LIGHT = "light"


def init_colors(theme: str = THEME_DARK) -> None:
    """Initialize curses color pairs for the chosen theme."""
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass

    # Check that the terminal supports enough color pairs
    max_pairs = curses.COLOR_PAIRS if hasattr(curses, "COLOR_PAIRS") else 0
    if max_pairs < PAIR_LABEL + 1:
        # Terminal doesn't support enough color pairs; skip init
        return

    if theme == THEME_DARK:
        _init_dark()
    else:
        _init_light()


def _init_dark() -> None:
    """Dark theme: dark background with bright accents."""
    bg = curses.COLOR_BLACK

    curses.init_pair(PAIR_TITLE, curses.COLOR_CYAN, bg)
    curses.init_pair(PAIR_STATUS, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(PAIR_AGENT_BODY, curses.COLOR_YELLOW, bg)
    curses.init_pair(PAIR_AGENT_HEAD, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_DESK, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_MONITOR, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_MONITOR_TEXT, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_WALL, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_FLOOR, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_PLANT, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_COFFEE, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_WARNING, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_SUCCESS, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_THOUGHT, curses.COLOR_CYAN, bg)
    curses.init_pair(PAIR_SERVER_ON, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_SERVER_OFF, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_WHITEBOARD, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_GEAR, curses.COLOR_MAGENTA, bg)
    curses.init_pair(PAIR_BLOCK_PY, curses.COLOR_YELLOW, bg)
    curses.init_pair(PAIR_BLOCK_JS, curses.COLOR_YELLOW, bg)
    curses.init_pair(PAIR_BLOCK_TS, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_CLOCK, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_DIM, curses.COLOR_WHITE, bg)
    curses.init_pair(PAIR_ACCENT, curses.COLOR_MAGENTA, bg)
    curses.init_pair(PAIR_NIGHT_SKY, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_DAY_SKY, curses.COLOR_CYAN, bg)
    curses.init_pair(PAIR_PROGRESS, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_LABEL, curses.COLOR_CYAN, bg)


def _init_light() -> None:
    """Light theme: light background with dark accents."""
    bg = curses.COLOR_WHITE

    curses.init_pair(PAIR_TITLE, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_STATUS, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(PAIR_AGENT_BODY, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_AGENT_HEAD, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_DESK, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_MONITOR, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_MONITOR_TEXT, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_WALL, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_FLOOR, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_PLANT, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_COFFEE, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_WARNING, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_SUCCESS, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_THOUGHT, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_SERVER_ON, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_SERVER_OFF, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_WHITEBOARD, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_GEAR, curses.COLOR_MAGENTA, bg)
    curses.init_pair(PAIR_BLOCK_PY, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_BLOCK_JS, curses.COLOR_RED, bg)
    curses.init_pair(PAIR_BLOCK_TS, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_CLOCK, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_DIM, curses.COLOR_BLACK, bg)
    curses.init_pair(PAIR_ACCENT, curses.COLOR_MAGENTA, bg)
    curses.init_pair(PAIR_NIGHT_SKY, curses.COLOR_BLUE, bg)
    curses.init_pair(PAIR_DAY_SKY, curses.COLOR_CYAN, bg)
    curses.init_pair(PAIR_PROGRESS, curses.COLOR_GREEN, bg)
    curses.init_pair(PAIR_LABEL, curses.COLOR_BLUE, bg)
