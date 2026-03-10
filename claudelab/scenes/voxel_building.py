"""Voxel building scene — conveyor belt, agents carry code blocks."""

from __future__ import annotations

from claudelab.palette import (
    CONVEYOR_GRAY, CONVEYOR_DARK,
    GOLD_BLOCK, LAPIS, REDSTONE, EMERALD, DIAMOND,
    PROGRESS_GREEN, PROGRESS_BG,
    STONE_DARK,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import CARRYING, WALKING
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Code block colors (different "languages")
_BLOCK_COLORS = [GOLD_BLOCK, LAPIS, REDSTONE, EMERALD, DIAMOND]


def _draw_conveyor(buf: PixelBuffer, x: int, y: int, w: int, fi: int) -> None:
    """Draw an animated conveyor belt."""
    for dx in range(w):
        # Belt surface
        if (dx + fi) % 4 == 0:
            c = CONVEYOR_DARK
        else:
            c = CONVEYOR_GRAY
        buf.set_pixel(x + dx, y, c)
        buf.set_pixel(x + dx, y + 1, c)
    # Belt supports
    for dx in range(0, w, 6):
        buf.set_pixel(x + dx, y + 2, STONE_DARK)
        buf.set_pixel(x + dx, y + 3, STONE_DARK)


def _draw_code_block(buf: PixelBuffer, x: int, y: int, color: tuple[int, int, int]) -> None:
    """Draw a 3x3 code block."""
    shade = (max(0, color[0] - 30), max(0, color[1] - 30), max(0, color[2] - 30))
    buf.fill_rect(x, y, 3, 3, color)
    buf.set_pixel(x, y, shade)
    buf.set_pixel(x + 2, y + 2, shade)


def _draw_block_stack(buf: PixelBuffer, x: int, y: int, count: int, fi: int) -> None:
    """Draw stacked code blocks on the platform."""
    for i in range(count):
        color = _BLOCK_COLORS[i % len(_BLOCK_COLORS)]
        _draw_code_block(buf, x, y - i * 3, color)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(4, pixel_h * 2 // 5)
        floor_y = wall_h

        # Conveyor belt
        conv_w = min(width - 10, width * 2 // 3)
        conv_x = 3
        conv_y = floor_y + 4
        if conv_w >= 10:
            _draw_conveyor(buf, conv_x, conv_y, conv_w, fi)

        # Carrier agent walking along conveyor
        if conv_w >= 10:
            carrier = CARRYING[fi % len(CARRYING)]
            agent_x = conv_x + ((fi * 4) % max(1, conv_w - carrier.width))
            agent_y = conv_y - carrier.height
            buf.draw_sprite(carrier, agent_x, agent_y)

        # Second agent walking the other way
        if width >= 55 and conv_w >= 10:
            walker = WALKING[fi % len(WALKING)]
            w_x = conv_x + conv_w - ((fi * 3) % max(1, conv_w - walker.width)) - walker.width
            w_x = max(conv_x, w_x)
            w_y = conv_y - walker.height
            buf.draw_sprite(walker, w_x, w_y)

        # Code blocks on conveyor (moving right)
        if conv_w >= 20:
            for i in range(3):
                bx = conv_x + 5 + ((fi * 4 + i * 8) % max(1, conv_w - 8))
                by = conv_y - 3
                _draw_code_block(buf, bx, by, _BLOCK_COLORS[(fi + i) % len(_BLOCK_COLORS)])

        # Block stack (accumulates over frames)
        if width >= 50:
            stack_x = width - 12
            stack_y = floor_y + 3
            stack_count = min(fi + 1, 4)
            _draw_block_stack(buf, stack_x, stack_y, stack_count, fi)

        # Progress bar
        if width >= 40:
            bar_w = min(16, width // 4)
            bar_x = 3
            bar_y = pixel_h - 4
            fill = ((fi + 1) * bar_w) // NUM_FRAMES
            for dx in range(bar_w):
                c = PROGRESS_GREEN if dx < fill else PROGRESS_BG
                buf.set_pixel(bar_x + dx, bar_y, c)
                buf.set_pixel(bar_x + dx, bar_y + 1, c)

        frames.append(buf)
    return frames
