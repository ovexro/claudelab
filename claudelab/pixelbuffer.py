"""Pixel buffer with half-block rendering for ClaudeLab voxel mode.

The PixelBuffer represents a 2D grid of RGB pixels.  Each terminal cell
displays two vertically stacked pixels using the Unicode upper-half-block
character (▀) with foreground = top pixel and background = bottom pixel.
This doubles the effective vertical resolution.
"""

from __future__ import annotations

from claudelab.palette import BG_BLACK

# Pre-computed ANSI reset
_RESET = "\x1b[0m"

Color = tuple[int, int, int]


class Sprite:
    """A small pixel-art image with optional transparency."""

    __slots__ = ("width", "height", "pixels")

    def __init__(self, width: int, height: int, pixels: list[list[Color | None]]) -> None:
        self.width = width
        self.height = height
        self.pixels = pixels

    @classmethod
    def from_pixel_art(cls, rows: list[str], color_map: dict[str, Color | None]) -> Sprite:
        """Create a sprite from character-art rows with a color legend.

        Example::

            Sprite.from_pixel_art([
                "..HH..",
                ".SSSS.",
                ".CCCC.",
            ], {"H": (75,50,30), "S": (200,160,120), "C": (50,160,200), ".": None})
        """
        pixels: list[list[Color | None]] = []
        width = 0
        for row in rows:
            prow: list[Color | None] = []
            for ch in row:
                prow.append(color_map.get(ch))
            pixels.append(prow)
            if len(prow) > width:
                width = len(prow)
        # Pad rows to uniform width
        for prow in pixels:
            while len(prow) < width:
                prow.append(None)
        return cls(width, len(pixels), pixels)


class PixelBuffer:
    """A 2D pixel grid that renders to half-block ANSI strings."""

    __slots__ = ("width", "height", "pixels", "_bg")

    def __init__(self, width: int, height: int, bg: Color = BG_BLACK) -> None:
        """Create a buffer *width* pixels wide and *height* pixels tall.

        *height* should be even (2 pixel rows per terminal row).
        """
        self.width = width
        self.height = height if height % 2 == 0 else height + 1
        self._bg = bg
        self.pixels: list[list[Color]] = [
            [bg] * width for _ in range(self.height)
        ]

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

    def get_pixel(self, x: int, y: int) -> Color:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return self._bg

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color) -> None:
        for dy in range(h):
            py = y + dy
            if py < 0 or py >= self.height:
                continue
            for dx in range(w):
                px = x + dx
                if 0 <= px < self.width:
                    self.pixels[py][px] = color

    def draw_sprite(self, sprite: Sprite, x: int, y: int) -> None:
        """Blit a sprite onto the buffer (None pixels are transparent)."""
        for sy in range(sprite.height):
            py = y + sy
            if py < 0 or py >= self.height:
                continue
            srow = sprite.pixels[sy]
            for sx in range(sprite.width):
                px = x + sx
                if px < 0 or px >= self.width:
                    continue
                c = srow[sx]
                if c is not None:
                    self.pixels[py][px] = c

    def copy_from(self, other: PixelBuffer) -> None:
        """Copy all pixels from *other* into this buffer."""
        for y in range(min(self.height, other.height)):
            row = other.pixels[y]
            dst = self.pixels[y]
            for x in range(min(self.width, other.width)):
                dst[x] = row[x]

    def upscale(self, factor: int = 4) -> PixelBuffer:
        """Return a new PixelBuffer scaled up by *factor* (nearest-neighbor)."""
        new_w = self.width * factor
        new_h = self.height * factor
        out = PixelBuffer(new_w, new_h, self._bg)
        for y in range(self.height):
            row = self.pixels[y]
            for x in range(self.width):
                c = row[x]
                for dy in range(factor):
                    out_row = out.pixels[y * factor + dy]
                    for dx in range(factor):
                        out_row[x * factor + dx] = c
        return out

    def render_to_halfblocks(self) -> list[str]:
        """Render the pixel buffer to ANSI-colored half-block strings.

        Each pair of pixel rows becomes one terminal row.  Returns a list
        of strings (one per terminal row), each containing embedded ANSI
        escape sequences for 24-bit color.
        """
        lines: list[str] = []
        # ANSI color cache to avoid repeated string formatting
        _cache: dict[tuple[Color, Color], str] = {}

        for term_row in range(self.height // 2):
            top_row = self.pixels[term_row * 2]
            bot_row = self.pixels[term_row * 2 + 1]
            parts: list[str] = []
            prev_key: tuple[Color, Color] | None = None

            for col in range(self.width):
                top = top_row[col]
                bot = bot_row[col]
                key = (top, bot)

                if key == prev_key:
                    # Same colors as previous cell -- just emit the char
                    parts.append("\u2580")
                else:
                    esc = _cache.get(key)
                    if esc is None:
                        esc = (
                            f"\x1b[38;2;{top[0]};{top[1]};{top[2]}m"
                            f"\x1b[48;2;{bot[0]};{bot[1]};{bot[2]}m"
                        )
                        _cache[key] = esc
                    parts.append(esc + "\u2580")
                    prev_key = key

            parts.append(_RESET)
            lines.append("".join(parts))

        return lines
