"""Voxel-style agent sprites for ClaudeLab.

Each sprite is defined as character-art with a color legend, then
converted to a :class:`~claudelab.pixelbuffer.Sprite` via
``Sprite.from_pixel_art``.  Agents are Minecraft-Steve-like block
characters ~8 pixels wide by 12 pixels tall (= 6 terminal rows).
"""

from __future__ import annotations

from claudelab.palette import (
    HAIR_BROWN, SKIN, SKIN_SHADOW,
    SHIRT_CYAN, SHIRT_DARK_CYAN,
    SHIRT_RED, SHIRT_DARK_RED,
    PANTS_INDIGO, PANTS_SHADOW,
    SHOE_GRAY, EYE_WHITE, EYE_PUPIL,
    COFFEE_BROWN, COFFEE_CREAM,
    GOLD_BLOCK, LAPIS,
)
from claudelab.pixelbuffer import Sprite

# ---------------------------------------------------------------------------
# Color legends
# ---------------------------------------------------------------------------

_AGENT1 = {
    "H": HAIR_BROWN,
    "S": SKIN,
    "s": SKIN_SHADOW,
    "W": EYE_WHITE,
    "E": EYE_PUPIL,
    "C": SHIRT_CYAN,
    "c": SHIRT_DARK_CYAN,
    "P": PANTS_INDIGO,
    "p": PANTS_SHADOW,
    "G": SHOE_GRAY,
    ".": None,
}

_AGENT2 = {
    "H": HAIR_BROWN,
    "S": SKIN,
    "s": SKIN_SHADOW,
    "W": EYE_WHITE,
    "E": EYE_PUPIL,
    "C": SHIRT_RED,
    "c": SHIRT_DARK_RED,
    "P": PANTS_INDIGO,
    "p": PANTS_SHADOW,
    "G": SHOE_GRAY,
    ".": None,
}

# ---------------------------------------------------------------------------
# Sitting agents (at desk)
# ---------------------------------------------------------------------------

_SIT_IDLE = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCC.",
    ".CCCCCC.",
    "..CCCC..",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

_SIT_TYPE_L = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..sSss..",
    ".CCCCCC.",
    ".CCCCCC.",
    "cCC..CC.",
    "c.......",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

_SIT_TYPE_R = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..sSss..",
    ".CCCCCC.",
    ".CCCCCC.",
    ".CC..CCc",
    ".......c",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

_SIT_TYPE_BOTH = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..sSss..",
    ".CCCCCC.",
    ".CCCCCC.",
    "cCC..CCc",
    "c......c",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

# ---------------------------------------------------------------------------
# Standing agents
# ---------------------------------------------------------------------------

_STAND = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCC.",
    ".CCCCCC.",
    ".CC..CC.",
    ".CC..CC.",
    "..PPPP..",
    "..PPPP..",
    "..PP.PP.",
    "..GG.GG.",
]

_STAND_POINT = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCCc",
    ".CCCCCCc",
    ".CC....c",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PP.PP.",
    "..GG.GG.",
]

_STAND_EXAMINE = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCC.",
    ".CCCCCC.",
    ".CC..CC.",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PP.PP.",
    "..GG.GG.",
]

# ---------------------------------------------------------------------------
# Walking agents
# ---------------------------------------------------------------------------

_WALK_1 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCC.",
    ".CCCCCC.",
    ".CC..CC.",
    ".CC..CC.",
    "..PPPP..",
    "..PPPP..",
    ".PP...PP",
    ".GG...GG",
]

_WALK_2 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCC.",
    ".CCCCCC.",
    ".CC..CC.",
    ".CC..CC.",
    "..PPPP..",
    "..PPPP..",
    "..PP.PP.",
    "..GG.GG.",
]

# ---------------------------------------------------------------------------
# Carrying (walking + block in hand)
# ---------------------------------------------------------------------------

_CARRY_BLOCK = {
    "H": HAIR_BROWN,
    "S": SKIN,
    "s": SKIN_SHADOW,
    "W": EYE_WHITE,
    "E": EYE_PUPIL,
    "C": SHIRT_CYAN,
    "c": SHIRT_DARK_CYAN,
    "P": PANTS_INDIGO,
    "p": PANTS_SHADOW,
    "G": SHOE_GRAY,
    "B": GOLD_BLOCK,  # the block being carried
    "b": LAPIS,
    ".": None,
}

_CARRY_1 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCCBB",
    ".CCCCCCBB",
    ".CC..CC..",
    ".CC..CC..",
    "..PPPP...",
    "..PPPP...",
    ".PP...PP.",
    ".GG...GG.",
]

_CARRY_2 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCCbb",
    ".CCCCCCbb",
    ".CC..CC..",
    ".CC..CC..",
    "..PPPP...",
    "..PPPP...",
    "..PP.PP..",
    "..GG.GG..",
]

# ---------------------------------------------------------------------------
# Drinking coffee
# ---------------------------------------------------------------------------

_DRINK_MAP = {
    **_AGENT1,
    "K": COFFEE_BROWN,
    "k": COFFEE_CREAM,
}

_DRINK_1 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSSKk",
    ".CCCCCC.",
    ".CCCCCC.",
    "..CCCC..",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

_DRINK_2 = [
    "..HHHH..",
    "..HHHHKk",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCC.",
    ".CCCCCC.",
    "..CCCC..",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

# ---------------------------------------------------------------------------
# Leaning back (idle)
# ---------------------------------------------------------------------------

_LEAN = [
    "...HHHH.",
    "...HHHH.",
    "..SWESWs",
    "...SSSS.",
    "..CCCCCC",
    "..CCCCCC",
    "...CCCC.",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PPPP..",
    "..GGGG..",
]

# ---------------------------------------------------------------------------
# Button push (running scene)
# ---------------------------------------------------------------------------

_PUSH_1 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    ".CCCCCCc",
    ".CCCCCCc",
    ".CC.....",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PP.PP.",
    "..GG.GG.",
]

_PUSH_2 = [
    "..HHHH..",
    "..HHHH..",
    ".SWESWE.",
    "..SSSS..",
    "cCCCCCC.",
    "cCCCCCC.",
    ".....CC.",
    "........",
    "..PPPP..",
    "..PPPP..",
    "..PP.PP.",
    "..GG.GG.",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _make(rows: list[str], cmap: dict) -> Sprite:
    return Sprite.from_pixel_art(rows, cmap)


# Pre-built sprite objects
SITTING_IDLE_1 = _make(_SIT_IDLE, _AGENT1)
SITTING_IDLE_2 = _make(_SIT_IDLE, _AGENT2)

SITTING_TYPING = [
    _make(_SIT_TYPE_L, _AGENT1),
    _make(_SIT_TYPE_R, _AGENT1),
    _make(_SIT_TYPE_BOTH, _AGENT1),
    _make(_SIT_IDLE, _AGENT1),
]

SITTING_TYPING_2 = [
    _make(_SIT_TYPE_L, _AGENT2),
    _make(_SIT_TYPE_R, _AGENT2),
    _make(_SIT_TYPE_BOTH, _AGENT2),
    _make(_SIT_IDLE, _AGENT2),
]

STANDING_NEUTRAL_1 = _make(_STAND, _AGENT1)
STANDING_NEUTRAL_2 = _make(_STAND, _AGENT2)

STANDING_POINTING = [
    _make(_STAND_POINT, _AGENT1),
    _make(_STAND, _AGENT1),
]

STANDING_EXAMINING = [
    _make(_STAND_EXAMINE, _AGENT2),
    _make(_STAND, _AGENT2),
]

WALKING = [
    _make(_WALK_1, _AGENT1),
    _make(_WALK_2, _AGENT1),
]

CARRYING = [
    _make(_CARRY_1, _CARRY_BLOCK),
    _make(_CARRY_2, _CARRY_BLOCK),
]

DRINKING = [
    _make(_DRINK_1, _DRINK_MAP),
    _make(_DRINK_2, _DRINK_MAP),
    _make(_DRINK_1, _DRINK_MAP),
]

LEANING = _make(_LEAN, _AGENT2)

BUTTON_PUSH = [
    _make(_PUSH_1, _AGENT1),
    _make(_PUSH_2, _AGENT1),
    _make(_STAND, _AGENT1),
]
