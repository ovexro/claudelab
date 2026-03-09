#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────
# ClaudeLab Hook Script
#
# Add this to your Claude Code hooks configuration so ClaudeLab can
# detect what Claude Code is doing in real time.
#
# Setup:
#   1. Copy this file somewhere on your PATH or note its full path.
#   2. Add the hook to ~/.claude/hooks.json:
#
#      {
#        "hooks": {
#          "PreToolUse": [
#            {
#              "matcher": "",
#              "hooks": ["bash /path/to/claudelab-hook.sh pre $TOOL_NAME"]
#            }
#          ],
#          "PostToolUse": [
#            {
#              "matcher": "",
#              "hooks": ["bash /path/to/claudelab-hook.sh post $TOOL_NAME $EXIT_CODE"]
#            }
#          ]
#        }
#      }
#
# The script writes a simple activity string to ~/.claudelab/state
# which ClaudeLab reads to drive the animation.
# ──────────────────────────────────────────────────────────────────────

set -euo pipefail

STATE_DIR="${HOME}/.claudelab"
STATE_FILE="${STATE_DIR}/state"

# Ensure state directory exists
mkdir -p "${STATE_DIR}"

write_state() {
    printf '%s' "$1" > "${STATE_FILE}"
}

PHASE="${1:-}"       # "pre" or "post"
TOOL="${2:-}"        # Tool name: Edit, Write, Bash, Read, Glob, Grep, etc.
EXIT_CODE="${3:-0}"  # Exit code (only meaningful for PostToolUse)

case "${PHASE}" in
    pre)
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
            *)
                write_state "thinking"
                ;;
        esac
        ;;
    post)
        if [ "${EXIT_CODE}" != "0" ]; then
            write_state "debugging"
        else
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
        fi
        ;;
    *)
        # Unknown phase -- default to thinking
        write_state "thinking"
        ;;
esac

exit 0
