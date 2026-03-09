"""Idle scene -- agent at coffee machine, agent leaning back in chair,
clock ticking, peaceful ambient animation (plant swaying).
"""

from __future__ import annotations

from claudelab.office import (
    build_office_bg,
    stamp,
    COFFEE_MACHINE,
    DESK_WITH_MONITOR,
    CLOCK_FRAMES,
    PLANT_FRAMES,
    get_window,
)
from claudelab.agents import DRINKING_FRAMES, LEANING_FRAMES, SITTING_IDLE

NUM_FRAMES = 8

# Steam rising from coffee cup
_STEAM: list[list[str]] = [
    ["  ~  "],
    [" ~ ~ "],
    ["  ~  "],
    [" ~~~ "],
]

# Chat bubbles between idle agents
_CHAT_BUBBLES: list[list[str]] = [
    ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
     "\u2502 nice! \u2502",
     "\u2514\u2500\u252c\u2500\u2500\u2500\u2500\u2518",
     "  \u2502      "],
    ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
     "\u2502  tea? \u2502",
     "\u2514\u2500\u252c\u2500\u2500\u2500\u2500\u2518",
     "  \u2502      "],
    ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
     "\u2502  yep! \u2502",
     "\u2514\u2500\u252c\u2500\u2500\u2500\u2500\u2518",
     "  \u2502      "],
    ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
     "\u2502  :)   \u2502",
     "\u2514\u2500\u252c\u2500\u2500\u2500\u2500\u2518",
     "  \u2502      "],
]


def get_frames(width: int, height: int) -> list[list[str]]:
    """Return animation frames for the idle scene."""
    frames: list[list[str]] = []

    for fi in range(NUM_FRAMES):
        bg = build_office_bg(width, height)

        floor = height - 2
        coffee_col = 4
        desk_col = min(width - 16, max(22, width // 2 - 5))
        plant_col = min(width - 10, max(42, width - 14))
        clock_col = min(width - 8, max(16, width // 3))
        window_col = min(width - 16, max(50, width - 18))

        # --- coffee machine ---
        cm = COFFEE_MACHINE[fi % len(COFFEE_MACHINE)]
        cm_row = floor - len(cm)
        if cm_row > 3 and coffee_col + 9 < width:
            bg = stamp(bg, cm, cm_row, coffee_col)

        # --- agent 1: drinking coffee near the machine ---
        drink = DRINKING_FRAMES[fi % len(DRINKING_FRAMES)]
        drink_row = cm_row - len(drink)
        if drink_row > 1 and coffee_col + 12 < width:
            bg = stamp(bg, drink, drink_row, coffee_col + 9)

        # --- steam above cup ---
        steam = _STEAM[fi % len(_STEAM)]
        steam_row = drink_row - 1
        if steam_row >= 1 and coffee_col + 16 < width:
            bg = stamp(bg, steam, steam_row, coffee_col + 10)

        # --- desk with agent 2 leaning back ---
        desk_row = floor - len(DESK_WITH_MONITOR)
        if desk_row > 3 and desk_col + 14 < width:
            bg = stamp(bg, DESK_WITH_MONITOR, desk_row, desk_col)

        lean = LEANING_FRAMES[fi % len(LEANING_FRAMES)]
        lean_row = desk_row - len(lean)
        if lean_row > 1 and desk_col + 7 < width:
            bg = stamp(bg, lean, lean_row, desk_col + 2)

        # --- chat bubble above leaning agent ---
        chat = _CHAT_BUBBLES[fi % len(_CHAT_BUBBLES)]
        chat_row = lean_row - len(chat)
        if chat_row >= 1 and desk_col + 12 < width:
            bg = stamp(bg, chat, chat_row, desk_col)

        # --- clock on wall ---
        clk = CLOCK_FRAMES[fi % len(CLOCK_FRAMES)]
        if clock_col + 5 < width and height > 8:
            bg = stamp(bg, clk, 1, clock_col)

        # --- plant (swaying) ---
        pf = fi % len(PLANT_FRAMES)
        p_row = floor - len(PLANT_FRAMES[0])
        if p_row > 1 and plant_col + 7 < width:
            bg = stamp(bg, PLANT_FRAMES[pf], p_row, plant_col)

        # --- window ---
        win = get_window()
        if window_col + 14 < width and height > 8:
            bg = stamp(bg, win, 1, window_col)

        # --- ambient: peaceful message ---
        msgs = [
            "  ~ all quiet ~  ",
            " ~ break time ~  ",
            "  ~ relaxing ~   ",
            " ~ standby ...~  ",
        ]
        msg = msgs[fi % len(msgs)]
        msg_row = floor
        msg_col = max(2, (width - len(msg)) // 2)
        if msg_col + len(msg) < width:
            bg = stamp(bg, [msg], msg_row, msg_col)

        frames.append(bg)

    return frames
