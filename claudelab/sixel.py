"""Pure-Python sixel encoder for ClaudeLab.

Sixel graphics render actual pixels in the terminal — no character blocks.
Each sixel character encodes a 1-wide × 6-tall pixel strip. Colors are
assigned to registers and layered with the $ (carriage return) operator.

Since ClaudeLab uses a fixed palette, we map palette colors to sixel
registers at startup — no color quantization needed.
"""

from __future__ import annotations

import os
import sys
import select
import termios
import tty

ESC = "\x1b"
DCS = f"{ESC}P"
ST = f"{ESC}\\"


def detect_sixel() -> bool:
    """Query terminal for sixel support using DA1 (Device Attributes).

    Sends ESC[c and checks if the response contains ";4" which indicates
    sixel capability. Returns False on timeout or if not supported.
    """
    # Quick env-var shortcut for known terminals
    term_program = os.environ.get("TERM_PROGRAM", "").lower()
    if term_program in ("wezterm", "mintty"):
        return True

    # Check if stdout is a terminal
    if not os.isatty(sys.stdout.fileno()):
        return False

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        # Send DA1 query
        sys.stdout.write(f"{ESC}[c")
        sys.stdout.flush()

        # Read response with timeout
        response = ""
        deadline = 0.3  # 300ms timeout
        while True:
            ready, _, _ = select.select([fd], [], [], deadline)
            if not ready:
                break
            ch = os.read(fd, 1).decode("ascii", errors="ignore")
            response += ch
            if ch == "c":  # Response ends with 'c'
                break
            deadline = 0.05  # Shorter timeout for subsequent chars
    except (OSError, ValueError):
        return False
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # DA1 response format: ESC [ ? 65 ; 1 ; 2 ; 4 ; ... c
    # Presence of "4" in the parameter list indicates sixel support
    return ";4" in response


class SixelEncoder:
    """Encode pixel data as sixel escape sequences.

    Optimized for ClaudeLab's fixed palette: colors are registered once
    and reused across frames.
    """

    __slots__ = ("_palette", "_color_map")

    def __init__(self) -> None:
        self._palette: list[tuple[int, int, int]] = []
        self._color_map: dict[tuple[int, int, int], int] = {}

    def register_color(self, color: tuple[int, int, int]) -> int:
        """Register a color and return its register index."""
        if color in self._color_map:
            return self._color_map[color]
        idx = len(self._palette)
        self._palette.append(color)
        self._color_map[color] = idx
        return idx

    def register_colors(self, colors: list[tuple[int, int, int]]) -> None:
        """Register multiple colors at once."""
        for c in colors:
            self.register_color(c)

    def _build_palette_string(self) -> str:
        """Build sixel palette definition string."""
        parts: list[str] = []
        for i, (r, g, b) in enumerate(self._palette):
            # Sixel uses 0-100 range for RGB
            sr = r * 100 // 255
            sg = g * 100 // 255
            sb = b * 100 // 255
            parts.append(f"#{i};2;{sr};{sg};{sb}")
        return "".join(parts)

    def encode(
        self,
        pixels: list[list[tuple[int, int, int]]],
        width: int,
        height: int,
    ) -> str:
        """Encode a pixel grid as a sixel string.

        Parameters
        ----------
        pixels : 2D list of RGB tuples [y][x]
        width : pixel width
        height : pixel height

        Returns a complete sixel escape sequence (DCS...ST).
        """
        cmap = self._color_map

        # Ensure all colors are registered
        for y in range(height):
            row = pixels[y]
            for x in range(width):
                c = row[x]
                if c not in cmap:
                    self.register_color(c)

        # Build output
        parts: list[str] = [f"{DCS}0;1;0q"]  # p2=1: don't fill background
        parts.append(self._build_palette_string())

        # Process in bands of 6 rows
        for band_y in range(0, height, 6):
            band_h = min(6, height - band_y)

            # Group pixels by color in this band
            # color_register -> list of (x, sixel_value) but we build per-color scanlines
            color_strips: dict[int, list[int]] = {}

            for x in range(width):
                # For each column, find which colors appear in this 6-pixel strip
                col_colors: dict[int, int] = {}  # color_reg -> bit pattern
                for bit in range(band_h):
                    c = pixels[band_y + bit][x]
                    reg = cmap[c]
                    if reg not in col_colors:
                        col_colors[reg] = 0
                    col_colors[reg] |= (1 << bit)

                for reg, bits in col_colors.items():
                    if reg not in color_strips:
                        color_strips[reg] = [0] * width
                    color_strips[reg][x] = bits

            # Emit each color layer with RLE
            first_color = True
            for reg, strip in color_strips.items():
                if not first_color:
                    parts.append("$")  # CR — return to start of this band
                first_color = False

                parts.append(f"#{reg}")

                # RLE encode the strip
                i = 0
                while i < width:
                    val = strip[i]
                    ch = chr(val + 0x3F)
                    # Count run
                    run = 1
                    while i + run < width and strip[i + run] == val:
                        run += 1
                    if run >= 3:
                        parts.append(f"!{run}{ch}")
                    elif run == 2:
                        parts.append(ch + ch)
                    else:
                        parts.append(ch)
                    i += run

            parts.append("-")  # LF — move to next band

        parts.append(ST)
        return "".join(parts)

    def encode_from_buffer(self, buf) -> str:
        """Encode a PixelBuffer as sixel. Convenience wrapper."""
        return self.encode(buf.pixels, buf.width, buf.height)
