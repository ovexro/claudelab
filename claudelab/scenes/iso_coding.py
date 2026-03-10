"""Isometric coding scene — agents type at desks in a 3D office."""

from __future__ import annotations

import random

from claudelab.palette import (
    MONITOR_TEXT_GREEN, MONITOR_TEXT_YELLOW, MONITOR_TEXT_WHITE,
    MONITOR_TEXT_CYAN, MONITOR_BG,
)
from claudelab.pixelbuffer import PixelBuffer
from claudelab.sprites import SITTING_TYPING, SITTING_TYPING_2
from claudelab.iso_office import build_iso_office, iso_agent_pos

NUM_FRAMES = 8

# Deterministic "code" patterns
_rng = random.Random(42)
_CODE_COLORS = [MONITOR_TEXT_GREEN, MONITOR_TEXT_YELLOW, MONITOR_TEXT_WHITE, MONITOR_TEXT_CYAN]
_CODE_PATTERNS: list[list[list[tuple[int, int, int]]]] = []
for _ in range(NUM_FRAMES):
    frame_lines: list[list[tuple[int, int, int]]] = []
    for _line in range(8):
        indent = _rng.randint(0, 3)
        line_len = _rng.randint(2, 6)
        row: list[tuple[int, int, int]] = [MONITOR_BG] * indent
        for _c in range(line_len):
            row.append(_rng.choice(_CODE_COLORS))
        frame_lines.append(row)
    _CODE_PATTERNS.append(frame_lines)


def _draw_code_on_monitor(
    buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int,
) -> None:
    """Fill monitor screen area with scrolling code pixels."""
    pattern = _CODE_PATTERNS[fi % len(_CODE_PATTERNS)]
    for dy in range(min(mh, len(pattern))):
        row = pattern[(dy + fi) % len(pattern)]
        for dx in range(min(mw, len(row))):
            buf.set_pixel(mx + dx, my + dy, row[dx])


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf, layout = build_iso_office(width, pixel_h, fi)

        ox = layout["origin_x"]
        oy = layout["origin_y"]

        # Agent 1 typing at desk 1
        if width >= 40:
            agent = SITTING_TYPING[fi % len(SITTING_TYPING)]
            ax, ay = iso_agent_pos(
                layout["agent1_gx"], layout["agent1_gy"],
                ox, oy, agent.height,
            )
            buf.draw_sprite(agent, ax, ay)

            # Code on monitor 1
            mx, my, mw, mh = layout["mon1_rect"]
            _draw_code_on_monitor(buf, mx, my, mw, mh, fi)

        # Agent 2 typing at desk 2
        if width >= 60:
            agent2 = SITTING_TYPING_2[fi % len(SITTING_TYPING_2)]
            ax2, ay2 = iso_agent_pos(
                layout["agent2_gx"], layout["agent2_gy"],
                ox, oy, agent2.height,
            )
            buf.draw_sprite(agent2, ax2, ay2)

            # Code on monitor 2
            mx2, my2, mw2, mh2 = layout["mon2_rect"]
            _draw_code_on_monitor(buf, mx2, my2, mw2, mh2, fi + 3)

        frames.append(buf)
    return frames
