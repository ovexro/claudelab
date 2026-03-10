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
    DESK_TOP, DESK_TOP_LIGHT, DESK_TOP_DARK, DESK_EDGE,
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
    COFFEE_MUG,
    BOOK_RED, BOOK_BLUE, BOOK_GREEN, BOOK_YELLOW,
    PAPER_WHITE, PAPER_SHADOW,
    CLOCK_FACE, CLOCK_HAND,
    STAR,
    BIRCH_PLANK,
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

    # Draw desk top surface — dark walnut to contrast with oak floor
    for dy in range(TILE_H):
        if dy < hh:
            span = (dy + 1) * hw // hh
        else:
            span = (TILE_H - dy) * hw // hh
        for dx in range(-span + 1, span):
            px = cx + dx
            py = top_y - hh + dy
            if dx < 0:
                c = DESK_TOP_LIGHT
            elif dx > 0:
                c = DESK_TOP_DARK
            else:
                c = DESK_TOP
            buf.set_pixel(px, py, c)

    # Front edge thickness (3px for more visibility)
    for dy in range(1, 4):
        for half_row in range(hh):
            span = (hh - half_row) * hw // hh
            y = top_y + half_row + dy
            # Right face of desk edge
            for dx in range(0, span):
                buf.set_pixel(cx + dx, y, DESK_TOP_DARK)
            # Left face
            for dx in range(-span + 1, 1):
                buf.set_pixel(cx + dx, y, DESK_EDGE)

    # Legs (4 thin lines at corners, 2px wide)
    leg_positions = [
        (-hw + 2, -hh + 1),  # back-left
        (hw - 2, -hh + 1),   # back-right
        (-hw + 3, hh - 1),   # front-left
        (hw - 3, hh - 1),    # front-right
    ]
    for lx, ly in leg_positions:
        leg_x = cx + lx
        leg_y = top_y + ly
        for h in range(desk_h - 1):
            buf.set_pixel(leg_x, leg_y + 2 + h, DESK_EDGE)
            buf.set_pixel(leg_x + 1, leg_y + 2 + h, DESK_TOP_DARK)


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
    mon_w = 18
    mon_h = 12
    mx = cx - mon_w // 2
    my = base_y - mon_h - 2  # above desk surface

    # Stand (wider base)
    buf.set_pixel(cx, base_y - 2, IRON_DARK)
    buf.set_pixel(cx, base_y - 1, IRON_DARK)
    for dx in range(-2, 3):
        buf.set_pixel(cx + dx, base_y, IRON_DARK)

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
    """Draw an isometric office chair — bigger and more visible."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    # Seat (wider diamond, 4px above floor)
    seat_y = cy - 4
    seat_hw = 6
    seat_hh = 3
    for dy in range(6):
        if dy < seat_hh:
            span = (dy + 1) * seat_hw // seat_hh
        else:
            span = (6 - dy) * seat_hw // seat_hh
        for dx in range(-span + 1, span):
            c = CHAIR_HIGHLIGHT if dx < 0 else CHAIR_DARK
            buf.set_pixel(cx + dx, seat_y - seat_hh + dy, c)

    # Back rest (wider, taller rectangle behind seat)
    back_x = cx - 3
    back_y = seat_y - seat_hh - 6
    buf.fill_rect(back_x, back_y, 5, 6, CHAIR_DARK)
    # Highlight left edge and top
    for dy in range(6):
        buf.set_pixel(back_x, back_y + dy, CHAIR_HIGHLIGHT)
    for dx in range(5):
        buf.set_pixel(back_x + dx, back_y, CHAIR_HIGHLIGHT)

    # Center post (2px wide)
    buf.set_pixel(cx, cy - 2, CHAIR_SHADOW)
    buf.set_pixel(cx, cy - 1, CHAIR_SHADOW)
    buf.set_pixel(cx + 1, cy - 2, CHAIR_SHADOW)
    buf.set_pixel(cx + 1, cy - 1, CHAIR_SHADOW)
    # Wheel base (wider star shape)
    for dx in [-3, -1, 0, 1, 3]:
        buf.set_pixel(cx + dx, cy, CHAIR_SHADOW)
    buf.set_pixel(cx - 2, cy + 1, CHAIR_SHADOW)
    buf.set_pixel(cx + 2, cy + 1, CHAIR_SHADOW)


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

    # Server units with staggered LED phases
    for row in range(1, rack_h - 1, 2):
        buf.fill_rect(rx + 1, ry + row, rack_w - 2, 1, IRON_BLOCK)
        # Staggered LEDs — each LED uses its own phase for more random patterns
        led1_phase = (fi * 3 + row * 7 + 0 * 13) % 5
        led2_phase = (fi * 3 + row * 7 + 1 * 13) % 5
        colors = [LED_GREEN, LED_AMBER, LED_GREEN, LED_OFF, LED_AMBER]
        buf.set_pixel(rx + 1, ry + row, colors[led1_phase])
        buf.set_pixel(rx + rack_w - 2, ry + row, colors[led2_phase])

    # Top highlight
    for dx in range(rack_w):
        buf.set_pixel(rx + dx, ry, STONE_HIGHLIGHT)


def _draw_iso_plant(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    fi: int,
) -> None:
    """Draw a larger potted plant in isometric view with smooth sway."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    # Pot (bigger — 7x5)
    buf.fill_rect(cx - 3, cy - 4, 7, 4, POT_TERRACOTTA)
    # Pot rim
    buf.fill_rect(cx - 4, cy - 5, 9, 1, POT_TERRACOTTA)
    # Pot shadow
    buf.set_pixel(cx - 3, cy - 4, (150, 80, 45))
    buf.set_pixel(cx - 3, cy - 3, (150, 80, 45))
    # Soil
    buf.fill_rect(cx - 2, cy - 5, 5, 1, (80, 55, 35))

    # Stem (taller)
    for dy in range(5):
        buf.set_pixel(cx, cy - 6 - dy, LEAF_DARK)
        buf.set_pixel(cx + 1, cy - 6 - dy, LEAF_DARK)

    # Leaves — 4 smooth sway positions using fi % 16
    phase = fi % 16
    if phase < 4:
        sway = 0
    elif phase < 8:
        sway = 1
    elif phase < 12:
        sway = 0
    else:
        sway = -1

    # Large leaf canopy (much bigger)
    leaf_base = cy - 11
    # Top row
    for dx in range(-1, 3):
        buf.set_pixel(cx + dx + sway, leaf_base - 3, LEAF_LIGHT)
    # Second row
    for dx in range(-2, 4):
        c = LEAF_LIGHT if dx < 1 else LEAF_GREEN
        buf.set_pixel(cx + dx + sway, leaf_base - 2, c)
    # Middle rows (widest)
    for dy in range(-1, 2):
        for dx in range(-3, 5):
            if dx < 0:
                c = LEAF_LIGHT
            elif dx > 2:
                c = LEAF_DARK
            else:
                c = LEAF_GREEN
            buf.set_pixel(cx + dx + sway, leaf_base + dy, c)
    # Bottom row
    for dx in range(-2, 4):
        c = LEAF_GREEN if dx < 2 else LEAF_DARK
        buf.set_pixel(cx + dx + sway, leaf_base + 2, c)


# ---------------------------------------------------------------------------
# New furniture
# ---------------------------------------------------------------------------

def _draw_window(
    buf: PixelBuffer,
    grid_w: int,
    origin_x: int, origin_y: int,
    wall_h: int,
) -> None:
    """Draw a rectangular window on the back wall showing sky color.

    Centered on the back wall, approximately 10x8 pixels.
    """
    sky = _get_sky_color()
    is_night = _get_sky_color() == SKY_NIGHT

    # Find center of back wall — use midpoint of gx range at gy=0
    mid_gx = grid_w / 2.0
    cx, cy = iso_to_screen(mid_gx, 0, origin_x, origin_y)
    # Window sits on the wall face, offset upward by ~60% of wall height
    win_w = 10
    win_h = 8
    wx = cx - win_w // 2
    wy = cy - int(wall_h * 0.7) - win_h // 2

    # Frame (glass pane border)
    buf.fill_rect(wx - 1, wy - 1, win_w + 2, win_h + 2, GLASS_PANE)
    # Sky interior
    buf.fill_rect(wx, wy, win_w, win_h, sky)

    # Window cross-bar (frame detail)
    for dx in range(win_w):
        buf.set_pixel(wx + dx, wy + win_h // 2, GLASS_PANE)
    for dy in range(win_h):
        buf.set_pixel(wx + win_w // 2, wy + dy, GLASS_PANE)

    # Night stars
    if is_night:
        buf.set_pixel(wx + 2, wy + 2, STAR)
        buf.set_pixel(wx + 7, wy + 1, STAR)


def _draw_bookcase(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
) -> None:
    """Draw a tall narrow bookcase against the left wall (6px wide, 12px tall)."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)

    bk_w = 6
    bk_h = 12
    bx = cx - bk_w // 2
    by = cy - bk_h

    # Main body (dark oak)
    buf.fill_rect(bx, by, bk_w, bk_h, OAK_LOG)

    # Shelves (horizontal lines) and books
    book_colors = [BOOK_RED, BOOK_BLUE, BOOK_GREEN, BOOK_YELLOW]
    for shelf_idx, shelf_y in enumerate(range(1, bk_h - 1, 3)):
        # Shelf plank
        for dx in range(bk_w):
            buf.set_pixel(bx + dx, by + shelf_y + 2, OAK_PLANK_DARK)
        # Book spines on this shelf (fill 2px tall rows above the shelf plank)
        for book_x in range(1, bk_w - 1):
            color = book_colors[(shelf_idx * 3 + book_x) % len(book_colors)]
            buf.set_pixel(bx + book_x, by + shelf_y, color)
            buf.set_pixel(bx + book_x, by + shelf_y + 1, color)

    # Top edge highlight
    for dx in range(bk_w):
        buf.set_pixel(bx + dx, by, OAK_PLANK_LIGHT)


def _draw_keyboard(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    desk_h: int = 6,
) -> None:
    """Draw a small keyboard on the desk surface (6x2 pixels)."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    # Keyboard sits on the desk surface, slightly in front of the monitor
    ky = cy - desk_h + 1
    kx = cx - 3

    # Keyboard body
    buf.fill_rect(kx, ky, 6, 2, KEYBOARD_DARK)
    # Key highlights (alternating pattern)
    for dx in range(0, 6, 2):
        buf.set_pixel(kx + dx, ky, KEYBOARD_KEY)
    for dx in range(1, 6, 2):
        buf.set_pixel(kx + dx, ky + 1, KEYBOARD_KEY)


def _draw_coffee_mug(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    desk_h: int = 6,
) -> None:
    """Draw a tiny 3x3 coffee mug on the desk surface."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    # Place mug to the right side of the desk
    mx = cx + 3
    my = cy - desk_h - 1

    # Mug body (3x3)
    buf.fill_rect(mx, my, 3, 3, COFFEE_MUG)
    # Coffee visible at top
    buf.set_pixel(mx, my, COFFEE_BROWN)
    buf.set_pixel(mx + 1, my, COFFEE_BROWN)
    buf.set_pixel(mx + 2, my, COFFEE_BROWN)


def _draw_wall_clock(
    buf: PixelBuffer,
    grid_w: int,
    origin_x: int, origin_y: int,
    wall_h: int,
) -> None:
    """Draw a 5x5 wall clock on the back wall, to the right of the window."""
    # Position: right side of back wall, ~75% along the width
    clock_gx = grid_w * 0.75
    cx, cy = iso_to_screen(clock_gx, 0, origin_x, origin_y)
    # Offset up into the wall
    clk_x = cx - 2
    clk_y = cy - int(wall_h * 0.65) - 2

    # Clock face (5x5 circle approximation — filled square with corner cutoffs)
    buf.fill_rect(clk_x, clk_y, 5, 5, CLOCK_FACE)
    # Cut corners for roundness
    buf.set_pixel(clk_x, clk_y, STONE)
    buf.set_pixel(clk_x + 4, clk_y, STONE)
    buf.set_pixel(clk_x, clk_y + 4, STONE)
    buf.set_pixel(clk_x + 4, clk_y + 4, STONE)

    # Border ring (overwrite edges with darker tone)
    for dx in range(1, 4):
        buf.set_pixel(clk_x + dx, clk_y, CLOCK_HAND)
        buf.set_pixel(clk_x + dx, clk_y + 4, CLOCK_HAND)
    for dy in range(1, 4):
        buf.set_pixel(clk_x, clk_y + dy, CLOCK_HAND)
        buf.set_pixel(clk_x + 4, clk_y + dy, CLOCK_HAND)

    # Center dot
    buf.set_pixel(clk_x + 2, clk_y + 2, CLOCK_HAND)
    # Hour hand (pointing up-right)
    buf.set_pixel(clk_x + 3, clk_y + 1, CLOCK_HAND)
    # Minute hand (pointing up)
    buf.set_pixel(clk_x + 2, clk_y + 1, CLOCK_HAND)


def _draw_paper_stack(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    desk_h: int = 6,
) -> None:
    """Draw a small stack of papers (4x3, slightly offset) on the desk."""
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    # Place papers to the left side of the desk
    px = cx - 5
    py = cy - desk_h - 1

    # Bottom sheet (slightly offset right)
    buf.fill_rect(px + 1, py + 1, 4, 3, PAPER_SHADOW)
    # Middle sheet (slightly offset)
    buf.fill_rect(px, py + 1, 4, 3, PAPER_SHADOW)
    # Top sheet
    buf.fill_rect(px, py, 4, 3, PAPER_WHITE)


def _draw_contact_shadow(
    buf: PixelBuffer,
    gx: float, gy: float,
    origin_x: int, origin_y: int,
    width: int = 4,
) -> None:
    """Draw a contact shadow under furniture by darkening existing floor pixels.

    Draws a small dark oval (2px tall) at the object's base position.
    """
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    half_w = width // 2

    # Shadow is 1 row tall, subtle darkening
    span = half_w
    for dx in range(-span, span + 1):
        px = cx + dx
        py = cy
        r, g, b = buf.get_pixel(px, py)
        r = max(0, r - 12)
        g = max(0, g - 12)
        b = max(0, b - 12)
        buf.set_pixel(px, py, (r, g, b))


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
    The sprite's feet will be at the bottom of the tile diamond.
    """
    cx, cy = iso_to_screen(gx + 0.5, gy + 0.5, origin_x, origin_y)
    # Center horizontally, feet at the bottom of the diamond (cy + TILE_H//4)
    # This anchors the agent to the floor surface properly
    foot_y = cy + TILE_H // 4
    return cx - 8, foot_y - sprite_h  # 8 = half of 16px sprite width


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------

def build_iso_office(
    width: int,
    pixel_height: int,
    frame_idx: int = 0,
) -> tuple[PixelBuffer, dict]:
    """Build the isometric office as a PixelBuffer.

    Dynamically scales the grid to fill the terminal. The isometric floor
    diamond is sized to span the full width, with walls filling the space
    above.

    Returns (buffer, layout) where layout contains computed positions
    for scene code to place agents and overlays.
    """
    buf = PixelBuffer(width, pixel_height, BG_DARK)

    # -------------------------------------------------------------------
    # Dynamic grid sizing: fill the screen
    # -------------------------------------------------------------------
    # The iso floor diamond bounding box for grid_w × grid_d:
    #   pixel_width  = (grid_w + grid_d) * TILE_W / 2
    #   pixel_height = (grid_w + grid_d) * TILE_H / 2
    # We want the floor to span the full terminal width.
    # Reserve ~30-35% of height for walls above the floor.
    wall_frac = 0.30
    floor_budget_h = int(pixel_height * (1.0 - wall_frac))

    # Total tiles (grid_w + grid_d) to fill width:
    total_tiles_for_width = (width * 2) // TILE_W
    # Total tiles to fill floor height budget:
    total_tiles_for_height = (floor_budget_h * 2) // TILE_H

    # Use the smaller to ensure it fits both dimensions
    total_tiles = min(total_tiles_for_width, total_tiles_for_height)
    total_tiles = max(total_tiles, 4)  # absolute minimum

    # Split roughly 55/45 between width and depth (wider than deep)
    grid_w = max(2, int(total_tiles * 0.55))
    grid_d = max(2, total_tiles - grid_w)
    # Clamp so the diamond fits the screen
    while (grid_w + grid_d) * TILE_W // 2 > width and grid_w + grid_d > 3:
        if grid_w > grid_d:
            grid_w -= 1
        else:
            grid_d -= 1

    # Floor diamond bounding box
    floor_pixel_w = (grid_w + grid_d) * TILE_W // 2
    floor_pixel_h = (grid_w + grid_d) * TILE_H // 2

    # Wall height: fill space above the floor
    wall_pixel_h = max(8, pixel_height - floor_pixel_h - 2)

    # Origin: the iso(0,0) point. Position so floor diamond is centered
    # horizontally and the bottom of the diamond reaches near the bottom.
    # Leftmost floor point: iso(0, grid_d) → x = origin_x - grid_d * TW/2
    # Rightmost: iso(grid_w, 0) → x = origin_x + grid_w * TW/2
    # Center: origin_x + (grid_w - grid_d) * TW/4 = width/2
    origin_x = width // 2 - (grid_w - grid_d) * TILE_W // 4

    # Topmost floor point: iso(0,0) → y = origin_y
    # Bottommost: iso(grid_w, grid_d) → y = origin_y + floor_pixel_h
    # We want bottommost near pixel_height:
    origin_y = pixel_height - floor_pixel_h - 1

    # Draw walls first (behind everything)
    _draw_back_wall(buf, grid_w, grid_d, origin_x, origin_y, wall_pixel_h)
    _draw_left_wall(buf, grid_d, origin_x, origin_y, wall_pixel_h)

    # Window on back wall (drawn over the wall)
    _draw_window(buf, grid_w, origin_x, origin_y, wall_pixel_h)

    # Wall clock on back wall (to the right of window)
    _draw_wall_clock(buf, grid_w, origin_x, origin_y, wall_pixel_h)

    # Draw floor
    _draw_floor(buf, grid_w, grid_d, origin_x, origin_y)

    # -------------------------------------------------------------------
    # Contact shadows — drawn on floor before furniture
    # -------------------------------------------------------------------
    desk1_gx = 1.0
    desk1_gy = 1.0
    desk2_gx = min(grid_w - 2.0, max(3.0, grid_w * 0.5))
    desk2_gy = 1.0
    plant_gy = min(grid_d - 1.0, max(2.0, grid_d * 0.7))

    # Shadows under desks
    _draw_contact_shadow(buf, desk1_gx, desk1_gy, origin_x, origin_y, 5)
    if width >= 50:
        _draw_contact_shadow(buf, desk2_gx, desk2_gy, origin_x, origin_y, 5)
    # Shadow under chairs
    _draw_contact_shadow(buf, desk1_gx, desk1_gy + 1.2, origin_x, origin_y, 3)
    if width >= 50:
        _draw_contact_shadow(buf, desk2_gx, desk2_gy + 1.2, origin_x, origin_y, 3)
    # Shadow under server rack
    if width >= 50:
        _draw_contact_shadow(buf, grid_w - 1.5, 0.5, origin_x, origin_y, 4)
    # Shadow under plant
    _draw_contact_shadow(buf, 0.0, plant_gy, origin_x, origin_y, 2)
    # Shadow under bookcase
    _draw_contact_shadow(buf, 0.0, 2.0, origin_x, origin_y, 3)
    # Shadow under agent positions
    _draw_contact_shadow(buf, desk1_gx, desk1_gy + 0.8, origin_x, origin_y, 3)
    if width >= 50:
        _draw_contact_shadow(buf, desk2_gx, desk2_gy + 0.8, origin_x, origin_y, 3)

    # -------------------------------------------------------------------
    # Furniture — placed relative to grid, scales with room size
    # -------------------------------------------------------------------
    # Bookcase against left wall (behind desks, at grid position 0,2)
    _draw_bookcase(buf, 0.0, 2.0, origin_x, origin_y)

    # Desk 1: near back-left
    _draw_iso_desk(buf, desk1_gx, desk1_gy, origin_x, origin_y)
    mon1_rect = _draw_iso_monitor(buf, desk1_gx, desk1_gy, origin_x, origin_y)
    _draw_keyboard(buf, desk1_gx, desk1_gy, origin_x, origin_y)
    _draw_coffee_mug(buf, desk1_gx, desk1_gy, origin_x, origin_y)
    _draw_iso_chair(buf, desk1_gx, desk1_gy + 1.2, origin_x, origin_y)

    # Desk 2: offset to the right
    if width >= 50:
        _draw_iso_desk(buf, desk2_gx, desk2_gy, origin_x, origin_y)
        mon2_rect = _draw_iso_monitor(buf, desk2_gx, desk2_gy, origin_x, origin_y)
        _draw_keyboard(buf, desk2_gx, desk2_gy, origin_x, origin_y)
        _draw_paper_stack(buf, desk2_gx, desk2_gy, origin_x, origin_y)
        _draw_iso_chair(buf, desk2_gx, desk2_gy + 1.2, origin_x, origin_y)
    else:
        mon2_rect = (0, 0, 0, 0)

    # Server rack (back-right area)
    if width >= 50:
        _draw_iso_server_rack(
            buf, grid_w - 1.5, 0.5, origin_x, origin_y, frame_idx,
        )

    # Plant (front-left area)
    _draw_iso_plant(buf, 0.0, plant_gy, origin_x, origin_y, frame_idx)

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
        "agent1_gx": desk1_gx,
        "agent1_gy": desk1_gy + 0.8,
        "agent2_gx": desk2_gx,
        "agent2_gy": desk2_gy + 0.8,
    }

    return buf, layout
