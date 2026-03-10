"""Voxel thinking scene — agents sit at desks with thought bubbles."""

from __future__ import annotations

from claudelab.palette import (
    THOUGHT_CLOUD, THOUGHT_DARK, WARNING_YELLOW,
    MONITOR_TEXT_GREEN, MONITOR_BG, GLOWSTONE, COAL,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import SITTING_IDLE_1, SITTING_IDLE_2
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Thought bubble sprites
_BUBBLE_DOTS = Sprite.from_pixel_art([
    "...CCC..",
    "..CCCCC.",
    ".CDDCDC.",
    "..CCCCC.",
    "...CCC..",
    "....C...",
    ".....c..",
], {"C": THOUGHT_CLOUD, "D": THOUGHT_DARK, "c": THOUGHT_DARK, ".": None})

_BUBBLE_QUESTION = Sprite.from_pixel_art([
    "...CCC..",
    "..CCCCC.",
    ".CCYYCCC",
    "..CCYCC.",
    "...CYC..",
    "....C...",
    ".....c..",
], {"C": THOUGHT_CLOUD, "Y": WARNING_YELLOW, "c": THOUGHT_DARK, ".": None})

_BUBBLE_LIGHT = Sprite.from_pixel_art([
    "...CCC..",
    "..CCCCC.",
    ".CCGLCC.",
    "..CGLC..",
    "...CCC..",
    "....C...",
    ".....c..",
], {"C": THOUGHT_CLOUD, "G": GLOWSTONE, "L": (255, 230, 80), "c": THOUGHT_DARK, ".": None})

_BUBBLES = [_BUBBLE_DOTS, _BUBBLE_DOTS, _BUBBLE_QUESTION, _BUBBLE_QUESTION,
            _BUBBLE_LIGHT, _BUBBLE_LIGHT, _BUBBLE_DOTS, _BUBBLE_QUESTION]


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(4, pixel_h * 2 // 5)
        floor_y = wall_h
        desk_y = floor_y + 2

        # Agent 1 at desk 1
        agent_y = desk_y - SITTING_IDLE_1.height + 1
        if width >= 40:
            buf.draw_sprite(SITTING_IDLE_1, 5, agent_y)
            # Thought bubble
            bubble = _BUBBLES[fi % len(_BUBBLES)]
            buf.draw_sprite(bubble, 3, agent_y - bubble.height - 1)

        # Agent 2 at desk 2
        if width >= 60:
            desk2_x = width // 3 + 2
            buf.draw_sprite(SITTING_IDLE_2, desk2_x + 2, agent_y)
            # Cursor blink on monitor
            mon_x = desk2_x + 2
            mon_y = desk_y - 7 + 2
            if fi % 2 == 0:
                buf.set_pixel(mon_x, mon_y, MONITOR_TEXT_GREEN)
            else:
                buf.set_pixel(mon_x, mon_y, MONITOR_BG)

        # Lightbulb animation above agent 1
        if width >= 40:
            lb_x = 7
            lb_y = agent_y - _BUBBLES[0].height - 4
            if lb_y >= 0:
                intensity = fi % 4
                if intensity >= 2:
                    buf.set_pixel(lb_x, lb_y, GLOWSTONE)
                    buf.set_pixel(lb_x + 1, lb_y, GLOWSTONE)
                elif intensity == 1:
                    buf.set_pixel(lb_x, lb_y, COAL)

        frames.append(buf)
    return frames
