"""Voxel debugging scene — red alerts, whiteboard, error traces."""

from __future__ import annotations

from claudelab.palette import (
    BIRCH_PLANK, MONITOR_TEXT_RED, MONITOR_BG,
    WARNING_RED, WARNING_YELLOW, MONITOR_FRAME,
    LED_RED, LED_OFF, OUTLINE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import STANDING_POINTING, STANDING_EXAMINING
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Larger warning triangle
_WARNING = Sprite.from_pixel_art([
    "....OYO.....",
    "...OYYYO....",
    "..OYYYYYO...",
    ".OYYYRYYYO..",
    "OYYYYYYYYY0.",
    "OOOOOOOOOOO.",
], {"Y": WARNING_YELLOW, "R": WARNING_RED, "O": OUTLINE, "0": OUTLINE, ".": None})


def _selective_red_tint(buf: PixelBuffer) -> None:
    """Subtle red tint — stronger on monitors/rack, lighter on background."""
    for y in range(buf.height):
        for x in range(buf.width):
            r, g, b = buf.pixels[y][x]
            # Stronger tint on dark areas (monitors, tech)
            if r + g + b < 200:
                r = min(255, r + 30)
                g = max(0, g - 15)
                b = max(0, b - 15)
            else:
                r = min(255, r + 12)
                g = max(0, g - 5)
                b = max(0, b - 5)
            buf.pixels[y][x] = (r, g, b)


def _draw_whiteboard(buf: PixelBuffer, x: int, y: int, w: int, h: int, fi: int) -> None:
    """Draw whiteboard with error diagram."""
    buf.fill_rect(x, y, w, h, BIRCH_PLANK)
    # Frame
    for dx in range(w):
        buf.set_pixel(x + dx, y, MONITOR_FRAME)
        buf.set_pixel(x + dx, y + h - 1, MONITOR_FRAME)
    for dy in range(h):
        buf.set_pixel(x, y + dy, MONITOR_FRAME)
        buf.set_pixel(x + w - 1, y + dy, MONITOR_FRAME)
    # Diagram: boxes connected by arrow
    box_y = y + 2
    # Box 1
    buf.fill_rect(x + 2, box_y, 4, 3, (220, 220, 220))
    for dx in range(4):
        buf.set_pixel(x + 2 + dx, box_y, MONITOR_TEXT_RED)
    # Arrow
    for dx in range(6, min(w - 4, 10)):
        buf.set_pixel(x + dx, box_y + 1, WARNING_RED)
    # Box 2 (red = error)
    if w > 12:
        buf.fill_rect(x + w - 6, box_y, 4, 3, WARNING_RED)
    # Error lines below
    for dy in range(box_y + 4, y + h - 1):
        line_len = ((dy + fi) * 3) % (w - 3) + 1
        for dx in range(1, min(1 + line_len, w - 1)):
            if (dx + fi) % 3 != 0:
                buf.set_pixel(x + dx, dy, MONITOR_TEXT_RED)


def _draw_error_monitor(buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int) -> None:
    """Fill monitor with error text."""
    for dy in range(2, mh - 2):
        for dx in range(2, mw - 2):
            if (dx + fi) % 4 == 0:
                buf.set_pixel(mx + dx, my + dy, MONITOR_TEXT_RED)
            elif (dx + dy + fi) % 6 == 0:
                buf.set_pixel(mx + dx, my + dy, WARNING_YELLOW)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(6, pixel_h * 7 // 20)
        floor_y = wall_h
        desk_y = floor_y + 2
        desk_w = min(14, width // 5)

        # Whiteboard on wall
        wb_w = min(16, width // 4)
        wb_h = min(10, wall_h - 3)
        wb_x = width // 3
        if wb_w >= 8 and wb_h >= 6 and width >= 45:
            _draw_whiteboard(buf, wb_x, 1, wb_w, wb_h, fi)

        # Agent 1 pointing at whiteboard
        if width >= 45:
            pointer = STANDING_POINTING[fi % len(STANDING_POINTING)]
            agent_y = floor_y - pointer.height + 4
            buf.draw_sprite(pointer, wb_x - 4 if wb_w >= 8 else 10, agent_y)

        # Agent 2 examining monitor
        if width >= 40:
            examiner = STANDING_EXAMINING[fi % len(STANDING_EXAMINING)]
            agent_y = desk_y - examiner.height + 1
            buf.draw_sprite(examiner, 5, agent_y)
            _draw_error_monitor(buf, 5, desk_y - 10, min(10, desk_w - 2), 8, fi)

        # Warning triangle (blinks)
        if width >= 50 and fi % 3 != 2:
            buf.draw_sprite(_WARNING, width // 2, 0)

        # Server LEDs go red
        if width >= 50:
            rack_x = width - 10
            rack_h = min(12, pixel_h - floor_y - 2)
            rack_y = floor_y - rack_h + 2
            for row in range(1, rack_h - 1, 2):
                led = LED_RED if (fi + row) % 2 == 0 else LED_OFF
                buf.set_pixel(rack_x + 1, rack_y + row, led)
                buf.set_pixel(rack_x + 4, rack_y + row, led)

        # Apply selective red tint
        _selective_red_tint(buf)

        frames.append(buf)
    return frames
