"""Main render loop for ClaudeLab.

Drives the curses display at ~8 FPS, compositing the title bar, the
current scene, and the status bar into the terminal.  Handles terminal
resize (SIGWINCH) gracefully.
"""

from __future__ import annotations

import curses
import datetime
import signal
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
from claudelab.scenes import get_scene_frames

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
    status_text = f" Activity: {activity.upper():10s}  |  {now}  |  ClaudeLab v0.1.0 "
    padded = status_text.ljust(width)[:width]
    try:
        stdscr.addnstr(row, 0, padded, width, curses.color_pair(PAIR_STATUS))
    except curses.error:
        pass


# ---------------------------------------------------------------------------
# Scene rendering
# ---------------------------------------------------------------------------

def _draw_scene(
    stdscr: curses.window,
    scene_rows: list[str],
    start_row: int,
    width: int,
    max_rows: int,
    activity: str,
) -> None:
    """Draw the scene frame rows onto the screen."""
    # Choose a color pair based on activity
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
            # Truncate to width and write
            text = row_text[:width]
            stdscr.addnstr(r, 0, text, width, base_pair)
        except curses.error:
            pass


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
    ) -> None:
        self.stdscr = stdscr
        self.activity_fn = activity_fn
        self.fps = max(1, min(fps, 30))
        self.demo = demo
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
        self._cached_frames: list[list[str]] = []

    # -- signal handlers ---------------------------------------------------

    def handle_resize(self, signum: int, frame: object) -> None:
        """Handle SIGWINCH."""
        self._resized = True

    def stop(self) -> None:
        """Signal the render loop to stop."""
        self._running = False

    # -- frame cache -------------------------------------------------------

    def _get_frames(self, activity: str, width: int, height: int) -> list[list[str]]:
        dims = (width, height)
        if activity != self._cached_activity or dims != self._cached_dims:
            self._cached_activity = activity
            self._cached_dims = dims
            self._cached_frames = get_scene_frames(activity, width, height)
            self._frame_idx = 0
        return self._cached_frames

    # -- main loop ---------------------------------------------------------

    def run(self) -> None:
        """Run the render loop until stopped or interrupted."""
        # Install resize handler
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
                curses.endwin()
                self.stdscr.refresh()
                self._cached_activity = ""  # Force regeneration

            try:
                height, width = self.stdscr.getmaxyx()
            except curses.error:
                time.sleep(interval)
                continue

            if height < 5 or width < 20:
                # Terminal too small
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

            frame = all_frames[self._frame_idx % len(all_frames)]
            self._frame_idx += 1

            # -- draw --
            self.stdscr.erase()

            _draw_title(self.stdscr, width)
            _draw_scene(self.stdscr, frame, 1, width, scene_height, activity)
            _draw_status(self.stdscr, height - 1, width, activity)

            self.stdscr.noutrefresh()
            curses.doupdate()

            # -- timing --
            elapsed = time.monotonic() - t0
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
