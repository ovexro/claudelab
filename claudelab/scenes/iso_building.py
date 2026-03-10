"""Isometric building scene — conveyor belt, code blocks, agents carry."""

from __future__ import annotations

from claudelab.palette import (
    CONVEYOR_GRAY, CONVEYOR_DARK, CONVEYOR_LIGHT,
    GOLD_BLOCK, LAPIS, REDSTONE, EMERALD, DIAMOND,
    PROGRESS_GREEN, PROGRESS_BG, PROGRESS_FRAME,
    STONE_DARK, IRON_DARK, OUTLINE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import CARRYING, WALKING
from claudelab.iso_office import build_iso_office, iso_to_screen, iso_agent_pos, TILE_W, TILE_H

NUM_FRAMES = 8

_BLOCK_COLORS = [GOLD_BLOCK, LAPIS, REDSTONE, EMERALD, DIAMOND]


def _draw_iso_conveyor(
    buf: PixelBuffer,
    ox: int, oy: int,
    start_gx: float, gy: float,
    length: int,
    fi: int,
) -> tuple[list[tuple[int, int]], int]:
    """Draw an isometric conveyor belt along the grid X axis.

    Returns list of (screen_x, screen_y) points along the belt for placing
    blocks, and the belt height in pixels for placing agents above.
    """
    shift = fi // 2
    belt_h = 3  # height of belt sides in pixels
    points = []

    for step in range(length):
        gx = start_gx + step * 0.5
        cx, cy = iso_to_screen(gx, gy, ox, oy)
        cx2, cy2 = iso_to_screen(gx + 0.5, gy, ox, oy)
        points.append((cx, cy))

        # Draw belt surface segment (isometric strip)
        dx = cx2 - cx
        dy = cy2 - cy
        steps = max(1, abs(dx))
        for s in range(steps):
            t = s / max(1, steps)
            px = int(cx + t * dx)
            py = int(cy + t * dy)
            # Belt pattern — animated stripes
            stripe = (s + shift) % 4
            if stripe == 0:
                c = CONVEYOR_DARK
            elif stripe == 1:
                c = CONVEYOR_LIGHT
            else:
                c = CONVEYOR_GRAY
            # Belt is 3px wide perpendicular to direction
            for bw in range(-1, 2):
                buf.set_pixel(px + bw, py, c)
            # Side walls
            for bh in range(1, belt_h + 1):
                buf.set_pixel(px - 2, py + bh, IRON_DARK)
                buf.set_pixel(px + 2, py + bh, STONE_DARK)
            # Rails on top edges
            buf.set_pixel(px - 2, py, STONE_DARK)
            buf.set_pixel(px + 2, py, STONE_DARK)

    # Supports (legs) every few segments
    for i in range(0, length, 3):
        gx = start_gx + i * 0.5
        cx, cy = iso_to_screen(gx, gy, ox, oy)
        for bh in range(belt_h + 1, belt_h + 5):
            buf.set_pixel(cx - 1, cy + bh, STONE_DARK)
            buf.set_pixel(cx, cy + bh, STONE_DARK)

    return points, belt_h


_SHADOW_COLOR = (20, 20, 25)

def _draw_code_block(buf: PixelBuffer, x: int, y: int, color: tuple, size: int = 5) -> None:
    """Draw a shaded code block with 1px drop shadow."""
    shade = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
    light = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
    # Drop shadow (1px below and 1px right)
    for dx in range(size):
        buf.set_pixel(x + dx + 1, y + size, _SHADOW_COLOR)
    for dy in range(size):
        buf.set_pixel(x + size, y + dy + 1, _SHADOW_COLOR)
    # Block face
    buf.fill_rect(x, y, size, size, color)
    for dx in range(size):
        buf.set_pixel(x + dx, y, light)
    for dy in range(size):
        buf.set_pixel(x, y + dy, light)
    for dx in range(size):
        buf.set_pixel(x + dx, y + size - 1, shade)
    for dy in range(size):
        buf.set_pixel(x + size - 1, y + dy, shade)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf, layout = build_iso_office(width, pixel_h, fi)
        ox = layout["origin_x"]
        oy = layout["origin_y"]
        gw = layout["grid_w"]
        gd = layout["grid_d"]

        # Isometric conveyor belt running across the floor
        conv_gy = max(2.0, gd * 0.6)  # Place in front half of room
        conv_start_gx = 1.0
        conv_len = max(4, gw - 2)  # segments (each 0.5 grid units)
        points, belt_h = _draw_iso_conveyor(
            buf, ox, oy, conv_start_gx, conv_gy, conv_len, fi,
        )

        # Carrier agent walking along the conveyor path
        if points:
            carrier = CARRYING[fi % len(CARRYING)]
            idx = (fi * 2) % max(1, len(points))
            px, py = points[idx]
            buf.draw_sprite(carrier, px - carrier.width // 2, py - carrier.height - belt_h)

        # Second agent walking opposite direction
        if width >= 55 and len(points) > 4:
            walker = WALKING[fi % len(WALKING)]
            idx2 = (len(points) - 1) - ((fi * 2) % max(1, len(points)))
            idx2 = max(0, min(idx2, len(points) - 1))
            px2, py2 = points[idx2]
            buf.draw_sprite(walker, px2 - walker.width // 2, py2 - walker.height - belt_h)

        # Code blocks on conveyor (moving along iso path)
        if len(points) >= 6:
            _speeds = [3, 5, 4]
            for i in range(min(3, len(points) // 3)):
                speed = _speeds[i]
                bidx = (fi * speed + i * (len(points) // 3)) % len(points)
                bx, by = points[bidx]
                _draw_code_block(buf, bx - 2, by - 7, _BLOCK_COLORS[(fi + i) % len(_BLOCK_COLORS)])

        # Block stack accumulating at end of conveyor
        if points and width >= 50:
            end_x, end_y = points[-1]
            stack_count = min(fi + 1, 4)
            for i in range(stack_count):
                color = _BLOCK_COLORS[i % len(_BLOCK_COLORS)]
                _draw_code_block(buf, end_x + 4, end_y - i * 5 - 3, color)

        # Progress bar at bottom
        if width >= 40:
            bar_w = min(20, width // 3)
            bar_x = (width - bar_w) // 2
            bar_y = pixel_h - 4
            buf.fill_rect(bar_x - 1, bar_y - 1, bar_w + 2, 4, PROGRESS_FRAME)
            buf.fill_rect(bar_x, bar_y, bar_w, 2, PROGRESS_BG)
            fill = ((fi + 1) * bar_w) // NUM_FRAMES
            for dx in range(fill):
                buf.set_pixel(bar_x + dx, bar_y, PROGRESS_GREEN)
                buf.set_pixel(bar_x + dx, bar_y + 1, PROGRESS_GREEN)

        frames.append(buf)
    return frames
