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

from claudelab.colors import detect_color_mode, init_colors
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
    parser.add_argument(
        "--renderer",
        choices=["auto", "iso", "sixel", "voxel", "ascii"],
        default="auto",
        help="Rendering mode (default: auto). iso=isometric 3D, sixel=pixel graphics, voxel=half-block, ascii=classic",
    )
    return parser.parse_args(argv)


def _curses_main(stdscr: curses.window, args: argparse.Namespace, mode: str) -> None:
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
        voxel=(mode in ("voxel", "sixel")),
        sixel=(mode == "sixel"),
        iso=(mode == "iso"),
    )

    try:
        renderer.run()
    except KeyboardInterrupt:
        pass


def _resolve_mode(renderer_arg: str) -> str:
    """Resolve the rendering mode *before* curses takes over."""
    if renderer_arg == "sixel":
        from claudelab.sixel import detect_sixel
        if not detect_sixel():
            print("ClaudeLab: sixel not supported by terminal, falling back to voxel", file=sys.stderr)
            return "voxel"
        return "sixel"
    if renderer_arg == "auto":
        cm = detect_color_mode()
        return "iso" if cm in ("truecolor", "256") else "ascii"
    return renderer_arg  # "voxel" or "ascii"


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``claudelab`` console script."""
    args = _parse_args(argv)

    # Resolve renderer mode before curses init (sixel detection needs raw terminal)
    mode = _resolve_mode(args.renderer)

    # Start background activity detection (unless in demo mode)
    if not args.demo:
        start_detection()

    try:
        curses.wrapper(lambda stdscr: _curses_main(stdscr, args, mode))
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"\nClaudeLab error: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
    finally:
        stop_detection()
        # Ensure terminal is left in a clean state
        print("\nClaudeLab stopped.", file=sys.stderr)


if __name__ == "__main__":
    main()
