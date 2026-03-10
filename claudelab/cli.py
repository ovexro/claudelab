"""ClaudeLab CLI commands -- install, doctor, uninstall.

Provides automatic setup and diagnostics so users don't need to
manually edit configuration files.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Shared state file -- /tmp is world-writable, works regardless of which user
# runs Claude Code vs ClaudeLab.  Ephemeral by nature (cleared on reboot),
# which is fine since activity state is transient.
STATE_FILE = Path("/tmp/claudelab.state")

# Where Claude Code stores its settings
CLAUDE_SETTINGS = Path.home() / ".claude" / "settings.json"

HOOK_EVENTS = ("PreToolUse", "PostToolUse", "PostToolUseFailure")


def _find_hook_script() -> Path | None:
    """Locate the ClaudeLab hook script.

    Search order:
    1. Next to this package (git clone / editable install)
    2. Installed via pip (alongside the package in site-packages)
    3. Common clone locations
    """
    # 1. Relative to this file (repo layout: claudelab/cli.py -> ../hooks/)
    repo_hook = Path(__file__).resolve().parent.parent / "hooks" / "claudelab-hook.sh"
    if repo_hook.exists():
        return repo_hook

    # 2. Check if installed as package data
    try:
        import importlib.resources as ir
        ref = ir.files("claudelab") / "hooks" / "claudelab-hook.sh"
        if hasattr(ref, "_path") and Path(ref._path).exists():
            return Path(ref._path)
    except Exception:
        pass

    # 3. Common locations
    for candidate in [
        Path.home() / "claudelab" / "hooks" / "claudelab-hook.sh",
        Path("/opt/claudelab/hooks/claudelab-hook.sh"),
        Path("/usr/local/share/claudelab/hooks/claudelab-hook.sh"),
    ]:
        if candidate.exists():
            return candidate

    return None


def _read_settings() -> dict:
    """Read Claude Code settings.json, returning empty dict if missing."""
    if not CLAUDE_SETTINGS.exists():
        return {}
    try:
        return json.loads(CLAUDE_SETTINGS.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _write_settings(data: dict) -> None:
    """Write Claude Code settings.json with proper formatting."""
    CLAUDE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    CLAUDE_SETTINGS.write_text(json.dumps(data, indent=2) + "\n")


def _make_hook_entry(hook_path: str) -> dict:
    """Create a single hook config entry."""
    return {
        "matcher": "",
        "hooks": [
            {
                "type": "command",
                "command": hook_path,
            }
        ],
    }


def _hooks_already_installed(settings: dict, hook_path: str) -> bool:
    """Check if ClaudeLab hooks are already present in settings."""
    hooks = settings.get("hooks", {})
    for event in HOOK_EVENTS:
        entries = hooks.get(event, [])
        for entry in entries:
            for h in entry.get("hooks", []):
                if h.get("command", "") == hook_path:
                    return True
    return False


# ---------------------------------------------------------------------------
# install
# ---------------------------------------------------------------------------

def cmd_install() -> int:
    """Auto-configure ClaudeLab hooks in Claude Code settings."""
    print("ClaudeLab Install")
    print("=" * 40)

    # 1. Find hook script
    hook_path = _find_hook_script()
    if hook_path is None:
        print("\n[ERROR] Could not find claudelab-hook.sh")
        print("  Expected locations:")
        print("  - ./hooks/claudelab-hook.sh (git clone)")
        print("  - ~/claudelab/hooks/claudelab-hook.sh")
        print("\n  If you installed via pip, try reinstalling:")
        print("  pip install claudelab")
        return 1

    hook_str = str(hook_path)
    print(f"\n[1/4] Found hook script: {hook_str}")

    # 2. Make executable
    current_mode = hook_path.stat().st_mode
    if not (current_mode & stat.S_IXUSR):
        hook_path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print("[2/4] Made hook script executable")
    else:
        print("[2/4] Hook script already executable")

    # 3. Configure Claude Code settings
    settings = _read_settings()

    if _hooks_already_installed(settings, hook_str):
        print("[3/4] Hooks already configured in Claude Code settings")
    else:
        hooks = settings.get("hooks", {})
        for event in HOOK_EVENTS:
            existing = hooks.get(event, [])
            existing.append(_make_hook_entry(hook_str))
            hooks[event] = existing
        settings["hooks"] = hooks
        _write_settings(settings)
        print(f"[3/4] Added hooks to {CLAUDE_SETTINGS}")

    # 4. Test state file is writable
    try:
        STATE_FILE.write_text("idle")
        print(f"[4/4] State file OK: {STATE_FILE}")
    except OSError as e:
        print(f"[4/4] WARNING: Cannot write state file {STATE_FILE}: {e}")

    # Success
    print("\n" + "=" * 40)
    print("ClaudeLab installed successfully!")
    print("\nUsage:")
    print("  1. Open a new terminal (or tmux pane)")
    print("  2. Run: claudelab")
    print("  3. Use Claude Code in another terminal")
    print("  4. Watch your AI engineers react!\n")
    return 0


# ---------------------------------------------------------------------------
# doctor
# ---------------------------------------------------------------------------

def cmd_doctor() -> int:
    """Diagnose ClaudeLab setup and report issues."""
    print("ClaudeLab Doctor")
    print("=" * 40)
    issues = 0

    # 1. Hook script
    hook_path = _find_hook_script()
    if hook_path is None:
        print("\n[FAIL] Hook script not found")
        print("  Fix: Run 'claudelab install'")
        issues += 1
    else:
        is_exec = os.access(hook_path, os.X_OK)
        if is_exec:
            print(f"\n[ OK ] Hook script: {hook_path}")
        else:
            print(f"\n[FAIL] Hook script not executable: {hook_path}")
            print(f"  Fix: chmod +x {hook_path}")
            issues += 1

    # 2. Claude Code settings
    if not CLAUDE_SETTINGS.exists():
        print("[FAIL] Claude Code settings not found")
        print(f"  Expected: {CLAUDE_SETTINGS}")
        print("  Fix: Run 'claudelab install'")
        issues += 1
    else:
        settings = _read_settings()
        hooks = settings.get("hooks", {})
        hook_str = str(hook_path) if hook_path else ""

        if not hooks:
            print("[FAIL] No hooks configured in Claude Code settings")
            print("  Fix: Run 'claudelab install'")
            issues += 1
        elif hook_str and _hooks_already_installed(settings, hook_str):
            print("[ OK ] Hooks configured in Claude Code settings")
        else:
            print("[WARN] Hooks exist but ClaudeLab hook not found")
            print("  Fix: Run 'claudelab install'")
            issues += 1

    # 3. State file
    if STATE_FILE.exists():
        try:
            content = STATE_FILE.read_text().strip()
            age = time.time() - STATE_FILE.stat().st_mtime
            if age < 60:
                print(f"[ OK ] State file: {STATE_FILE} (value={content!r}, {age:.0f}s ago)")
            elif age < 300:
                print(f"[WARN] State file is stale: {age:.0f}s old (value={content!r})")
                print("  This is normal if Claude Code hasn't been used recently")
            else:
                print(f"[WARN] State file very stale: {age:.0f}s old")
                print("  Hooks may not be firing. Try using Claude Code and check again")
                issues += 1
        except OSError as e:
            print(f"[FAIL] Cannot read state file: {e}")
            issues += 1
    else:
        print(f"[WARN] State file not found: {STATE_FILE}")
        print("  This is normal if Claude Code hasn't been used since install")

    # 4. State file writable
    try:
        test_file = STATE_FILE.parent / ".claudelab-test"
        test_file.write_text("test")
        test_file.unlink()
        print(f"[ OK ] State directory writable: {STATE_FILE.parent}")
    except OSError:
        print(f"[FAIL] Cannot write to {STATE_FILE.parent}")
        issues += 1

    # 5. Python version
    py_ver = sys.version_info
    if py_ver >= (3, 10):
        print(f"[ OK ] Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    else:
        print(f"[FAIL] Python {py_ver.major}.{py_ver.minor} — need 3.10+")
        issues += 1

    # 6. Terminal capabilities
    term = os.environ.get("TERM", "unknown")
    colorterm = os.environ.get("COLORTERM", "")
    print(f"[INFO] Terminal: TERM={term}, COLORTERM={colorterm}")

    # Summary
    print("\n" + "=" * 40)
    if issues == 0:
        print("All checks passed! ClaudeLab is ready.")
    else:
        print(f"Found {issues} issue(s). Run 'claudelab install' to fix.")
    return 1 if issues > 0 else 0


# ---------------------------------------------------------------------------
# uninstall
# ---------------------------------------------------------------------------

def cmd_uninstall() -> int:
    """Remove ClaudeLab hooks from Claude Code settings."""
    print("ClaudeLab Uninstall")
    print("=" * 40)

    # 1. Remove hooks from settings
    if CLAUDE_SETTINGS.exists():
        settings = _read_settings()
        hooks = settings.get("hooks", {})
        removed = 0

        for event in HOOK_EVENTS:
            entries = hooks.get(event, [])
            new_entries = []
            for entry in entries:
                hook_list = entry.get("hooks", [])
                filtered = [h for h in hook_list if "claudelab" not in h.get("command", "").lower()]
                if filtered:
                    entry["hooks"] = filtered
                    new_entries.append(entry)
                elif hook_list:
                    removed += len(hook_list) - len(filtered)
            if new_entries:
                hooks[event] = new_entries
            elif event in hooks:
                del hooks[event]
                removed += 1

        if not hooks:
            settings.pop("hooks", None)

        if removed > 0:
            _write_settings(settings)
            print(f"\n[OK] Removed ClaudeLab hooks from {CLAUDE_SETTINGS}")
        else:
            print("\n[OK] No ClaudeLab hooks found in settings")
    else:
        print("\n[OK] No Claude Code settings file found")

    # 2. Clean up state file
    if STATE_FILE.exists():
        try:
            STATE_FILE.unlink()
            print(f"[OK] Removed state file: {STATE_FILE}")
        except OSError:
            print(f"[WARN] Could not remove {STATE_FILE}")

    print("\nClaudeLab uninstalled. Your Claude Code settings are preserved.")
    print("To reinstall: claudelab install\n")
    return 0
