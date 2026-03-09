"""Building scene -- agents carrying blocks labeled with file extensions,
assembly line animation, progress bar.
"""

from __future__ import annotations

from claudelab.office import (
    build_office_bg,
    stamp,
    CONVEYOR_BELT,
    ASSEMBLY_PLATFORM,
    PLANT_FRAMES,
    get_window,
)
from claudelab.agents import CARRYING_FRAMES, WALKING_FRAMES

NUM_FRAMES = 8

# Code blocks (the things agents carry)
_BLOCK_LABELS = [".py", ".js", ".ts", ".rs", ".go", ".md", ".sh", ".cx"]

_BLOCKS: list[list[str]] = [
    [
        "\u2590" + lbl + "\u258c",
    ]
    for lbl in _BLOCK_LABELS
]

# Stack being built on the platform
_STACK_FRAMES: list[list[list[str]]] = [
    [
        ["\u2588\u2588\u2588\u2588"],
    ],
    [
        ["\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588"],
    ],
    [
        ["\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588"],
    ],
    [
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
    ],
    [
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
        ["\u2588\u2588\u2588\u2588\u2588\u2588"],
    ],
    [
        ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2510"],
        ["\u2502 DONE \u2502"],
        ["\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2518"],
    ],
    [
        ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2510"],
        ["\u2502 DONE \u2502"],
        ["\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2518"],
    ],
    [
        ["\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2510"],
        ["\u2502 DONE \u2502"],
        ["\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2518"],
    ],
]

# Progress bar
_BUILD_PROGRESS: list[str] = [
    "BUILD [\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591]  0%",
    "BUILD [\u2588\u2591\u2591\u2591\u2591\u2591\u2591\u2591] 12%",
    "BUILD [\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591] 25%",
    "BUILD [\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591] 37%",
    "BUILD [\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591] 50%",
    "BUILD [\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591] 75%",
    "BUILD [\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2591] 87%",
    "BUILD [\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588] OK!",
]


def get_frames(width: int, height: int) -> list[list[str]]:
    """Return animation frames for the building scene."""
    frames: list[list[str]] = []

    for fi in range(NUM_FRAMES):
        bg = build_office_bg(width, height)

        floor = height - 2
        conveyor_col = 3
        conveyor_len = min(25, width - 8)
        platform_col = min(width - 16, max(32, width // 2 + 4))
        plant_col = min(width - 10, max(52, width - 12))
        window_col = min(width - 16, max(55, width - 18))

        # --- conveyor belt ---
        belt_row = floor - 1
        belt_line = "\u2550" * conveyor_len
        if belt_row > 3 and conveyor_col + conveyor_len < width:
            bg = stamp(bg, [belt_line], belt_row, conveyor_col)

        # --- carrying agent (walks along conveyor) ---
        carry = CARRYING_FRAMES[fi % len(CARRYING_FRAMES)]
        agent_x = conveyor_col + ((fi * 3) % max(1, conveyor_len - 8))
        agent_row = belt_row - len(carry)
        if agent_row > 2 and agent_x + 10 < width:
            bg = stamp(bg, carry, agent_row, agent_x)

        # --- block label above carried block ---
        blk = _BLOCKS[fi % len(_BLOCKS)]
        blk_row = agent_row
        if blk_row > 1 and agent_x + 11 < width:
            bg = stamp(bg, blk, blk_row, agent_x + 6)

        # --- second agent walking other direction ---
        walk = WALKING_FRAMES[fi % len(WALKING_FRAMES)]
        a2_x = conveyor_col + conveyor_len - ((fi * 3) % max(1, conveyor_len - 6)) - 5
        a2_x = max(conveyor_col, min(a2_x, conveyor_col + conveyor_len - 5))
        a2_row = belt_row - len(walk)
        if a2_row > 2 and a2_x + 5 < width and abs(a2_x - agent_x) > 6:
            bg = stamp(bg, walk, a2_row, a2_x)

        # --- assembly platform ---
        plat_row = floor - len(ASSEMBLY_PLATFORM)
        if plat_row > 3 and platform_col + 12 < width:
            bg = stamp(bg, ASSEMBLY_PLATFORM, plat_row, platform_col)

        # --- growing stack on platform ---
        stack_pieces = _STACK_FRAMES[fi % len(_STACK_FRAMES)]
        stack_height = len(stack_pieces)
        for si, piece_rows in enumerate(stack_pieces):
            sr = plat_row - stack_height + si
            if sr > 1 and platform_col + 8 < width:
                bg = stamp(bg, piece_rows, sr, platform_col + 2)

        # --- progress bar ---
        prog = _BUILD_PROGRESS[fi % len(_BUILD_PROGRESS)]
        prog_row = 2
        prog_col = max(2, (width - len(prog)) // 2)
        if prog_row < floor and prog_col + len(prog) < width:
            bg = stamp(bg, [prog], prog_row, prog_col)

        # --- plant ---
        pf = fi % len(PLANT_FRAMES)
        p_row = floor - len(PLANT_FRAMES[0])
        if p_row > 1 and plant_col + 7 < width:
            bg = stamp(bg, PLANT_FRAMES[pf], p_row, plant_col)

        # --- window ---
        win = get_window()
        if window_col + 14 < width and height > 8:
            bg = stamp(bg, win, 1, window_col)

        frames.append(bg)

    return frames
