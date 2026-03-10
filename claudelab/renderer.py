"""Main render loop for ClaudeLab.

Drives the curses display at ~8 FPS, compositing the title bar, the
current scene, and the status bar into the terminal.  Handles terminal
resize (SIGWINCH) gracefully.

Supports three rendering modes:
- **ascii**: curses color pairs + ASCII line-drawing art
- **voxel**: 24-bit ANSI color + half-block pixel art
- **sixel**: actual pixel graphics via sixel escape sequences
"""

from __future__ import annotations

import curses
import datetime
import signal
import sys
import time
from typing import Callable

from claudelab.colors import (
    PAIR_TITLE,
    PAIR_STATUS,
    PAIR_ACCENT,
    PAIR_MONITOR_TEXT,
    PAIR_WARNING,
    PAIR_LABEL,
    PAIR_DIM,
)
from claudelab.scenes import get_scene_frames, get_voxel_scene_frames, get_iso_scene_frames

# ---------------------------------------------------------------------------
# Title bar
# ---------------------------------------------------------------------------

_TITLE = " AI ENGINEERING LAB "
_TITLE_BORDER_CHAR = "\u2550"


def _draw_title(stdscr: curses.window, width: int) -> None:
    """Render the title bar on row 0."""
    pad_total = max(0, width - len(_TITLE) - 2)
    left = pad_total // 2
    right = pad_total - left
    title_line = _TITLE_BORDER_CHAR * left + " " + _TITLE + " " + _TITLE_BORDER_CHAR * right
    try:
        stdscr.addnstr(0, 0, title_line[:width], width, curses.color_pair(PAIR_TITLE) | curses.A_BOLD)
    except curses.error:
        pass


# ---------------------------------------------------------------------------
# Status bar
# ---------------------------------------------------------------------------

def _draw_status(stdscr: curses.window, row: int, width: int, activity: str) -> None:
    """Render the status bar at the given row."""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    from claudelab import __version__
    status_text = f" Activity: {activity.upper():10s}  |  {now}  |  ClaudeLab v{__version__} "
    padded = status_text.ljust(width)[:width]
    try:
        stdscr.addnstr(row, 0, padded, width, curses.color_pair(PAIR_STATUS))
    except curses.error:
        pass


# ---------------------------------------------------------------------------
# ASCII scene rendering (classic mode)
# ---------------------------------------------------------------------------

def _draw_scene_ascii(
    stdscr: curses.window,
    scene_rows: list[str],
    start_row: int,
    width: int,
    max_rows: int,
    activity: str,
) -> None:
    """Draw the scene frame rows onto the screen (classic ASCII mode)."""
    color_map = {
        "thinking": PAIR_LABEL,
        "coding": PAIR_MONITOR_TEXT,
        "debugging": PAIR_WARNING,
        "running": PAIR_ACCENT,
        "building": PAIR_LABEL,
        "idle": PAIR_DIM,
    }
    base_pair = curses.color_pair(color_map.get(activity, PAIR_DIM))

    for i, row_text in enumerate(scene_rows):
        if i >= max_rows:
            break
        r = start_row + i
        try:
            text = row_text[:width].ljust(width)
            stdscr.addnstr(r, 0, text, width, base_pair)
        except curses.error:
            pass


def _draw_scene_voxel(
    ansi_lines: list[str],
    start_row: int,
    width: int,
    max_rows: int,
) -> None:
    """Write pre-rendered ANSI half-block lines directly to stdout."""
    out = sys.stdout
    parts: list[str] = []
    for i, line in enumerate(ansi_lines):
        if i >= max_rows:
            break
        # Move cursor to position and write the ANSI line
        parts.append(f"\x1b[{start_row + i + 1};1H{line}\x1b[0m")
    out.write("".join(parts))
    out.flush()


def _draw_scene_sixel(
    sixel_data: str,
    start_row: int,
) -> None:
    """Write sixel-encoded pixel data to stdout."""
    out = sys.stdout
    # Position cursor at the start of the scene area
    out.write(f"\x1b[{start_row + 1};1H")
    out.write(sixel_data)
    out.flush()


# ---------------------------------------------------------------------------
# Main render loop
# ---------------------------------------------------------------------------

class Renderer:
    """Drives the curses display loop."""

    def __init__(
        self,
        stdscr: curses.window,
        activity_fn: Callable[[], str],
        fps: int = 8,
        demo: bool = False,
        voxel: bool = False,
        sixel: bool = False,
        iso: bool = False,
    ) -> None:
        self.stdscr = stdscr
        self.activity_fn = activity_fn
        self.fps = max(1, min(fps, 30))
        if self.fps != fps:
            print(f"ClaudeLab: FPS clamped to {self.fps} (requested {fps})", file=sys.stderr)
        self.demo = demo
        self.iso = iso
        self.voxel = voxel or sixel or iso  # all pixel modes use PixelBuffer
        self.sixel = sixel
        self._running = True
        self._resized = False
        self._frame_idx = 0
        self._demo_cycle = 0
        self._demo_activities = [
            "thinking", "coding", "debugging", "running", "building", "idle",
        ]
        self._demo_frames_per_activity = fps * 4  # 4 seconds per activity

        # Cache scene frames so we don't regenerate every tick
        self._cached_activity: str = ""
        self._cached_dims: tuple[int, int] = (0, 0)
        self._cached_frames: list = []

        # Sixel encoder (lazy-init)
        self._sixel_encoder = None
        self._sixel_cache: dict[int, str] = {}  # frame_idx -> sixel string

    # -- signal handlers ---------------------------------------------------

    def handle_resize(self, signum: int, frame: object) -> None:
        """Handle SIGWINCH."""
        self._resized = True

    def stop(self) -> None:
        """Signal the render loop to stop."""
        self._running = False

    # -- frame cache -------------------------------------------------------

    def _get_frames(self, activity: str, width: int, height: int) -> list:
        dims = (width, height)
        if activity != self._cached_activity or dims != self._cached_dims:
            self._cached_activity = activity
            self._cached_dims = dims
            if self.iso:
                self._cached_frames = get_iso_scene_frames(activity, width, height)
            elif self.voxel:
                # Sixel renders at higher resolution (4x)
                if self.sixel:
                    scale = 4
                    self._cached_frames = get_voxel_scene_frames(
                        activity, width * scale, height * scale
                    )
                else:
                    self._cached_frames = get_voxel_scene_frames(activity, width, height)
            else:
                self._cached_frames = get_scene_frames(activity, width, height)
            self._frame_idx = 0
            self._sixel_cache.clear()
        return self._cached_frames

    def _get_sixel_encoder(self):
        """Lazily create the sixel encoder."""
        if self._sixel_encoder is None:
            from claudelab.sixel import SixelEncoder
            from claudelab import palette
            self._sixel_encoder = SixelEncoder()
            # Pre-register all palette colors
            all_colors = [
                v for v in vars(palette).values()
                if isinstance(v, tuple) and len(v) == 3
                and all(isinstance(c, int) for c in v)
            ]
            self._sixel_encoder.register_colors(all_colors)
        return self._sixel_encoder

    # -- main loop ---------------------------------------------------------

    def run(self) -> None:
        """Run the render loop until stopped or interrupted."""
        old_handler = signal.signal(signal.SIGWINCH, self.handle_resize)

        try:
            self._loop()
        finally:
            signal.signal(signal.SIGWINCH, old_handler)

    def _loop(self) -> None:
        interval = 1.0 / self.fps

        while self._running:
            t0 = time.monotonic()

            # Handle resize
            if self._resized:
                self._resized = False
                try:
                    curses.endwin()
                    self.stdscr = curses.initscr()
                    self.stdscr.nodelay(True)
                    self.stdscr.timeout(0)
                    curses.curs_set(0)
                except curses.error:
                    pass
                self._cached_activity = ""  # Force regeneration

            try:
                height, width = self.stdscr.getmaxyx()
            except curses.error:
                time.sleep(interval)
                continue

            if height < 7 or width < 20:
                self.stdscr.erase()
                msg = "Too small!"
                try:
                    self.stdscr.addstr(0, 0, msg[:width])
                except curses.error:
                    pass
                self.stdscr.noutrefresh()
                curses.doupdate()
                time.sleep(interval)
                continue

            # Determine activity
            if self.demo:
                cycle_pos = self._demo_cycle // self._demo_frames_per_activity
                activity = self._demo_activities[cycle_pos % len(self._demo_activities)]
                self._demo_cycle += 1
            else:
                activity = self.activity_fn()

            # Get scene frames (leaves 2 rows for title + status)
            scene_height = height - 2
            scene_width = width
            all_frames = self._get_frames(activity, scene_width, scene_height)

            if not all_frames:
                time.sleep(interval)
                continue

            fidx = self._frame_idx % len(all_frames)
            frame = all_frames[fidx]
            self._frame_idx += 1

            # -- draw (synchronized output to prevent flicker) --
            out = sys.stdout
            out.write("\x1b[?2026h")  # Begin synchronized update
            out.flush()

            _draw_title(self.stdscr, width)

            if self.sixel:
                # Encode PixelBuffer to sixel (cached per frame index)
                if fidx not in self._sixel_cache:
                    encoder = self._get_sixel_encoder()
                    self._sixel_cache[fidx] = encoder.encode_from_buffer(frame)
                sixel_str = self._sixel_cache[fidx]

                # Flush title via curses
                self.stdscr.noutrefresh()
                curses.doupdate()
                # Write sixel scene
                _draw_scene_sixel(sixel_str, 1)
                # Status bar
                _draw_status(self.stdscr, height - 1, width, activity)
                self.stdscr.noutrefresh()
                curses.doupdate()
            elif self.voxel:
                # frame is a PixelBuffer -- render to ANSI and write to stdout
                ansi_lines = frame.render_to_halfblocks()
                # Flush curses title first
                self.stdscr.noutrefresh()
                curses.doupdate()
                # Write voxel scene via raw ANSI
                _draw_scene_voxel(ansi_lines, 1, width, scene_height)
                # Draw status bar via curses (move cursor back)
                _draw_status(self.stdscr, height - 1, width, activity)
                self.stdscr.noutrefresh()
                curses.doupdate()
            else:
                # frame is list[str] -- classic ASCII rendering
                _draw_scene_ascii(self.stdscr, frame, 1, width, scene_height, activity)
                _draw_status(self.stdscr, height - 1, width, activity)
                self.stdscr.noutrefresh()
                curses.doupdate()

            out.write("\x1b[?2026l")  # End synchronized update
            out.flush()

            # -- timing --
            elapsed = time.monotonic() - t0
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
