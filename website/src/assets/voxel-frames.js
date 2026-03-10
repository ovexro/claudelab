// NES-quality isometric 2.5D voxel frames for ClaudeLab website
// Mirrors Python iso_office.py — renders to HTML <span> half-block elements

// ─── Palette (3-tone shading) ──────────────────────────────────────

const P = {
  // Outline
  OL: [15, 10, 20],
  // Stone wall
  STONE_HL: [190, 190, 195], STONE: [128, 128, 128], STONE_L: [160, 160, 160], STONE_D: [80, 80, 80],
  COBBLE: [110, 110, 110],
  // Wood
  OAK_L: [200, 160, 100], OAK: [170, 130, 80], OAK_D: [140, 105, 65], OAK_LOG: [85, 65, 40],
  BIRCH: [200, 190, 160],
  // Metal
  IRON: [200, 200, 200], IRON_D: [150, 150, 155],
  // Agent — hair
  HAIR_HL: [110, 80, 50], HAIR: [75, 50, 30], HAIR_D: [45, 25, 12],
  // Agent — skin
  SKIN_HL: [230, 195, 160], SKIN: [200, 160, 120], SKIN_S: [160, 120, 80], SKIN_D: [120, 85, 55],
  // Agent — eyes
  EYE_W: [255, 255, 255], EYE_P: [30, 30, 60],
  // Agent — shirts (3-tone)
  S1L: [90, 200, 240], S1: [50, 160, 200], S1D: [35, 120, 160],
  S2L: [240, 90, 90], S2: [200, 50, 50], S2D: [150, 35, 35],
  // Agent — pants/shoes
  PL: [60, 75, 180], P: [40, 50, 140], PS: [28, 35, 100],
  SH_HL: [120, 120, 125], SH: [80, 80, 80],
  // Sky
  SKY: [120, 180, 255], NIGHT: [15, 15, 45],
  SUN: [255, 230, 80], MOON: [230, 230, 210], STAR: [255, 255, 200], CLOUD: [240, 240, 255],
  // Tech
  MON_BG: [25, 30, 50], MON_GLOW: [35, 45, 70], MON_FR: [55, 55, 70],
  MON_GR: [80, 255, 80], MON_WH: [210, 210, 210], MON_YL: [255, 220, 80],
  MON_RD: [255, 80, 80], MON_CY: [80, 220, 255],
  LED_G: [50, 255, 50], LED_R: [255, 50, 50], LED_A: [255, 180, 0], LED_O: [50, 50, 55],
  // Objects
  LEAF_L: [80, 190, 70], LEAF: [50, 150, 50], LEAF_D: [30, 110, 30],
  POT: [180, 100, 60],
  COFFEE: [110, 65, 30], MUG: [240, 240, 245],
  STEAM: [210, 210, 230], STEAM_F: [150, 150, 170],
  CH_HL: [90, 75, 60], CH: [60, 50, 40], CH_S: [35, 28, 20],
  KB_D: [55, 55, 60], KB_K: [90, 90, 95],
  GLOW: [210, 190, 120],
  // Effects
  THOUGHT_L: [245, 245, 255], THOUGHT: [220, 220, 240], THOUGHT_D: [180, 180, 200],
  WARN_R: [220, 40, 40], WARN_Y: [255, 210, 50],
  GEAR_L: [200, 120, 240], GEAR: [160, 80, 200], GEAR_D: [120, 55, 155],
  CONV_L: [180, 180, 190], CONV: [150, 150, 160], CONV_D: [110, 110, 120],
  PROG_G: [50, 220, 50], PROG_BG: [50, 50, 55], PROG_FR: [80, 80, 90],
  GOLD: [240, 200, 50], LAPIS: [50, 70, 180], RED: [180, 40, 40],
  EMERALD: [50, 200, 80], DIAMOND: [80, 210, 230],
  BB: [65, 50, 35], BB_D: [45, 35, 25],
  // BG
  BG: [20, 20, 28],
};

// ─── PixelBuffer ────────────────────────────────────────────────────

class PixelBuffer {
  constructor(w, h) {
    this.w = w;
    this.h = h % 2 === 0 ? h : h + 1;
    this.px = [];
    for (let y = 0; y < this.h; y++) {
      const row = [];
      for (let x = 0; x < this.w; x++) row.push(P.BG);
      this.px.push(row);
    }
  }
  set(x, y, c) {
    if (x >= 0 && x < this.w && y >= 0 && y < this.h) this.px[y][x] = c;
  }
  get(x, y) {
    if (x >= 0 && x < this.w && y >= 0 && y < this.h) return this.px[y][x];
    return P.BG;
  }
  fill(x, y, w, h, c) {
    for (let dy = 0; dy < h; dy++)
      for (let dx = 0; dx < w; dx++)
        this.set(x + dx, y + dy, c);
  }
  sprite(art, map, x, y) {
    for (let sy = 0; sy < art.length; sy++)
      for (let sx = 0; sx < art[sy].length; sx++) {
        const c = map[art[sy][sx]];
        if (c) this.set(x + sx, y + sy, c);
      }
  }
  toHtml() {
    const lines = [];
    const cache = {};
    for (let tr = 0; tr < this.h / 2; tr++) {
      const top = this.px[tr * 2], bot = this.px[tr * 2 + 1];
      let html = '';
      let prevKey = null;
      for (let x = 0; x < this.w; x++) {
        const t = top[x], b = bot[x];
        const key = `${t[0]},${t[1]},${t[2]}|${b[0]},${b[1]},${b[2]}`;
        if (key === prevKey) {
          html += '\u2580';
        } else {
          if (prevKey !== null) html += '</span>';
          let span = cache[key];
          if (!span) {
            span = `<span style="color:rgb(${t[0]},${t[1]},${t[2]});background:rgb(${b[0]},${b[1]},${b[2]})">`;
            cache[key] = span;
          }
          html += span + '\u2580';
          prevKey = key;
        }
      }
      if (prevKey !== null) html += '</span>';
      lines.push(html);
    }
    return lines;
  }
  /** Write pixel data into an ImageData for canvas rendering. */
  toImageData() {
    const data = new Uint8ClampedArray(this.w * this.h * 4);
    for (let y = 0; y < this.h; y++) {
      const row = this.px[y];
      for (let x = 0; x < this.w; x++) {
        const c = row[x];
        const i = (y * this.w + x) * 4;
        data[i] = c[0]; data[i + 1] = c[1]; data[i + 2] = c[2]; data[i + 3] = 255;
      }
    }
    return new ImageData(data, this.w, this.h);
  }
}

// ─── Agent color legends ────────────────────────────────────────────

const A1 = {
  'O': P.OL,
  '1': P.HAIR_HL, 'H': P.HAIR, 'h': P.HAIR_D,
  'L': P.SKIN_HL, 'S': P.SKIN, 's': P.SKIN_S, 'd': P.SKIN_D,
  'W': P.EYE_W, 'E': P.EYE_P,
  'T': P.S1L, 'C': P.S1, 'c': P.S1D,
  'Q': P.PL, 'P': P.P, 'p': P.PS,
  'g': P.SH_HL, 'G': P.SH,
  '.': null,
};
const A2 = { ...A1, 'T': P.S2L, 'C': P.S2, 'c': P.S2D };

// ─── NES Sprite art (16x20) ────────────────────────────────────────

const SP = {
  sit: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '....OcCCCCcO....',
    '....OccccccO....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  sitL: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '..OcCCCCCCCCcO..',
    '..Oc...OCCCcO...',
    '..O....OccccO...',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  sitR: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '...OCCCcO...cO..',
    '...OccccO....O..',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  sitBoth: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '..OcCCCCCCCCcO..',
    '..OcCCCCCCCCcO..',
    '..Oc..OCCCc..O..',
    '..O...Occcc..O..',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  sitThink: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSsO....',
    '...OOTTCCTTsO...',
    '...OCCCCCCCsLO..',
    '...OCCCCCCCCcO..',
    '....OcCCCCcO....',
    '....OccccccO....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  stand: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '...OcCCCCCCcO...',
    '...OcCC..CCcO...',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPPO...',
    '....OPPpO.pPPO..',
    '...OgGGO..OgGGO.',
    '...OGGGO..OOGGO.',
    '....OOO....OOO..',
  ],
  point: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOOOO.',
    '...OCCCCCCCCcccO',
    '...OCCCCCCCCcccO',
    '...OcCCCCCCcOOsO',
    '...OcCC..CCcO...',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPPO...',
    '....OPPpO.pPPO..',
    '...OgGGO..OgGGO.',
    '...OGGGO..OOGGO.',
    '....OOO....OOO..',
  ],
  examine: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '...OcCCCCCCcO...',
    '....OCC..CCO....',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPPO...',
    '....OPPpO.pPPO..',
    '...OgGGO..OgGGO.',
    '...OGGGO..OOGGO.',
    '....OOO....OOO..',
  ],
  walk1: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '...OcCCCCCCcO...',
    '...OcCC..CCcO...',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '...OPPPpO.pPPO..',
    '..OPPpO....pPPO.',
    '..OgGGO...OgGGO.',
    '..OGGGO...OOGGO.',
    '...OOO.....OOO..',
  ],
  walk2: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '...OcCCCCCCcO...',
    '...OcCC..CCcO...',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPpOpPPO...',
    '....OPPpOpPPO...',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  lean: [
    '.......OOOOOO...',
    '......O1HHHH1O..',
    '......OHHHHH1O..',
    '.....OOHHHHHhOO.',
    '.....OLWESWLEO..',
    '.....OSSdSdSSO..',
    '......OSSSSO....',
    '....OOTTCCTTOO..',
    '....OCCCCCCCCcO.',
    '....OCCCCCCCCcO.',
    '.....OcCCCCcO...',
    '.....OccccccO...',
    '.....OQPPPPQO...',
    '.....OPPPPPPO...',
    '.....OPPPpPPO...',
    '.....OPPpOpPPO..',
    '.....OppOOppO...',
    '....OgGGOOgGGO..',
    '....OGGGOOOGGO..',
    '.....OOO..OOO...',
  ],
  push1: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOOOO.',
    '...OCCCCCCCCcccO',
    '...OCCCCCCCCccsO',
    '...OcCCCCCCcOOO.',
    '...OcCC..CCcO...',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPPO...',
    '....OPPpO.pPPO..',
    '...OgGGO..OgGGO.',
    '...OGGGO..OOGGO.',
    '....OOO....OOO..',
  ],
  push2: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '.OOOOTCCCCTTOO..',
    'OcsccCCCCCCCCO..',
    'OsccCCCCCCCCcO..',
    '.OOOcCCCCCCcO...',
    '...OcCC..CCcO...',
    '....OcccccO.....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPPO...',
    '....OPPpO.pPPO..',
    '...OgGGO..OgGGO.',
    '...OGGGO..OOGGO.',
    '....OOO....OOO..',
  ],
  drink1: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOO..',
    '....OLWESWLEO...',
    '....OSSdSdSSO...',
    '.....OSSSSO.....',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcOMO',
    '....OcCCCCcOOMkO',
    '....OccccccOOKOO',
    '....OQPPPPQO.OO.',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
  drink2: [
    '......OOOOOO....',
    '.....O1HHHH1O...',
    '.....OHHHHH1O...',
    '....OOHHHHHhOMO.',
    '....OLWESWLEOMkO',
    '....OSSdSdSSOOKO',
    '.....OSSSSO..OO.',
    '...OOTTCCTTOO...',
    '...OCCCCCCCCcO..',
    '...OCCCCCCCCcO..',
    '....OcCCCCcO....',
    '....OccccccO....',
    '....OQPPPPQO....',
    '....OPPPPPPO....',
    '....OPPPpPPO....',
    '....OPPpOpPPO...',
    '....OppOOppO....',
    '...OgGGOOgGGO...',
    '...OGGGOOOGGO...',
    '....OOO..OOO....',
  ],
};

const DRINK_MAP = { ...A1, 'M': P.MUG, 'K': P.COFFEE, 'k': [220, 195, 150] };
const CARRY_MAP = { ...A1, 'B': P.GOLD, 'b': P.LAPIS, 'D': P.DIAMOND };

const CARRY1 = [
  '....OBBBBBO.....',
  '....ObBBBbO.....',
  '....OOOOOOO.....',
  '.....OsSssSO....',
  '.....O1HHHHO....',
  '....OOHHHH1OO...',
  '....OLWESWLEO...',
  '....OSSdSdSSO...',
  '.....OSSSSO.....',
  '...OOTTCCTTOO...',
  '...OCCCCCCCCcO..',
  '...OCCCCCCCCcO..',
  '...OcCCCCCCcO...',
  '....OcccccO.....',
  '....OQPPPPQO....',
  '...OPPPpO.pPPO..',
  '..OPPpO....pPPO.',
  '..OgGGO...OgGGO.',
  '..OGGGO...OOGGO.',
  '...OOO.....OOO..',
];
const CARRY2 = [
  '....OBBBBBO.....',
  '....ObBBBbO.....',
  '....OOOOOOO.....',
  '.....OsSssSO....',
  '.....O1HHHHO....',
  '....OOHHHH1OO...',
  '....OLWESWLEO...',
  '....OSSdSdSSO...',
  '.....OSSSSO.....',
  '...OOTTCCTTOO...',
  '...OCCCCCCCCcO..',
  '...OCCCCCCCCcO..',
  '...OcCCCCCCcO...',
  '....OcccccO.....',
  '....OQPPPPQO....',
  '....OPPpOpPPO...',
  '....OPPpOpPPO...',
  '...OgGGOOgGGO...',
  '...OGGGOOOGGO...',
  '....OOO..OOO....',
];

// ─── Isometric math (ported from iso_office.py) ─────────────────────

const TILE_W = 16;
const TILE_H = 8;

function isoToScreen(gx, gy, ox, oy) {
  const sx = Math.floor((gx - gy) * TILE_W / 2 + ox);
  const sy = Math.floor((gx + gy) * TILE_H / 2 + oy);
  return [sx, sy];
}

// ─── Isometric drawing primitives ───────────────────────────────────

function drawIsoDiamond(buf, cx, cy, color, highlight, shadow) {
  const hw = TILE_W >> 1;
  const hh = TILE_H >> 1;
  for (let dy = 0; dy < TILE_H; dy++) {
    let span;
    if (dy < hh) {
      span = Math.floor((dy + 1) * hw / hh);
    } else {
      span = Math.floor((TILE_H - dy) * hw / hh);
    }
    for (let dx = -span + 1; dx < span; dx++) {
      const px = cx + dx;
      const py = cy - hh + dy;
      let c;
      if (dx < 0 && highlight) c = highlight;
      else if (dx > 0 && shadow) c = shadow;
      else c = color;
      buf.set(px, py, c);
    }
  }
}

// ─── Isometric room geometry ────────────────────────────────────────

function drawIsoFloor(buf, gridW, gridD, ox, oy) {
  for (let gy = 0; gy < gridD; gy++) {
    for (let gx = 0; gx < gridW; gx++) {
      const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);
      if ((gx + gy) % 2 === 0) {
        drawIsoDiamond(buf, cx, cy, P.OAK, P.OAK_L, P.OAK_D);
      } else {
        drawIsoDiamond(buf, cx, cy, P.OAK_D, P.OAK, P.OAK_LOG);
      }
    }
  }
}

function drawBackWall(buf, gridW, gridD, ox, oy, wallH) {
  for (let gx = 0; gx < gridW; gx++) {
    const [x1, y1] = isoToScreen(gx, 0, ox, oy);
    const [x2, y2] = isoToScreen(gx + 1, 0, ox, oy);
    const dx = x2 - x1;
    for (let step = 0; step < Math.max(1, dx); step++) {
      const t = dx !== 0 ? step / Math.max(1, dx) : 0;
      const x = x1 + step;
      const y = Math.floor(y1 + t * (y2 - y1));
      for (let h = 0; h < wallH; h++) {
        const frac = h / Math.max(1, wallH - 1);
        // Brick pattern
        const bx = (x + (((Math.floor((y - h) / 3)) % 2) ? 3 : 0)) % 6;
        const by = ((y - h) % 3 + 3) % 3;
        let c;
        if (bx === 0 || by === 0) {
          c = P.STONE_D;
        } else if (frac > 0.7) {
          c = P.STONE_L;
        } else if (frac > 0.3) {
          c = P.STONE;
        } else {
          c = P.STONE_D;
        }
        buf.set(x, y - h, c);
      }
    }
    // Top edge highlight
    for (let step = 0; step < Math.max(1, dx); step++) {
      const x = x1 + step;
      const t = dx !== 0 ? step / Math.max(1, dx) : 0;
      const y = Math.floor(y1 + t * (y2 - y1));
      buf.set(x, y - wallH, P.STONE_HL);
    }
  }
}

function drawLeftWall(buf, gridD, ox, oy, wallH) {
  for (let gy = 0; gy < gridD; gy++) {
    const [x1, y1] = isoToScreen(0, gy, ox, oy);
    const [x2, y2] = isoToScreen(0, gy + 1, ox, oy);
    const dx = x2 - x1;
    const steps = Math.max(1, Math.abs(dx));
    for (let step = 0; step < steps; step++) {
      const t = step / Math.max(1, steps);
      const x = Math.floor(x1 + t * dx);
      const y = Math.floor(y1 + t * (y2 - y1));
      for (let h = 0; h < wallH; h++) {
        const frac = h / Math.max(1, wallH - 1);
        // Left wall darker (shadow side)
        const bx = (x + (((Math.floor((y - h) / 3)) % 2) ? 3 : 0)) % 6;
        const by = ((y - h) % 3 + 3) % 3;
        let c;
        if (bx === 0 || by === 0) {
          c = P.COBBLE;
        } else if (frac > 0.7) {
          c = P.STONE;
        } else if (frac > 0.3) {
          c = P.STONE_D;
        } else {
          c = P.COBBLE;
        }
        buf.set(x, y - h, c);
      }
    }
  }
}

// ─── Isometric furniture ────────────────────────────────────────────

function drawIsoDesk(buf, gx, gy, ox, oy) {
  const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);
  const deskH = 6;
  const topY = cy - deskH;
  const hw = Math.floor(TILE_W * 0.7);
  const hh = TILE_H >> 1;

  // Desk top surface
  for (let dy = 0; dy < TILE_H; dy++) {
    let span;
    if (dy < hh) span = Math.floor((dy + 1) * hw / hh);
    else span = Math.floor((TILE_H - dy) * hw / hh);
    for (let dx = -span + 1; dx < span; dx++) {
      const px = cx + dx;
      const py = topY - hh + dy;
      let c;
      if (dx < 0) c = P.OAK_L;
      else if (dx > 0) c = P.OAK_D;
      else c = P.OAK;
      buf.set(px, py, c);
    }
  }

  // Front edge thickness (2px)
  for (let dy = 1; dy <= 2; dy++) {
    for (let halfRow = 0; halfRow < hh; halfRow++) {
      const span = Math.floor((hh - halfRow) * hw / hh);
      const y = topY + halfRow + dy;
      for (let dx = 0; dx < span; dx++) buf.set(cx + dx, y, P.OAK_D);
      for (let dx = -span + 1; dx <= 0; dx++) buf.set(cx + dx, y, P.OAK);
    }
  }

  // Legs
  const legPositions = [
    [-hw + 2, -hh + 1],
    [hw - 2, -hh + 1],
    [-hw + 3, hh - 1],
    [hw - 3, hh - 1],
  ];
  for (const [lx, ly] of legPositions) {
    const legX = cx + lx;
    const legY = topY + ly;
    for (let h = 0; h < deskH - 2; h++) {
      buf.set(legX, legY + 2 + h, P.OAK_LOG);
    }
  }
}

function drawIsoMonitor(buf, gx, gy, ox, oy, deskH = 6) {
  const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);
  const baseY = cy - deskH;
  const monW = 12;
  const monH = 9;
  const mx = cx - (monW >> 1);
  const my = baseY - monH - 2;

  // Stand
  buf.set(cx, baseY - 2, P.IRON_D);
  buf.set(cx, baseY - 1, P.IRON_D);
  buf.set(cx - 1, baseY, P.IRON_D);
  buf.set(cx, baseY, P.IRON_D);
  buf.set(cx + 1, baseY, P.IRON_D);

  // Frame
  buf.fill(mx, my, monW, monH, P.MON_FR);
  // Glow border
  buf.fill(mx + 1, my + 1, monW - 2, monH - 2, P.MON_GLOW);
  // Screen
  buf.fill(mx + 2, my + 2, monW - 4, monH - 4, P.MON_BG);
  // Power LED
  buf.set(mx + monW - 2, my + monH - 1, P.LED_G);

  return [mx + 2, my + 2, monW - 4, monH - 4];
}

function drawIsoChair(buf, gx, gy, ox, oy) {
  const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);
  const seatY = cy - 3;
  const seatHw = 4;
  const seatHh = 2;

  // Seat diamond
  for (let dy = 0; dy < 4; dy++) {
    let span;
    if (dy < seatHh) span = Math.floor((dy + 1) * seatHw / seatHh);
    else span = Math.floor((4 - dy) * seatHw / seatHh);
    for (let dx = -span + 1; dx < span; dx++) {
      const c = dx < 0 ? P.CH_HL : P.CH;
      buf.set(cx + dx, seatY - seatHh + dy, c);
    }
  }

  // Back rest
  const backX = cx - 2;
  const backY = seatY - seatHh - 4;
  buf.fill(backX, backY, 3, 4, P.CH);
  buf.set(backX, backY, P.CH_HL);

  // Center post
  buf.set(cx, cy - 1, P.CH_S);
  // Wheel base
  buf.set(cx - 2, cy, P.CH_S);
  buf.set(cx, cy, P.CH_S);
  buf.set(cx + 2, cy, P.CH_S);
}

function drawIsoServerRack(buf, gx, gy, ox, oy, fi) {
  const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);
  const rackW = 8;
  const rackH = 16;
  const rx = cx - (rackW >> 1);
  const ry = cy - rackH;

  // Main body
  buf.fill(rx, ry, rackW, rackH, P.IRON_D);

  // Server units
  for (let row = 1; row < rackH - 1; row += 2) {
    buf.fill(rx + 1, ry + row, rackW - 2, 1, P.IRON);
    const colors = [P.LED_G, P.LED_A, P.LED_G, P.LED_O];
    const led1 = (fi + row) % 4;
    const led2 = (fi + row + 2) % 4;
    buf.set(rx + 1, ry + row, colors[led1]);
    buf.set(rx + rackW - 2, ry + row, colors[led2]);
  }

  // Top highlight
  for (let dx = 0; dx < rackW; dx++) {
    buf.set(rx + dx, ry, P.STONE_HL);
  }
}

function drawIsoPlant(buf, gx, gy, ox, oy, fi) {
  const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);

  // Pot
  buf.fill(cx - 2, cy - 3, 5, 3, P.POT);
  buf.set(cx - 2, cy - 3, [160, 85, 50]);

  // Stem
  buf.set(cx, cy - 4, P.LEAF_D);
  buf.set(cx, cy - 5, P.LEAF_D);
  buf.set(cx, cy - 6, P.LEAF_D);

  // Leaves (sway)
  const sway = fi % 8 < 4 ? 1 : 0;
  buf.set(cx - 1 + sway, cy - 7, P.LEAF_L);
  buf.set(cx + sway, cy - 7, P.LEAF);
  buf.set(cx + 1, cy - 7, P.LEAF);
  buf.set(cx - 2 + sway, cy - 6, P.LEAF);
  buf.set(cx + 2, cy - 6, P.LEAF_D);
  buf.set(cx - 1, cy - 5, P.LEAF);
  buf.set(cx + 1, cy - 5, P.LEAF_D);
}

// ─── Agent positioning ──────────────────────────────────────────────

function isoAgentPos(gx, gy, ox, oy, spriteH) {
  const [cx, cy] = isoToScreen(gx + 0.5, gy + 0.5, ox, oy);
  return [cx - 8, cy - spriteH];
}

// ─── Main isometric office builder ──────────────────────────────────

function buildIsoOffice(w, ph, fi) {
  const buf = new PixelBuffer(w, ph);

  // Dynamic grid sizing: fill the screen (matches Python algorithm)
  const wallFrac = 0.30;
  const floorBudgetH = Math.floor(ph * (1.0 - wallFrac));

  let totalTilesForWidth = Math.floor((w * 2) / TILE_W);
  let totalTilesForHeight = Math.floor((floorBudgetH * 2) / TILE_H);
  let totalTiles = Math.min(totalTilesForWidth, totalTilesForHeight);
  totalTiles = Math.max(totalTiles, 4);

  let gridW = Math.max(2, Math.floor(totalTiles * 0.55));
  let gridD = Math.max(2, totalTiles - gridW);

  while ((gridW + gridD) * TILE_W / 2 > w && gridW + gridD > 3) {
    if (gridW > gridD) gridW--;
    else gridD--;
  }

  const floorPixelH = Math.floor((gridW + gridD) * TILE_H / 2);
  const wallPixelH = Math.max(8, ph - floorPixelH - 2);
  const originX = Math.floor(w / 2 - (gridW - gridD) * TILE_W / 4);
  const originY = ph - floorPixelH - 1;

  // Draw walls first (behind everything)
  drawBackWall(buf, gridW, gridD, originX, originY, wallPixelH);
  drawLeftWall(buf, gridD, originX, originY, wallPixelH);

  // Draw floor
  drawIsoFloor(buf, gridW, gridD, originX, originY);

  // Furniture — placed relative to grid, scales with room size
  const desk1Gx = 1.0;
  const desk1Gy = 1.0;
  drawIsoDesk(buf, desk1Gx, desk1Gy, originX, originY);
  const mon1Rect = drawIsoMonitor(buf, desk1Gx, desk1Gy, originX, originY);
  drawIsoChair(buf, desk1Gx, desk1Gy + 1.2, originX, originY);

  // Desk 2: offset to the right
  const desk2Gx = Math.min(gridW - 2.0, Math.max(3.0, gridW * 0.5));
  const desk2Gy = 1.0;
  let mon2Rect = [0, 0, 0, 0];
  if (w >= 50) {
    drawIsoDesk(buf, desk2Gx, desk2Gy, originX, originY);
    mon2Rect = drawIsoMonitor(buf, desk2Gx, desk2Gy, originX, originY);
    drawIsoChair(buf, desk2Gx, desk2Gy + 1.2, originX, originY);
  }

  // Server rack (back-right area)
  if (w >= 50) {
    drawIsoServerRack(buf, gridW - 1.5, 0.5, originX, originY, fi);
  }

  // Plant (front-left area)
  const plantGy = Math.min(gridD - 1.0, Math.max(2.0, gridD * 0.7));
  drawIsoPlant(buf, 0.0, plantGy, originX, originY, fi);

  const layout = {
    originX,
    originY,
    gridW,
    gridD,
    wallH: wallPixelH,
    desk1Gx,
    desk1Gy,
    desk2Gx,
    desk2Gy,
    mon1Rect,
    mon2Rect,
    agent1Gx: desk1Gx,
    agent1Gy: desk1Gy + 0.8,
    agent2Gx: desk2Gx,
    agent2Gy: desk2Gy + 0.8,
  };

  return { buf, layout };
}

// ─── Scene generators (isometric) ───────────────────────────────────

function genThinking(w, h, n = 8) {
  const ph = h * 2;
  const bubbles = [
    { art: ['....OOOOOO..','..OOLLLLLOO.','.OLLDDLDLLO.','.OLLDLLDDLO.','.OLLDDDLLLO.','..OOLLLLLOO.','....OOOOOO..','.....OO.....','......OO....'],
      map: { O: P.THOUGHT_D, L: P.THOUGHT, D: P.THOUGHT_L, '.': null } },
    { art: ['....OOOOOO..','..OOLLLLLOO.','.OLL.YY.LLO.','.OLL..Y.LLO.','.OLLL.Y.LLO.','..OOLLYLLOO.','....OOOOOO..','.....OO.....','......OO....'],
      map: { O: P.THOUGHT_D, L: P.THOUGHT, Y: P.WARN_Y, '.': null } },
    { art: ['....OOOOOO..','..OOLLLLLOO.','.OLL.GG.LLO.','.OLLGGGGLLLO','.OLL.GG.LLO.','..OOLLLLLOO.','....OOOOOO..','.....OO.....','......OO....'],
      map: { O: P.THOUGHT_D, L: P.THOUGHT, G: P.GLOW, '.': null } },
  ];
  const bSeq = [0, 0, 1, 1, 2, 2, 0, 1];
  const spriteH = SP.sitThink.length;

  return Array.from({ length: n }, (_, fi) => {
    const { buf, layout } = buildIsoOffice(w, ph, fi);
    const ox = layout.originX;
    const oy = layout.originY;

    // Agent 1 thinking at desk
    if (w >= 40) {
      const [ax, ay] = isoAgentPos(layout.agent1Gx, layout.agent1Gy, ox, oy, spriteH);
      buf.sprite(SP.sitThink, A1, ax, ay);

      // Thought bubble above agent
      const b = bubbles[bSeq[fi % bSeq.length]];
      const by = Math.max(0, ay - b.art.length - 1);
      buf.sprite(b.art, b.map, ax - 2, by);
    }

    // Agent 2 idle at desk 2
    if (w >= 60) {
      const [ax2, ay2] = isoAgentPos(layout.agent2Gx, layout.agent2Gy, ox, oy, SP.sit.length);
      buf.sprite(SP.sit, A2, ax2, ay2);

      // Cursor blink on monitor 2
      const [mx, my] = layout.mon2Rect;
      if (fi % 2 === 0) buf.set(mx + 1, my + 1, P.MON_GR);
      else buf.set(mx + 1, my + 1, P.MON_BG);
    }

    return buf;
  });
}

function genCoding(w, h, n = 8) {
  const ph = h * 2;
  const rng = (s) => ((s * 1103515245 + 12345) & 0x7fffffff) % 256;
  const cc = [P.MON_GR, P.MON_YL, P.MON_WH, P.MON_CY];
  const types = [SP.sitL, SP.sitR, SP.sitBoth, SP.sit];
  const spriteH = SP.sit.length;

  return Array.from({ length: n }, (_, fi) => {
    const { buf, layout } = buildIsoOffice(w, ph, fi);
    const ox = layout.originX;
    const oy = layout.originY;

    // Agent 1 typing at desk 1
    if (w >= 40) {
      const agent = types[fi % types.length];
      const [ax, ay] = isoAgentPos(layout.agent1Gx, layout.agent1Gy, ox, oy, agent.length);
      buf.sprite(agent, A1, ax, ay);

      // Code on monitor 1
      const [mx, my, mw, mh] = layout.mon1Rect;
      for (let r = 0; r < Math.min(mh, 4); r++)
        for (let c = 0; c < mw; c++) {
          const seed = rng(fi * 100 + r * 10 + c);
          if (seed > 70) buf.set(mx + c, my + r, cc[seed % cc.length]);
        }
    }

    // Agent 2 typing at desk 2
    if (w >= 60) {
      const agent2 = types[(fi + 2) % types.length];
      const [ax2, ay2] = isoAgentPos(layout.agent2Gx, layout.agent2Gy, ox, oy, agent2.length);
      buf.sprite(agent2, A2, ax2, ay2);

      // Code on monitor 2
      const [mx2, my2, mw2, mh2] = layout.mon2Rect;
      for (let r = 0; r < Math.min(mh2, 4); r++)
        for (let c = 0; c < mw2; c++) {
          const seed = rng((fi + 3) * 100 + r * 10 + c);
          if (seed > 50) buf.set(mx2 + c, my2 + r, cc[seed % cc.length]);
        }
    }

    return buf;
  });
}

function genDebugging(w, h, n = 8) {
  const ph = h * 2;
  const warnArt = [
    '....OYO.....',
    '...OYYYO....',
    '..OYYYYYO...',
    '.OYYYRYYYO..',
    'OYYYYYYYYY0.',
    'OOOOOOOOOOO.',
  ];
  const warnMap = { Y: P.WARN_Y, R: P.WARN_R, O: P.OL, '0': P.OL, '.': null };

  return Array.from({ length: n }, (_, fi) => {
    const { buf, layout } = buildIsoOffice(w, ph, fi);
    const ox = layout.originX;
    const oy = layout.originY;
    const wallH = layout.wallH;

    // Whiteboard on wall area
    const wbW = Math.min(14, Math.floor(w / 5));
    const wbH = Math.min(8, wallH - 2);
    if (wbW >= 8 && wbH >= 5) {
      const wbX = ox - Math.floor(wbW / 2);
      const wbY = Math.max(1, oy - wallH + 2);
      // Board
      buf.fill(wbX, wbY, wbW, wbH, P.BIRCH);
      // Frame
      for (let dx = 0; dx < wbW; dx++) { buf.set(wbX + dx, wbY, P.MON_FR); buf.set(wbX + dx, wbY + wbH - 1, P.MON_FR); }
      for (let dy = 0; dy < wbH; dy++) { buf.set(wbX, wbY + dy, P.MON_FR); buf.set(wbX + wbW - 1, wbY + dy, P.MON_FR); }
      // Diagram: boxes + arrow
      const boxY = wbY + 2;
      buf.fill(wbX + 2, boxY, 3, 2, [220, 220, 220]);
      for (let dx = 5; dx < Math.min(wbW - 4, 9); dx++) buf.set(wbX + dx, boxY + 1, P.WARN_R);
      if (wbW > 10) buf.fill(wbX + wbW - 5, boxY, 3, 2, P.WARN_R);
      // Error lines
      for (let dy = boxY + 3; dy < wbY + wbH - 1; dy++) {
        const lineLen = ((dy + fi) * 3) % (wbW - 3) + 1;
        for (let dx = 1; dx < Math.min(1 + lineLen, wbW - 1); dx++) {
          if ((dx + fi) % 3 !== 0) buf.set(wbX + dx, dy, P.MON_RD);
        }
      }
    }

    // Agent 1 pointing
    if (w >= 40) {
      const ptr = fi % 2 === 0 ? SP.point : SP.stand;
      const [ax, ay] = isoAgentPos(
        layout.desk1Gx - 0.5, layout.desk1Gy - 0.3,
        ox, oy, ptr.length,
      );
      buf.sprite(ptr, A1, ax, ay);
    }

    // Agent 2 examining monitor
    if (w >= 60) {
      const ex = fi % 2 === 0 ? SP.examine : SP.stand;
      const [ax2, ay2] = isoAgentPos(layout.agent2Gx, layout.agent2Gy, ox, oy, ex.length);
      buf.sprite(ex, A2, ax2, ay2);

      // Error text on monitor 2
      const [mx2, my2, mw2, mh2] = layout.mon2Rect;
      for (let dy = 0; dy < mh2; dy++)
        for (let dx = 0; dx < mw2; dx++) {
          if ((dx + fi) % 4 === 0) buf.set(mx2 + dx, my2 + dy, P.MON_RD);
          else if ((dx + dy + fi) % 6 === 0) buf.set(mx2 + dx, my2 + dy, P.WARN_Y);
        }
    }

    // Error text on monitor 1
    const [mx1, my1, mw1, mh1] = layout.mon1Rect;
    for (let dy = 0; dy < mh1; dy++)
      for (let dx = 0; dx < mw1; dx++) {
        if ((dx + fi) % 4 === 0) buf.set(mx1 + dx, my1 + dy, P.MON_RD);
        else if ((dx + dy + fi) % 6 === 0) buf.set(mx1 + dx, my1 + dy, P.WARN_Y);
      }

    // Warning triangle (blinks)
    if (fi % 3 !== 2) {
      buf.sprite(warnArt, warnMap, Math.floor(w / 2) - 5, 0);
    }

    // Red tint
    for (let y = 0; y < buf.h; y++)
      for (let x = 0; x < buf.w; x++) {
        const [r, g, b] = buf.px[y][x];
        if (r + g + b < 200)
          buf.px[y][x] = [Math.min(255, r + 30), Math.max(0, g - 15), Math.max(0, b - 15)];
        else
          buf.px[y][x] = [Math.min(255, r + 12), Math.max(0, g - 5), Math.max(0, b - 5)];
      }

    return buf;
  });
}

function genRunning(w, h, n = 8) {
  const ph = h * 2;
  const gMap = { G: P.GEAR, g: P.GEAR_D, L: P.GEAR_L, O: P.OL, '.': null };
  const gears = [
    ['..OGGO..', '.OLLLLO.', 'OLLGGLLO', 'OLGGGLLO', 'OLGGGLLO', 'OLLGGLLO', '.OLLLLO.', '..OGGO..'],
    ['.OG..GO.', 'OLLLLGO.', '.OLggLLO', 'OLLggLLO', 'OLLggLLO', 'OLLggLO.', '.OGLLLLO', '.OG..GO.'],
    ['..OGGO..', '.OLLLLO.', 'OLLggLLO', 'OLgggLLO', 'OLLgggLO', 'OLLggLLO', '.OLLLLO.', '..OGGO..'],
    ['.OG..GO.', '.OGLLLLO', 'OLLggLO.', 'OLLggLLO', 'OLLggLLO', '.OLggLLO', 'OLLLLGO.', '.OG..GO.'],
  ];

  return Array.from({ length: n }, (_, fi) => {
    const { buf, layout } = buildIsoOffice(w, ph, fi);
    const ox = layout.originX;
    const oy = layout.originY;
    const wallH = layout.wallH;

    // Control panel on wall area
    const panelW = Math.min(14, Math.floor(w / 5));
    const panelH = Math.min(7, wallH - 2);
    if (panelW >= 8 && panelH >= 5) {
      const panelX = ox - Math.floor(panelW / 2) + 10;
      const panelY = Math.max(1, oy - wallH + 2);
      buf.fill(panelX, panelY, panelW, panelH, P.IRON_D);
      buf.fill(panelX + 1, panelY + 1, panelW - 2, panelH - 2, P.IRON);
      for (let dx = 1; dx < panelW - 1; dx++) buf.set(panelX + dx, panelY + 1, [220, 220, 225]);
      for (let bx = 2; bx < panelW - 2; bx += 3)
        for (let by = 2; by < Math.min(panelH - 1, 6); by++) {
          const idx = bx + by * panelW;
          const state = (fi + idx) % 5;
          const colors = [P.LED_G, P.LED_A, P.LED_G, P.LED_G, P.LED_O];
          buf.set(panelX + bx, panelY + by, colors[state]);
          buf.set(panelX + bx + 1, panelY + by, P.IRON_D);
        }
    }

    // Agent pushing buttons
    if (w >= 40) {
      const pushes = [SP.push1, SP.push2, SP.stand];
      const agent = pushes[fi % pushes.length];
      const [ax, ay] = isoAgentPos(
        layout.desk1Gx + 0.5, layout.desk1Gy - 0.3,
        ox, oy, agent.length,
      );
      buf.sprite(agent, A1, ax, ay);
    }

    // Gear animation (on floor, right side)
    if (w >= 55) {
      const gear = gears[fi % gears.length];
      const [gearX, gearY] = isoToScreen(layout.gridW - 2.0, layout.gridD - 2.0, ox, oy);
      buf.sprite(gear, gMap, gearX - 4, gearY - gear.length);
    }

    // Log on monitor 1
    const [mx1, my1, mw1, mh1] = layout.mon1Rect;
    for (let dy = 0; dy < mh1; dy++) {
      const lineLen = ((dy + fi) * 3) % Math.max(1, mw1) + 1;
      for (let dx = 0; dx < Math.min(lineLen, mw1); dx++) {
        const c = (dy + fi) % 3 !== 0 ? P.MON_GR : P.MON_WH;
        buf.set(mx1 + dx, my1 + dy, c);
      }
    }

    // Log on monitor 2
    if (w >= 60) {
      const [mx2, my2, mw2, mh2] = layout.mon2Rect;
      for (let dy = 0; dy < mh2; dy++) {
        const lineLen = ((dy + fi + 3) * 3) % Math.max(1, mw2) + 1;
        for (let dx = 0; dx < Math.min(lineLen, mw2); dx++) {
          const c = (dy + fi + 3) % 3 !== 0 ? P.MON_GR : P.MON_WH;
          buf.set(mx2 + dx, my2 + dy, c);
        }
      }
    }

    // Progress bar at bottom
    if (w >= 40) {
      const barW = Math.min(24, Math.floor(w / 3));
      const barX = Math.floor((w - barW) / 2);
      const barY = ph - 4;
      buf.fill(barX - 1, barY - 1, barW + 2, 4, P.PROG_FR);
      buf.fill(barX, barY, barW, 2, P.PROG_BG);
      const fill = Math.floor(((fi + 1) * barW) / n);
      for (let dx = 0; dx < fill; dx++) {
        const c = dx === fill - 1 ? [100, 255, 100] : dx === fill - 2 ? [70, 240, 70] : P.PROG_G;
        buf.set(barX + dx, barY, c);
        buf.set(barX + dx, barY + 1, c);
      }
    }

    return buf;
  });
}

function genBuilding(w, h, n = 8) {
  const ph = h * 2;
  const bColors = [P.GOLD, P.LAPIS, P.RED, P.EMERALD, P.DIAMOND];

  return Array.from({ length: n }, (_, fi) => {
    const { buf, layout } = buildIsoOffice(w, ph, fi);
    const ox = layout.originX;
    const oy = layout.originY;

    // Conveyor belt across the floor area
    const convW = Math.min(w - 14, Math.floor(w * 2 / 3));
    const convX = Math.floor((w - convW) / 2);
    const floorScreenY = oy + Math.floor((layout.gridW + layout.gridD) * 4 / 2);
    const convY = Math.min(floorScreenY - 2, ph - 10);

    if (convW >= 12) {
      // Conveyor belt
      for (let dx = 0; dx < convW; dx++) {
        const m = (dx + fi) % 4;
        buf.set(convX + dx, convY, m === 0 ? P.CONV_D : m === 1 ? P.CONV_L : P.CONV);
        buf.set(convX + dx, convY + 1, m === 0 ? P.CONV_D : P.CONV);
      }
      // Side rails
      for (let dx = 0; dx < convW; dx++) {
        buf.set(convX + dx, convY - 1, P.STONE_D);
        buf.set(convX + dx, convY + 2, P.STONE_D);
      }
      // Supports
      for (let dx = 0; dx < convW; dx += 8)
        for (let dy = 3; dy < 6; dy++) {
          buf.set(convX + dx, convY + dy, P.STONE_D);
          buf.set(convX + dx + 1, convY + dy, P.STONE_D);
        }
    }

    // Carrier agent walking along conveyor
    if (convW >= 12) {
      const agentX = convX + ((fi * 5) % Math.max(1, convW - 16));
      buf.sprite(CARRY1, CARRY_MAP, agentX, convY - CARRY1.length - 1);
    }

    // Second agent walking opposite direction
    if (w >= 55 && convW >= 12) {
      const wx2 = convX + convW - ((fi * 4) % Math.max(1, convW - 16)) - 16;
      const walkSprite = fi % 2 === 0 ? SP.walk1 : SP.walk2;
      buf.sprite(walkSprite, A1, Math.max(convX, wx2), convY - walkSprite.length - 1);
    }

    // Code blocks on conveyor
    if (convW >= 24) {
      for (let i = 0; i < 3; i++) {
        const bx = convX + 6 + ((fi * 5 + i * 10) % Math.max(1, convW - 10));
        const by = convY - 5;
        const bc = bColors[(fi + i) % bColors.length];
        const shade = [Math.max(0, bc[0] - 40), Math.max(0, bc[1] - 40), Math.max(0, bc[2] - 40)];
        const light = [Math.min(255, bc[0] + 30), Math.min(255, bc[1] + 30), Math.min(255, bc[2] + 30)];
        buf.fill(bx, by, 5, 5, bc);
        for (let dx = 0; dx < 5; dx++) buf.set(bx + dx, by, light);
        for (let dy = 0; dy < 5; dy++) buf.set(bx, by + dy, light);
        for (let dx = 0; dx < 5; dx++) buf.set(bx + dx, by + 4, shade);
        for (let dy = 0; dy < 5; dy++) buf.set(bx + 4, by + dy, shade);
      }
    }

    // Block stack accumulating
    if (w >= 50) {
      const stackX = convX + convW + 2;
      const stackY = convY;
      const stackCount = Math.min(fi + 1, 4);
      for (let i = 0; i < stackCount; i++) {
        const bc = bColors[i % bColors.length];
        const shade = [Math.max(0, bc[0] - 40), Math.max(0, bc[1] - 40), Math.max(0, bc[2] - 40)];
        const light = [Math.min(255, bc[0] + 30), Math.min(255, bc[1] + 30), Math.min(255, bc[2] + 30)];
        buf.fill(stackX, stackY - i * 5, 5, 5, bc);
        for (let dx = 0; dx < 5; dx++) buf.set(stackX + dx, stackY - i * 5, light);
        for (let dy = 0; dy < 5; dy++) buf.set(stackX + 4, stackY - i * 5 + dy, shade);
      }
    }

    // Progress bar at bottom
    if (w >= 40) {
      const barW = Math.min(20, Math.floor(w / 3));
      const barX = Math.floor((w - barW) / 2);
      const barY = ph - 4;
      buf.fill(barX - 1, barY - 1, barW + 2, 4, P.PROG_FR);
      buf.fill(barX, barY, barW, 2, P.PROG_BG);
      const fill = Math.floor(((fi + 1) * barW) / n);
      for (let dx = 0; dx < fill; dx++) {
        buf.set(barX + dx, barY, P.PROG_G);
        buf.set(barX + dx, barY + 1, P.PROG_G);
      }
    }

    return buf;
  });
}

function genIdle(w, h, n = 8) {
  const ph = h * 2;
  const chatA = ['..OOOOOOO.', '.OLLLTLLLO', '.OLTTLTLLO', '.OLLLTLLLO', '..OOOOOOO.', '.OO.......', 'OO........'];
  const chatB = ['.OOOOOOO..', 'OLLLWLLLO.', 'OLLWWLLLO.', 'OLLLWLLLO.', '.OOOOOOO..', '.......OO.', '........OO'];
  const chatMapA = { O: P.THOUGHT_D, L: P.THOUGHT, T: P.THOUGHT_L, '.': null };
  const chatMapB = { O: P.THOUGHT_D, L: P.THOUGHT, W: P.MON_WH, '.': null };

  return Array.from({ length: n }, (_, fi) => {
    const { buf, layout } = buildIsoOffice(w, ph, fi);
    const ox = layout.originX;
    const oy = layout.originY;

    // Agent 1 drinking coffee
    if (w >= 40) {
      const drinks = [SP.drink1, SP.drink2, SP.drink1];
      const drinker = drinks[fi % drinks.length];
      const [ax, ay] = isoAgentPos(layout.agent1Gx, layout.agent1Gy, ox, oy, drinker.length);
      buf.sprite(drinker, DRINK_MAP, ax, ay);

      // Steam from mug
      const parts = [[0, 0], [1, -1], [-1, -2], [0, -3], [1, -4], [-1, -5]];
      for (let i = 0; i < parts.length; i++) {
        const [dx, ddy] = parts[i];
        const py = ay - 2 + ddy - (fi % 4);
        const ppx = ax + 12 + dx + ((fi + i) % 3 - 1);
        if (py >= 0 && ppx >= 0 && ppx < buf.w) {
          const fade = Math.abs(ddy) + fi % 4;
          buf.set(ppx, py, fade < 3 ? P.STEAM : P.STEAM_F);
          if (ppx + 1 < buf.w) buf.set(ppx + 1, py, fade < 2 ? P.STEAM : P.STEAM_F);
        }
      }
    }

    // Agent 2 leaning / idle
    if (w >= 60) {
      const agent2 = fi % 4 < 2 ? SP.lean : SP.sit;
      const [ax2, ay2] = isoAgentPos(layout.agent2Gx, layout.agent2Gy, ox, oy, agent2.length);
      buf.sprite(agent2, A2, ax2, ay2);
    }

    // Chat bubbles
    if (w >= 55) {
      if (fi % 4 < 2) {
        const drinkerH = SP.drink1.length;
        const [ax, ay] = isoAgentPos(layout.agent1Gx, layout.agent1Gy, ox, oy, drinkerH);
        const bubY = Math.max(0, ay - chatA.length - 2);
        buf.sprite(chatA, chatMapA, ax + 14, bubY);
      } else if (fi % 4 === 2 && w >= 60) {
        const leanH = SP.lean.length;
        const [ax2, ay2] = isoAgentPos(layout.agent2Gx, layout.agent2Gy, ox, oy, leanH);
        const bubY = Math.max(0, ay2 - chatB.length - 2);
        buf.sprite(chatB, chatMapB, ax2 + 14, bubY);
      }
    }

    return buf;
  });
}

// ─── Exports ────────────────────────────────────────────────────────

export const LOGO = [
  '  _____ _                 _      _          _     ',
  ' / ____| |               | |    | |        | |    ',
  '| |    | | __ _ _   _  __| | ___| |     __ | |__  ',
  '| |    | |/ _` | | | |/ _` |/ _ \\ |    / _` | \'_ \\ ',
  '| |____| | (_| | |_| | (_| |  __/ |___| (_| | |_) |',
  ' \\_____|_|\\__,_|\\__,_|\\__,_|\\___|______\\__,_|_.__/ ',
];

export const SCENES = {
  thinking: {
    name: 'Thinking', icon: '.o( ? )',
    description: 'Claude is analyzing the problem. Agent sits with animated thought bubbles in the isometric office.',
    trigger: 'Triggered when Claude reads files or formulates a plan',
    generateFrames: genThinking,
  },
  coding: {
    name: 'Coding', icon: '>>_',
    description: 'Active code generation. Two agents type at desks with scrolling code on isometric monitors.',
    trigger: 'Triggered when Claude writes or edits code files',
    generateFrames: genCoding,
  },
  debugging: {
    name: 'Debugging', icon: '/!\\',
    description: 'Red-tinted office with whiteboard error diagrams. Agents point and examine bugs.',
    trigger: 'Triggered when Claude investigates errors or test failures',
    generateFrames: genDebugging,
  },
  running: {
    name: 'Running', icon: '[>>]',
    description: 'Control panel with LED grid, rotating gears, and progress bar on the isometric floor.',
    trigger: 'Triggered when Claude runs shell commands or tests',
    generateFrames: genRunning,
  },
  building: {
    name: 'Building', icon: '\u2590\u2588\u258C',
    description: 'Conveyor belt with animated rollers carries colored code blocks across the diamond-tile floor.',
    trigger: 'Triggered when Claude runs build or compilation commands',
    generateFrames: genBuilding,
  },
  idle: {
    name: 'Idle', icon: '~\u2615~',
    description: 'Coffee break. Agent drinks coffee with rising steam while another leans back and chats.',
    trigger: 'Shown when Claude Code is idle or between tasks',
    generateFrames: genIdle,
  },
};

export function getPreviewFrame(sceneKey, width = 40, height = 14) {
  const scene = SCENES[sceneKey];
  if (!scene) return null;
  return scene.generateFrames(width, height, 1)[0] || null;
}

export function getHeroFrames(width = 68, height = 20) {
  const all = [];
  for (const key of ['thinking', 'coding', 'debugging', 'running', 'building', 'idle']) {
    const scene = SCENES[key];
    const frames = scene.generateFrames(width, height, 4);
    for (const frame of frames) all.push({ buf: frame, scene: key, label: scene.name });
  }
  return all;
}

/**
 * Render a PixelBuffer to a canvas element.
 * Uses image-rendering: pixelated for crisp pixel art scaling.
 */
export function renderToCanvas(canvas, buf, scale = 0) {
  if (!canvas || !buf) return;
  const ctx = canvas.getContext('2d');
  // Auto-scale: fit canvas container width
  if (scale === 0) {
    scale = Math.max(1, Math.floor(canvas.clientWidth / buf.w));
  }
  canvas.width = buf.w * scale;
  canvas.height = buf.h * scale;
  // Draw pixel by pixel (faster than ImageData for small buffers with scaling)
  for (let y = 0; y < buf.h; y++) {
    const row = buf.px[y];
    for (let x = 0; x < buf.w; x++) {
      const c = row[x];
      ctx.fillStyle = `rgb(${c[0]},${c[1]},${c[2]})`;
      ctx.fillRect(x * scale, y * scale, scale, scale);
    }
  }
}
