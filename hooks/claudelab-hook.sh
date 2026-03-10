#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# ClaudeLab Hook Script
#
# Claude Code hooks receive JSON on stdin with tool_name, hook_event_name, etc.
# This script reads that JSON and writes the detected activity to
# ~/.claudelab/state, which ClaudeLab reads to drive the animation.
#
# Setup:
#   1. Ensure this file is executable: chmod +x claudelab-hook.sh
#   2. Add hooks to ~/.claude/settings.json (see README.md for full config)
# ──────────────────────────────────────────────────────────────────────

# Shared state file in /tmp -- works regardless of which user runs Claude Code
# vs ClaudeLab (no $HOME mismatch issues).
STATE_FILE="/tmp/claudelab.state"

write_state() {
    # Atomic write via temp file to prevent corruption from concurrent calls
    local tmp="${STATE_FILE}.$$"
    printf '%s' "$1" > "${tmp}" && mv -f "${tmp}" "${STATE_FILE}"
}

# Read JSON from stdin and extract all fields in a single Python call
INPUT=$(cat)
eval "$(echo "$INPUT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print('HOOK_EVENT=' + repr(d.get('hook_event_name', '')))
    print('TOOL=' + repr(d.get('tool_name', '')))
    print('HAS_ERROR=' + ('yes' if d.get('error', '') else 'no'))
except Exception:
    print('HOOK_EVENT=')
    print('TOOL=')
    print('HAS_ERROR=no')
" 2>/dev/null)" || { HOOK_EVENT=""; TOOL=""; HAS_ERROR="no"; }

case "${HOOK_EVENT}" in
    PreToolUse)
        case "${TOOL}" in
            Edit|Write|MultiEdit|NotebookEdit)
                write_state "coding"
                ;;
            Bash|bash)
                write_state "running"
                ;;
            Read|Glob|Grep)
                write_state "thinking"
                ;;
            Agent)
                write_state "building"
                ;;
            *)
                write_state "thinking"
                ;;
        esac
        ;;
    PostToolUse)
        case "${TOOL}" in
            Edit|Write|MultiEdit|NotebookEdit)
                write_state "building"
                ;;
            Bash|bash)
                write_state "running"
                ;;
            *)
                write_state "thinking"
                ;;
        esac
        ;;
    PostToolUseFailure)
        write_state "debugging"
        ;;
    *)
        write_state "thinking"
        ;;
esac

exit 0
