"""Isometric debugging scene — red alerts, error traces, agents investigate."""

from __future__ import annotations

from claudelab.palette import (
    BIRCH_PLANK, MONITOR_TEXT_RED, MONITOR_BG,
    WARNING_RED, WARNING_YELLOW, MONITOR_FRAME,
    LED_RED, LED_OFF, OUTLINE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import STANDING_POINTING, STANDING_EXAMINING
from claudelab.iso_office import build_iso_office, iso_to_screen, iso_agent_pos

NUM_FRAMES = 8

_WARNING = Sprite.from_pixel_art([
    "....OYO.....",
    "...OYYYO....",
    "..OYYYYYO...",
    ".OYYYRYYYO..",
    "OYYYYYYYYY0.",
    "OOOOOOOOOOO.",
], {"Y": WARNING_YELLOW, "R": WARNING_RED, "O": OUTLINE, "0": OUTLINE, ".": None})


def _selective_red_tint(buf: PixelBuffer) -> None:
    """Subtle red tint — stronger on dark areas."""
    for y in range(buf.height):
        for x in range(buf.width):
            r, g, b = buf.pixels[y][x]
            if r + g + b < 200:
                r = min(255, r + 30)
                g = max(0, g - 15)
                b = max(0, b - 15)
            else:
                r = min(255, r + 12)
                g = max(0, g - 5)
                b = max(0, b - 5)
            buf.pixels[y][x] = (r, g, b)


def _draw_error_monitor(buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int) -> None:
    """Fill monitor with error text."""
    for dy in range(mh):
        for dx in range(mw):
            if (dx + fi) % 4 == 0:
                buf.set_pixel(mx + dx, my + dy, MONITOR_TEXT_RED)
            elif (dx + dy + fi) % 6 == 0:
                buf.set_pixel(mx + dx, my + dy, WARNING_YELLOW)


def _draw_whiteboard(buf: PixelBuffer, x: int, y: int, w: int, h: int, fi: int) -> None:
    """Draw whiteboard with error diagram on wall area."""
    buf.fill_rect(x, y, w, h, BIRCH_PLANK)
    # Frame
    for dx in range(w):
        buf.set_pixel(x + dx, y, MONITOR_FRAME)
        buf.set_pixel(x + dx, y + h - 1, MONITOR_FRAME)
    for dy in range(h):
        buf.set_pixel(x, y + dy, MONITOR_FRAME)
        buf.set_pixel(x + w - 1, y + dy, MONITOR_FRAME)
    # Diagram: boxes + arrow
    box_y = y + 2
    buf.fill_rect(x + 2, box_y, 3, 2, (220, 220, 220))
    for dx in range(5, min(w - 4, 9)):
        buf.set_pixel(x + dx, box_y + 1, WARNING_RED)
    if w > 10:
        buf.fill_rect(x + w - 5, box_y, 3, 2, WARNING_RED)
    # Error lines
    for dy in range(box_y + 3, y + h - 1):
        line_len = ((dy + fi) * 3) % (w - 3) + 1
        for dx in range(1, min(1 + line_len, w - 1)):
            if (dx + fi) % 3 != 0:
                buf.set_pixel(x + dx, dy, MONITOR_TEXT_RED)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf, layout = build_iso_office(width, pixel_h, fi)
        ox = layout["origin_x"]
        oy = layout["origin_y"]
        wall_h = layout["wall_h"]

        # Whiteboard on wall area (above the floor)
        wb_w = min(14, width // 5)
        wb_h = min(8, wall_h - 2)
        if wb_w >= 8 and wb_h >= 5:
            # Position on back wall area
            wb_x = ox - wb_w // 2
            wb_y = max(1, oy - wall_h + 2)
            _draw_whiteboard(buf, wb_x, wb_y, wb_w, wb_h, fi)

        # Agent 1 pointing (standing near whiteboard area)
        if width >= 40:
            pointer = STANDING_POINTING[fi % len(STANDING_POINTING)]
            ax, ay = iso_agent_pos(
                layout["desk1_gx"] - 0.5, layout["desk1_gy"] - 0.3,
                ox, oy, pointer.height,
            )
            buf.draw_sprite(pointer, ax, ay)

        # Agent 2 examining monitor with errors
        if width >= 60:
            examiner = STANDING_EXAMINING[fi % len(STANDING_EXAMINING)]
            ax2, ay2 = iso_agent_pos(
                layout["agent2_gx"], layout["agent2_gy"],
                ox, oy, examiner.height,
            )
            buf.draw_sprite(examiner, ax2, ay2)

            # Error text on monitor 2
            mx, my, mw, mh = layout["mon2_rect"]
            _draw_error_monitor(buf, mx, my, mw, mh, fi)

        # Error text on monitor 1
        mx1, my1, mw1, mh1 = layout["mon1_rect"]
        _draw_error_monitor(buf, mx1, my1, mw1, mh1, fi)

        # Warning triangle (blinks)
        if fi % 3 != 2:
            buf.draw_sprite(_WARNING, width // 2 - 5, 0)

        # Red tint
        _selective_red_tint(buf)

        frames.append(buf)
    return frames
