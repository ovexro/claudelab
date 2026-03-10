"""Minecraft-inspired RGB color palette for ClaudeLab voxel renderer.

Each material has 3 tones (highlight, base, shadow) for NES-style
directional shading.  Light source is upper-left.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Outline / linework
# ---------------------------------------------------------------------------
OUTLINE = (15, 10, 20)

# ---------------------------------------------------------------------------
# Block materials
# ---------------------------------------------------------------------------
STONE_HIGHLIGHT = (190, 190, 195)
STONE = (128, 128, 128)
STONE_LIGHT = (160, 160, 160)
STONE_DARK = (80, 80, 80)
COBBLESTONE = (110, 110, 110)

DIRT = (134, 96, 67)
DIRT_DARK = (100, 70, 50)
GRASS_TOP = (91, 170, 60)
GRASS_SIDE = (95, 120, 55)

OAK_PLANK_LIGHT = (200, 160, 100)
OAK_PLANK = (170, 130, 80)
OAK_PLANK_DARK = (140, 105, 65)
OAK_LOG = (85, 65, 40)
OAK_LOG_BARK = (100, 80, 55)
BIRCH_PLANK = (200, 190, 160)

# Desk material — darker walnut to contrast with oak floor
DESK_TOP = (110, 75, 50)
DESK_TOP_LIGHT = (135, 95, 65)
DESK_TOP_DARK = (85, 58, 38)
DESK_EDGE = (70, 48, 30)

GLASS = (180, 215, 235)
GLASS_PANE = (160, 200, 225)

IRON_BLOCK = (200, 200, 200)
IRON_DARK = (150, 150, 155)

GOLD_BLOCK = (240, 200, 50)
REDSTONE = (180, 40, 40)
REDSTONE_GLOW = (255, 60, 60)
EMERALD = (50, 200, 80)
DIAMOND = (80, 210, 230)
LAPIS = (50, 70, 180)
COAL = (40, 40, 40)
OBSIDIAN = (20, 15, 30)
GLOWSTONE = (210, 190, 120)

# ---------------------------------------------------------------------------
# Agent colors — 3-tone shading per material
# ---------------------------------------------------------------------------
SKIN_HIGHLIGHT = (230, 195, 160)
SKIN = (200, 160, 120)
SKIN_SHADOW = (160, 120, 80)
SKIN_DARK = (120, 85, 55)

HAIR_HIGHLIGHT = (110, 80, 50)
HAIR_BROWN = (75, 50, 30)
HAIR_DARK = (45, 25, 12)

SHIRT_CYAN_LIGHT = (90, 200, 240)
SHIRT_CYAN = (50, 160, 200)
SHIRT_DARK_CYAN = (35, 120, 160)

SHIRT_RED_LIGHT = (240, 90, 90)
SHIRT_RED = (200, 50, 50)
SHIRT_DARK_RED = (150, 35, 35)

PANTS_LIGHT = (60, 75, 180)
PANTS_INDIGO = (40, 50, 140)
PANTS_SHADOW = (28, 35, 100)

SHOE_HIGHLIGHT = (120, 120, 125)
SHOE_GRAY = (80, 80, 80)

EYE_WHITE = (255, 255, 255)
EYE_PUPIL = (30, 30, 60)

# ---------------------------------------------------------------------------
# Environment / sky
# ---------------------------------------------------------------------------
SKY_DAY = (120, 180, 255)
SKY_DAWN = (255, 180, 120)
SKY_DUSK = (200, 120, 80)
SKY_NIGHT = (15, 15, 45)
CLOUD = (240, 240, 255)
SUN = (255, 230, 80)
MOON = (230, 230, 210)
STAR = (255, 255, 200)

# ---------------------------------------------------------------------------
# Tech / monitors
# ---------------------------------------------------------------------------
MONITOR_BG = (25, 30, 50)
MONITOR_GLOW = (35, 45, 70)
MONITOR_FRAME = (55, 55, 70)
MONITOR_TEXT_GREEN = (80, 255, 80)
MONITOR_TEXT_WHITE = (210, 210, 210)
MONITOR_TEXT_YELLOW = (255, 220, 80)
MONITOR_TEXT_RED = (255, 80, 80)
MONITOR_TEXT_CYAN = (80, 220, 255)
LED_GREEN = (50, 255, 50)
LED_RED = (255, 50, 50)
LED_AMBER = (255, 180, 0)
LED_OFF = (50, 50, 55)

# ---------------------------------------------------------------------------
# Objects
# ---------------------------------------------------------------------------
COFFEE_BROWN = (110, 65, 30)
COFFEE_CREAM = (220, 195, 150)
COFFEE_MUG = (240, 240, 245)
STEAM_WHITE = (240, 240, 255)
STEAM_FADE = (190, 190, 210)
LEAF_GREEN = (50, 150, 50)
LEAF_DARK = (30, 110, 30)
LEAF_LIGHT = (80, 190, 70)
POT_TERRACOTTA = (180, 100, 60)
CHAIR_HIGHLIGHT = (140, 120, 100)
CHAIR_DARK = (100, 85, 70)
CHAIR_SHADOW = (65, 55, 45)
KEYBOARD_DARK = (55, 55, 60)
KEYBOARD_KEY = (90, 90, 95)
BOOK_RED = (180, 50, 40)
BOOK_BLUE = (50, 70, 160)
BOOK_GREEN = (50, 130, 60)
BOOK_YELLOW = (200, 180, 50)
PAPER_WHITE = (235, 235, 230)
PAPER_SHADOW = (200, 200, 195)
CLOCK_FACE = (230, 225, 210)
CLOCK_HAND = (40, 40, 45)

# ---------------------------------------------------------------------------
# UI / effects
# ---------------------------------------------------------------------------
WARNING_RED = (220, 40, 40)
WARNING_YELLOW = (255, 210, 50)
GEAR_PURPLE = (160, 80, 200)
GEAR_DARK = (120, 55, 155)
GEAR_LIGHT = (200, 120, 240)
CONVEYOR_GRAY = (150, 150, 160)
CONVEYOR_DARK = (110, 110, 120)
CONVEYOR_LIGHT = (180, 180, 190)
PROGRESS_GREEN = (50, 220, 50)
PROGRESS_BG = (50, 50, 55)
PROGRESS_FRAME = (80, 80, 90)
THOUGHT_CLOUD = (220, 220, 240)
THOUGHT_DARK = (180, 180, 200)
THOUGHT_LIGHT = (245, 245, 255)

# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
BG_BLACK = (10, 10, 15)
BG_DARK = (20, 20, 28)
BASEBOARD = (65, 50, 35)
BASEBOARD_DARK = (45, 35, 25)

# Transparent sentinel
TRANSPARENT: tuple[int, int, int] | None = None
