"""Activity detection for ClaudeLab.

Detects what Claude Code is currently doing through three mechanisms:

1. **Hook state file** -- The ClaudeLab hook script writes the current
   activity to ``~/.claudelab/state``.  This is the primary source.
2. **JSONL log watching** -- Watches Claude Code's JSONL log files under
   ``~/.claude/projects/`` for recent entries.
3. **inotify (via ctypes)** -- Monitors the working directory for file-
   system changes without any external dependencies.

The public API is a single function:

    get_current_activity() -> str

returning one of: ``"thinking"``, ``"coding"``, ``"debugging"``,
``"running"``, ``"building"``, ``"idle"``.
"""

from __future__ import annotations

import ctypes
import ctypes.util
import glob
import json
import os
import struct
import threading
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_ACTIVITIES = frozenset(
    {"thinking", "coding", "debugging", "running", "building", "idle"}
)
DEFAULT_ACTIVITY = "idle"

STATE_FILE = Path.home() / ".claudelab" / "state"
CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Timeouts (seconds)
_THINKING_TIMEOUT = 10
_IDLE_TIMEOUT = 60

# inotify constants (Linux)
IN_MODIFY = 0x00000002
IN_CREATE = 0x00000100
IN_DELETE = 0x00000200
IN_MOVED_TO = 0x00000080
IN_ALL = IN_MODIFY | IN_CREATE | IN_DELETE | IN_MOVED_TO

# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_last_activity: str = DEFAULT_ACTIVITY
_last_event_time: float = 0.0
_inotify_thread: threading.Thread | None = None
_log_thread: threading.Thread | None = None
_stop_event = threading.Event()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_current_activity() -> str:
    """Return the current detected activity as a string."""
    # 1. Try the hook state file (primary, most reliable)
    activity = _read_state_file()
    if activity is not None:
        return activity

    # 2. Check elapsed time since last filesystem event
    with _lock:
        elapsed = time.monotonic() - _last_event_time if _last_event_time else float("inf")
        last = _last_activity

    if elapsed < _THINKING_TIMEOUT:
        return last
    if elapsed < _IDLE_TIMEOUT:
        return "thinking"
    return "idle"


def start_detection(watch_dir: str | None = None) -> None:
    """Start background detection threads.

    Parameters
    ----------
    watch_dir:
        Directory to watch with inotify.  Defaults to the current
        working directory.
    """
    global _inotify_thread, _log_thread
    _stop_event.clear()

    # Ensure state directory exists
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # inotify filesystem watcher
    if watch_dir is None:
        watch_dir = os.getcwd()
    _inotify_thread = threading.Thread(
        target=_inotify_watcher,
        args=(watch_dir,),
        daemon=True,
        name="claudelab-inotify",
    )
    _inotify_thread.start()

    # Log watcher
    _log_thread = threading.Thread(
        target=_log_watcher,
        daemon=True,
        name="claudelab-logwatch",
    )
    _log_thread.start()


def stop_detection() -> None:
    """Signal background threads to stop."""
    _stop_event.set()


# ---------------------------------------------------------------------------
# State file reader
# ---------------------------------------------------------------------------

def _read_state_file() -> str | None:
    """Read the hook-written state file and return the activity if fresh."""
    try:
        if not STATE_FILE.exists():
            return None
        stat = STATE_FILE.stat()
        age = time.time() - stat.st_mtime
        if age > _IDLE_TIMEOUT:
            return "idle"
        if age > _THINKING_TIMEOUT:
            return "thinking"
        text = STATE_FILE.read_text().strip().lower()
        if text in VALID_ACTIVITIES:
            return text
    except OSError:
        pass
    return None


# ---------------------------------------------------------------------------
# inotify watcher (via ctypes, no external deps)
# ---------------------------------------------------------------------------

def _inotify_watcher(watch_dir: str) -> None:
    """Watch *watch_dir* for filesystem changes using Linux inotify."""
    libc_name = ctypes.util.find_library("c")
    if libc_name is None:
        return  # Not on Linux or libc unavailable
    try:
        libc = ctypes.CDLL(libc_name, use_errno=True)
    except OSError:
        return

    # Ensure the functions exist
    for fn_name in ("inotify_init", "inotify_add_watch"):
        if not hasattr(libc, fn_name):
            return

    fd = libc.inotify_init()
    if fd < 0:
        return

    try:
        wd = libc.inotify_add_watch(
            fd,
            watch_dir.encode("utf-8"),
            ctypes.c_uint32(IN_ALL),
        )
        if wd < 0:
            return

        buf_size = 4096
        while not _stop_event.is_set():
            # Use select to avoid blocking forever
            import select

            rlist, _, _ = select.select([fd], [], [], 1.0)
            if not rlist:
                continue
            data = os.read(fd, buf_size)
            if not data:
                continue
            _process_inotify_events(data)
    finally:
        os.close(fd)


def _process_inotify_events(data: bytes) -> None:
    """Parse raw inotify event data and update shared state."""
    offset = 0
    while offset < len(data):
        # struct inotify_event: int wd, uint32_t mask, uint32_t cookie, uint32_t len
        if offset + 16 > len(data):
            break
        _wd, mask, _cookie, name_len = struct.unpack_from("iIII", data, offset)
        offset += 16

        name_bytes = data[offset : offset + name_len]
        offset += name_len
        name = name_bytes.rstrip(b"\x00").decode("utf-8", errors="replace")

        activity = _classify_fs_event(mask, name)
        with _lock:
            global _last_activity, _last_event_time
            _last_activity = activity
            _last_event_time = time.monotonic()


def _classify_fs_event(mask: int, name: str) -> str:
    """Map an inotify event to an activity string."""
    lower = name.lower()

    # Source code changes -> coding
    code_exts = (
        ".py", ".js", ".ts", ".jsx", ".tsx", ".rs", ".go", ".java",
        ".c", ".cpp", ".h", ".rb", ".sh", ".toml", ".yaml", ".yml",
        ".json", ".html", ".css",
    )
    if any(lower.endswith(ext) for ext in code_exts):
        if mask & IN_MODIFY:
            return "coding"
        if mask & (IN_CREATE | IN_MOVED_TO):
            return "building"

    # Build / config artifacts
    build_names = ("build", "dist", "target", "node_modules", "__pycache__")
    if any(bn in lower for bn in build_names):
        return "building"

    # Test / log files
    if "test" in lower or "spec" in lower:
        return "running"

    # Default for any write activity
    if mask & IN_MODIFY:
        return "coding"

    return "coding"


# ---------------------------------------------------------------------------
# Log watcher -- parse Claude Code JSONL logs
# ---------------------------------------------------------------------------

def _log_watcher() -> None:
    """Periodically scan Claude Code JSONL logs for recent activity."""
    while not _stop_event.is_set():
        try:
            _scan_claude_logs()
        except Exception:
            pass
        # Don't scan too aggressively
        _stop_event.wait(3.0)


def _scan_claude_logs() -> None:
    """Look for the most recent JSONL log and classify the last entry."""
    if not CLAUDE_PROJECTS_DIR.exists():
        return

    # Find most recent .jsonl file
    pattern = str(CLAUDE_PROJECTS_DIR / "**" / "*.jsonl")
    jsonl_files = glob.glob(pattern, recursive=True)
    if not jsonl_files:
        return

    # Sort by mtime, pick newest
    try:
        newest = max(jsonl_files, key=os.path.getmtime)
    except (OSError, ValueError):
        return

    # Only read if modified recently (last 30 seconds)
    try:
        mtime = os.path.getmtime(newest)
    except OSError:
        return
    if time.time() - mtime > 30:
        return

    # Read last few lines
    try:
        with open(newest, "r", errors="replace") as f:
            # Seek near the end for efficiency
            try:
                f.seek(0, 2)
                size = f.tell()
                f.seek(max(0, size - 4096))
            except OSError:
                f.seek(0)
            lines = f.readlines()
    except OSError:
        return

    if not lines:
        return

    # Parse the last valid JSON line
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue

        activity = _classify_log_entry(entry)
        if activity:
            with _lock:
                global _last_activity, _last_event_time
                _last_activity = activity
                _last_event_time = time.monotonic()
        break


def _classify_log_entry(entry: dict) -> str | None:
    """Classify a JSONL log entry into an activity."""
    # Look for tool use patterns
    msg_type = entry.get("type", "")
    tool = entry.get("tool", "")
    content = str(entry.get("content", ""))

    if "error" in content.lower() or "error" in msg_type.lower():
        return "debugging"

    if tool in ("Edit", "Write", "MultiEdit"):
        return "coding"

    if tool in ("Bash", "bash"):
        cmd = str(entry.get("command", ""))
        if any(kw in cmd for kw in ("test", "pytest", "npm test", "cargo test")):
            return "running"
        if any(kw in cmd for kw in ("build", "compile", "make", "npm run")):
            return "building"
        return "running"

    if tool in ("Read", "Glob", "Grep"):
        return "thinking"

    if msg_type == "assistant":
        return "thinking"

    return None
