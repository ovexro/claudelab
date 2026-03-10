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

# Colors for code syntax elements
_KW_GREEN = MONITOR_TEXT_GREEN      # keywords: def, for, if, return, import
_KW_CYAN = MONITOR_TEXT_CYAN        # builtins / types
_STR_YELLOW = MONITOR_TEXT_YELLOW   # strings / numbers
_VAR_WHITE = MONITOR_TEXT_WHITE     # variables / identifiers
_PUNC_WHITE = (170, 170, 180)      # punctuation (dimmer white)

# Structured code-like line templates.
# Each template is a list of (indent, [(length, color), ...]) describing
# pixel segments that mimic real code structure.
_LINE_TEMPLATES = [
    # def function():
    (0, [(3, _KW_GREEN), (1, MONITOR_BG), (4, _VAR_WHITE), (1, _PUNC_WHITE), (1, _PUNC_WHITE)]),
    # "    return val"
    (3, [(6, _KW_GREEN), (1, MONITOR_BG), (3, _VAR_WHITE)]),
    # "  if cond:"
    (1, [(2, _KW_GREEN), (1, MONITOR_BG), (4, _VAR_WHITE), (1, _PUNC_WHITE)]),
    # "    for x in items:"
    (2, [(3, _KW_GREEN), (1, MONITOR_BG), (1, _VAR_WHITE), (1, MONITOR_BG), (2, _KW_GREEN), (1, MONITOR_BG), (3, _VAR_WHITE), (1, _PUNC_WHITE)]),
    # "import module"
    (0, [(6, _KW_CYAN), (1, MONITOR_BG), (5, _VAR_WHITE)]),
    # "  x = func(arg)"
    (1, [(1, _VAR_WHITE), (1, MONITOR_BG), (1, _PUNC_WHITE), (1, MONITOR_BG), (4, _KW_CYAN), (1, _PUNC_WHITE), (3, _STR_YELLOW), (1, _PUNC_WHITE)]),
    # "    print("text")"
    (2, [(5, _KW_CYAN), (1, _PUNC_WHITE), (4, _STR_YELLOW), (1, _PUNC_WHITE)]),
    # blank line
    (0, []),
    # "  # comment"
    (1, [(1, (100, 100, 120)), (1, MONITOR_BG), (6, (100, 100, 120))]),
    # "    self.val = x"
    (2, [(4, _KW_CYAN), (1, _PUNC_WHITE), (3, _VAR_WHITE), (1, MONITOR_BG), (1, _PUNC_WHITE), (1, MONITOR_BG), (1, _VAR_WHITE)]),
    # "  elif cond:"
    (1, [(4, _KW_GREEN), (1, MONITOR_BG), (4, _VAR_WHITE), (1, _PUNC_WHITE)]),
    # "      data.append(v)"
    (3, [(4, _VAR_WHITE), (1, _PUNC_WHITE), (6, _KW_CYAN), (1, _PUNC_WHITE), (1, _VAR_WHITE), (1, _PUNC_WHITE)]),
    # "  class Name:"
    (1, [(5, _KW_GREEN), (1, MONITOR_BG), (4, _KW_CYAN), (1, _PUNC_WHITE)]),
    # "    try:"
    (2, [(3, _KW_GREEN), (1, _PUNC_WHITE)]),
    # "      raise Error"
    (3, [(5, _KW_GREEN), (1, MONITOR_BG), (5, _KW_CYAN)]),
    # "  result = []"
    (1, [(6, _VAR_WHITE), (1, MONITOR_BG), (1, _PUNC_WHITE), (1, MONITOR_BG), (1, _PUNC_WHITE), (1, _PUNC_WHITE)]),
]

def _build_line(template_idx: int) -> list[tuple[int, int, int]]:
    """Build a pixel row from a line template."""
    indent, segments = _LINE_TEMPLATES[template_idx % len(_LINE_TEMPLATES)]
    row: list[tuple[int, int, int]] = [MONITOR_BG] * indent
    for length, color in segments:
        row.extend([color] * length)
    return row

# Pre-build a long code listing (enough lines to scroll through all frames)
_CODE_LISTING: list[list[tuple[int, int, int]]] = []
_rng = random.Random(42)
_template_order = list(range(len(_LINE_TEMPLATES)))
_rng.shuffle(_template_order)
for i in range(NUM_FRAMES + 16):
    _CODE_LISTING.append(_build_line(_template_order[i % len(_template_order)]))

# Each frame scrolls by 1 row to simulate code writing
_CODE_PATTERNS: list[list[list[tuple[int, int, int]]]] = []
for fi in range(NUM_FRAMES):
    frame_lines: list[list[tuple[int, int, int]]] = []
    for line_idx in range(8):
        frame_lines.append(_CODE_LISTING[(fi + line_idx) % len(_CODE_LISTING)])
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
