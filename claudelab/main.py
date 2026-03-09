"""ClaudeLab -- main entry point.

Launches the curses-based terminal UI showing animated ASCII art of
AI "engineers" working while Claude Code runs.

Usage
-----
    claudelab              # after pip install
    python -m claudelab    # direct invocation

Flags
-----
    --theme dark|light     # colour theme (default: dark)
    --fps N                # animation frame rate (default: 8)
    --demo                 # cycle through all scenes for demonstration
"""

from __future__ import annotations

import argparse
import curses
import sys

from claudelab.colors import init_colors
from claudelab.detector import get_current_activity, start_detection, stop_detection
from claudelab.renderer import Renderer


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="claudelab",
        description="A visual terminal companion for Claude Code",
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default="dark",
        help="Colour theme (default: dark)",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=8,
        help="Animation frame rate (default: 8)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Cycle through all scenes for demonstration",
    )
    return parser.parse_args(argv)


def _curses_main(stdscr: curses.window, args: argparse.Namespace) -> None:
    """Curses application body."""
    # Terminal setup
    curses.curs_set(0)           # hide cursor
    stdscr.nodelay(True)         # non-blocking getch
    stdscr.timeout(0)

    init_colors(args.theme)

    renderer = Renderer(
        stdscr,
        activity_fn=get_current_activity,
        fps=args.fps,
        demo=args.demo,
    )

    try:
        renderer.run()
    except KeyboardInterrupt:
        pass


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``claudelab`` console script."""
    args = _parse_args(argv)

    # Start background activity detection (unless in demo mode)
    if not args.demo:
        start_detection()

    try:
        curses.wrapper(lambda stdscr: _curses_main(stdscr, args))
    except KeyboardInterrupt:
        pass
    finally:
        stop_detection()
        # Ensure terminal is left in a clean state
        print("\nClaudeLab stopped.", file=sys.stderr)


if __name__ == "__main__":
    main()
