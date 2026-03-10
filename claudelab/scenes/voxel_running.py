"""Voxel running scene — control panel, spinning gear, progress bar."""

from __future__ import annotations

from claudelab.palette import (
    GEAR_PURPLE, GEAR_DARK, IRON_BLOCK, IRON_DARK,
    PROGRESS_GREEN, PROGRESS_BG,
    LED_GREEN, LED_AMBER, LED_OFF,
    MONITOR_TEXT_GREEN, MONITOR_TEXT_WHITE, MONITOR_BG,
)
from claudelab.pixelbuffer import PixelBuffer, Sprite
from claudelab.sprites import BUTTON_PUSH
from claudelab.voxel_office import build_voxel_office

NUM_FRAMES = 8

# Gear sprites (4 rotation frames)
_GEAR_MAP = {"G": GEAR_PURPLE, "g": GEAR_DARK, ".": None}
_GEAR_FRAMES = [
    Sprite.from_pixel_art([
        "..GG..",
        ".GGGG.",
        "GGggGG",
        "GGggGG",
        ".GGGG.",
        "..GG..",
    ], _GEAR_MAP),
    Sprite.from_pixel_art([
        ".G..G.",
        "GGGGG.",
        ".GggGG",
        "GGggG.",
        ".GGGGG",
        ".G..G.",
    ], _GEAR_MAP),
    Sprite.from_pixel_art([
        "..GG..",
        ".GGGG.",
        "GGggGG",
        "GGggGG",
        ".GGGG.",
        "..GG..",
    ], _GEAR_MAP),
    Sprite.from_pixel_art([
        ".G..G.",
        ".GGGGG",
        "GGggG.",
        ".GggGG",
        "GGGGG.",
        ".G..G.",
    ], _GEAR_MAP),
]


def _draw_control_panel(buf: PixelBuffer, x: int, y: int, w: int, h: int, fi: int) -> None:
    """Draw a control panel with blinking indicators."""
    buf.fill_rect(x, y, w, h, IRON_DARK)
    buf.fill_rect(x + 1, y + 1, w - 2, h - 2, IRON_BLOCK)
    # Buttons / LEDs
    for bx in range(2, w - 2, 2):
        for by in range(1, min(h - 1, 4)):
            idx = bx + by * w
            led_state = (fi + idx) % 4
            if led_state == 0:
                c = LED_GREEN
            elif led_state == 1:
                c = LED_AMBER
            elif led_state == 2:
                c = LED_GREEN
            else:
                c = LED_OFF
            buf.set_pixel(x + bx, y + by, c)


def _draw_progress_bar(buf: PixelBuffer, x: int, y: int, w: int, fi: int) -> None:
    """Draw an animated progress bar."""
    fill = ((fi + 1) * w) // NUM_FRAMES
    for dx in range(w):
        c = PROGRESS_GREEN if dx < fill else PROGRESS_BG
        buf.set_pixel(x + dx, y, c)
        buf.set_pixel(x + dx, y + 1, c)


def _draw_log_output(buf: PixelBuffer, mx: int, my: int, mw: int, mh: int, fi: int) -> None:
    """Draw scrolling log lines on a monitor."""
    for dy in range(1, mh - 1):
        line_len = ((dy + fi) * 3) % (mw - 2) + 1
        for dx in range(1, min(1 + line_len, mw - 1)):
            c = MONITOR_TEXT_GREEN if (dy + fi) % 3 != 0 else MONITOR_TEXT_WHITE
            buf.set_pixel(mx + dx, my + dy, c)


def get_frames(width: int, height: int) -> list[PixelBuffer]:
    pixel_h = height * 2
    frames: list[PixelBuffer] = []

    for fi in range(NUM_FRAMES):
        buf = build_voxel_office(width, pixel_h, fi)

        wall_h = max(4, pixel_h * 2 // 5)
        floor_y = wall_h
        desk_y = floor_y + 2
        desk_w = min(10, width // 6)

        # Control panel (on the wall)
        panel_w = min(14, width // 4)
        panel_h = min(6, wall_h - 2)
        if panel_w >= 6 and panel_h >= 4:
            panel_x = width // 3
            _draw_control_panel(buf, panel_x, 1, panel_w, panel_h, fi)

        # Agent pushing buttons
        if width >= 45:
            agent = BUTTON_PUSH[fi % len(BUTTON_PUSH)]
            agent_y = floor_y - agent.height + 4
            buf.draw_sprite(agent, panel_x - 2 if panel_w >= 6 else 12, agent_y)

        # Gear animation
        if width >= 55:
            gear = _GEAR_FRAMES[fi % len(_GEAR_FRAMES)]
            gear_x = width // 2 + 8
            gear_y = floor_y - gear.height
            buf.draw_sprite(gear, gear_x, gear_y)

        # Progress bar
        if width >= 40:
            bar_w = min(20, width // 3)
            bar_x = 3
            bar_y = pixel_h - 4
            _draw_progress_bar(buf, bar_x, bar_y, bar_w, fi)

        # Log on monitor
        if width >= 40:
            _draw_log_output(buf, 4, desk_y - 7, min(8, desk_w - 2), 6, fi)

        frames.append(buf)
    return frames
