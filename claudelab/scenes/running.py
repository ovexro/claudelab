"""Running scene -- agent at a control panel pushing buttons, server rack
with blinking lights, spinning gear / progress animation.
"""

from __future__ import annotations

from claudelab.office import (
    build_office_bg,
    stamp,
    CONTROL_PANEL,
    CONTROL_PANEL_ACTIVE,
    SERVER_RACK,
    PLANT_FRAMES,
    get_window,
)
from claudelab.agents import BUTTON_PUSH_FRAMES

NUM_FRAMES = 8

# Spinning gear animation
_GEAR_FRAMES: list[list[str]] = [
    [
        "  \u250c\u2500\u2510  ",
        " \u2500\u2524\u25cf\u251c\u2500 ",
        "  \u2514\u2500\u2518  ",
    ],
    [
        "  \\ /  ",
        " \u2500 \u25cf \u2500 ",
        "  / \\  ",
    ],
    [
        "  \u250c\u2500\u2510  ",
        " \u2500\u2524\u25cf\u251c\u2500 ",
        "  \u2514\u2500\u2518  ",
    ],
    [
        "  | |  ",
        "  \u2500\u25cf\u2500  ",
        "  | |  ",
    ],
]

# Progress bar animation
_PROGRESS_FRAMES: list[list[str]] = [
    ["[\u2588\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591] 10%"],
    ["[\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591] 20%"],
    ["[\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591\u2591] 40%"],
    ["[\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591\u2591] 50%"],
    ["[\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591\u2591] 60%"],
    ["[\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2591\u2591\u2591] 70%"],
    ["[\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2591] 90%"],
    ["[\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588] OK!"],
]

# Output log lines
_LOG_LINES: list[str] = [
    "> compiling...",
    "> linking...",
    "> tests: 42 pass",
    "> building...",
    "> deploy: ok",
    "> checks pass",
    "> lint: clean",
    "> done.",
]


def get_frames(width: int, height: int) -> list[list[str]]:
    """Return animation frames for the running scene."""
    frames: list[list[str]] = []

    for fi in range(NUM_FRAMES):
        bg = build_office_bg(width, height)

        floor = height - 2
        panel_col = 6
        server_col = min(width - 12, max(24, width // 2 - 4))
        gear_col = min(width - 10, max(38, width * 2 // 3))
        plant_col = min(width - 10, max(52, width - 12))
        window_col = min(width - 16, max(55, width - 18))

        # --- control panel ---
        panel = CONTROL_PANEL_ACTIVE if fi % 2 == 0 else CONTROL_PANEL
        panel_row = floor - len(panel)
        if panel_row > 3 and panel_col + 14 < width:
            bg = stamp(bg, panel, panel_row, panel_col)

        # --- agent pushing buttons ---
        agent = BUTTON_PUSH_FRAMES[fi % len(BUTTON_PUSH_FRAMES)]
        agent_row = panel_row - len(agent)
        if agent_row > 1:
            bg = stamp(bg, agent, agent_row, panel_col + 3)

        # --- server rack with blinking lights ---
        srv = SERVER_RACK[fi % len(SERVER_RACK)]
        srv_row = floor - len(srv)
        if srv_row > 1 and server_col + 10 < width:
            bg = stamp(bg, srv, srv_row, server_col)

        # --- spinning gear ---
        gear = _GEAR_FRAMES[fi % len(_GEAR_FRAMES)]
        gear_row = max(3, floor // 2 - 1)
        if gear_col + 7 < width and gear_row + 3 < floor:
            bg = stamp(bg, gear, gear_row, gear_col)

        # --- progress bar ---
        prog = _PROGRESS_FRAMES[fi % len(_PROGRESS_FRAMES)]
        prog_row = gear_row + 4
        if prog_row < floor and gear_col + 15 < width:
            bg = stamp(bg, prog, prog_row, gear_col - 1)

        # --- log output ---
        log_col = 4
        log_start_row = 2
        visible_logs = min(fi + 1, len(_LOG_LINES), floor - log_start_row - 2)
        for li in range(visible_logs):
            idx = (fi - visible_logs + 1 + li) % len(_LOG_LINES)
            lr = log_start_row + li
            line = _LOG_LINES[idx]
            if lr < floor and log_col + len(line) < width:
                bg = stamp(bg, [line], lr, log_col)

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
