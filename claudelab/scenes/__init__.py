"""Scene modules for ClaudeLab.

Each scene module exposes:

    get_frames(width: int, height: int) -> list[list[str]]

returning a list of animation frames, where each frame is a list of row
strings ready to be rendered to the terminal.
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
    """Return animation frames for the given *activity*."""
    module = SCENE_MAP.get(activity)
    if module is None:
        module = idle
    return module.get_frames(width, height)  # type: ignore[union-attr]
