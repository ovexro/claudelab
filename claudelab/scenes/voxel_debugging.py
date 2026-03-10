"""Voxel debugging scene — red tint, error on monitor, whiteboard."""

from __future__ import annotations

from claudelab.palette import (
    BIRCH_PLANK, MONITOR_TEXT_RED, MONITOR_BG,
    WARNING_RED, WARNING_YELLOW, MONITOR_FRAME,
    LED_RED, LED_OFF,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import STANDING_POINTING, STANDING_EXAMINING
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Warning triangle sprite
_WARNING = Sprite.from_pixel_art([
    "...Y...",
    "..YYY..",
    ".YYRYY.",
    "YYYYYYY",
], {"Y": WARNING_YELLOW, "R": WARNING_RED, ".": None})


def _red_tint(buf: PixelBuffer) -> None:
    """Apply a subtle red tint to the entire buffer."""
    for y in range(buf.height):
        for x in range(buf.width):
            r, g, b = buf.pixels[y][x]
            r = min(255, r + 25)
            g = max(0, g - 10)
            b = max(0, b - 10)
            buf.pixels[y][x] = (r, g, b)


def _draw_whiteboard(buf: PixelBuffer, x: int, y: int, w: int, h: int, fi: int) -> None:
    """Draw a whiteboard with error diagram."""
    buf.fill_rect(x, y, w, h, BIRCH_PLANK)
    # Frame
    for dx in range(w):
        buf.set_pixel(x + dx, y, MONITOR_FRAME)
        buf.set_pixel(x + dx, y + h - 1, MONITOR_FRAME)
    for dy in range(h):
        buf.set_pixel(x, y + dy, MONITOR_FRAME)
        buf.set_pixel(x + w - 1, y + dy, MONITOR_FRAME)

    # Diagram lines (vary by frame)
    line_y = y + 2
    for dx in range(1, w - 2):
        if (dx + fi) % 3 != 0:
            buf.set_pixel(x + dx, line_y, MONITOR_TEXT_RED)
    # Arrow
    if fi % 2 == 0:
        for dy in range(2):
            buf.set_pixel(x + w // 2, line_y + 1 + dy, WARNING_RED)


def _draw_error_monitor(buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int) -> None:
    """Draw error text on a monitor."""
    for dy in range(1, mh - 1):
        for dx in range(1, mw - 1):
            if (dx + fi) % 4 == 0:
                buf.set_pixel(mx + dx, my + dy, MONITOR_TEXT_RED)
            elif (dx + dy + fi) % 6 == 0:
                buf.set_pixel(mx + dx, my + dy, WARNING_YELLOW)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(4, pixel_h * 2 // 5)
        floor_y = wall_h
        desk_y = floor_y + 2
        desk_w = min(10, width // 6)

        # Whiteboard on wall
        wb_w = min(12, width // 5)
        wb_h = min(8, wall_h - 2)
        if wb_w >= 6 and wb_h >= 4 and width >= 45:
            wb_x = width // 3
            _draw_whiteboard(buf, wb_x, 1, wb_w, wb_h, fi)

        # Agent 1 pointing at whiteboard
        if width >= 45:
            pointer = STANDING_POINTING[fi % len(STANDING_POINTING)]
            agent_y = floor_y - pointer.height + 4
            buf.draw_sprite(pointer, wb_x - 2 if wb_w >= 6 else 10, agent_y)

        # Agent 2 examining monitor
        if width >= 40:
            examiner = STANDING_EXAMINING[fi % len(STANDING_EXAMINING)]
            agent_y = desk_y - examiner.height + 1
            buf.draw_sprite(examiner, 5, agent_y)
            # Error on monitor
            _draw_error_monitor(buf, 4, desk_y - 7, min(8, desk_w - 2), 6, fi)

        # Warning triangle (blinks)
        if width >= 50 and fi % 3 != 2:
            buf.draw_sprite(_WARNING, width // 2, 1)

        # Server LEDs go red
        if width >= 50:
            rack_x = width - 8
            rack_h = min(10, pixel_h - floor_y - 2)
            rack_y = floor_y - rack_h + 2
            for row in range(1, rack_h - 1, 2):
                led = LED_RED if (fi + row) % 2 == 0 else LED_OFF
                buf.set_pixel(rack_x + 2, rack_y + row, led)

        # Apply red tint
        _red_tint(buf)

        frames.append(buf)
    return frames
