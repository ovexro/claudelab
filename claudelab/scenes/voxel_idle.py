"""Voxel idle scene — agents drink coffee, lean back, chat."""

from __future__ import annotations

from claudelab.palette import (
    STEAM_WHITE, STEAM_FADE, THOUGHT_CLOUD, THOUGHT_DARK,
    MONITOR_TEXT_WHITE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import DRINKING, LEANING, SITTING_IDLE_2
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Chat bubble sprites
_CHAT_1 = Sprite.from_pixel_art([
    ".CCCCC.",
    "CCTTTCC",
    "CCTTTCC",
    ".CCCCC.",
    "CC.....",
], {"C": THOUGHT_CLOUD, "T": MONITOR_TEXT_WHITE, ".": None})

_CHAT_2 = Sprite.from_pixel_art([
    ".CCCCC.",
    "CCDDTCC",
    "CCTDDCC",
    ".CCCCC.",
    ".....CC",
], {"C": THOUGHT_CLOUD, "T": MONITOR_TEXT_WHITE, "D": THOUGHT_DARK, ".": None})


def _draw_steam(buf: PixelBuffer, x: int, base_y: int, fi: int) -> None:
    """Draw rising steam particles."""
    particles = [
        (0, 0), (1, -1), (-1, -2), (0, -3), (1, -4),
    ]
    for i, (dx, dy) in enumerate(particles):
        py = base_y + dy - (fi % 4)
        px = x + dx + ((fi + i) % 3 - 1)
        if py >= 0 and 0 <= px < buf.width:
            fade = abs(dy) + (fi % 4)
            c = STEAM_WHITE if fade < 3 else STEAM_FADE
            buf.set_pixel(px, py, c)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(4, pixel_h * 2 // 5)
        floor_y = wall_h
        desk_y = floor_y + 2

        # Agent 1 drinking coffee at desk
        if width >= 40:
            drinker = DRINKING[fi % len(DRINKING)]
            agent_y = desk_y - drinker.height + 1
            buf.draw_sprite(drinker, 5, agent_y)

            # Steam from coffee
            _draw_steam(buf, 12, agent_y - 2, fi)

        # Agent 2 leaning back / idle at desk 2
        if width >= 60:
            desk2_x = width // 3 + 2
            if fi % 4 < 2:
                buf.draw_sprite(LEANING, desk2_x + 2, desk_y - LEANING.height + 1)
            else:
                buf.draw_sprite(SITTING_IDLE_2, desk2_x + 2, desk_y - SITTING_IDLE_2.height + 1)

        # Chat bubbles (alternate between agents)
        if width >= 55:
            if fi % 4 < 2:
                buf.draw_sprite(_CHAT_1, 14, desk_y - 16)
            elif fi % 4 == 2:
                desk2_x = width // 3 + 2
                buf.draw_sprite(_CHAT_2, desk2_x + 10, desk_y - 16)

        # Steam from coffee machine
        if width >= 55:
            cm_x = width // 2 + 4
            cm_y = floor_y + 2
            _draw_steam(buf, cm_x + 1, cm_y - 2, fi + 3)

        frames.append(buf)
    return frames
