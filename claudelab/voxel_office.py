"""Voxel-style office background for ClaudeLab.

Builds a PixelBuffer containing the static office elements: stone walls,
wood floor, window with day/night sky, desks, monitors, server rack,
plant, and coffee machine.
"""

from __future__ import annotations

import datetime

from claudelab.palette import (
    STONE, STONE_DARK, STONE_LIGHT,
    OAK_PLANK, OAK_PLANK_DARK, OAK_LOG,
    IRON_BLOCK, IRON_DARK,
    MONITOR_BG, MONITOR_FRAME,
    LED_GREEN, LED_RED, LED_AMBER, LED_OFF,
    LEAF_GREEN, LEAF_DARK, POT_TERRACOTTA,
    COFFEE_BROWN, IRON_BLOCK as MACHINE_BODY,
    GLASS_PANE,
    SKY_DAY, SKY_DAWN, SKY_DUSK, SKY_NIGHT,
    SUN, MOON, STAR, CLOUD,
    BG_BLACK, CHAIR_DARK,
)
from claudelab.pixelbuffer import PixelBuffer


def _get_sky_color() -> tuple[int, int, int]:
    """Return the sky color based on current time of day."""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 8:
        return SKY_DAWN
    elif 8 <= hour < 18:
        return SKY_DAY
    elif 18 <= hour < 21:
        return SKY_DUSK
    else:
        return SKY_NIGHT


def _draw_wall(buf: PixelBuffer, wall_h: int) -> None:
    """Draw a stone brick wall pattern across the top of the buffer."""
    for y in range(wall_h):
        for x in range(buf.width):
            # Brick pattern: offset every other row by 2
            bx = (x + (2 if (y // 2) % 2 else 0)) % 4
            by = y % 2
            if bx == 0 or by == 0:
                buf.set_pixel(x, y, STONE_DARK)
            else:
                # Vary the stone slightly
                buf.set_pixel(x, y, STONE if (x + y) % 5 != 0 else STONE_LIGHT)


def _draw_floor(buf: PixelBuffer, floor_y: int) -> None:
    """Draw wood plank flooring from floor_y to buffer bottom."""
    for y in range(floor_y, buf.height):
        for x in range(buf.width):
            if y % 3 == 0:
                buf.set_pixel(x, y, OAK_PLANK_DARK)
            else:
                buf.set_pixel(x, y, OAK_PLANK)


def _draw_window(buf: PixelBuffer, x: int, y: int, w: int, h: int, frame_idx: int) -> None:
    """Draw a window with sky, optional sun/moon/stars."""
    sky = _get_sky_color()
    is_night = sky == SKY_NIGHT

    # Frame
    for dx in range(w):
        buf.set_pixel(x + dx, y, OAK_LOG)
        buf.set_pixel(x + dx, y + h - 1, OAK_LOG)
    for dy in range(h):
        buf.set_pixel(x, y + dy, OAK_LOG)
        buf.set_pixel(x + w - 1, y + dy, OAK_LOG)
    # Cross bar
    mid_x = x + w // 2
    mid_y = y + h // 2
    for dy in range(1, h - 1):
        buf.set_pixel(mid_x, y + dy, OAK_LOG)
    for dx in range(1, w - 1):
        buf.set_pixel(x + dx, mid_y, OAK_LOG)

    # Sky fill
    for dy in range(1, h - 1):
        for dx in range(1, w - 1):
            if dx != mid_x - x and dy != mid_y - y:
                buf.set_pixel(x + dx, y + dy, sky)

    if is_night:
        # Stars (deterministic from frame_idx so they twinkle)
        star_positions = [(2, 2), (5, 1), (3, 4), (7, 3), (9, 2)]
        for i, (sx, sy) in enumerate(star_positions):
            px = x + 1 + (sx % (w - 2))
            py = y + 1 + (sy % (h - 2))
            if (frame_idx + i) % 3 != 0:  # twinkle
                buf.set_pixel(px, py, STAR)
        # Moon
        buf.set_pixel(x + w - 3, y + 2, MOON)
        buf.set_pixel(x + w - 4, y + 2, MOON)
        buf.set_pixel(x + w - 3, y + 3, MOON)
    elif sky == SKY_DAY:
        # Sun
        buf.set_pixel(x + 2, y + 2, SUN)
        buf.set_pixel(x + 3, y + 2, SUN)
        buf.set_pixel(x + 2, y + 3, SUN)
        buf.set_pixel(x + 3, y + 3, SUN)
        # Cloud
        if w > 8:
            for dx in range(3):
                buf.set_pixel(x + w - 4 + dx, y + 2, CLOUD)
            buf.set_pixel(x + w - 5, y + 3, CLOUD)
            for dx in range(4):
                buf.set_pixel(x + w - 5 + dx, y + 3, CLOUD)


def _draw_desk(buf: PixelBuffer, x: int, y: int, w: int) -> None:
    """Draw a desk surface and legs."""
    # Surface (2 pixels tall)
    buf.fill_rect(x, y, w, 2, OAK_PLANK)
    # Legs
    for dy in range(2, 6):
        buf.set_pixel(x + 1, y + dy, OAK_LOG)
        buf.set_pixel(x + w - 2, y + dy, OAK_LOG)


def _draw_chair(buf: PixelBuffer, x: int, y: int) -> None:
    """Draw a small chair."""
    # Seat
    buf.fill_rect(x, y, 4, 1, CHAIR_DARK)
    # Back
    buf.fill_rect(x, y - 3, 1, 3, CHAIR_DARK)
    # Legs
    buf.set_pixel(x, y + 1, CHAIR_DARK)
    buf.set_pixel(x + 3, y + 1, CHAIR_DARK)


def _draw_monitor(buf: PixelBuffer, x: int, y: int, w: int = 8, h: int = 6) -> None:
    """Draw a monitor frame (content filled by scenes)."""
    # Frame
    buf.fill_rect(x, y, w, h, MONITOR_FRAME)
    # Screen interior
    buf.fill_rect(x + 1, y + 1, w - 2, h - 2, MONITOR_BG)
    # Stand
    buf.fill_rect(x + w // 2 - 1, y + h, 2, 1, IRON_DARK)
    buf.fill_rect(x + w // 2 - 2, y + h + 1, 4, 1, IRON_DARK)


def _draw_server_rack(buf: PixelBuffer, x: int, y: int, h: int, frame_idx: int) -> None:
    """Draw a server rack with blinking LEDs."""
    w = 4
    # Outer frame
    buf.fill_rect(x, y, w, h, IRON_DARK)
    # Server units
    for row in range(1, h - 1, 2):
        buf.fill_rect(x + 1, y + row, w - 2, 1, IRON_BLOCK)
        # LED (alternates based on frame and position)
        led_state = (frame_idx + row) % 4
        if led_state == 0:
            led_color = LED_GREEN
        elif led_state == 1:
            led_color = LED_AMBER
        elif led_state == 2:
            led_color = LED_GREEN
        else:
            led_color = LED_OFF
        buf.set_pixel(x + w - 2, y + row, led_color)


def _draw_plant(buf: PixelBuffer, x: int, y: int, frame_idx: int) -> None:
    """Draw a potted plant."""
    # Pot
    buf.fill_rect(x, y + 4, 4, 2, POT_TERRACOTTA)
    buf.set_pixel(x + 1, y + 4, POT_TERRACOTTA)
    # Stem
    buf.set_pixel(x + 2, y + 3, LEAF_DARK)
    buf.set_pixel(x + 2, y + 2, LEAF_DARK)
    # Leaves (slight sway based on frame)
    sway = 1 if frame_idx % 8 < 4 else 0
    buf.set_pixel(x + 1 + sway, y, LEAF_GREEN)
    buf.set_pixel(x + 2 + sway, y, LEAF_GREEN)
    buf.set_pixel(x + 3, y + 1, LEAF_GREEN)
    buf.set_pixel(x + sway, y + 1, LEAF_DARK)
    buf.set_pixel(x + 1, y + 2, LEAF_GREEN)
    buf.set_pixel(x + 3, y + 2, LEAF_GREEN)


def _draw_coffee_machine(buf: PixelBuffer, x: int, y: int) -> None:
    """Draw a small coffee machine."""
    buf.fill_rect(x, y, 3, 4, IRON_BLOCK)
    buf.set_pixel(x + 1, y + 1, COFFEE_BROWN)
    buf.set_pixel(x + 1, y + 2, COFFEE_BROWN)
    buf.set_pixel(x, y + 4, IRON_DARK)
    buf.set_pixel(x + 1, y + 4, IRON_DARK)
    buf.set_pixel(x + 2, y + 4, IRON_DARK)


def build_voxel_office(
    width: int,
    pixel_height: int,
    frame_idx: int = 0,
) -> PixelBuffer:
    """Build the office background as a PixelBuffer.

    Parameters
    ----------
    width: Terminal columns (= pixel width).
    pixel_height: Total pixel rows (= terminal scene rows * 2).
    frame_idx: Current animation frame (for LED blinks, plant sway, etc.).

    Returns a PixelBuffer with the static office elements drawn.
    """
    buf = PixelBuffer(width, pixel_height, BG_BLACK)

    # Layout proportions
    wall_h = max(4, pixel_height * 2 // 5)  # ~40% wall
    floor_y = wall_h

    _draw_wall(buf, wall_h)
    _draw_floor(buf, floor_y)

    # Window (upper right area of the wall)
    win_w = min(12, width // 5)
    win_h = min(8, wall_h - 2)
    if win_w >= 6 and win_h >= 4:
        win_x = width - win_w - 3
        win_y = 1
        _draw_window(buf, win_x, win_y, win_w, win_h, frame_idx)

    # Desks (on the floor)
    desk_y = floor_y + 2
    desk_w = min(10, width // 6)
    if width >= 40:
        _draw_desk(buf, 3, desk_y, desk_w)
        _draw_monitor(buf, 4, desk_y - 7, min(8, desk_w - 2), 6)
        _draw_chair(buf, 4, desk_y + 5)

    if width >= 60:
        desk2_x = width // 3 + 2
        _draw_desk(buf, desk2_x, desk_y, desk_w)
        _draw_monitor(buf, desk2_x + 1, desk_y - 7, min(8, desk_w - 2), 6)
        _draw_chair(buf, desk2_x + 1, desk_y + 5)

    # Server rack (right side, on floor)
    if width >= 50:
        rack_h = min(10, pixel_height - floor_y - 2)
        rack_x = width - 8
        rack_y = floor_y - rack_h + 2
        if rack_h >= 6:
            _draw_server_rack(buf, rack_x, rack_y, rack_h, frame_idx)

    # Plant (left corner on floor)
    if pixel_height - floor_y > 8:
        _draw_plant(buf, 1, floor_y + 1, frame_idx)

    # Coffee machine (near middle)
    if width >= 55:
        cm_x = width // 2 + 4
        cm_y = floor_y + 2
        _draw_coffee_machine(buf, cm_x, cm_y)

    return buf
