"""NES-quality office background for ClaudeLab voxel renderer.

Three visual layers: back wall with depth gradient, furniture mid-ground,
and wood plank floor with perspective seams.
"""

from __future__ import annotations

import datetime

from claudelab.palette import (
    STONE, STONE_DARK, STONE_LIGHT, STONE_HIGHLIGHT,
    OAK_PLANK, OAK_PLANK_DARK, OAK_PLANK_LIGHT, OAK_LOG,
    IRON_BLOCK, IRON_DARK,
    MONITOR_BG, MONITOR_FRAME, MONITOR_GLOW,
    LED_GREEN, LED_AMBER, LED_OFF,
    LEAF_GREEN, LEAF_DARK, LEAF_LIGHT, POT_TERRACOTTA,
    COFFEE_BROWN, IRON_BLOCK as MACHINE_BODY,
    GLASS_PANE,
    SKY_DAY, SKY_DAWN, SKY_DUSK, SKY_NIGHT,
    SUN, MOON, STAR, CLOUD,
    BG_BLACK, CHAIR_DARK, CHAIR_HIGHLIGHT, CHAIR_SHADOW,
    BASEBOARD, BASEBOARD_DARK,
    KEYBOARD_DARK, KEYBOARD_KEY,
    GLOWSTONE,
)
from claudelab.pixelbuffer import PixelBuffer


def _get_sky_color() -> tuple[int, int, int]:
    """Return sky color based on time of day."""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 8:
        return SKY_DAWN
    elif 8 <= hour < 18:
        return SKY_DAY
    elif 18 <= hour < 21:
        return SKY_DUSK
    else:
        return SKY_NIGHT


def _dither(x: int, y: int, ca: tuple, cb: tuple, t: float) -> tuple:
    """2x2 Bayer dither between two colors."""
    bayer = ((0, 2), (3, 1))
    return ca if bayer[y % 2][x % 2] / 4.0 < t else cb


def _draw_wall(buf: PixelBuffer, wall_h: int) -> None:
    """Draw stone wall with depth gradient and brick pattern."""
    for y in range(wall_h - 2):  # leave 2px for baseboard
        # Vertical gradient: darker at top (ceiling shadow), lighter middle
        if y < 2:
            base, mortar = STONE_DARK, (65, 65, 65)
        elif y < wall_h // 3:
            base, mortar = STONE, STONE_DARK
        else:
            base, mortar = STONE_LIGHT, STONE

        for x in range(buf.width):
            # Brick pattern with offset rows
            bx = (x + (3 if (y // 3) % 2 else 0)) % 6
            by = y % 3
            if bx == 0 or by == 0:
                buf.set_pixel(x, y, mortar)
            else:
                # Subtle variation
                if (x * 7 + y * 13) % 17 == 0:
                    buf.set_pixel(x, y, STONE_HIGHLIGHT)
                else:
                    buf.set_pixel(x, y, base)

    # Baseboard molding (2 pixels tall)
    bb_y = wall_h - 2
    for x in range(buf.width):
        buf.set_pixel(x, bb_y, BASEBOARD)
        buf.set_pixel(x, bb_y + 1, BASEBOARD_DARK)


def _draw_floor(buf: PixelBuffer, floor_y: int) -> None:
    """Draw wood floor with plank seams and depth gradient."""
    for y in range(floor_y, buf.height):
        dist = y - floor_y  # distance from wall
        for x in range(buf.width):
            # Plank pattern (3-tone repeating)
            plank_row = dist % 4
            if plank_row == 0:
                c = OAK_PLANK_DARK  # seam between planks
            elif plank_row == 1:
                c = OAK_PLANK_LIGHT if dist < 4 else OAK_PLANK
            else:
                c = OAK_PLANK

            # Vertical seams every 8 pixels (offset per row group)
            seam_offset = 4 if (dist // 4) % 2 else 0
            if (x + seam_offset) % 8 == 0:
                c = OAK_PLANK_DARK

            # Darken planks near wall (distance shadow)
            if dist < 2:
                c = OAK_PLANK_DARK

            buf.set_pixel(x, y, c)


def _draw_window(buf: PixelBuffer, x: int, y: int, w: int, h: int, fi: int) -> None:
    """Draw window with sky, sun/moon/stars, and frame."""
    sky = _get_sky_color()
    is_night = sky == SKY_NIGHT

    # Outer frame (oak)
    for dx in range(w):
        buf.set_pixel(x + dx, y, OAK_LOG)
        buf.set_pixel(x + dx, y + h - 1, OAK_LOG)
    for dy in range(h):
        buf.set_pixel(x, y + dy, OAK_LOG)
        buf.set_pixel(x + w - 1, y + dy, OAK_LOG)

    # Cross bars
    mid_x = x + w // 2
    mid_y = y + h // 2
    for dy in range(1, h - 1):
        buf.set_pixel(mid_x, y + dy, OAK_LOG)
    for dx in range(1, w - 1):
        buf.set_pixel(x + dx, mid_y, OAK_LOG)

    # Sky fill with subtle gradient
    for dy in range(1, h - 1):
        for dx in range(1, w - 1):
            if dx == mid_x - x or dy == mid_y - y:
                continue
            # Gradient: slightly lighter at top
            t = dy / max(1, h - 2)
            if is_night:
                shade = (max(10, 15 - int(t * 8)), max(10, 15 - int(t * 8)), max(30, 45 - int(t * 15)))
            else:
                shade = sky
            buf.set_pixel(x + dx, y + dy, shade)

    if is_night:
        # Stars
        stars = [(2, 2), (5, 1), (3, 4), (7, 3), (9, 2), (4, 1), (8, 4)]
        for i, (sx, sy) in enumerate(stars):
            px = x + 1 + (sx % max(1, w - 3))
            py = y + 1 + (sy % max(1, h - 3))
            if (fi + i) % 3 != 0:
                buf.set_pixel(px, py, STAR)
        # Moon
        if w > 6:
            buf.set_pixel(x + w - 3, y + 2, MOON)
            buf.set_pixel(x + w - 4, y + 2, MOON)
            buf.set_pixel(x + w - 3, y + 3, MOON)
            buf.set_pixel(x + w - 4, y + 3, (210, 210, 195))
    elif sky == SKY_DAY:
        # Sun (larger, with glow)
        for dy in range(3):
            for dx in range(3):
                buf.set_pixel(x + 2 + dx, y + 1 + dy, SUN)
        buf.set_pixel(x + 3, y + 1, (255, 245, 140))  # bright center
        # Cloud
        if w > 8:
            cloud_x = x + w - 6
            for dx in range(4):
                buf.set_pixel(cloud_x + dx, y + 3, CLOUD)
            for dx in range(5):
                buf.set_pixel(cloud_x - 1 + dx, y + 4, CLOUD)
            buf.set_pixel(cloud_x + 1, y + 2, CLOUD)
            buf.set_pixel(cloud_x + 2, y + 2, CLOUD)


def _draw_desk(buf: PixelBuffer, x: int, y: int, w: int) -> None:
    """Draw desk with thick surface, front panel, and legs."""
    # Surface (3 pixels thick with highlight on top edge)
    for dx in range(w):
        buf.set_pixel(x + dx, y, OAK_PLANK_LIGHT)  # top highlight
    buf.fill_rect(x, y + 1, w, 2, OAK_PLANK)
    # Front panel shadow
    for dx in range(w):
        buf.set_pixel(x + dx, y + 3, OAK_PLANK_DARK)
    # Legs
    for dy in range(4, 8):
        buf.set_pixel(x + 1, y + dy, OAK_LOG)
        buf.set_pixel(x + w - 2, y + dy, OAK_LOG)


def _draw_keyboard(buf: PixelBuffer, x: int, y: int) -> None:
    """Draw a small keyboard on desk surface."""
    buf.fill_rect(x, y, 8, 2, KEYBOARD_DARK)
    # Key highlights
    for dx in range(0, 8, 2):
        buf.set_pixel(x + dx, y, KEYBOARD_KEY)
    for dx in range(1, 7, 2):
        buf.set_pixel(x + dx, y + 1, KEYBOARD_KEY)


def _draw_chair(buf: PixelBuffer, x: int, y: int) -> None:
    """Draw office chair with back, seat, and legs."""
    # Back (tall, with highlight on left)
    buf.set_pixel(x, y - 4, CHAIR_HIGHLIGHT)
    buf.fill_rect(x, y - 3, 1, 3, CHAIR_DARK)
    buf.set_pixel(x, y, CHAIR_SHADOW)
    # Seat (5px wide)
    buf.set_pixel(x, y + 1, CHAIR_HIGHLIGHT)
    buf.fill_rect(x + 1, y + 1, 3, 1, CHAIR_DARK)
    buf.set_pixel(x + 4, y + 1, CHAIR_SHADOW)
    # Center post
    buf.set_pixel(x + 2, y + 2, CHAIR_SHADOW)
    # Wheel base
    buf.set_pixel(x, y + 3, CHAIR_SHADOW)
    buf.set_pixel(x + 2, y + 3, CHAIR_SHADOW)
    buf.set_pixel(x + 4, y + 3, CHAIR_SHADOW)


def _draw_monitor(buf: PixelBuffer, x: int, y: int, w: int = 10, h: int = 8) -> None:
    """Draw monitor with frame, screen glow, and stand."""
    # Frame
    buf.fill_rect(x, y, w, h, MONITOR_FRAME)
    # Screen glow (1px inside frame)
    buf.fill_rect(x + 1, y + 1, w - 2, h - 2, MONITOR_GLOW)
    # Screen interior
    buf.fill_rect(x + 2, y + 2, w - 4, h - 4, MONITOR_BG)
    # Power LED
    buf.set_pixel(x + w - 2, y + h - 1, (50, 255, 50))
    # Stand
    buf.fill_rect(x + w // 2 - 1, y + h, 2, 2, IRON_DARK)
    buf.fill_rect(x + w // 2 - 2, y + h + 2, 5, 1, IRON_DARK)


def _draw_server_rack(buf: PixelBuffer, x: int, y: int, h: int, fi: int) -> None:
    """Draw server rack with dual LED columns."""
    w = 6
    buf.fill_rect(x, y, w, h, IRON_DARK)
    for row in range(1, h - 1, 2):
        # Server unit
        buf.fill_rect(x + 1, y + row, w - 2, 1, IRON_BLOCK)
        # Ventilation pattern
        for dx in range(1, w - 1):
            if dx % 2 == 0:
                buf.set_pixel(x + dx, y + row, (180, 180, 185))
        # Dual LEDs
        led1 = (fi + row) % 4
        led2 = (fi + row + 2) % 4
        colors = [LED_GREEN, LED_AMBER, LED_GREEN, LED_OFF]
        buf.set_pixel(x + 1, y + row, colors[led1])
        buf.set_pixel(x + w - 2, y + row, colors[led2])


def _draw_plant(buf: PixelBuffer, x: int, y: int, fi: int) -> None:
    """Draw potted plant with leaves that sway."""
    # Pot (with shading)
    buf.fill_rect(x, y + 5, 5, 2, POT_TERRACOTTA)
    buf.set_pixel(x, y + 5, (160, 85, 50))      # shadow left
    buf.set_pixel(x + 4, y + 6, (160, 85, 50))   # shadow right
    # Stem
    buf.set_pixel(x + 2, y + 4, LEAF_DARK)
    buf.set_pixel(x + 2, y + 3, LEAF_DARK)
    buf.set_pixel(x + 2, y + 2, LEAF_DARK)
    # Leaves (sway with frame)
    sway = 1 if fi % 8 < 4 else 0
    # Top cluster
    buf.set_pixel(x + 1 + sway, y, LEAF_LIGHT)
    buf.set_pixel(x + 2 + sway, y, LEAF_GREEN)
    buf.set_pixel(x + 3, y, LEAF_GREEN)
    # Mid cluster
    buf.set_pixel(x + sway, y + 1, LEAF_GREEN)
    buf.set_pixel(x + 1, y + 1, LEAF_LIGHT)
    buf.set_pixel(x + 3, y + 1, LEAF_GREEN)
    buf.set_pixel(x + 4, y + 1, LEAF_DARK)
    # Lower
    buf.set_pixel(x + 1, y + 2, LEAF_GREEN)
    buf.set_pixel(x + 3, y + 2, LEAF_DARK)


def _draw_coffee_machine(buf: PixelBuffer, x: int, y: int) -> None:
    """Draw coffee machine with spout and drip tray."""
    # Body
    buf.fill_rect(x, y, 4, 5, IRON_BLOCK)
    buf.set_pixel(x, y, (220, 220, 225))  # highlight top-left
    buf.fill_rect(x + 3, y, 1, 5, IRON_DARK)  # shadow right
    # Coffee window
    buf.set_pixel(x + 1, y + 1, COFFEE_BROWN)
    buf.set_pixel(x + 2, y + 1, COFFEE_BROWN)
    buf.set_pixel(x + 1, y + 2, (90, 50, 20))
    buf.set_pixel(x + 2, y + 2, (90, 50, 20))
    # Spout
    buf.set_pixel(x + 1, y + 3, IRON_DARK)
    # Drip tray
    buf.fill_rect(x, y + 5, 4, 1, IRON_DARK)


def _draw_ceiling_light(buf: PixelBuffer, x: int, y: int, w: int) -> None:
    """Draw ceiling-mounted light fixture."""
    # Fixture body
    buf.fill_rect(x, y, w, 2, IRON_DARK)
    buf.fill_rect(x + 1, y + 1, w - 2, 1, GLOWSTONE)
    # Light cone (subtle brightening on wall below)
    for dy in range(2, 5):
        spread = dy - 1
        for dx in range(-spread, w + spread):
            px = x + dx
            py = y + dy
            if 0 <= px < buf.width and 0 <= py < buf.height:
                r, g, b = buf.pixels[py][px]
                r = min(255, r + 12)
                g = min(255, g + 10)
                b = min(255, b + 8)
                buf.pixels[py][px] = (r, g, b)


def build_voxel_office(
    width: int,
    pixel_height: int,
    frame_idx: int = 0,
) -> PixelBuffer:
    """Build the office background as a PixelBuffer."""
    buf = PixelBuffer(width, pixel_height, BG_BLACK)

    # Layout: ~35% wall (slightly less to accommodate taller sprites)
    wall_h = max(6, pixel_height * 7 // 20)
    floor_y = wall_h

    _draw_wall(buf, wall_h)
    _draw_floor(buf, floor_y)

    # Window (upper-right)
    win_w = min(14, width // 4)
    win_h = min(10, wall_h - 3)
    if win_w >= 8 and win_h >= 6:
        win_x = width - win_w - 3
        _draw_window(buf, win_x, 1, win_w, win_h, frame_idx)

    # Ceiling light
    if width >= 50 and wall_h >= 8:
        _draw_ceiling_light(buf, width // 3, 0, 8)

    # Desks
    desk_y = floor_y + 2
    desk_w = min(14, width // 5)
    if width >= 40:
        _draw_desk(buf, 3, desk_y, desk_w)
        _draw_monitor(buf, 5, desk_y - 10, min(10, desk_w - 2), 8)
        _draw_keyboard(buf, 5, desk_y - 1)
        _draw_chair(buf, 5, desk_y + 6)

    if width >= 60:
        desk2_x = width // 3 + 4
        _draw_desk(buf, desk2_x, desk_y, desk_w)
        _draw_monitor(buf, desk2_x + 2, desk_y - 10, min(10, desk_w - 2), 8)
        _draw_keyboard(buf, desk2_x + 2, desk_y - 1)
        _draw_chair(buf, desk2_x + 2, desk_y + 6)

    # Server rack (right side)
    if width >= 50:
        rack_h = min(12, pixel_height - floor_y - 2)
        rack_x = width - 10
        rack_y = floor_y - rack_h + 2
        if rack_h >= 8:
            _draw_server_rack(buf, rack_x, rack_y, rack_h, frame_idx)

    # Plant (left corner)
    if pixel_height - floor_y > 10:
        _draw_plant(buf, 1, floor_y + 1, frame_idx)

    # Coffee machine
    if width >= 55:
        cm_x = width // 2 + 6
        cm_y = floor_y + 2
        _draw_coffee_machine(buf, cm_x, cm_y)

    return buf
