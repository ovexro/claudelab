"""Minecraft-inspired RGB color palette for ClaudeLab voxel renderer."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Block materials
# ---------------------------------------------------------------------------
STONE = (128, 128, 128)
STONE_DARK = (80, 80, 80)
STONE_LIGHT = (160, 160, 160)
COBBLESTONE = (110, 110, 110)
DIRT = (134, 96, 67)
DIRT_DARK = (100, 70, 50)
GRASS_TOP = (91, 170, 60)
GRASS_SIDE = (95, 120, 55)
OAK_PLANK = (170, 130, 80)
OAK_PLANK_DARK = (140, 105, 65)
OAK_LOG = (85, 65, 40)
OAK_LOG_BARK = (100, 80, 55)
BIRCH_PLANK = (200, 190, 160)
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
# Agent colors (Steve-like)
# ---------------------------------------------------------------------------
SKIN = (200, 160, 120)
SKIN_SHADOW = (160, 120, 80)
HAIR_BROWN = (75, 50, 30)
SHIRT_CYAN = (50, 160, 200)
SHIRT_DARK_CYAN = (35, 120, 160)
PANTS_INDIGO = (40, 50, 140)
PANTS_SHADOW = (28, 35, 100)
SHOE_GRAY = (80, 80, 80)
EYE_WHITE = (255, 255, 255)
EYE_PUPIL = (30, 30, 60)

# Agent variant 2 (different shirt color)
SHIRT_RED = (200, 50, 50)
SHIRT_DARK_RED = (150, 35, 35)

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
STEAM_WHITE = (210, 210, 230)
STEAM_FADE = (150, 150, 170)
LEAF_GREEN = (50, 150, 50)
LEAF_DARK = (30, 110, 30)
POT_TERRACOTTA = (180, 100, 60)
CHAIR_DARK = (60, 50, 40)

# ---------------------------------------------------------------------------
# UI / effects
# ---------------------------------------------------------------------------
WARNING_RED = (220, 40, 40)
WARNING_YELLOW = (255, 210, 50)
GEAR_PURPLE = (160, 80, 200)
GEAR_DARK = (120, 55, 155)
CONVEYOR_GRAY = (150, 150, 160)
CONVEYOR_DARK = (110, 110, 120)
PROGRESS_GREEN = (50, 220, 50)
PROGRESS_BG = (50, 50, 55)
THOUGHT_CLOUD = (220, 220, 240)
THOUGHT_DARK = (180, 180, 200)

# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
BG_BLACK = (10, 10, 15)
BG_DARK = (20, 20, 28)

# Transparent sentinel
TRANSPARENT: tuple[int, int, int] | None = None
