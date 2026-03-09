// ASCII art frames for ClaudeLab website animations
// Based on the actual ClaudeLab terminal application

export const LOGO = [
  '  _____ _                 _      _          _     ',
  ' / ____| |               | |    | |        | |    ',
  '| |    | | __ _ _   _  __| | ___| |     __ | |__  ',
  '| |    | |/ _` | | | |/ _` |/ _ \\ |    / _` | \'_ \\ ',
  '| |____| | (_| | |_| | (_| |  __/ |___| (_| | |_) |',
  ' \\_____|_|\\__,_|\\__,_|\\__,_|\\___|______\\__,_|_.__/ ',
];

export const LOGO_SMALL = [
  ' ╔═══════════════════════╗',
  ' ║   C L A U D E L A B   ║',
  ' ╚═══════════════════════╝',
];

// Office background builder (simplified for web)
function buildOfficeBg(width, height) {
  const rows = [];
  // Ceiling
  rows.push('┌' + '─'.repeat(width - 2) + '┐');
  // Middle rows
  for (let r = 1; r < height - 1; r++) {
    rows.push('│' + ' '.repeat(width - 2) + '│');
  }
  // Floor
  rows.push('└' + '─'.repeat(width - 2) + '┘');
  return rows;
}

function stamp(canvas, piece, row, col) {
  const out = [...canvas];
  for (let dy = 0; dy < piece.length; dy++) {
    const r = row + dy;
    if (r < 0 || r >= out.length) continue;
    const rowChars = [...out[r]];
    for (let dx = 0; dx < piece[dy].length; dx++) {
      const c = col + dx;
      if (c < 0 || c >= rowChars.length) continue;
      if (piece[dy][dx] !== ' ') {
        rowChars[c] = piece[dy][dx];
      }
    }
    out[r] = rowChars.join('');
  }
  return out;
}

// Agent sprites
const SITTING_IDLE = [
  '  ◉  ',
  ' /|\\ ',
  ' / \\ ',
];

const SITTING_TYPING = [
  [
    '  ◉  ',
    ' /|\\ ',
    ' _/ \\ ',
  ],
  [
    '  ◉  ',
    ' /|\\',
    ' / \\_ ',
  ],
  [
    '  ◉  ',
    ' /|\\ ',
    ' _/ \\_ ',
  ],
  [
    '  ◉  ',
    ' /|\\ ',
    ' / \\ ',
  ],
];

const STANDING_POINTING = [
  [
    '  ◉  ',
    ' /|--',
    ' / \\ ',
  ],
  [
    '  ◉ /',
    ' /|/ ',
    ' / \\ ',
  ],
];

const STANDING_EXAMINING = [
  [
    '  ◉o ',
    ' /|\\ ',
    ' / \\ ',
  ],
  [
    '  ◉ o',
    ' /|\\ ',
    ' / \\ ',
  ],
];

const CARRYING = [
  [
    '  ◉  ',
    ' /|\\ ▐█▌',
    ' /   ',
  ],
  [
    '  ◉  ',
    ' /|\\ ▐█▌',
    '   \\ ',
  ],
  [
    '  ◉  ',
    ' /|\\ ▐█▌',
    ' | | ',
  ],
];

const BUTTON_PUSH = [
  [
    '  ◉  ',
    ' /|\\-',
    ' / \\ ',
  ],
  [
    '  ◉  ',
    ' /|\\ ',
    ' / \\ ',
  ],
  [
    '  ◉  ',
    '-/|\\ ',
    ' / \\ ',
  ],
];

const DRINKING = [
  [
    '  ◉┐',
    ' /|  ',
    ' / \\ ',
  ],
  [
    '  ◉/ ',
    ' /|  ',
    ' / \\ ',
  ],
];

const LEANING = [
  [
    '  ◉  ',
    '  |\\  ',
    ' / \\ ',
  ],
  [
    '  ◉  ',
    '  |\\ ',
    ' / \\ ',
  ],
];

// Furniture
const DESK_WITH_MONITOR = [
  '┌────────┐',
  '│▓▓░░▓▓░░│',
  '└────────┘',
  '│────────│',
  '┌──────────────┐',
  '└────┴──┴────┘',
];

const PLANT_FRAMES = [
  [
    '  \\|/  ',
    '  /|\\  ',
    ' \\|/|  ',
    ' [▓▓▓] ',
  ],
  [
    '  \\|/  ',
    '  /|\\  ',
    '  |\\|/ ',
    ' [▓▓▓] ',
  ],
];

const CLOCK_FRAMES = [
  [
    '┌───┐',
    '│ | │',
    '│    │',
    '└───┘',
  ],
  [
    '┌───┐',
    '│  / │',
    '│    │',
    '└───┘',
  ],
  [
    '┌───┐',
    '│ -- │',
    '│    │',
    '└───┘',
  ],
  [
    '┌───┐',
    '│  \\ │',
    '│    │',
    '└───┘',
  ],
];

const WINDOW = [
  '┌────────────┐',
  '│░░░░░░░░░░░░│',
  '│░░░░ day ░░░│',
  '│░░░░░░░░░░░░│',
  '└────────────┘',
];

const THOUGHT_BUBBLES = [
  '  .o( ... )',
  '  .o(  ?  )',
  '  .o(  !  )',
  '  .o( >>> )',
  '  .o( <*> )',
  '  .o( ~~~ )',
];

const LIGHTBULB_FRAMES = [
  '     ',
  '  .  ',
  '  o  ',
  ' (!) ',
  ' (*) ',
  ' (*) ',
  ' (!) ',
  '  o  ',
];

const WHITEBOARD_DEBUG = [
  '┌──────────────────┐',
  '│  BUG TRACKER       │',
  '│  [x] parse error   │',
  '│  [ ] null ref      │',
  '│  [ ] off-by-one    │',
  '│  ┌─┐─>┌─┐─>┌─┐    │',
  '│  │A│  │B│  │C│    │',
  '└──────────────────┘',
];

const SERVER_RACK = [
  [
    '┌────────┐',
    '│██ ● ● ○│',
    '├────────┤',
    '│██ ○ ● ●│',
    '├────────┤',
    '│██ ● ○ ●│',
    '├────────┤',
    '│░░░░░░░░│',
    '└────────┘',
  ],
  [
    '┌────────┐',
    '│██ ○ ● ●│',
    '├────────┤',
    '│██ ● ● ○│',
    '├────────┤',
    '│██ ○ ● ●│',
    '├────────┤',
    '│▓▓▓▓▓▓▓▓│',
    '└────────┘',
  ],
];

const CONTROL_PANEL = [
  '┌────────────┐',
  '│ (●) (○) (●) │',
  '│ [██] [░░] │',
  '│ ──────── │',
  '└────────────┘',
];

const CONTROL_PANEL_ACTIVE = [
  '┌────────────┐',
  '│ (●) (●) (●) │',
  '│ [██] [██] │',
  '│ ──────── │',
  '└────────────┘',
];

const COFFEE_MACHINE = [
  [
    '  ┌───┐  ',
    '  │ C │  ',
    '┌─┴───┴─┐',
    '│ ▒▒▒▒▒ │',
    '│  ▒▒▒  │',
    '│ ┌┐   │',
    '│ └┘   │',
    '└───────┘',
  ],
  [
    '  ┌───┐  ',
    '  │ C │  ',
    '┌─┴───┴─┐',
    '│ ▓▓▓▓▓ │',
    '│  ▓▓▓  │',
    '│ ┌┐~  │',
    '│ └┘   │',
    '└───────┘',
  ],
];

const CONVEYOR_BELT = '═'.repeat(25);

const ASSEMBLY_PLATFORM = [
  '▄▄▄▄▄▄▄▄▄▄▄▄',
  '█  BUILD   █',
  '▀▀▀▀▀▀▀▀▀▀▀▀',
];

const GEAR_FRAMES = [
  [
    '  ┌─┐  ',
    ' ─┤●├─ ',
    '  └─┘  ',
  ],
  [
    '  \\ /  ',
    ' ─ ● ─ ',
    '  / \\  ',
  ],
  [
    '  ┌─┐  ',
    ' ─┤●├─ ',
    '  └─┘  ',
  ],
  [
    '  | |  ',
    '  ─●─  ',
    '  | |  ',
  ],
];

const PROGRESS_FRAMES = [
  '[█░░░░░░░░░] 10%',
  '[██░░░░░░░░] 20%',
  '[████░░░░░░] 40%',
  '[█████░░░░░] 50%',
  '[██████░░░░] 60%',
  '[███████░░░] 70%',
  '[█████████░] 90%',
  '[██████████] OK!',
];

const BUILD_PROGRESS = [
  'BUILD [░░░░░░░░]  0%',
  'BUILD [█░░░░░░░] 12%',
  'BUILD [██░░░░░░] 25%',
  'BUILD [███░░░░░] 37%',
  'BUILD [████░░░░] 50%',
  'BUILD [██████░░] 75%',
  'BUILD [███████░] 87%',
  'BUILD [████████] OK!',
];

const CODE_SNIPPETS = [
  'def main():',
  '  for x in',
  '  if val > ',
  '  return ok',
  'import sys ',
  'class Node:',
  '  self.nxt ',
  'yield item ',
  'async def :',
  '  await fn ',
  'try: parse ',
  'except Err:',
  'fn(&mut s) ',
  'let v = [] ',
  'match res {',
  '  Ok(v) => ',
];

const WARNINGS = [
  [
    ' /!\\ ',
    '/ ! \\',
    '-----',
  ],
  [
    ' /!\\ ',
    '/ ! \\',
    '-----',
  ],
  [
    '     ',
    '     ',
    '     ',
  ],
  [
    ' /!\\ ',
    '/ ! \\',
    '-----',
  ],
];

const MAGNIFY_MONITOR = [
  [
    '┌────────┐',
    '│ ERR:42 │',
    '│>fix_it │',
    '│ return │',
    '└────────┘',
    '    ││    ',
  ],
  [
    '┌────────┐',
    '│ ln 41: │',
    '│ ERR:42 │',
    '│>fix_it │',
    '└────────┘',
    '    ││    ',
  ],
  [
    '┌────────┐',
    '│ type?  │',
    '│ null!  │',
    '│>trace  │',
    '└────────┘',
    '    ││    ',
  ],
  [
    '┌────────┐',
    '│>stack  │',
    '│ at L42 │',
    '│ found! │',
    '└────────┘',
    '    ││    ',
  ],
];

const CHAT_BUBBLES = [
  [
    '┌───────┐',
    '│ nice! │',
    '└─┬────┘',
    '  │      ',
  ],
  [
    '┌───────┐',
    '│  tea? │',
    '└─┬────┘',
    '  │      ',
  ],
  [
    '┌───────┐',
    '│  yep! │',
    '└─┬────┘',
    '  │      ',
  ],
  [
    '┌───────┐',
    '│  :)   │',
    '└─┬────┘',
    '  │      ',
  ],
];

const STEAM = [
  ['  ~  '],
  [' ~ ~ '],
  ['  ~  '],
  [' ~~~ '],
];

const BLOCK_LABELS = ['.py', '.js', '.ts', '.rs', '.go', '.md', '.sh', '.cx'];

const STACK_FRAMES = [
  [['████']],
  [['████'], ['████']],
  [['████'], ['████'], ['████']],
  [['██████'], ['██████'], ['██████']],
  [['██████'], ['██████'], ['██████'], ['██████']],
  [['┌──────┐'], ['│ DONE │'], ['└──────┘']],
  [['┌──────┐'], ['│ DONE │'], ['└──────┘']],
  [['┌──────┐'], ['│ DONE │'], ['└──────┘']],
];

const LOG_LINES = [
  '> compiling...',
  '> linking...',
  '> tests: 42 pass',
  '> building...',
  '> deploy: ok',
  '> checks pass',
  '> lint: clean',
  '> done.',
];

const IDLE_MSGS = [
  '  ~ all quiet ~  ',
  ' ~ break time ~  ',
  '  ~ relaxing ~   ',
  ' ~ standby ...~  ',
];

// ─── Scene generators ────────────────────────────────────────────────

function generateThinkingFrames(width, height, numFrames = 8) {
  const frames = [];
  for (let fi = 0; fi < numFrames; fi++) {
    let bg = buildOfficeBg(width, height);
    const floor = height - 2;
    const desk1Col = 4;
    const desk2Col = Math.min(width - 16, Math.max(22, Math.floor(width / 2) - 5));
    const plantCol = Math.min(width - 10, Math.max(40, width - 14));
    const clockCol = Math.min(width - 8, Math.max(16, Math.floor(width / 2)));
    const windowCol = Math.min(width - 16, Math.max(50, width - 18));

    const deskRow = floor - DESK_WITH_MONITOR.length;
    if (deskRow > 3 && desk1Col + 14 < width) bg = stamp(bg, DESK_WITH_MONITOR, deskRow, desk1Col);
    if (deskRow > 3 && desk2Col + 14 < width) bg = stamp(bg, DESK_WITH_MONITOR, deskRow, desk2Col);

    const pf = fi % PLANT_FRAMES.length;
    const plantRow = floor - PLANT_FRAMES[0].length;
    if (plantRow > 1 && plantCol + 7 < width) bg = stamp(bg, PLANT_FRAMES[pf], plantRow, plantCol);

    const cf = fi % CLOCK_FRAMES.length;
    if (clockCol + 5 < width && height > 8) bg = stamp(bg, CLOCK_FRAMES[cf], 1, clockCol);

    if (windowCol + 14 < width && height > 8) bg = stamp(bg, WINDOW, 1, windowCol);

    const agent = SITTING_IDLE;
    const agent1Row = deskRow - agent.length;
    if (agent1Row > 1) bg = stamp(bg, agent, agent1Row, desk1Col + 2);
    if (agent1Row > 1 && desk2Col + 7 < width) bg = stamp(bg, agent, agent1Row, desk2Col + 2);

    const tb = THOUGHT_BUBBLES[fi % THOUGHT_BUBBLES.length];
    const bubbleRow = agent1Row - 1;
    if (bubbleRow >= 1) bg = stamp(bg, [tb], bubbleRow, desk1Col);

    const tb2 = THOUGHT_BUBBLES[(fi + 3) % THOUGHT_BUBBLES.length];
    const bubble2Row = agent1Row - 1;
    if (bubble2Row >= 1 && desk2Col + 12 < width) bg = stamp(bg, [tb2], bubble2Row, desk2Col);

    const lb = LIGHTBULB_FRAMES[fi % LIGHTBULB_FRAMES.length];
    const lbRow = bubbleRow - 1;
    if (lbRow >= 1) bg = stamp(bg, [lb], lbRow, desk1Col + 1);

    // Blinking cursor
    const cursorRow = deskRow + 1;
    if (cursorRow >= 0 && cursorRow < bg.length) {
      const rowChars = [...bg[cursorRow]];
      const cp1 = desk1Col + 2;
      if (cp1 < rowChars.length) rowChars[cp1] = fi % 2 === 0 ? '█' : ' ';
      const cp2 = desk2Col + 2;
      if (cp2 < rowChars.length) rowChars[cp2] = fi % 3 === 0 ? '█' : ' ';
      bg[cursorRow] = rowChars.join('');
    }

    frames.push(bg);
  }
  return frames;
}

function makeCodeMonitor(frameIdx) {
  const snippets = [
    CODE_SNIPPETS[(frameIdx * 3) % CODE_SNIPPETS.length],
    CODE_SNIPPETS[(frameIdx * 3 + 1) % CODE_SNIPPETS.length],
    CODE_SNIPPETS[(frameIdx * 3 + 2) % CODE_SNIPPETS.length],
  ];
  const padded = snippets.map(s => s.substring(0, 8).padEnd(8));
  const cursor = frameIdx % 2 === 0 ? '█' : ' ';
  return [
    '┌────────┐',
    '│' + padded[0] + '│',
    '│' + padded[1] + '│',
    '│' + padded[2] + cursor,
    '└────────┘',
    '    ││    ',
  ];
}

function generateCodingFrames(width, height, numFrames = 8) {
  const frames = [];
  const deskBase = [
    '┌──────────────┐',
    '└────┴──┴────┘',
  ];
  for (let fi = 0; fi < numFrames; fi++) {
    let bg = buildOfficeBg(width, height);
    const floor = height - 2;
    const desk1Col = 4;
    const desk2Col = Math.min(width - 16, Math.max(22, Math.floor(width / 2) - 5));
    const desk3Col = Math.min(width - 16, Math.max(40, Math.floor(width * 3 / 4) - 5));
    const plantCol = Math.min(width - 10, Math.max(55, width - 12));
    const windowCol = Math.min(width - 16, Math.max(50, width - 18));

    const mon = makeCodeMonitor(fi);
    const mon2 = makeCodeMonitor((fi + 2) % numFrames);
    const mon3 = makeCodeMonitor((fi + 5) % numFrames);
    const deskRow = floor - mon.length - 2;

    if (deskRow > 4) {
      if (desk1Col + 14 < width) {
        bg = stamp(bg, mon, deskRow, desk1Col);
        bg = stamp(bg, deskBase, deskRow + mon.length, desk1Col - 1);
      }
      if (desk2Col + 14 < width) {
        bg = stamp(bg, mon2, deskRow, desk2Col);
        bg = stamp(bg, deskBase, deskRow + mon2.length, desk2Col - 1);
      }
      if (desk3Col + 14 < width && desk3Col > desk2Col + 14) {
        bg = stamp(bg, mon3, deskRow, desk3Col);
        bg = stamp(bg, deskBase, deskRow + mon3.length, desk3Col - 1);
      }
    }

    const agent = SITTING_TYPING[fi % SITTING_TYPING.length];
    const agentRow = deskRow - agent.length;
    if (agentRow > 1 && desk1Col + 7 < width) bg = stamp(bg, agent, agentRow, desk1Col + 2);
    const agent2 = SITTING_TYPING[(fi + 1) % SITTING_TYPING.length];
    if (agentRow > 1 && desk2Col + 7 < width) bg = stamp(bg, agent2, agentRow, desk2Col + 2);
    if (desk3Col + 14 < width && desk3Col > desk2Col + 14 && agentRow > 1) {
      const agent3 = SITTING_TYPING[(fi + 3) % SITTING_TYPING.length];
      bg = stamp(bg, agent3, agentRow, desk3Col + 2);
    }

    const pf = fi % PLANT_FRAMES.length;
    const plantRow = floor - PLANT_FRAMES[0].length;
    if (plantRow > 1 && plantCol + 7 < width) bg = stamp(bg, PLANT_FRAMES[pf], plantRow, plantCol);

    if (windowCol + 14 < width && height > 8) bg = stamp(bg, WINDOW, 1, windowCol);

    const indicator = '  >> CODING IN PROGRESS <<';
    const indCol = Math.max(2, Math.floor((width - indicator.length) / 2));
    if (indCol + indicator.length < width && fi % 2 === 0) {
      bg = stamp(bg, [indicator], 2, indCol);
    }

    frames.push(bg);
  }
  return frames;
}

function generateDebuggingFrames(width, height, numFrames = 8) {
  const frames = [];
  const deskBase = [
    '┌──────────────┐',
    '└────┴──┴────┘',
  ];
  for (let fi = 0; fi < numFrames; fi++) {
    let bg = buildOfficeBg(width, height);
    const floor = height - 2;
    const wbCol = 4;
    const monitorCol = Math.min(width - 16, Math.max(28, Math.floor(width / 2)));
    const serverCol = Math.min(width - 12, Math.max(46, width - 14));
    const plantCol = Math.min(width - 10, Math.max(60, width - 12));
    const windowCol = Math.min(width - 16, Math.max(50, width - 18));

    const wbRow = 2;
    if (wbRow + WHITEBOARD_DEBUG.length < floor && wbCol + 20 < width) {
      bg = stamp(bg, WHITEBOARD_DEBUG, wbRow, wbCol);
    }

    const a1 = STANDING_POINTING[fi % STANDING_POINTING.length];
    const a1Row = wbRow + WHITEBOARD_DEBUG.length;
    if (a1Row + a1.length < floor) bg = stamp(bg, a1, a1Row, wbCol + 6);

    const mon = MAGNIFY_MONITOR[fi % MAGNIFY_MONITOR.length];
    const monRow = floor - mon.length - deskBase.length;
    if (monRow > 3 && monitorCol + 14 < width) {
      bg = stamp(bg, mon, monRow, monitorCol);
      bg = stamp(bg, deskBase, monRow + mon.length, monitorCol - 1);
    }

    const a2 = STANDING_EXAMINING[fi % STANDING_EXAMINING.length];
    const a2Row = monRow - a2.length;
    if (a2Row > 1 && monitorCol + 7 < width) bg = stamp(bg, a2, a2Row, monitorCol + 2);

    const srv = SERVER_RACK[fi % SERVER_RACK.length];
    const srvRow = floor - srv.length;
    if (srvRow > 1 && serverCol + 10 < width) bg = stamp(bg, srv, srvRow, serverCol);

    const warn = WARNINGS[fi % WARNINGS.length];
    const warnCol = monitorCol + 12;
    if (warnCol + 5 < width && 2 + 3 < height) bg = stamp(bg, warn, 2, warnCol);

    const pf = fi % PLANT_FRAMES.length;
    const plantRow = floor - PLANT_FRAMES[0].length;
    if (plantRow > 1 && plantCol + 7 < width) bg = stamp(bg, PLANT_FRAMES[pf], plantRow, plantCol);

    if (windowCol + 14 < width && height > 8) bg = stamp(bg, WINDOW, 1, windowCol);

    frames.push(bg);
  }
  return frames;
}

function generateRunningFrames(width, height, numFrames = 8) {
  const frames = [];
  for (let fi = 0; fi < numFrames; fi++) {
    let bg = buildOfficeBg(width, height);
    const floor = height - 2;
    const panelCol = 6;
    const serverCol = Math.min(width - 12, Math.max(24, Math.floor(width / 2) - 4));
    const gearCol = Math.min(width - 10, Math.max(38, Math.floor(width * 2 / 3)));
    const plantCol = Math.min(width - 10, Math.max(52, width - 12));
    const windowCol = Math.min(width - 16, Math.max(55, width - 18));

    const panel = fi % 2 === 0 ? CONTROL_PANEL_ACTIVE : CONTROL_PANEL;
    const panelRow = floor - panel.length;
    if (panelRow > 3 && panelCol + 14 < width) bg = stamp(bg, panel, panelRow, panelCol);

    const agent = BUTTON_PUSH[fi % BUTTON_PUSH.length];
    const agentRow = panelRow - agent.length;
    if (agentRow > 1) bg = stamp(bg, agent, agentRow, panelCol + 3);

    const srv = SERVER_RACK[fi % SERVER_RACK.length];
    const srvRow = floor - srv.length;
    if (srvRow > 1 && serverCol + 10 < width) bg = stamp(bg, srv, srvRow, serverCol);

    const gear = GEAR_FRAMES[fi % GEAR_FRAMES.length];
    const gearRow = Math.max(3, Math.floor(floor / 2) - 1);
    if (gearCol + 7 < width && gearRow + 3 < floor) bg = stamp(bg, gear, gearRow, gearCol);

    const prog = PROGRESS_FRAMES[fi % PROGRESS_FRAMES.length];
    const progRow = gearRow + 4;
    if (progRow < floor && gearCol + 15 < width) bg = stamp(bg, [prog], progRow, gearCol - 1);

    const logCol = 4;
    const logStartRow = 2;
    const visibleLogs = Math.min(fi + 1, LOG_LINES.length, floor - logStartRow - 2);
    for (let li = 0; li < visibleLogs; li++) {
      const idx = (fi - visibleLogs + 1 + li + LOG_LINES.length) % LOG_LINES.length;
      const lr = logStartRow + li;
      if (lr < floor && logCol + LOG_LINES[idx].length < width) {
        bg = stamp(bg, [LOG_LINES[idx]], lr, logCol);
      }
    }

    const pf = fi % PLANT_FRAMES.length;
    const plantRow = floor - PLANT_FRAMES[0].length;
    if (plantRow > 1 && plantCol + 7 < width) bg = stamp(bg, PLANT_FRAMES[pf], plantRow, plantCol);

    if (windowCol + 14 < width && height > 8) bg = stamp(bg, WINDOW, 1, windowCol);

    frames.push(bg);
  }
  return frames;
}

function generateBuildingFrames(width, height, numFrames = 8) {
  const frames = [];
  for (let fi = 0; fi < numFrames; fi++) {
    let bg = buildOfficeBg(width, height);
    const floor = height - 2;
    const conveyorCol = 3;
    const conveyorLen = Math.min(25, width - 8);
    const platformCol = Math.min(width - 16, Math.max(32, Math.floor(width / 2) + 4));
    const plantCol = Math.min(width - 10, Math.max(52, width - 12));
    const windowCol = Math.min(width - 16, Math.max(55, width - 18));

    // Conveyor belt
    const beltRow = floor - 1;
    const beltLine = '═'.repeat(conveyorLen);
    if (beltRow > 3 && conveyorCol + conveyorLen < width) {
      bg = stamp(bg, [beltLine], beltRow, conveyorCol);
    }

    // Carrying agent
    const carry = CARRYING[fi % CARRYING.length];
    const agentX = conveyorCol + ((fi * 3) % Math.max(1, conveyorLen - 8));
    const agentRow = beltRow - carry.length;
    if (agentRow > 2 && agentX + 10 < width) bg = stamp(bg, carry, agentRow, agentX);

    // Block label
    const blkLabel = '▐' + BLOCK_LABELS[fi % BLOCK_LABELS.length] + '▌';
    if (agentRow > 1 && agentX + 11 < width) bg = stamp(bg, [blkLabel], agentRow, agentX + 6);

    // Assembly platform
    const platRow = floor - ASSEMBLY_PLATFORM.length;
    if (platRow > 3 && platformCol + 12 < width) {
      bg = stamp(bg, ASSEMBLY_PLATFORM, platRow, platformCol);
    }

    // Growing stack
    const stackPieces = STACK_FRAMES[fi % STACK_FRAMES.length];
    const stackHeight = stackPieces.length;
    for (let si = 0; si < stackPieces.length; si++) {
      const sr = platRow - stackHeight + si;
      if (sr > 1 && platformCol + 8 < width) {
        bg = stamp(bg, stackPieces[si], sr, platformCol + 2);
      }
    }

    // Progress bar
    const prog = BUILD_PROGRESS[fi % BUILD_PROGRESS.length];
    const progCol = Math.max(2, Math.floor((width - prog.length) / 2));
    if (progCol + prog.length < width) bg = stamp(bg, [prog], 2, progCol);

    const pf = fi % PLANT_FRAMES.length;
    const plantRow = floor - PLANT_FRAMES[0].length;
    if (plantRow > 1 && plantCol + 7 < width) bg = stamp(bg, PLANT_FRAMES[pf], plantRow, plantCol);

    if (windowCol + 14 < width && height > 8) bg = stamp(bg, WINDOW, 1, windowCol);

    frames.push(bg);
  }
  return frames;
}

function generateIdleFrames(width, height, numFrames = 8) {
  const frames = [];
  for (let fi = 0; fi < numFrames; fi++) {
    let bg = buildOfficeBg(width, height);
    const floor = height - 2;
    const coffeeCol = 4;
    const deskCol = Math.min(width - 16, Math.max(22, Math.floor(width / 2) - 5));
    const plantCol = Math.min(width - 10, Math.max(42, width - 14));
    const clockCol = Math.min(width - 8, Math.max(16, Math.floor(width / 3)));
    const windowCol = Math.min(width - 16, Math.max(50, width - 18));

    const cm = COFFEE_MACHINE[fi % COFFEE_MACHINE.length];
    const cmRow = floor - cm.length;
    if (cmRow > 3 && coffeeCol + 9 < width) bg = stamp(bg, cm, cmRow, coffeeCol);

    const drink = DRINKING[fi % DRINKING.length];
    const drinkRow = cmRow - drink.length;
    if (drinkRow > 1 && coffeeCol + 12 < width) bg = stamp(bg, drink, drinkRow, coffeeCol + 9);

    const steam = STEAM[fi % STEAM.length];
    const steamRow = drinkRow - 1;
    if (steamRow >= 1 && coffeeCol + 16 < width) bg = stamp(bg, steam, steamRow, coffeeCol + 10);

    const deskRow = floor - DESK_WITH_MONITOR.length;
    if (deskRow > 3 && deskCol + 14 < width) bg = stamp(bg, DESK_WITH_MONITOR, deskRow, deskCol);

    const lean = LEANING[fi % LEANING.length];
    const leanRow = deskRow - lean.length;
    if (leanRow > 1 && deskCol + 7 < width) bg = stamp(bg, lean, leanRow, deskCol + 2);

    const chat = CHAT_BUBBLES[fi % CHAT_BUBBLES.length];
    const chatRow = leanRow - chat.length;
    if (chatRow >= 1 && deskCol + 12 < width) bg = stamp(bg, chat, chatRow, deskCol);

    const clk = CLOCK_FRAMES[fi % CLOCK_FRAMES.length];
    if (clockCol + 5 < width && height > 8) bg = stamp(bg, clk, 1, clockCol);

    const pf = fi % PLANT_FRAMES.length;
    const plantRow = floor - PLANT_FRAMES[0].length;
    if (plantRow > 1 && plantCol + 7 < width) bg = stamp(bg, PLANT_FRAMES[pf], plantRow, plantCol);

    if (windowCol + 14 < width && height > 8) bg = stamp(bg, WINDOW, 1, windowCol);

    const msg = IDLE_MSGS[fi % IDLE_MSGS.length];
    const msgCol = Math.max(2, Math.floor((width - msg.length) / 2));
    if (msgCol + msg.length < width) bg = stamp(bg, [msg], floor, msgCol);

    frames.push(bg);
  }
  return frames;
}

// ─── Exported scene data ─────────────────────────────────────────────

export const SCENES = {
  thinking: {
    name: 'Thinking',
    description: 'Claude is analyzing the problem, reading code, and planning the approach.',
    trigger: 'Triggered when Claude reads files or formulates a plan',
    generateFrames: generateThinkingFrames,
    icon: '.o( ? )',
  },
  coding: {
    name: 'Coding',
    description: 'Active code generation. Multiple engineers typing simultaneously at their workstations.',
    trigger: 'Triggered when Claude writes or edits code files',
    generateFrames: generateCodingFrames,
    icon: '>>_',
  },
  debugging: {
    name: 'Debugging',
    description: 'Engineers at the whiteboard tracking bugs, examining error traces with magnifying glass.',
    trigger: 'Triggered when Claude investigates errors or test failures',
    generateFrames: generateDebuggingFrames,
    icon: '/!\\',
  },
  running: {
    name: 'Running',
    description: 'Control panel activated, server rack blinking, progress bar advancing as commands execute.',
    trigger: 'Triggered when Claude runs shell commands or tests',
    generateFrames: generateRunningFrames,
    icon: '[>>]',
  },
  building: {
    name: 'Building',
    description: 'Engineers carry code blocks along conveyor belt to the assembly platform. Stack grows.',
    trigger: 'Triggered when Claude runs build or compilation commands',
    generateFrames: generateBuildingFrames,
    icon: '▐█▌',
  },
  idle: {
    name: 'Idle',
    description: 'Coffee break. Engineers chat, relax, and sip coffee while waiting for the next task.',
    trigger: 'Shown when Claude Code is idle or between tasks',
    generateFrames: generateIdleFrames,
    icon: '~☕~',
  },
};

// Generate a small preview frame for feature cards (compact)
export function getPreviewFrame(sceneKey, width = 40, height = 14) {
  const scene = SCENES[sceneKey];
  if (!scene) return [];
  const frames = scene.generateFrames(width, height, 1);
  return frames[0] || [];
}

// Generate animation frames for hero section
export function getHeroFrames(width = 68, height = 20) {
  const allFrames = [];
  const sceneOrder = ['thinking', 'coding', 'debugging', 'running', 'building', 'idle'];

  for (const sceneKey of sceneOrder) {
    const scene = SCENES[sceneKey];
    // Generate 4 frames per scene for the hero animation
    const frames = scene.generateFrames(width, height, 4);
    for (const frame of frames) {
      allFrames.push({ lines: frame, scene: sceneKey, label: scene.name });
    }
  }

  return allFrames;
}
