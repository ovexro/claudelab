"""Isometric running scene — control panel, gear, progress bar, logs."""

from __future__ import annotations

from claudelab.palette import (
    GEAR_PURPLE, GEAR_DARK, GEAR_LIGHT,
    IRON_BLOCK, IRON_DARK,
    PROGRESS_GREEN, PROGRESS_BG, PROGRESS_FRAME,
    LED_GREEN, LED_AMBER, LED_OFF,
    MONITOR_TEXT_GREEN, MONITOR_TEXT_WHITE, MONITOR_BG,
    OUTLINE,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import BUTTON_PUSH
from claudelab.iso_office import build_iso_office, iso_to_screen, iso_agent_pos

NUM_FRAMES = 8

_GEAR_MAP = {"G": GEAR_PURPLE, "g": GEAR_DARK, "L": GEAR_LIGHT, "O": OUTLINE, ".": None}
_GEAR_FRAMES = [
    Sprite.from_pixel_art([
        "..OGGO..",
        ".OLLLLO.",
        "OLLGGLLO",
        "OLGGGLLO",
        "OLGGGLLO",
        "OLLGGLLO",
        ".OLLLLO.",
        "..OGGO..",
    ], _GEAR_MAP),
    Sprite.from_pixel_art([
        ".OG..GO.",
        "OLLLLGO.",
        ".OLggLLO",
        "OLLggLLO",
        "OLLggLLO",
        "OLLggLO.",
        ".OGLLLLO",
        ".OG..GO.",
    ], _GEAR_MAP),
    Sprite.from_pixel_art([
        "..OGGO..",
        ".OLLLLO.",
        "OLLggLLO",
        "OLgggLLO",
        "OLLgggLO",
        "OLLggLLO",
        ".OLLLLO.",
        "..OGGO..",
    ], _GEAR_MAP),
    Sprite.from_pixel_art([
        ".OG..GO.",
        ".OGLLLLO",
        "OLLggLO.",
        "OLLggLLO",
        "OLLggLLO",
        ".OLggLLO",
        "OLLLLGO.",
        ".OG..GO.",
    ], _GEAR_MAP),
]


def _draw_control_panel(buf: PixelBuffer, x: int, y: int, w: int, h: int, fi: int) -> None:
    """Draw control panel with LEDs."""
    buf.fill_rect(x, y, w, h, IRON_DARK)
    buf.fill_rect(x + 1, y + 1, w - 2, h - 2, IRON_BLOCK)
    for dx in range(1, w - 1):
        buf.set_pixel(x + dx, y + 1, (220, 220, 225))
    for bx in range(2, w - 2, 3):
        for by in range(2, min(h - 1, 6)):
            idx = bx + by * w
            state = (fi + idx) % 5
            colors = [LED_GREEN, LED_AMBER, LED_GREEN, LED_GREEN, LED_OFF]
            buf.set_pixel(x + bx, y + by, colors[state])
            buf.set_pixel(x + bx + 1, y + by, IRON_DARK)


def _draw_progress_bar(buf: PixelBuffer, x: int, y: int, w: int, fi: int) -> None:
    """Draw framed progress bar."""
    buf.fill_rect(x - 1, y - 1, w + 2, 4, PROGRESS_FRAME)
    buf.fill_rect(x, y, w, 2, PROGRESS_BG)
    fill = ((fi + 1) * w) // NUM_FRAMES
    for dx in range(fill):
        if dx == fill - 1:
            c = (100, 255, 100)
        elif dx == fill - 2:
            c = (70, 240, 70)
        else:
            c = PROGRESS_GREEN
        buf.set_pixel(x + dx, y, c)
        buf.set_pixel(x + dx, y + 1, c)


def _draw_log_output(buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int) -> None:
    """Draw scrolling log lines on monitor."""
    for dy in range(mh):
        line_len = ((dy + fi) * 3) % max(1, mw) + 1
        for dx in range(min(line_len, mw)):
            c = MONITOR_TEXT_GREEN if (dy + fi) % 3 != 0 else MONITOR_TEXT_WHITE
            buf.set_pixel(mx + dx, my + dy, c)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf, layout = build_iso_office(width, pixel_h, fi)
        ox = layout["origin_x"]
        oy = layout["origin_y"]
        wall_h = layout["wall_h"]

        # Control panel on wall area
        panel_w = min(14, width // 5)
        panel_h = min(7, wall_h - 2)
        if panel_w >= 8 and panel_h >= 5:
            panel_x = ox - panel_w // 2 + 10
            panel_y = max(1, oy - wall_h + 2)
            _draw_control_panel(buf, panel_x, panel_y, panel_w, panel_h, fi)

        # Agent pushing buttons (standing near panel)
        if width >= 40:
            agent = BUTTON_PUSH[fi % len(BUTTON_PUSH)]
            ax, ay = iso_agent_pos(
                layout["desk1_gx"] + 0.5, layout["desk1_gy"] - 0.3,
                ox, oy, agent.height,
            )
            buf.draw_sprite(agent, ax, ay)

        # Gear animation (on floor, right side)
        if width >= 55:
            gear = _GEAR_FRAMES[fi % len(_GEAR_FRAMES)]
            gx, gy = iso_to_screen(
                layout["grid_w"] - 2.0, layout["grid_d"] - 2.0,
                ox, oy,
            )
            buf.draw_sprite(gear, gx - 4, gy - gear.height)

        # Log on monitor 1
        mx1, my1, mw1, mh1 = layout["mon1_rect"]
        _draw_log_output(buf, mx1, my1, mw1, mh1, fi)

        # Log on monitor 2
        if width >= 60:
            mx2, my2, mw2, mh2 = layout["mon2_rect"]
            _draw_log_output(buf, mx2, my2, mw2, mh2, fi + 3)

        # Progress bar at bottom
        if width >= 40:
            bar_w = min(24, width // 3)
            bar_x = (width - bar_w) // 2
            bar_y = pixel_h - 4
            _draw_progress_bar(buf, bar_x, bar_y, bar_w, fi)

        frames.append(buf)
    return frames
