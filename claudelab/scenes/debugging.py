"""Debugging scene -- an agent at the whiteboard with diagrams, another
examining code with a magnifying-glass effect, red warning indicators.
"""

from __future__ import annotations

from claudelab.office import (
    build_office_bg,
    stamp,
    WHITEBOARD_DEBUG,
    SERVER_RACK,
    PLANT_FRAMES,
    get_window,
)
from claudelab.agents import STANDING_POINTING, STANDING_EXAMINING

NUM_FRAMES = 8

# Warning / error indicator animations
_WARNINGS: list[list[str]] = [
    [
        " /!\\ ",
        "/ ! \\",
        "-----",
    ],
    [
        " /!\\ ",
        "/ ! \\",
        "-----",
    ],
    [
        "     ",
        "     ",
        "     ",
    ],
    [
        " /!\\ ",
        "/ ! \\",
        "-----",
    ],
]

# Magnifying glass effect around code on a monitor
_MAGNIFY_MONITOR: list[list[str]] = [
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502 ERR:42 \u2502",
        "\u2502>fix_it \u2502",
        "\u2502 return \u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502 ln 41: \u2502",
        "\u2502 ERR:42 \u2502",
        "\u2502>fix_it \u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502 type? \u2502",
        "\u2502 null! \u2502",
        "\u2502>trace \u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
    [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502>stack \u2502",
        "\u2502 at L42 \u2502",
        "\u2502 found! \u2502",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ],
]

# Desk under the monitor
_DESK_BASE: list[str] = [
    "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
    "\u2514\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2518",
]


def get_frames(width: int, height: int) -> list[list[str]]:
    """Return animation frames for the debugging scene."""
    frames: list[list[str]] = []

    for fi in range(NUM_FRAMES):
        bg = build_office_bg(width, height)

        floor = height - 2
        wb_col = 4
        monitor_col = min(width - 16, max(28, width // 2))
        server_col = min(width - 12, max(46, width - 14))
        plant_col = min(width - 10, max(60, width - 12))
        window_col = min(width - 16, max(50, width - 18))

        # --- whiteboard ---
        wb_row = 2
        if wb_row + len(WHITEBOARD_DEBUG) < floor and wb_col + 20 < width:
            bg = stamp(bg, WHITEBOARD_DEBUG, wb_row, wb_col)

        # --- agent 1: pointing at whiteboard ---
        a1 = STANDING_POINTING[fi % len(STANDING_POINTING)]
        a1_row = wb_row + len(WHITEBOARD_DEBUG)
        if a1_row + len(a1) < floor:
            bg = stamp(bg, a1, a1_row, wb_col + 6)

        # --- monitor with magnifying glass ---
        mon = _MAGNIFY_MONITOR[fi % len(_MAGNIFY_MONITOR)]
        mon_row = floor - len(mon) - len(_DESK_BASE)
        if mon_row > 3 and monitor_col + 14 < width:
            bg = stamp(bg, mon, mon_row, monitor_col)
            bg = stamp(bg, _DESK_BASE, mon_row + len(mon), monitor_col - 1)

        # --- agent 2: examining monitor ---
        a2 = STANDING_EXAMINING[fi % len(STANDING_EXAMINING)]
        a2_row = mon_row - len(a2)
        if a2_row > 1 and monitor_col + 7 < width:
            bg = stamp(bg, a2, a2_row, monitor_col + 2)

        # --- server rack ---
        srv = SERVER_RACK[fi % len(SERVER_RACK)]
        srv_row = floor - len(srv)
        if srv_row > 1 and server_col + 10 < width:
            bg = stamp(bg, srv, srv_row, server_col)

        # --- warning indicators ---
        warn = _WARNINGS[fi % len(_WARNINGS)]
        warn_row = 2
        warn_col = monitor_col + 12
        if warn_col + 5 < width and warn_row + 3 < height:
            bg = stamp(bg, warn, warn_row, warn_col)

        # --- plant ---
        pf = fi % len(PLANT_FRAMES)
        plant_row = floor - len(PLANT_FRAMES[0])
        if plant_row > 1 and plant_col + 7 < width:
            bg = stamp(bg, PLANT_FRAMES[pf], plant_row, plant_col)

        # --- window ---
        win = get_window()
        if window_col + 14 < width and height > 8:
            bg = stamp(bg, win, 1, window_col)

        frames.append(bg)

    return frames
