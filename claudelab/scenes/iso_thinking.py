"""Isometric thinking scene — agents ponder with thought bubbles."""

from __future__ import annotations

from claudelab.palette import (
    THOUGHT_CLOUD, THOUGHT_DARK, THOUGHT_LIGHT,
    WARNING_YELLOW, GLOWSTONE,
    MONITOR_TEXT_GREEN, MONITOR_BG,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import SITTING_THINK_1, SITTING_THINK_2, SITTING_IDLE_2
from claudelab.iso_office import build_iso_office, iso_agent_pos

NUM_FRAMES = 8

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
        buf, layout = build_iso_office(width, pixel_h, fi)
        ox = layout["origin_x"]
        oy = layout["origin_y"]

        # Agent 1 thinking at desk
        if width >= 40:
            ax, ay = iso_agent_pos(
                layout["agent1_gx"], layout["agent1_gy"],
                ox, oy, SITTING_THINK_1.height,
            )
            buf.draw_sprite(SITTING_THINK_1, ax, ay)

            # Thought bubble above agent
            bubble = _BUBBLES[fi % len(_BUBBLES)]
            bub_y = max(0, ay - bubble.height - 1)
            buf.draw_sprite(bubble, ax - 2, bub_y)

        # Agent 2 idle at desk 2
        if width >= 60:
            ax2, ay2 = iso_agent_pos(
                layout["agent2_gx"], layout["agent2_gy"],
                ox, oy, SITTING_IDLE_2.height,
            )
            buf.draw_sprite(SITTING_IDLE_2, ax2, ay2)

            # Cursor blink on monitor 2
            mx, my, mw, mh = layout["mon2_rect"]
            if fi % 2 == 0:
                buf.set_pixel(mx + 1, my + 1, MONITOR_TEXT_GREEN)
            else:
                buf.set_pixel(mx + 1, my + 1, MONITOR_BG)

        frames.append(buf)
    return frames
