"""Thinking scene -- agents sit at desks with animated thought bubbles,
blinking cursors on monitors, and lightbulb animations above their heads.
"""

from __future__ import annotations

from claudelab.office import (
    build_office_bg,
    stamp,
    DESK_WITH_MONITOR,
    PLANT_FRAMES,
    CLOCK_FRAMES,
    get_window,
)
from claudelab.agents import (
    SITTING_IDLE,
    THOUGHT_BUBBLES,
    LIGHTBULB_FRAMES,
)

NUM_FRAMES = 8


def get_frames(width: int, height: int) -> list[list[str]]:
    """Return *NUM_FRAMES* animation frames for the thinking scene."""
    frames: list[list[str]] = []

    for fi in range(NUM_FRAMES):
        bg = build_office_bg(width, height)

        # --- furniture positions (adapt to width) ---
        desk1_col = 4
        desk2_col = min(width - 16, max(22, width // 2 - 5))
        plant_col = min(width - 10, max(40, width - 14))
        clock_col = min(width - 8, max(16, width // 2))
        window_col = min(width - 16, max(50, width - 18))

        # Floor row for placing furniture on
        floor = height - 2

        # --- place desks ---
        desk_row = floor - len(DESK_WITH_MONITOR)
        if desk_row > 3 and desk1_col + 14 < width:
            bg = stamp(bg, DESK_WITH_MONITOR, desk_row, desk1_col)
        if desk_row > 3 and desk2_col + 14 < width:
            bg = stamp(bg, DESK_WITH_MONITOR, desk_row, desk2_col)

        # --- plant (animated sway) ---
        plant_f = fi % len(PLANT_FRAMES)
        plant_row = floor - len(PLANT_FRAMES[0])
        if plant_row > 1 and plant_col + 7 < width:
            bg = stamp(bg, PLANT_FRAMES[plant_f], plant_row, plant_col)

        # --- clock ---
        clock_f = fi % len(CLOCK_FRAMES)
        if clock_col + 5 < width and height > 8:
            bg = stamp(bg, CLOCK_FRAMES[clock_f], 1, clock_col)

        # --- window ---
        win = get_window()
        if window_col + 14 < width and height > 8:
            bg = stamp(bg, win, 1, window_col)

        # --- agents ---
        agent_frame = SITTING_IDLE[fi % len(SITTING_IDLE)]
        agent1_row = desk_row - len(agent_frame)
        if agent1_row > 1:
            bg = stamp(bg, agent_frame, agent1_row, desk1_col + 2)
        agent2_row = desk_row - len(agent_frame)
        if agent2_row > 1 and desk2_col + 7 < width:
            bg = stamp(bg, agent_frame, agent2_row, desk2_col + 2)

        # --- thought bubbles ---
        tb = THOUGHT_BUBBLES[fi % len(THOUGHT_BUBBLES)]
        bubble_row = agent1_row - 2
        if bubble_row >= 1:
            bg = stamp(bg, tb, bubble_row, desk1_col)

        tb2 = THOUGHT_BUBBLES[(fi + 3) % len(THOUGHT_BUBBLES)]
        bubble2_row = agent2_row - 2
        if bubble2_row >= 1 and desk2_col + 12 < width:
            bg = stamp(bg, tb2, bubble2_row, desk2_col)

        # --- lightbulb above agent 1 ---
        lb = LIGHTBULB_FRAMES[fi % len(LIGHTBULB_FRAMES)]
        lb_row = bubble_row - 1
        if lb_row >= 1:
            bg = stamp(bg, lb, lb_row, desk1_col + 1)

        # --- blinking cursor on monitors ---
        cursor_row = desk_row + 1
        if 0 <= cursor_row < len(bg):
            row_chars = list(bg[cursor_row])
            cursor_pos = desk1_col + 2
            if cursor_pos < len(row_chars):
                row_chars[cursor_pos] = "\u2588" if fi % 2 == 0 else " "
            cursor_pos2 = desk2_col + 2
            if cursor_pos2 < len(row_chars):
                row_chars[cursor_pos2] = "\u2588" if fi % 3 == 0 else " "
            bg[cursor_row] = "".join(row_chars)

        frames.append(bg)

    return frames
