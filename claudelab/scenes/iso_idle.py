"""Isometric idle scene — agents drink coffee, lean, chat."""

from __future__ import annotations

from claudelab.palette import (
    STEAM_WHITE, STEAM_FADE,
    THOUGHT_CLOUD, THOUGHT_DARK, THOUGHT_LIGHT,
    MONITOR_TEXT_WHITE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import DRINKING, LEANING, SITTING_IDLE_2
from claudelab.iso_office import build_iso_office, iso_agent_pos

NUM_FRAMES = 8

_CHAT_1 = Sprite.from_pixel_art([
    "..OOOOOOO.",
    ".OLLLTLLLO",
    ".OLTTLTLLO",
    ".OLLLTLLLO",
    "..OOOOOOO.",
    ".OO.......",
    "OO........",
], {"O": THOUGHT_DARK, "L": THOUGHT_CLOUD, "T": THOUGHT_LIGHT, ".": None})

_CHAT_2 = Sprite.from_pixel_art([
    ".OOOOOOO..",
    "OLLLWLLLO.",
    "OLLWWLLLO.",
    "OLLLWLLLO.",
    ".OOOOOOO..",
    ".......OO.",
    "........OO",
], {"O": THOUGHT_DARK, "L": THOUGHT_CLOUD, "W": MONITOR_TEXT_WHITE, ".": None})


def _draw_steam(buf: PixelBuffer, x: int, base_y: int, fi: int) -> None:
    """Draw rising steam particles — bigger, brighter, more visible."""
    _patterns = [
        [(0, 0), (1, -1), (-1, -2), (0, -3), (1, -4), (-1, -5), (0, -6), (1, -7)],
        [(1, 0), (0, -1), (1, -2), (-1, -3), (0, -4), (1, -5), (-1, -6), (0, -7)],
        [(-1, 0), (1, -1), (0, -2), (1, -3), (-1, -4), (0, -5), (1, -6), (-1, -7)],
        [(0, 0), (-1, -1), (1, -2), (0, -3), (-1, -4), (1, -5), (0, -6), (-1, -7)],
        [(1, 0), (-1, -1), (0, -2), (-1, -3), (1, -4), (0, -5), (-1, -6), (1, -7)],
        [(-1, 0), (0, -1), (-1, -2), (1, -3), (0, -4), (-1, -5), (1, -6), (0, -7)],
        [(0, 0), (1, -1), (0, -2), (-1, -3), (1, -4), (-1, -5), (0, -6), (1, -7)],
        [(1, 0), (-1, -1), (1, -2), (0, -3), (-1, -4), (0, -5), (1, -6), (-1, -7)],
    ]
    particles = _patterns[fi % 8]
    phase = fi % 8
    for i, (dx, dy) in enumerate(particles):
        py = base_y + dy - (phase // 2)
        px = x + dx + ((phase + i) % 3 - 1)
        if py >= 0 and 0 <= px < buf.width:
            fade = abs(dy) + (phase // 2)
            if fade < 3:
                c = STEAM_WHITE
            elif fade < 6:
                c = STEAM_FADE
            else:
                c = (160, 160, 180)
            # Draw 2px wide particles for visibility
            buf.set_pixel(px, py, c)
            if px + 1 < buf.width:
                buf.set_pixel(px + 1, py, c)
            # Extra bright core for lowest particles
            if fade < 2 and px - 1 >= 0:
                buf.set_pixel(px - 1, py, STEAM_FADE)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf, layout = build_iso_office(width, pixel_h, fi)
        ox = layout["origin_x"]
        oy = layout["origin_y"]

        # Agent 1 drinking coffee
        if width >= 40:
            drinker = DRINKING[fi % len(DRINKING)]
            ax, ay = iso_agent_pos(
                layout["agent1_gx"], layout["agent1_gy"],
                ox, oy, drinker.height,
            )
            buf.draw_sprite(drinker, ax, ay)

            # Steam from mug
            _draw_steam(buf, ax + 12, ay - 2, fi)

        # Agent 2 leaning / idle — slower breathing cycle (every 3 frames)
        if width >= 60:
            if fi % 6 < 3:
                agent2 = LEANING
            else:
                agent2 = SITTING_IDLE_2
            ax2, ay2 = iso_agent_pos(
                layout["agent2_gx"], layout["agent2_gy"],
                ox, oy, agent2.height,
            )
            buf.draw_sprite(agent2, ax2, ay2)

        # Chat bubbles
        if width >= 55:
            if fi % 4 < 2:
                ax, ay = iso_agent_pos(
                    layout["agent1_gx"], layout["agent1_gy"],
                    ox, oy, DRINKING[0].height,
                )
                bub_y = max(0, ay - _CHAT_1.height - 2)
                buf.draw_sprite(_CHAT_1, ax + 14, bub_y)
            elif fi % 4 == 2 and width >= 60:
                ax2, ay2 = iso_agent_pos(
                    layout["agent2_gx"], layout["agent2_gy"],
                    ox, oy, LEANING.height,
                )
                bub_y = max(0, ay2 - _CHAT_2.height - 2)
                buf.draw_sprite(_CHAT_2, ax2 + 14, bub_y)

        frames.append(buf)
    return frames
