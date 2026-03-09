"""Coding scene -- agents actively typing at computers with code scrolling
on their monitors.  Multiple agents can be coding simultaneously.
"""

from __future__ import annotations

import random

from claudelab.office import (
    build_office_bg,
    stamp,
    DESK_WITH_MONITOR,
    PLANT_FRAMES,
    get_window,
)
from claudelab.agents import SITTING_TYPING_FRAMES

NUM_FRAMES = 8

# Pre-generated "code" lines for monitor display
_CODE_SNIPPETS = [
    "def main():",
    "  for x in",
    "  if val > ",
    "  return ok",
    "import sys ",
    "class Node:",
    "  self.nxt ",
    "yield item ",
    "async def :",
    "  await fn ",
    "try: parse ",
    "except Err:",
    "fn(&mut s) ",
    "let v = [] ",
    "match res {",
    "  Ok(v) => ",
]

# Deterministic seed per session so frames are consistent
_rng = random.Random(42)
_monitor_lines: list[list[str]] = []
for _ in range(NUM_FRAMES):
    _monitor_lines.append([_rng.choice(_CODE_SNIPPETS) for _ in range(3)])


def _make_code_monitor(frame_idx: int) -> list[str]:
    """Build a monitor showing scrolling code for the given frame."""
    lines = _monitor_lines[frame_idx % len(_monitor_lines)]
    # Truncate/pad each line to 8 chars
    padded = [ln[:8].ljust(8) for ln in lines]
    cursor = "\u2588" if frame_idx % 2 == 0 else " "
    return [
        "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
        "\u2502" + padded[0] + "\u2502",
        "\u2502" + padded[1] + "\u2502",
        "\u2502" + padded[2] + cursor + "",
        "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518",
        "    \u2502\u2502    ",
    ]


def get_frames(width: int, height: int) -> list[list[str]]:
    """Return animation frames for the coding scene."""
    frames: list[list[str]] = []

    for fi in range(NUM_FRAMES):
        bg = build_office_bg(width, height)

        desk1_col = 4
        desk2_col = min(width - 16, max(22, width // 2 - 5))
        desk3_col = min(width - 16, max(40, width * 3 // 4 - 5))
        plant_col = min(width - 10, max(55, width - 12))
        window_col = min(width - 16, max(50, width - 18))
        floor = height - 2

        # --- monitors with code ---
        mon = _make_code_monitor(fi)
        mon2 = _make_code_monitor((fi + 2) % NUM_FRAMES)
        mon3 = _make_code_monitor((fi + 5) % NUM_FRAMES)

        desk_row = floor - len(mon) - 2
        desk_base = [
            "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510",
            "\u2514\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2518",
        ]

        if desk_row > 4:
            # Desk 1
            if desk1_col + 14 < width:
                bg = stamp(bg, mon, desk_row, desk1_col)
                bg = stamp(bg, desk_base, desk_row + len(mon), desk1_col - 1)
            # Desk 2
            if desk2_col + 14 < width:
                bg = stamp(bg, mon2, desk_row, desk2_col)
                bg = stamp(bg, desk_base, desk_row + len(mon2), desk2_col - 1)
            # Desk 3 (if room)
            if desk3_col + 14 < width and desk3_col > desk2_col + 14:
                bg = stamp(bg, mon3, desk_row, desk3_col)
                bg = stamp(bg, desk_base, desk_row + len(mon3), desk3_col - 1)

        # --- typing agents ---
        agent = SITTING_TYPING_FRAMES[fi % len(SITTING_TYPING_FRAMES)]
        agent_row = desk_row - len(agent)
        if agent_row > 1 and desk1_col + 7 < width:
            bg = stamp(bg, agent, agent_row, desk1_col + 2)
        agent2 = SITTING_TYPING_FRAMES[(fi + 1) % len(SITTING_TYPING_FRAMES)]
        if agent_row > 1 and desk2_col + 7 < width:
            bg = stamp(bg, agent2, agent_row, desk2_col + 2)
        if desk3_col + 14 < width and desk3_col > desk2_col + 14 and agent_row > 1:
            agent3 = SITTING_TYPING_FRAMES[(fi + 3) % len(SITTING_TYPING_FRAMES)]
            bg = stamp(bg, agent3, agent_row, desk3_col + 2)

        # --- plant ---
        pf = fi % len(PLANT_FRAMES)
        plant_row = floor - len(PLANT_FRAMES[0])
        if plant_row > 1 and plant_col + 7 < width:
            bg = stamp(bg, PLANT_FRAMES[pf], plant_row, plant_col)

        # --- window ---
        win = get_window()
        if window_col + 14 < width and height > 8:
            bg = stamp(bg, win, 1, window_col)

        # --- activity indicator ---
        indicator = "  >> CODING IN PROGRESS <<"
        ind_row = 2
        ind_col = max(2, (width - len(indicator)) // 2)
        if ind_row < height - 1 and ind_col + len(indicator) < width:
            if fi % 2 == 0:
                bg = stamp(bg, [indicator], ind_row, ind_col)

        frames.append(bg)

    return frames
