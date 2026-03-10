"""NES-quality agent sprites for ClaudeLab voxel renderer.

Sprites are 16px wide x 20px tall (8 terminal columns, 10 rows) with
1-pixel outlines and 3-tone directional shading (light from upper-left).
"""

from __future__ import annotations

from claudelab.palette import (
    OUTLINE,
    SKIN_HIGHLIGHT, SKIN, SKIN_SHADOW, SKIN_DARK,
    HAIR_HIGHLIGHT, HAIR_BROWN, HAIR_DARK,
    SHIRT_CYAN_LIGHT, SHIRT_CYAN, SHIRT_DARK_CYAN,
    SHIRT_RED_LIGHT, SHIRT_RED, SHIRT_DARK_RED,
    PANTS_LIGHT, PANTS_INDIGO, PANTS_SHADOW,
    SHOE_HIGHLIGHT, SHOE_GRAY,
    EYE_WHITE, EYE_PUPIL,
    COFFEE_BROWN, COFFEE_CREAM, COFFEE_MUG,
    GOLD_BLOCK, LAPIS, DIAMOND,
    KEYBOARD_DARK, KEYBOARD_KEY,
)
from claudelab.pixelbuffer import Sprite

# ---------------------------------------------------------------------------
# Color legends — "O"=outline, 3 tones per material
# ---------------------------------------------------------------------------

_AGENT1 = {
    "O": OUTLINE,
    # Hair: 1=highlight, H=base, h=dark
    "1": HAIR_HIGHLIGHT, "H": HAIR_BROWN, "h": HAIR_DARK,
    # Skin: L=highlight, S=base, s=shadow, d=dark
    "L": SKIN_HIGHLIGHT, "S": SKIN, "s": SKIN_SHADOW, "d": SKIN_DARK,
    # Eyes
    "W": EYE_WHITE, "E": EYE_PUPIL,
    # Shirt: T=light, C=base, c=dark
    "T": SHIRT_CYAN_LIGHT, "C": SHIRT_CYAN, "c": SHIRT_DARK_CYAN,
    # Pants: Q=light, P=base, p=dark
    "Q": PANTS_LIGHT, "P": PANTS_INDIGO, "p": PANTS_SHADOW,
    # Shoes: g=highlight, G=base
    "g": SHOE_HIGHLIGHT, "G": SHOE_GRAY,
    ".": None,
}

_AGENT2 = {
    **_AGENT1,
    "T": SHIRT_RED_LIGHT, "C": SHIRT_RED, "c": SHIRT_DARK_RED,
}

# ---------------------------------------------------------------------------
# Sitting idle (at desk, relaxed)
# ---------------------------------------------------------------------------

_SIT_IDLE = [
    "......OOOOOO....",  # 0  hair top outline
    ".....O1HHHH1O...",  # 1  hair highlight edges
    ".....OHHHHH1O...",  # 2  hair mid
    "....OOHHHHHhOO..",  # 3  hair bottom + ear hints
    "....OLWESWLEO...",  # 4  eyes row
    "....OSSdSdSSO...",  # 5  nose/mouth
    ".....OSSSSO.....",  # 6  neck
    "...OOTTCCTTOO...",  # 7  shoulders
    "...OCCCCCCCCcO..",  # 8  torso upper
    "...OCCCCCCCCcO..",  # 9  torso mid
    "....OcCCCCcO....",  # 10 torso lower
    "....OccccccO....",  # 11 waist
    "....OQPPPPQO....",  # 12 hips
    "....OPPPPPPO....",  # 13 upper legs
    "....OPPPpPPO....",  # 14 legs
    "....OPPpOpPPO...",  # 15 legs separating
    "....OppOOppO....",  # 16 lower legs
    "...OgGGOOgGGO...",  # 17 feet
    "...OGGGOOOGGO...",  # 18 feet base
    "....OOO..OOO....",  # 19 feet outline
]

# ---------------------------------------------------------------------------
# Sitting typing (3 poses for animation)
# ---------------------------------------------------------------------------

_SIT_TYPE_L = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "..OcCCCCCCCCcO..",
    "..Oc...OCCCcO...",
    "..O....OccccO...",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPO....",
    "....OPPpOpPPO...",
    "....OppOOppO....",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

_SIT_TYPE_R = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OCCCcO...cO..",
    "...OccccO....O..",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPO....",
    "....OPPpOpPPO...",
    "....OppOOppO....",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

_SIT_TYPE_BOTH = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "..OcCCCCCCCCcO..",
    "..OcCCCCCCCCcO..",
    "..Oc..OCCCc..O..",
    "..O...Occcc..O..",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPO....",
    "....OPPpOpPPO...",
    "....OppOOppO....",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

# ---------------------------------------------------------------------------
# Standing (neutral, pointing, examining)
# ---------------------------------------------------------------------------

_STAND = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OcCCCCCCcO...",
    "...OcCC..CCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPPO...",
    "....OPPpO.pPPO..",
    "...OgGGO..OgGGO.",
    "...OGGGO..OOGGO.",
    "....OOO....OOO..",
]

_STAND_POINT = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOOOO.",
    "...OCCCCCCCCcccO",
    "...OCCCCCCCCcccO",
    "...OcCCCCCCcOOsO",
    "...OcCC..CCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPPO...",
    "....OPPpO.pPPO..",
    "...OgGGO..OgGGO.",
    "...OGGGO..OOGGO.",
    "....OOO....OOO..",
]

_STAND_EXAMINE = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OcCCCCCCcO...",
    "....OCC..CCO....",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPPO...",
    "....OPPpO.pPPO..",
    "...OgGGO..OgGGO.",
    "...OGGGO..OOGGO.",
    "....OOO....OOO..",
]

# ---------------------------------------------------------------------------
# Walking (2 frames)
# ---------------------------------------------------------------------------

_WALK_1 = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OcCCCCCCcO...",
    "...OcCC..CCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "...OPPPpO.pPPO..",
    "..OPPpO....pPPO.",
    "..OgGGO...OgGGO.",
    "..OGGGO...OOGGO.",
    "...OOO.....OOO..",
]

_WALK_2 = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OcCCCCCCcO...",
    "...OcCC..CCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPpOpPPO...",
    "....OPPpOpPPO...",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

# ---------------------------------------------------------------------------
# Carrying block overhead (2 walk-cycle frames)
# ---------------------------------------------------------------------------

_CARRY_MAP = {
    **_AGENT1,
    "B": GOLD_BLOCK, "b": LAPIS, "D": DIAMOND,
}

_CARRY_1 = [
    "....OBBBBBO.....",
    "....ObBBBbO.....",
    "....OOOOOOO.....",
    ".....OsSssSO....",
    ".....O1HHHHO....",
    "....OOHHHH1OO...",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OcCCCCCCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "...OPPPpO.pPPO..",
    "..OPPpO....pPPO.",
    "..OgGGO...OgGGO.",
    "..OGGGO...OOGGO.",
    "...OOO.....OOO..",
]

_CARRY_2 = [
    "....OBBBBBO.....",
    "....ObBBBbO.....",
    "....OOOOOOO.....",
    ".....OsSssSO....",
    ".....O1HHHHO....",
    "....OOHHHH1OO...",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "...OcCCCCCCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPpOpPPO...",
    "....OPPpOpPPO...",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

# ---------------------------------------------------------------------------
# Drinking coffee (2 frames)
# ---------------------------------------------------------------------------

_DRINK_MAP = {
    **_AGENT1,
    "K": COFFEE_BROWN, "k": COFFEE_CREAM, "M": COFFEE_MUG,
}

_DRINK_1 = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcOMO",
    "....OcCCCCcOOMkO",
    "....OccccccOOKOO",
    "....OQPPPPQO.OO.",
    "....OPPPPPPO....",
    "....OPPPpPPO....",
    "....OPPpOpPPO...",
    "....OppOOppO....",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

_DRINK_2 = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOMO.",
    "....OLWESWLEOMkO",
    "....OSSdSdSSOOKO",
    ".....OSSSSO..OO.",
    "...OOTTCCTTOO...",
    "...OCCCCCCCCcO..",
    "...OCCCCCCCCcO..",
    "....OcCCCCcO....",
    "....OccccccO....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPO....",
    "....OPPpOpPPO...",
    "....OppOOppO....",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
]

# ---------------------------------------------------------------------------
# Leaning back in chair (idle scene)
# ---------------------------------------------------------------------------

_LEAN = [
    ".......OOOOOO...",
    "......O1HHHH1O..",
    "......OHHHHH1O..",
    ".....OOHHHHHhOO.",
    ".....OLWESWLEO..",
    ".....OSSdSdSSO..",
    "......OSSSSO....",
    "....OOTTCCTTOO..",
    "....OCCCCCCCCcO.",
    "....OCCCCCCCCcO.",
    ".....OcCCCCcO...",
    ".....OccccccO...",
    ".....OQPPPPQO...",
    ".....OPPPPPPO...",
    ".....OPPPpPPO...",
    ".....OPPpOpPPO..",
    ".....OppOOppO...",
    "....OgGGOOgGGO..",
    "....OGGGOOOGGO..",
    ".....OOO..OOO...",
]

# ---------------------------------------------------------------------------
# Button push (running scene, 2 frames)
# ---------------------------------------------------------------------------

_PUSH_1 = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    "...OOTTCCTTOOOO.",
    "...OCCCCCCCCcccO",
    "...OCCCCCCCCccsO",
    "...OcCCCCCCcOOO.",
    "...OcCC..CCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPPO...",
    "....OPPpO.pPPO..",
    "...OgGGO..OgGGO.",
    "...OGGGO..OOGGO.",
    "....OOO....OOO..",
]

_PUSH_2 = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSO.....",
    ".OOOOTCCCCTTOO..",
    "OcsccCCCCCCCCO..",
    "OsccCCCCCCCCcO..",
    ".OOOcCCCCCCcO...",
    "...OcCC..CCcO...",
    "....OcccccO.....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPPO...",
    "....OPPpO.pPPO..",
    "...OgGGO..OgGGO.",
    "...OGGGO..OOGGO.",
    "....OOO....OOO..",
]

# ---------------------------------------------------------------------------
# Sitting with chin on hand (thinking scene)
# ---------------------------------------------------------------------------

_SIT_THINK = [
    "......OOOOOO....",
    ".....O1HHHH1O...",
    ".....OHHHHH1O...",
    "....OOHHHHHhOO..",
    "....OLWESWLEO...",
    "....OSSdSdSSO...",
    ".....OSSSSsO....",
    "...OOTTCCTTsO...",
    "...OCCCCCCCsLO..",
    "...OCCCCCCCCcO..",
    "....OcCCCCcO....",
    "....OccccccO....",
    "....OQPPPPQO....",
    "....OPPPPPPO....",
    "....OPPPpPPO....",
    "....OPPpOpPPO...",
    "....OppOOppO....",
    "...OgGGOOgGGO...",
    "...OGGGOOOGGO...",
    "....OOO..OOO....",
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

SITTING_THINK_1 = _make(_SIT_THINK, _AGENT1)
SITTING_THINK_2 = _make(_SIT_THINK, _AGENT2)

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
    _make(_CARRY_1, _CARRY_MAP),
    _make(_CARRY_2, _CARRY_MAP),
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
