"""Isometric 2.5D office renderer for ClaudeLab.

Renders the office from an elevated diagonal camera angle, giving
a SimCity / Habbo Hotel style 3D appearance.  Floor tiles are diamonds,
walls recede at an angle, and objects are depth-sorted so closer items
draw over farther ones.

Coordinate system:
- World grid: (gx, gy) where gx goes right, gy goes "into" the screen
- Screen: iso_to_screen() maps grid → pixel coords
- Camera looks from front-left toward back-right
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
    SKY_DAY, SKY_DAWN, SKY_DUSK, SKY_NIGHT,
    BG_BLACK, BG_DARK,
    CHAIR_DARK, CHAIR_HIGHLIGHT, CHAIR_SHADOW,
    BASEBOARD, BASEBOARD_DARK,
    KEYBOARD_DARK, KEYBOARD_KEY,
    GLOWSTONE, GLASS_PANE,
    COBBLESTONE,
    COFFEE_BROWN,
)
from claudelab.pixelbuffer import PixelBuffer

# ---------------------------------------------------------------------------
# Isometric math
# ---------------------------------------------------------------------------

# Tile size in pixels (2:1 ratio is standard isometric)
TILE_W = 16   # width of diamond
TILE_H = 8    # height of diamond (half of width)


def iso_to_screen(
    gx: float, gy: float, origin_x: int, origin_y: int,
) -> tuple[int, int]:
    """Convert grid coordinates to screen pixel coordinates.

    The isometric projection maps:
      screen_x = (gx - gy) * TILE_W/2 + origin_x
      screen_y = (gx + gy) * TILE_H/2 + origin_y
    """
    sx = int((gx - gy) * TILE_W // 2 + origin_x)
    sy = int((gx + gy) * TILE_H // 2 + origin_y)
    return sx, sy


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def _draw_iso_diamond(
    buf: PixelBuffer, cx: int, cy: int,
    color: tuple[int, int, int],
    highlight: tuple[int, int, int] | None = None,
    shadow: tuple[int, int, int] | None = None,
) -> None:
    """Draw a filled isometric diamond (floor tile) centered at (cx, cy).

    Diamond spans TILE_W wide, TILE_H tall with the point at top.
    Left half gets highlight, right half gets shadow for 3D shading.
    """
    hw = TILE_W // 2
    hh = TILE_H // 2

    for dy in range(TILE_H):
        if dy < hh:
            # Top half: expanding
            span = (dy + 1) * hw // hh
        else:
            # Bottom half: contracting
            span = (TILE_H - dy) * hw // hh

        for dx in range(-span + 1, span):
            px = cx + dx
            py = cy - hh + dy
            if dx < 0 and highlight:
                c = highlight
            elif dx > 0 and shadow:
                c = shadow
            else:
                c = color
            buf.set_pixel(px, py, c)


def _draw_iso_block(
    buf: PixelBuffer, cx: int, cy: int, block_h: int,
    top_color: tuple[int, int, int],
    left_color: tuple[int, int, int],
    right_color: tuple[int, int, int],
) -> None:
    """Draw an isometric block (cube) with top face and two side faces.

    cx, cy is the center of the top diamond face.
    block_h is the height in pixels of the side faces.
    """
    hw = TILE_W // 2
    hh = TILE_H // 2

    # Draw top diamond
    _draw_iso_diamond(buf, cx, cy, top_color)

    # Draw left face (shaded)
    for dy in range(block_h):
        y_base = cy + hh + dy
        # Left face follows the left edge of the diamond downward
        for row_dy in range(hh):
            span_at = (hh - row_dy) * hw // hh
            px_start = cx - span_at + 1
            px_end = cx
            y = y_base - row_dy
            # Only draw the left-most column line at each depth
            pass

    # Simpler approach: draw the two visible side faces as filled polygons
    # Left face: from bottom-left of diamond going down
    for dy in range(block_h):
        # At each vertical step, the left face spans from
        # the left edge to the center bottom
        for row in range(hh):
            span = (row + 1) * hw // hh
            y = cy + hh + dy - row
            if row == 0:
                # Bottom edge of diamond at this depth
                for dx in range(-span + 1, 1):
                    buf.set_pixel(cx + dx, y, left_color)
            elif row == hh - 1:
                pass  # Already drawn by diamond

    # Actually let's use a cleaner approach for the side faces
    # Left face: trapezoid from bottom-left diamond edge going straight down
    for dy in range(1, block_h + 1):
        for half_row in range(hh):
            span = (hh - half_row) * hw // hh
            y = cy + half_row + dy
            x_left = cx - span + 1
            x_right = cx
            for x in range(x_left, x_right + 1):
                buf.set_pixel(x, y, left_color)

    # Right face: trapezoid from bottom-right diamond edge going down
    for dy in range(1, block_h + 1):
        for half_row in range(hh):
            span = (hh - half_row) * hw // hh
            y = cy + half_row + dy
            x_left = cx
            x_right = cx + span - 1
            for x in range(x_left, x_right + 1):
                buf.set_pixel(x, y, right_color)


def _draw_iso_wall_segment(
    buf: PixelBuffer,
    x1: int, y1: int, x2: int, y2: int,
    wall_h: int,
    face_color: tuple[int, int, int],
    shade_color: tuple[int, int, int],
) -> None:
    """Draw a wall between two isometric floor points.

    Draws a filled quadrilateral from (x1,y1)-(x2,y2) going up wall_h pixels.
    """
    # Sort by x
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    dx = x2 - x1
    dy = y2 - y1

    for step in range(max(1, abs(dx) + 1)):
        t = step / max(1, abs(dx)) if dx != 0 else 0
        x = x1 + int(t * dx)
        y = int(y1 + t * dy)
        # Draw vertical line from y up wall_h pixels
        for h in range(wall_h):
            # Gradient: darker at top
            frac = h / max(1, wall_h - 1)
            if frac < 0.3:
                c = shade_color
            else:
                c = face_color
            buf.set_pixel(x, y - h, c)


# ---------------------------------------------------------------------------
# Room geometry
# ---------------------------------------------------------------------------

def _get_sky_color() -> tuple[int, int, int]:
    hour = datetime.datetime.now().hour
    if 6 <= hour < 8:
        return SKY_DAWN
    elif 8 <= hour < 18:
        return SKY_DAY
    elif 18 <= hour < 21:
        return SKY_DUSK
    else:
        return SKY_NIGHT


def _draw_floor(
    buf: PixelBuffer,
    grid_w: int, grid_d: int,
    origin_x: int, origin_y: int,
) -> None:
    """Draw isometric floor tiles."""
    for gy in range(grid_d):
        for gx in range(grid_w):
            cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

            # Checkerboard pattern with wood tones
            if (gx + gy) % 2 == 0:
                _draw_iso_diamond(buf, cx, cy, OAK_PLANK,
                                  OAK_PLANK_LIGHT, OAK_PLANK_DARK)
            else:
                _draw_iso_diamond(buf, cx, cy, OAK_PLANK_DARK,
                                  OAK_PLANK, OAK_LOG)


def _draw_back_wall(
    buf: PixelBuffer,
    grid_w: int, grid_d: int,
    origin_x: int, origin_y: int,
    wall_h: int,
) -> None:
    """Draw the back wall (runs along gy=0, from gx=0 to gx=grid_w)."""
    for gx in range(grid_w):
        x1, y1 = iso_to_screen(gx, 0, origin_x, origin_y)
        x2, y2 = iso_to_screen(gx + 1, 0, origin_x, origin_y)

        # Fill wall face
        dx = x2 - x1
        for step in range(max(1, dx)):
            t = step / max(1, dx)
            x = x1 + step
            y = int(y1 + t * (y2 - y1))
            for h in range(wall_h):
                frac = h / max(1, wall_h - 1)
                # Brick pattern
                bx = (x + (3 if ((y - h) // 3) % 2 else 0)) % 6
                by = (y - h) % 3
                if bx == 0 or by == 0:
                    c = STONE_DARK
                elif frac > 0.7:
                    c = STONE_LIGHT
                elif frac > 0.3:
                    c = STONE
                else:
                    c = STONE_DARK
                buf.set_pixel(x, y - h, c)

        # Top edge highlight
        for step in range(max(1, dx)):
            x = x1 + step
            t = step / max(1, dx)
            y = int(y1 + t * (y2 - y1))
            buf.set_pixel(x, y - wall_h, STONE_HIGHLIGHT)


def _draw_left_wall(
    buf: PixelBuffer,
    grid_d: int,
    origin_x: int, origin_y: int,
    wall_h: int,
) -> None:
    """Draw the left wall (runs along gx=0, from gy=0 to gy=grid_d)."""
    for gy in range(grid_d):
        x1, y1 = iso_to_screen(0, gy, origin_x, origin_y)
        x2, y2 = iso_to_screen(0, gy + 1, origin_x, origin_y)

        dx = x2 - x1
        steps = max(1, abs(dx))
        for step in range(steps):
            t = step / max(1, steps)
            x = int(x1 + t * dx)
            y = int(y1 + t * (y2 - y1))
            for h in range(wall_h):
                frac = h / max(1, wall_h - 1)
                # Left wall is darker (shadow side)
                bx = (x + (3 if ((y - h) // 3) % 2 else 0)) % 6
                by = (y - h) % 3
                if bx == 0 or by == 0:
                    c = COBBLESTONE
                elif frac > 0.7:
                    c = STONE
                elif frac > 0.3:
                    c = STONE_DARK
                else:
                    c = COBBLESTONE
                buf.set_pixel(x, y - h, c)


# ---------------------------------------------------------------------------
# Isometric furniture
# ---------------------------------------------------------------------------

def _draw_iso_desk(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
) -> None:
    """Draw an isometric desk at grid position (gx, gy)."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    # Desk surface: a slightly elevated diamond
    desk_h = 6  # pixels above ground
    top_y = cy - desk_h

    # Surface (stretched diamond, 1.5 tiles wide)
    hw = int(TILE_W * 0.7)
    hh = TILE_H // 2

    # Draw desk top surface
    for dy in range(TILE_H):
        if dy < hh:
            span = (dy + 1) * hw // hh
        else:
            span = (TILE_H - dy) * hw // hh
        for dx in range(-span + 1, span):
            px = cx + dx
            py = top_y - hh + dy
            if dx < 0:
                c = OAK_PLANK_LIGHT
            elif dx > 0:
                c = OAK_PLANK_DARK
            else:
                c = OAK_PLANK
            buf.set_pixel(px, py, c)

    # Front edge thickness (2px)
    for dy in range(1, 3):
        for half_row in range(hh):
            span = (hh - half_row) * hw // hh
            y = top_y + half_row + dy
            # Right face of desk edge
            for dx in range(0, span):
                buf.set_pixel(cx + dx, y, OAK_PLANK_DARK)
            # Left face
            for dx in range(-span + 1, 1):
                buf.set_pixel(cx + dx, y, OAK_PLANK)

    # Legs (4 thin lines at corners)
    leg_positions = [
        (-hw + 2, -hh + 1),  # back-left
        (hw - 2, -hh + 1),   # back-right
        (-hw + 3, hh - 1),   # front-left
        (hw - 3, hh - 1),    # front-right
    ]
    for lx, ly in leg_positions:
        leg_x = cx + lx
        leg_y = top_y + ly
        for h in range(desk_h - 2):
            buf.set_pixel(leg_x, leg_y + 2 + h, OAK_LOG)


def _draw_iso_monitor(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    desk_h: int = 6,
) -> tuple[int, int, int, int]:
    """Draw an isometric monitor on a desk. Returns screen rect (x, y, w, h) for content."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    base_y = cy - desk_h

    # Monitor is a rectangle facing the viewer (billboard style)
    mon_w = 12
    mon_h = 9
    mx = cx - mon_w // 2
    my = base_y - mon_h - 2  # above desk surface

    # Stand
    buf.set_pixel(cx, base_y - 2, IRON_DARK)
    buf.set_pixel(cx, base_y - 1, IRON_DARK)
    buf.set_pixel(cx - 1, base_y, IRON_DARK)
    buf.set_pixel(cx, base_y, IRON_DARK)
    buf.set_pixel(cx + 1, base_y, IRON_DARK)

    # Frame
    buf.fill_rect(mx, my, mon_w, mon_h, MONITOR_FRAME)
    # Screen glow border
    buf.fill_rect(mx + 1, my + 1, mon_w - 2, mon_h - 2, MONITOR_GLOW)
    # Screen interior
    buf.fill_rect(mx + 2, my + 2, mon_w - 4, mon_h - 4, MONITOR_BG)
    # Power LED
    buf.set_pixel(mx + mon_w - 2, my + mon_h - 1, LED_GREEN)

    return (mx + 2, my + 2, mon_w - 4, mon_h - 4)


def _draw_iso_chair(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
) -> None:
    """Draw an isometric office chair."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    # Seat (small diamond, 2px above floor)
    seat_y = cy - 3
    seat_hw = 4
    seat_hh = 2
    for dy in range(4):
        if dy < seat_hh:
            span = (dy + 1) * seat_hw // seat_hh
        else:
            span = (4 - dy) * seat_hw // seat_hh
        for dx in range(-span + 1, span):
            c = CHAIR_HIGHLIGHT if dx < 0 else CHAIR_DARK
            buf.set_pixel(cx + dx, seat_y - seat_hh + dy, c)

    # Back rest (vertical rectangle behind seat)
    back_x = cx - 2
    back_y = seat_y - seat_hh - 4
    buf.fill_rect(back_x, back_y, 3, 4, CHAIR_DARK)
    buf.set_pixel(back_x, back_y, CHAIR_HIGHLIGHT)

    # Center post
    buf.set_pixel(cx, cy - 1, CHAIR_SHADOW)
    # Wheel base
    buf.set_pixel(cx - 2, cy, CHAIR_SHADOW)
    buf.set_pixel(cx, cy, CHAIR_SHADOW)
    buf.set_pixel(cx + 2, cy, CHAIR_SHADOW)


def _draw_iso_server_rack(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    fi: int,
) -> None:
    """Draw an isometric server rack."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    rack_w = 8
    rack_h = 16
    rx = cx - rack_w // 2
    ry = cy - rack_h

    # Main body
    buf.fill_rect(rx, ry, rack_w, rack_h, IRON_DARK)

    # Server units
    for row in range(1, rack_h - 1, 2):
        buf.fill_rect(rx + 1, ry + row, rack_w - 2, 1, IRON_BLOCK)
        # LEDs
        led1 = (fi + row) % 4
        led2 = (fi + row + 2) % 4
        colors = [LED_GREEN, LED_AMBER, LED_GREEN, LED_OFF]
        buf.set_pixel(rx + 1, ry + row, colors[led1])
        buf.set_pixel(rx + rack_w - 2, ry + row, colors[led2])

    # Top highlight
    for dx in range(rack_w):
        buf.set_pixel(rx + dx, ry, STONE_HIGHLIGHT)


def _draw_iso_plant(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    fi: int,
) -> None:
    """Draw a potted plant in isometric view."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    # Pot
    buf.fill_rect(cx - 2, cy - 3, 5, 3, POT_TERRACOTTA)
    buf.set_pixel(cx - 2, cy - 3, (160, 85, 50))  # shadow

    # Stem
    buf.set_pixel(cx, cy - 4, LEAF_DARK)
    buf.set_pixel(cx, cy - 5, LEAF_DARK)
    buf.set_pixel(cx, cy - 6, LEAF_DARK)

    # Leaves (sway)
    sway = 1 if fi % 8 < 4 else 0
    buf.set_pixel(cx - 1 + sway, cy - 7, LEAF_LIGHT)
    buf.set_pixel(cx + sway, cy - 7, LEAF_GREEN)
    buf.set_pixel(cx + 1, cy - 7, LEAF_GREEN)
    buf.set_pixel(cx - 2 + sway, cy - 6, LEAF_GREEN)
    buf.set_pixel(cx + 2, cy - 6, LEAF_DARK)
    buf.set_pixel(cx - 1, cy - 5, LEAF_GREEN)
    buf.set_pixel(cx + 1, cy - 5, LEAF_DARK)


# ---------------------------------------------------------------------------
# Character positioning
# ---------------------------------------------------------------------------

def iso_agent_pos(
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    sprite_h: int,
) -> tuple[int, int]:
    """Calculate screen position for a character sprite at grid (gx, gy).

    Returns (screen_x, screen_y) for the top-left of the sprite.
    The sprite's feet will be roughly at the grid position.
    """
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    # Center horizontally, feet at cy
    return cx - 8, cy - sprite_h  # 8 = half of 16px sprite width


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_iso_office(
    width: int,
    pixel_height: int,
    frame_idx: int = 0,
) -> tuple[PixelBuffer, dict]:
    """Build the isometric office as a PixelBuffer.

    Returns (buffer, layout) where layout contains computed positions
    for scene code to place agents and overlays.
    """
    buf = PixelBuffer(width, pixel_height, BG_DARK)

    # Grid dimensions (tiles)
    grid_w = 6   # tiles going right
    grid_d = 5   # tiles going into screen

    # Calculate origin so the floor is centered and fills the screen
    # The floor diamond's bounding box:
    # - leftmost point: iso(0, grid_d) → x = -grid_d * TW/2
    # - rightmost point: iso(grid_w, 0) → x = grid_w * TW/2
    # - topmost point: iso(0, 0) → y = 0
    # - bottommost point: iso(grid_w, grid_d) → y = (grid_w+grid_d) * TH/2
    floor_pixel_w = (grid_w + grid_d) * TILE_W // 2
    floor_pixel_h = (grid_w + grid_d) * TILE_H // 2

    origin_x = width // 2 + (grid_d - grid_w) * TILE_W // 4
    # Position floor so there's room for walls above and floor fills lower area
    wall_pixel_h = min(pixel_height // 3, 30)
    origin_y = wall_pixel_h + 4

    # Draw walls first (behind everything)
    _draw_back_wall(buf, grid_w, grid_d, origin_x, origin_y, wall_pixel_h)
    _draw_left_wall(buf, grid_d, origin_x, origin_y, wall_pixel_h)

    # Draw floor
    _draw_floor(buf, grid_w, grid_d, origin_x, origin_y)

    # Furniture positions (in grid coords)
    # Desk 1: near back-left
    desk1_gx, desk1_gy = 1.0, 1.0
    _draw_iso_desk(buf, desk1_gx, desk1_gy, origin_x, origin_y)
    mon1_rect = _draw_iso_monitor(buf, desk1_gx, desk1_gy, origin_x, origin_y)

    # Chair 1: in front of desk 1
    _draw_iso_chair(buf, desk1_gx, desk1_gy + 1.2, origin_x, origin_y)

    # Desk 2: near back-right
    desk2_gx, desk2_gy = 3.0, 1.0
    if width >= 60:
        _draw_iso_desk(buf, desk2_gx, desk2_gy, origin_x, origin_y)
        mon2_rect = _draw_iso_monitor(buf, desk2_gx, desk2_gy, origin_x, origin_y)
        _draw_iso_chair(buf, desk2_gx, desk2_gy + 1.2, origin_x, origin_y)
    else:
        mon2_rect = (0, 0, 0, 0)

    # Server rack (back-right corner)
    if width >= 50:
        _draw_iso_server_rack(buf, grid_w - 1.5, 0.5, origin_x, origin_y, frame_idx)

    # Plant (front-left)
    _draw_iso_plant(buf, 0.0, grid_d - 1.5, origin_x, origin_y, frame_idx)

    # Build layout info for scenes to use
    layout = {
        "origin_x": origin_x,
        "origin_y": origin_y,
        "grid_w": grid_w,
        "grid_d": grid_d,
        "wall_h": wall_pixel_h,
        "desk1_gx": desk1_gx,
        "desk1_gy": desk1_gy,
        "desk2_gx": desk2_gx,
        "desk2_gy": desk2_gy,
        "mon1_rect": mon1_rect,
        "mon2_rect": mon2_rect,
        # Agent positions (grid coords where agents should stand/sit)
        "agent1_gx": desk1_gx,
        "agent1_gy": desk1_gy + 0.8,
        "agent2_gx": desk2_gx,
        "agent2_gy": desk2_gy + 0.8,
    }

    return buf, layout
