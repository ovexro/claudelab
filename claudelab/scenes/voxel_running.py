"""Voxel running scene — control panel, gear, progress bar, logs."""

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
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Larger gear sprites (8x8, 4 rotation frames)
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
    """Draw control panel with LEDs and buttons."""
    # Outer frame
    buf.fill_rect(x, y, w, h, IRON_DARK)
    buf.fill_rect(x + 1, y + 1, w - 2, h - 2, IRON_BLOCK)
    # Highlight on top-left
    for dx in range(1, w - 1):
        buf.set_pixel(x + dx, y + 1, (220, 220, 225))
    # Button grid with LEDs
    for bx in range(2, w - 2, 3):
        for by in range(2, min(h - 1, 6)):
            idx = bx + by * w
            state = (fi + idx) % 5
            colors = [LED_GREEN, LED_AMBER, LED_GREEN, LED_GREEN, LED_OFF]
            buf.set_pixel(x + bx, y + by, colors[state])
            buf.set_pixel(x + bx + 1, y + by, IRON_DARK)  # button body


def _draw_progress_bar(buf: PixelBuffer, x: int, y: int, w: int, fi: int) -> None:
    """Draw framed progress bar."""
    # Frame
    buf.fill_rect(x - 1, y - 1, w + 2, 4, PROGRESS_FRAME)
    # Background
    buf.fill_rect(x, y, w, 2, PROGRESS_BG)
    # Fill
    fill = ((fi + 1) * w) // NUM_FRAMES
    for dx in range(fill):
        # Gradient green (brighter at leading edge)
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
    for dy in range(2, mh - 2):
        line_len = ((dy + fi) * 3) % max(1, mw - 4) + 1
        for dx in range(2, min(2 + line_len, mw - 2)):
            c = MONITOR_TEXT_GREEN if (dy + fi) % 3 != 0 else MONITOR_TEXT_WHITE
            buf.set_pixel(mx + dx, my + dy, c)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(6, pixel_h * 7 // 20)
        floor_y = wall_h
        desk_y = floor_y + 2

        # Control panel on wall
        panel_w = min(16, width // 4)
        panel_h = min(8, wall_h - 3)
        panel_x = width // 3
        if panel_w >= 8 and panel_h >= 5:
            _draw_control_panel(buf, panel_x, 1, panel_w, panel_h, fi)

        # Agent pushing buttons
        if width >= 45:
            agent = BUTTON_PUSH[fi % len(BUTTON_PUSH)]
            agent_y = floor_y - agent.height + 4
            buf.draw_sprite(agent, panel_x - 4 if panel_w >= 8 else 10, agent_y)

        # Gear animation
        if width >= 55:
            gear = _GEAR_FRAMES[fi % len(_GEAR_FRAMES)]
            gear_x = width // 2 + 10
            gear_y = floor_y - gear.height
            buf.draw_sprite(gear, gear_x, gear_y)

        # Progress bar
        if width >= 40:
            bar_w = min(24, width // 3)
            bar_x = 4
            bar_y = pixel_h - 5
            _draw_progress_bar(buf, bar_x, bar_y, bar_w, fi)

        # Log on monitor
        if width >= 40:
            desk_w = min(14, width // 5)
            _draw_log_output(buf, 5, desk_y - 10, min(10, desk_w - 2), 8, fi)

        frames.append(buf)
    return frames
