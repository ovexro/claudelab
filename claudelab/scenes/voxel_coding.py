"""Voxel coding scene — agents type, code scrolls on monitors."""

from __future__ import annotations

import random

from claudelab.palette import (
    MONITOR_TEXT_GREEN, MONITOR_TEXT_YELLOW, MONITOR_TEXT_WHITE,
    MONITOR_TEXT_CYAN, MONITOR_BG,
)
from claudelab.pixelbuffer import PixelBuffer
from claudelab.sprites import SITTING_TYPING, SITTING_TYPING_2
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Deterministic "code" patterns with indentation
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


def _draw_code_on_monitor(buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int) -> None:
    """Fill monitor screen area with scrolling code pixels."""
    pattern = _CODE_PATTERNS[fi % len(_CODE_PATTERNS)]
    for dy in range(min(mh - 4, len(pattern))):
        row = pattern[(dy + fi) % len(pattern)]
        for dx in range(min(mw - 4, len(row))):
            buf.set_pixel(mx + 2 + dx, my + 2 + dy, row[dx])


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(6, pixel_h * 7 // 20)
        floor_y = wall_h
        desk_y = floor_y + 2
        desk_w = min(14, width // 5)

        # Agent 1 typing
        if width >= 40:
            agent = SITTING_TYPING[fi % len(SITTING_TYPING)]
            agent_y = desk_y - agent.height + 1
            buf.draw_sprite(agent, 5, agent_y)
            _draw_code_on_monitor(buf, 5, desk_y - 10, min(10, desk_w - 2), 8, fi)

        # Agent 2 typing
        if width >= 60:
            desk2_x = width // 3 + 4
            agent2 = SITTING_TYPING_2[fi % len(SITTING_TYPING_2)]
            agent_y = desk_y - agent2.height + 1
            buf.draw_sprite(agent2, desk2_x + 3, agent_y)
            _draw_code_on_monitor(buf, desk2_x + 2, desk_y - 10, min(10, desk_w - 2), 8, fi + 3)

        frames.append(buf)
    return frames
