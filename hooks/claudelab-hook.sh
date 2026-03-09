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
#   2. Add to ~/.claude/hooks.json (see README.md for full config)
# ──────────────────────────────────────────────────────────────────────

STATE_DIR="${HOME}/.claudelab"
STATE_FILE="${STATE_DIR}/state"

mkdir -p "${STATE_DIR}"

write_state() {
    printf '%s' "$1" > "${STATE_FILE}"
}

# Read JSON from stdin
INPUT=$(cat)

# Extract fields using python3 (available everywhere, no jq dependency)
HOOK_EVENT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('hook_event_name',''))" 2>/dev/null || echo "")
TOOL=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_name',''))" 2>/dev/null || echo "")
HAS_ERROR=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('yes' if d.get('error','') else 'no')" 2>/dev/null || echo "no")

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
