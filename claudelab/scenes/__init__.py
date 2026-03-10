"""Scene modules for ClaudeLab.

Each scene module exposes:

    get_frames(width: int, height: int) -> list[list[str]]       # ASCII mode
    get_frames(width: int, height: int) -> list[PixelBuffer]     # Voxel mode

returning a list of animation frames.
"""

from __future__ import annotations

from claudelab.scenes import thinking, coding, debugging, running, building, idle

SCENE_MAP: dict[str, object] = {
    "thinking": thinking,
    "coding": coding,
    "debugging": debugging,
    "running": running,
    "building": building,
    "idle": idle,
}


def get_scene_frames(activity: str, width: int, height: int) -> list[list[str]]:
    """Return ASCII animation frames for the given *activity*."""
    module = SCENE_MAP.get(activity)
    if module is None:
        module = idle
    return module.get_frames(width, height)  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Voxel mode
# ---------------------------------------------------------------------------

_VOXEL_MAP: dict[str, object] | None = None


def _load_voxel_scenes() -> dict[str, object]:
    global _VOXEL_MAP
    if _VOXEL_MAP is None:
        from claudelab.scenes import (
            voxel_thinking, voxel_coding, voxel_debugging,
            voxel_running, voxel_building, voxel_idle,
        )
        _VOXEL_MAP = {
            "thinking": voxel_thinking,
            "coding": voxel_coding,
            "debugging": voxel_debugging,
            "running": voxel_running,
            "building": voxel_building,
            "idle": voxel_idle,
        }
    return _VOXEL_MAP


def get_voxel_scene_frames(activity: str, width: int, height: int) -> list:
    """Return voxel (PixelBuffer) animation frames for the given *activity*."""
    scenes = _load_voxel_scenes()
    module = scenes.get(activity)
    if module is None:
        module = scenes["idle"]
    return module.get_frames(width, height)  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Isometric mode
# ---------------------------------------------------------------------------

_ISO_MAP: dict[str, object] | None = None


def _load_iso_scenes() -> dict[str, object]:
    global _ISO_MAP
    if _ISO_MAP is None:
        from claudelab.scenes import iso_coding
        # For now, all activities use iso_coding as the proof of concept
        _ISO_MAP = {
            "thinking": iso_coding,
            "coding": iso_coding,
            "debugging": iso_coding,
            "running": iso_coding,
            "building": iso_coding,
            "idle": iso_coding,
        }
    return _ISO_MAP


def get_iso_scene_frames(activity: str, width: int, height: int) -> list:
    """Return isometric (PixelBuffer) animation frames for the given *activity*."""
    scenes = _load_iso_scenes()
    module = scenes.get(activity)
    if module is None:
        module = scenes["idle"]
    return module.get_frames(width, height)  # type: ignore[union-attr]
