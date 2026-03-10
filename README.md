```
   _____ _                 _        _           _
  / ____| |               | |      | |         | |
 | |    | | __ _ _   _  __| | ___  | |     __ _| |__
 | |    | |/ _` | | | |/ _` |/ _ \ | |    / _` | '_ \
 | |____| | (_| | |_| | (_| |  __/ | |___| (_| | |_) |
  \_____|_|\__,_|\__,_|\__,_|\___| |______\__,_|_.__/
```

# ClaudeLab

A visual terminal companion for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Run it in a tmux pane or a second terminal and watch animated ASCII art of AI "engineers" working while Claude Code edits your code, runs tests, and debugs issues.

**Zero dependencies.** Pure Python + curses. Works on any Linux terminal.

## What It Looks Like

```
══════════════════ AI ENGINEERING LAB ══════════════════
┌──────────────────────────────────────────────────────┐
│  .o( >>> )                ┌────┐   ┌────────────┐   │
│   (*)                     │ /  │   │░░░░░░░░░░░░│   │
│    ◉              ◉       └────┘   │░░ night░░░░│   │
│   /|\            /|\                │░░░░░░░░░░░░│   │
│   / \            / \                └────────────┘   │
│  ┌────────┐   ┌────────┐    \|/                      │
│  │▓▓░░▓▓░░│   │▓░▓░▓░▓░│    /|\                     │
│  └────────┘   └────────┘   \|/|                      │
│  │────────│   │────────│   [▓▓▓]                     │
│  ┌──────────┐ ┌──────────┐                           │
│  └────┴──┴──┘ └────┴──┴──┘                           │
└──────────────────────────────────────────────────────┘
 Activity: THINKING   |  14:32:07  |  ClaudeLab v0.1.0
```

## Features

- **6 animated scenes** that change based on what Claude Code is doing:
  - **Thinking** -- agents sit at desks with thought bubbles and blinking cursors
  - **Coding** -- agents type furiously as code scrolls on their monitors
  - **Debugging** -- agents examine a whiteboard and hunt for bugs
  - **Running** -- agents push buttons on a control panel, servers blink
  - **Building** -- agents carry code blocks on an assembly line
  - **Idle** -- agents drink coffee and chat

- **Activity detection** via three mechanisms:
  1. Claude Code hooks (primary -- real-time, reliable)
  2. JSONL log file watching (secondary)
  3. inotify filesystem monitoring (tertiary, via ctypes -- no deps)

- **Day/night cycle** -- the office window reflects real system time
- **Smooth animation** at configurable FPS (default 8)
- **Terminal resize** handled gracefully
- **Dark and light** colour themes

## Installation

Install from source (PyPI package coming soon):


```bash
git clone https://github.com/ovexro/claudelab.git
cd claudelab
pip install -e .
```

## Usage

### Basic

Open a second terminal (or a tmux pane) and run:

```bash
claudelab
```

Then use Claude Code in your main terminal as usual. ClaudeLab will detect the activity and animate accordingly.

### Demo Mode

To see all scenes cycle through without needing Claude Code:

```bash
claudelab --demo
```

### tmux Setup

A convenient way to use ClaudeLab is in a tmux split:

```bash
# Start a new tmux session
tmux new-session -s work

# Split the window horizontally (ClaudeLab on the right)
tmux split-window -h 'claudelab'

# Or split vertically (ClaudeLab on the bottom)
tmux split-window -v 'claudelab'
```

### CLI Options

| Flag              | Default | Description                               |
|-------------------|---------|-------------------------------------------|
| `--theme dark`    | `dark`  | Colour theme (`dark` or `light`)          |
| `--fps 8`         | `8`     | Animation frame rate (1-30)               |
| `--demo`          | off     | Cycle through all scenes automatically    |

## Hook Setup (Recommended)

For the best experience, set up the ClaudeLab hook so Claude Code reports its activity in real time.

1. Find the hook script:

```bash
# If installed via pip:
HOOK_PATH="$(python -c 'import claudelab, pathlib; print(pathlib.Path(claudelab.__file__).parent.parent / "hooks" / "claudelab-hook.sh")')"

# Or just point to it directly:
HOOK_PATH="/path/to/claudelab/hooks/claudelab-hook.sh"
```

2. Add the hook to your Claude Code settings. Create or edit `~/.claude/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/claudelab-hook.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/claudelab-hook.sh"
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/claudelab-hook.sh"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/claudelab-hook.sh` with the actual path from step 1. The hook receives JSON on stdin from Claude Code containing `hook_event_name` and `tool_name`.

3. Restart Claude Code. ClaudeLab will now receive real-time activity updates.

## How It Works

ClaudeLab runs a curses-based render loop at ~8 FPS. Each frame:

1. **Detect** the current activity (via hook state file, JSONL logs, or inotify)
2. **Select** the matching scene (thinking, coding, debugging, running, building, idle)
3. **Render** the scene's current animation frame into the terminal

The office background is persistent -- desks, plants, the server rack, and a window that shows the real time of day. Agents animate within the office based on the current scene.

### Activity Detection Priority

1. **Hook state file** (`~/.claudelab/state`) -- written by the hook script on every Claude Code tool use. Most reliable.
2. **JSONL log scanning** (`~/.claude/projects/**/*.jsonl`) -- parses Claude Code's log files for recent tool use entries.
3. **inotify** -- watches the current working directory for filesystem changes and infers activity from file types.
4. **Timeouts** -- if no activity is detected for 10+ seconds, falls back to "thinking". After 60+ seconds, falls back to "idle".

## Configuration

ClaudeLab stores its state in `~/.claudelab/`:

```
~/.claudelab/
└── state          # Current activity (written by hook, read by ClaudeLab)
```

## Contributing

Contributions are welcome! Some ideas:

- New scenes or agent animations
- More furniture / office decorations
- Music / sound effects (via terminal bell patterns?)
- Windows / macOS support (currently Linux-only for inotify)
- Configurable office layouts
- Multiple "characters" with different appearances

To develop:

```bash
git clone https://github.com/ovexro/claudelab.git
cd claudelab
pip install -e .
claudelab --demo
```

## License

MIT -- see [LICENSE](LICENSE).
