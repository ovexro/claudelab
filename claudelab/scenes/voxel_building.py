"""Voxel building scene — conveyor belt, code blocks, agents carry."""

from __future__ import annotations

from claudelab.palette import (
    CONVEYOR_GRAY, CONVEYOR_DARK, CONVEYOR_LIGHT,
    GOLD_BLOCK, LAPIS, REDSTONE, EMERALD, DIAMOND,
    PROGRESS_GREEN, PROGRESS_BG, PROGRESS_FRAME,
    STONE_DARK, OUTLINE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import CARRYING, WALKING
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

_BLOCK_COLORS = [GOLD_BLOCK, LAPIS, REDSTONE, EMERALD, DIAMOND]


def _draw_conveyor(buf: PixelBuffer, x: int, y: int, w: int, fi: int) -> None:
    """Draw animated conveyor belt with rollers."""
    # Belt surface (2px tall)
    for dx in range(w):
        if (dx + fi) % 4 == 0:
            c = CONVEYOR_DARK
        elif (dx + fi) % 4 == 1:
            c = CONVEYOR_LIGHT
        else:
            c = CONVEYOR_GRAY
        buf.set_pixel(x + dx, y, c)
        buf.set_pixel(x + dx, y + 1, CONVEYOR_GRAY if (dx + fi) % 4 != 0 else CONVEYOR_DARK)
    # Side rails
    for dx in range(w):
        buf.set_pixel(x + dx, y - 1, STONE_DARK)
        buf.set_pixel(x + dx, y + 2, STONE_DARK)
    # Supports
    for dx in range(0, w, 8):
        for dy in range(3, 6):
            buf.set_pixel(x + dx, y + dy, STONE_DARK)
            buf.set_pixel(x + dx + 1, y + dy, STONE_DARK)


def _draw_code_block(buf: PixelBuffer, x: int, y: int, color: tuple, size: int = 5) -> None:
    """Draw a shaded code block."""
    shade = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
    light = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
    buf.fill_rect(x, y, size, size, color)
    # Highlight top-left
    for dx in range(size):
        buf.set_pixel(x + dx, y, light)
    for dy in range(size):
        buf.set_pixel(x, y + dy, light)
    # Shadow bottom-right
    for dx in range(size):
        buf.set_pixel(x + dx, y + size - 1, shade)
    for dy in range(size):
        buf.set_pixel(x + size - 1, y + dy, shade)


def _draw_block_stack(buf: PixelBuffer, x: int, y: int, count: int, fi: int) -> None:
    """Draw stacked code blocks."""
    for i in range(count):
        color = _BLOCK_COLORS[i % len(_BLOCK_COLORS)]
        _draw_code_block(buf, x, y - i * 5, color)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(6, pixel_h * 7 // 20)
        floor_y = wall_h

        # Conveyor belt
        conv_w = min(width - 14, width * 2 // 3)
        conv_x = 4
        conv_y = floor_y + 5
        if conv_w >= 12:
            _draw_conveyor(buf, conv_x, conv_y, conv_w, fi)

        # Carrier agent
        if conv_w >= 12:
            carrier = CARRYING[fi % len(CARRYING)]
            agent_x = conv_x + ((fi * 5) % max(1, conv_w - carrier.width))
            agent_y = conv_y - carrier.height - 1
            buf.draw_sprite(carrier, agent_x, agent_y)

        # Second agent walking opposite direction
        if width >= 55 and conv_w >= 12:
            walker = WALKING[fi % len(WALKING)]
            w_x = conv_x + conv_w - ((fi * 4) % max(1, conv_w - walker.width)) - walker.width
            w_x = max(conv_x, w_x)
            w_y = conv_y - walker.height - 1
            buf.draw_sprite(walker, w_x, w_y)

        # Code blocks on conveyor (moving right)
        if conv_w >= 24:
            for i in range(3):
                bx = conv_x + 6 + ((fi * 5 + i * 10) % max(1, conv_w - 10))
                by = conv_y - 5
                _draw_code_block(buf, bx, by, _BLOCK_COLORS[(fi + i) % len(_BLOCK_COLORS)])

        # Block stack (accumulates)
        if width >= 50:
            stack_x = width - 14
            stack_y = floor_y + 4
            stack_count = min(fi + 1, 4)
            _draw_block_stack(buf, stack_x, stack_y, stack_count, fi)

        # Progress bar
        if width >= 40:
            bar_w = min(20, width // 3)
            bar_x = 4
            bar_y = pixel_h - 5
            buf.fill_rect(bar_x - 1, bar_y - 1, bar_w + 2, 4, PROGRESS_FRAME)
            buf.fill_rect(bar_x, bar_y, bar_w, 2, PROGRESS_BG)
            fill = ((fi + 1) * bar_w) // NUM_FRAMES
            for dx in range(fill):
                buf.set_pixel(bar_x + dx, bar_y, PROGRESS_GREEN)
                buf.set_pixel(bar_x + dx, bar_y + 1, PROGRESS_GREEN)

        frames.append(buf)
    return frames
