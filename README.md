```
   _____ _                 _        _           _
  / ____| |               | |      | |         | |
 | |    | | __ _ _   _  __| | ___  | |     __ _| |__
 | |    | |/ _` | | | |/ _` |/ _ \ | |    / _` | '_ \
 | |____| | (_| | |_| | (_| |  __/ | |___| (_| | |_) |
  \_____|_|\__,_|\__,_|\__,_|\___| |______\__,_|_.__/
```

# ClaudeLab

A visual terminal companion for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Run it in a tmux pane or a second terminal and watch an **isometric 2.5D office** of AI "engineers" working while Claude Code edits your code, runs tests, and debugs issues.

**Zero dependencies.** Pure Python + curses. Works on any Linux terminal with truecolor or 256-color support.

## Rendering Modes

| Mode | Style | Requirements |
|------|-------|-------------|
| **Isometric** (default) | 2.5D diamond-tile office, brick walls, depth-sorted furniture | Truecolor or 256-color terminal |
| **Voxel** | Half-block pixel art, flat perspective | Truecolor or 256-color terminal |
| **Sixel** | High-res pixel graphics (4x resolution) | Sixel-capable terminal (e.g. foot, mlterm) |
| **ASCII** | Classic text-mode office | Any terminal |

The default `auto` mode selects isometric for capable terminals, falling back to ASCII.

## Features

- **6 animated scenes** that change based on what Claude Code is doing:
  - **Thinking** -- agent sits with animated thought bubbles cycling through dots, question marks, and lightbulbs
  - **Coding** -- two agents type at desks with scrolling code on isometric monitors
  - **Debugging** -- red-tinted office with whiteboard error diagrams, agents point and examine bugs
  - **Running** -- control panel with LED grid, rotating gears, and progress bar on the isometric floor
  - **Building** -- conveyor belt with animated rollers carries colored code blocks across diamond tiles
  - **Idle** -- agent drinks coffee with rising steam while another leans back and chats

- **Dynamic scaling** -- the isometric office grid scales to fill your terminal, from 40 to 200+ columns
- **Day/night cycle** -- the office window reflects real system time
- **Activity detection** via Claude Code hooks (primary), JSONL log watching (secondary), and inotify filesystem monitoring (tertiary)
- **Smooth animation** at configurable FPS (default 8)
- **Terminal resize** handled gracefully

## Quick Start

```bash
pip install claudelab
claudelab install
```

That's it. The `install` command auto-detects the hook script, configures Claude Code hooks in `~/.claude/settings.json`, and verifies everything works. No manual JSON editing needed.

Or install from source:

```bash
git clone https://github.com/ovexro/claudelab.git
cd claudelab
pip install -e .
claudelab install
```

## Usage

### Basic

Open a second terminal (or a tmux pane) and run:

```bash
claudelab
```

Then use Claude Code in your main terminal as usual. ClaudeLab detects the activity and animates the matching scene.

### Demo Mode

To see all scenes cycle through without needing Claude Code:

```bash
claudelab --demo
```

### tmux Setup

```bash
tmux new-session -s work
tmux split-window -h 'claudelab'
```

### CLI Options

| Flag / Command | Default | Description |
|----------------|---------|-------------|
| `claudelab install` | | Auto-configure Claude Code hooks |
| `claudelab doctor` | | Diagnose setup issues |
| `claudelab uninstall` | | Remove hooks cleanly |
| `--renderer {auto,iso,sixel,voxel,ascii}` | `auto` | Rendering mode |
| `--theme {dark,light}` | `dark` | Colour theme |
| `--fps N` | `8` | Animation frame rate (1-30) |
| `--demo` | off | Cycle through all scenes automatically |

### Troubleshooting

If something isn't working, run the built-in diagnostics:

```bash
claudelab doctor
```

It checks hook configuration, permissions, state file freshness, Python version, and terminal capabilities — and tells you exactly what to fix.

## How It Works

ClaudeLab runs a curses-based render loop at ~8 FPS. Each frame:

1. **Detect** the current activity (hook state file, JSONL logs, or inotify)
2. **Select** the matching scene (thinking, coding, debugging, running, building, idle)
3. **Render** the isometric office with the scene's animation frame into the terminal

The isometric office dynamically sizes its diamond-tile floor grid to fill the terminal. Brick-textured walls, depth-sorted furniture (desks, monitors, chairs, server rack, plant), and character sprites are drawn back-to-front. Each scene adds its own overlays -- thought bubbles, conveyor belts, control panels, debug whiteboards, and more.

### Activity Detection Priority

1. **Hook state file** (`/tmp/claudelab.state`) -- written by the hook script on every tool use. Most reliable.
2. **JSONL log scanning** -- parses Claude Code's log files for recent tool use entries.
3. **inotify** -- watches the working directory for filesystem changes and infers activity.
4. **Timeouts** -- falls back to "thinking" after 10s, "idle" after 60s.

## Contributing

Contributions welcome! Ideas:

- New scenes or agent animations
- More furniture / office decorations
- Windows / macOS support
- Configurable office layouts
- Multiple character appearances

```bash
git clone https://github.com/ovexro/claudelab.git
cd claudelab
pip install -e .
claudelab --demo
```

## License

MIT -- see [LICENSE](LICENSE).
