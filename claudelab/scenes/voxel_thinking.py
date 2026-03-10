"""Voxel thinking scene — agents ponder with thought bubbles."""

from __future__ import annotations

from claudelab.palette import (
    THOUGHT_CLOUD, THOUGHT_DARK, THOUGHT_LIGHT,
    WARNING_YELLOW, GLOWSTONE,
    MONITOR_TEXT_GREEN, MONITOR_BG,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import SITTING_THINK_1, SITTING_THINK_2, SITTING_IDLE_2
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Larger thought bubbles (12x9) with outline and interior icons
_BUBBLE_DOTS = Sprite.from_pixel_art([
    "....OOOOOO..",
    "..OOLLLLLOO.",
    ".OLLDDLDLLO.",
    ".OLLDLLDDLO.",
    ".OLLDDDLLLO.",
    "..OOLLLLLOO.",
    "....OOOOOO..",
    ".....OO.....",
    "......OO....",
], {"O": THOUGHT_DARK, "L": THOUGHT_CLOUD, "D": THOUGHT_LIGHT, ".": None})

_BUBBLE_QUESTION = Sprite.from_pixel_art([
    "....OOOOOO..",
    "..OOLLLLLOO.",
    ".OLL.YY.LLO.",
    ".OLL..Y.LLO.",
    ".OLLL.Y.LLO.",
    "..OOLLYLLOO.",
    "....OOOOOO..",
    ".....OO.....",
    "......OO....",
], {"O": THOUGHT_DARK, "L": THOUGHT_CLOUD, "Y": WARNING_YELLOW, ".": None})

_BUBBLE_LIGHT = Sprite.from_pixel_art([
    "....OOOOOO..",
    "..OOLLLLLOO.",
    ".OLL.GG.LLO.",
    ".OLLGGGGLLLO",
    ".OLL.GG.LLO.",
    "..OOLLLLLOO.",
    "....OOOOOO..",
    ".....OO.....",
    "......OO....",
], {"O": THOUGHT_DARK, "L": THOUGHT_CLOUD, "G": GLOWSTONE, ".": None})

_BUBBLES = [_BUBBLE_DOTS, _BUBBLE_DOTS, _BUBBLE_QUESTION, _BUBBLE_QUESTION,
            _BUBBLE_LIGHT, _BUBBLE_LIGHT, _BUBBLE_DOTS, _BUBBLE_QUESTION]


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(6, pixel_h * 7 // 20)
        floor_y = wall_h
        desk_y = floor_y + 2

        # Agent 1 thinking at desk
        if width >= 40:
            agent_y = desk_y - SITTING_THINK_1.height + 1
            buf.draw_sprite(SITTING_THINK_1, 5, agent_y)
            # Thought bubble above
            bubble = _BUBBLES[fi % len(_BUBBLES)]
            bub_y = max(0, agent_y - bubble.height - 1)
            buf.draw_sprite(bubble, 2, bub_y)

        # Agent 2 at desk 2
        if width >= 60:
            desk2_x = width // 3 + 4
            buf.draw_sprite(SITTING_IDLE_2, desk2_x + 3, desk_y - SITTING_IDLE_2.height + 1)
            # Cursor blink on monitor
            mon_x = desk2_x + 4
            mon_y = desk_y - 8
            if fi % 2 == 0:
                buf.set_pixel(mon_x, mon_y, MONITOR_TEXT_GREEN)
            else:
                buf.set_pixel(mon_x, mon_y, MONITOR_BG)

        frames.append(buf)
    return frames
