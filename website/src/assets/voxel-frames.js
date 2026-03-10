// NES-quality voxel frames for ClaudeLab website
// Mirrors Python PixelBuffer — renders to HTML <span> half-block elements

// ─── Palette (3-tone shading) ──────────────────────────────────────

const P = {
  // Outline
  OL: [15, 10, 20],
  // Stone wall
  STONE_HL: [190, 190, 195], STONE: [128, 128, 128], STONE_L: [160, 160, 160], STONE_D: [80, 80, 80],
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
  BG: [10, 10, 15],
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

// ─── Office builder (NES quality) ──────────────────────────────────

function drawWall(buf, wallH) {
  for (let y = 0; y < wallH - 2; y++) {
    let base, mortar;
    if (y < 2) { base = P.STONE_D; mortar = [65, 65, 65]; }
    else if (y < wallH / 3) { base = P.STONE; mortar = P.STONE_D; }
    else { base = P.STONE_L; mortar = P.STONE; }
    for (let x = 0; x < buf.w; x++) {
      const bx = (x + ((y / 3 | 0) % 2 ? 3 : 0)) % 6;
      const by = y % 3;
      if (bx === 0 || by === 0) buf.set(x, y, mortar);
      else if ((x * 7 + y * 13) % 17 === 0) buf.set(x, y, P.STONE_HL);
      else buf.set(x, y, base);
    }
  }
  // Baseboard
  const bby = wallH - 2;
  for (let x = 0; x < buf.w; x++) {
    buf.set(x, bby, P.BB);
    buf.set(x, bby + 1, P.BB_D);
  }
}

function drawFloor(buf, fy) {
  for (let y = fy; y < buf.h; y++) {
    const dist = y - fy;
    for (let x = 0; x < buf.w; x++) {
      let c;
      const pr = dist % 4;
      if (pr === 0) c = P.OAK_D;
      else if (pr === 1 && dist < 4) c = P.OAK_L;
      else c = P.OAK;
      const seam = dist / 4 | 0;
      if ((x + (seam % 2 ? 4 : 0)) % 8 === 0) c = P.OAK_D;
      if (dist < 2) c = P.OAK_D;
      buf.set(x, y, c);
    }
  }
}

function drawWindow(buf, x, y, w, h, fi) {
  const sky = P.SKY;
  for (let dx = 0; dx < w; dx++) { buf.set(x + dx, y, P.OAK_LOG); buf.set(x + dx, y + h - 1, P.OAK_LOG); }
  for (let dy = 0; dy < h; dy++) { buf.set(x, y + dy, P.OAK_LOG); buf.set(x + w - 1, y + dy, P.OAK_LOG); }
  const mx = x + (w >> 1), my = y + (h >> 1);
  for (let dy = 1; dy < h - 1; dy++) buf.set(mx, y + dy, P.OAK_LOG);
  for (let dx = 1; dx < w - 1; dx++) buf.set(x + dx, my, P.OAK_LOG);
  for (let dy = 1; dy < h - 1; dy++)
    for (let dx = 1; dx < w - 1; dx++)
      if (dx !== mx - x && dy !== my - y) buf.set(x + dx, y + dy, sky);
  // Sun
  for (let dy = 0; dy < 3; dy++)
    for (let dx = 0; dx < 3; dx++)
      buf.set(x + 2 + dx, y + 1 + dy, P.SUN);
  buf.set(x + 3, y + 1, [255, 245, 140]);
  // Cloud
  if (w > 8) {
    const cx = x + w - 6;
    for (let dx = 0; dx < 4; dx++) buf.set(cx + dx, y + 3, P.CLOUD);
    for (let dx = -1; dx < 4; dx++) buf.set(cx + dx, y + 4, P.CLOUD);
    buf.set(cx + 1, y + 2, P.CLOUD); buf.set(cx + 2, y + 2, P.CLOUD);
  }
}

function drawDesk(buf, x, y, w) {
  for (let dx = 0; dx < w; dx++) buf.set(x + dx, y, P.OAK_L);
  buf.fill(x, y + 1, w, 2, P.OAK);
  for (let dx = 0; dx < w; dx++) buf.set(x + dx, y + 3, P.OAK_D);
  for (let dy = 4; dy < 8; dy++) { buf.set(x + 1, y + dy, P.OAK_LOG); buf.set(x + w - 2, y + dy, P.OAK_LOG); }
}

function drawKeyboard(buf, x, y) {
  buf.fill(x, y, 8, 2, P.KB_D);
  for (let dx = 0; dx < 8; dx += 2) buf.set(x + dx, y, P.KB_K);
  for (let dx = 1; dx < 7; dx += 2) buf.set(x + dx, y + 1, P.KB_K);
}

function drawChair(buf, x, y) {
  buf.set(x, y - 4, P.CH_HL);
  buf.fill(x, y - 3, 1, 3, P.CH);
  buf.set(x, y, P.CH_S);
  buf.set(x, y + 1, P.CH_HL);
  buf.fill(x + 1, y + 1, 3, 1, P.CH);
  buf.set(x + 4, y + 1, P.CH_S);
  buf.set(x + 2, y + 2, P.CH_S);
  buf.set(x, y + 3, P.CH_S); buf.set(x + 2, y + 3, P.CH_S); buf.set(x + 4, y + 3, P.CH_S);
}

function drawMonitor(buf, x, y, w = 10, h = 8) {
  buf.fill(x, y, w, h, P.MON_FR);
  buf.fill(x + 1, y + 1, w - 2, h - 2, P.MON_GLOW);
  buf.fill(x + 2, y + 2, w - 4, h - 4, P.MON_BG);
  buf.set(x + w - 2, y + h - 1, P.LED_G);
  buf.fill(x + (w >> 1) - 1, y + h, 2, 2, P.IRON_D);
  buf.fill(x + (w >> 1) - 2, y + h + 2, 5, 1, P.IRON_D);
}

function drawServerRack(buf, x, y, h, fi) {
  const w = 6;
  buf.fill(x, y, w, h, P.IRON_D);
  for (let r = 1; r < h - 1; r += 2) {
    buf.fill(x + 1, y + r, w - 2, 1, P.IRON);
    for (let dx = 1; dx < w - 1; dx++)
      if (dx % 2 === 0) buf.set(x + dx, y + r, [180, 180, 185]);
    const colors = [P.LED_G, P.LED_A, P.LED_G, P.LED_O];
    buf.set(x + 1, y + r, colors[(fi + r) % 4]);
    buf.set(x + w - 2, y + r, colors[(fi + r + 2) % 4]);
  }
}

function drawPlant(buf, x, y, fi) {
  buf.fill(x, y + 5, 5, 2, P.POT);
  buf.set(x, y + 5, [160, 85, 50]); buf.set(x + 4, y + 6, [160, 85, 50]);
  buf.set(x + 2, y + 4, P.LEAF_D); buf.set(x + 2, y + 3, P.LEAF_D); buf.set(x + 2, y + 2, P.LEAF_D);
  const s = fi % 8 < 4 ? 1 : 0;
  buf.set(x + 1 + s, y, P.LEAF_L); buf.set(x + 2 + s, y, P.LEAF); buf.set(x + 3, y, P.LEAF);
  buf.set(x + s, y + 1, P.LEAF); buf.set(x + 1, y + 1, P.LEAF_L); buf.set(x + 3, y + 1, P.LEAF); buf.set(x + 4, y + 1, P.LEAF_D);
  buf.set(x + 1, y + 2, P.LEAF); buf.set(x + 3, y + 2, P.LEAF_D);
}

function drawCoffeeMachine(buf, x, y) {
  buf.fill(x, y, 4, 5, P.IRON);
  buf.set(x, y, [220, 220, 225]);
  buf.fill(x + 3, y, 1, 5, P.IRON_D);
  buf.set(x + 1, y + 1, P.COFFEE); buf.set(x + 2, y + 1, P.COFFEE);
  buf.set(x + 1, y + 2, [90, 50, 20]); buf.set(x + 2, y + 2, [90, 50, 20]);
  buf.set(x + 1, y + 3, P.IRON_D);
  buf.fill(x, y + 5, 4, 1, P.IRON_D);
}

function drawCeilingLight(buf, x, y, w) {
  buf.fill(x, y, w, 2, P.IRON_D);
  buf.fill(x + 1, y + 1, w - 2, 1, P.GLOW);
  for (let dy = 2; dy < 5; dy++) {
    const spread = dy - 1;
    for (let dx = -spread; dx < w + spread; dx++) {
      const px = x + dx, py = y + dy;
      if (px >= 0 && px < buf.w && py >= 0 && py < buf.h) {
        const [r, g, b] = buf.px[py][px];
        buf.px[py][px] = [Math.min(255, r + 12), Math.min(255, g + 10), Math.min(255, b + 8)];
      }
    }
  }
}

function buildOffice(w, ph, fi) {
  const buf = new PixelBuffer(w, ph);
  const wallH = Math.max(6, Math.round(ph * 7 / 20));
  const fy = wallH;

  drawWall(buf, wallH);
  drawFloor(buf, fy);

  // Window
  const ww = Math.min(14, w / 4 | 0), wh = Math.min(10, wallH - 3);
  if (ww >= 8 && wh >= 6) drawWindow(buf, w - ww - 3, 1, ww, wh, fi);

  // Ceiling light
  if (w >= 50 && wallH >= 8) drawCeilingLight(buf, w / 3 | 0, 0, 8);

  const dw = Math.min(14, w / 5 | 0), dy = fy + 2;
  if (w >= 40) {
    drawDesk(buf, 3, dy, dw);
    drawMonitor(buf, 5, dy - 10, Math.min(10, dw - 2), 8);
    drawKeyboard(buf, 5, dy - 1);
    drawChair(buf, 5, dy + 6);
  }
  if (w >= 60) {
    const d2 = (w / 3 | 0) + 4;
    drawDesk(buf, d2, dy, dw);
    drawMonitor(buf, d2 + 2, dy - 10, Math.min(10, dw - 2), 8);
    drawKeyboard(buf, d2 + 2, dy - 1);
    drawChair(buf, d2 + 2, dy + 6);
  }
  if (w >= 50) {
    const rh = Math.min(12, ph - fy - 2);
    if (rh >= 8) drawServerRack(buf, w - 10, fy - rh + 2, rh, fi);
  }
  if (ph - fy > 10) drawPlant(buf, 1, fy + 1, fi);
  if (w >= 55) drawCoffeeMachine(buf, (w >> 1) + 6, fy + 2);

  return { buf, wallH, fy, dy, dw };
}

// ─── Scene generators ───────────────────────────────────────────────

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
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy, dy } = buildOffice(w, ph, fi);
    const ay = dy - 20 + 1;
    if (w >= 40) {
      buf.sprite(SP.sitThink, A1, 5, ay);
      const b = bubbles[bSeq[fi % bSeq.length]];
      const by = Math.max(0, ay - b.art.length - 1);
      buf.sprite(b.art, b.map, 2, by);
    }
    if (w >= 60) {
      const d2 = (w / 3 | 0) + 4;
      buf.sprite(SP.sit, A2, d2 + 3, dy - 20 + 1);
      buf.set(d2 + 4, dy - 8, fi % 2 === 0 ? P.MON_GR : P.MON_BG);
    }
    return buf;
  });
}

function genCoding(w, h, n = 8) {
  const ph = h * 2;
  const rng = (s) => ((s * 1103515245 + 12345) & 0x7fffffff) % 256;
  const cc = [P.MON_GR, P.MON_YL, P.MON_WH, P.MON_CY];
  const types = [SP.sitL, SP.sitR, SP.sitBoth, SP.sit];
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy, dy, dw } = buildOffice(w, ph, fi);
    const ay = dy - 20 + 1;
    if (w >= 40) {
      buf.sprite(types[fi % types.length], A1, 5, ay);
      const mx = 7, my = dy - 8, mw = Math.min(6, dw - 4);
      for (let r = 0; r < Math.min(4, 4); r++)
        for (let c = 0; c < mw; c++) {
          const seed = rng(fi * 100 + r * 10 + c);
          if (seed > 70) buf.set(mx + c, my + r, cc[seed % cc.length]);
        }
    }
    if (w >= 60) {
      const d2 = (w / 3 | 0) + 4;
      buf.sprite(types[(fi + 2) % types.length], A2, d2 + 3, ay);
      const mx = d2 + 4, my = dy - 8, mw = Math.min(6, dw - 4);
      for (let r = 0; r < 4; r++)
        for (let c = 0; c < mw; c++) {
          const seed = rng((fi + 3) * 100 + r * 10 + c);
          if (seed > 50) buf.set(mx + c, my + r, cc[seed % cc.length]);
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
    const { buf, wallH, fy, dy, dw } = buildOffice(w, ph, fi);
    // Whiteboard
    const wbW = Math.min(16, w / 4 | 0), wbH = Math.min(10, wallH - 3);
    const wx = w / 3 | 0;
    if (wbW >= 8 && wbH >= 6 && w >= 45) {
      buf.fill(wx, 1, wbW, wbH, P.BIRCH);
      for (let dx = 0; dx < wbW; dx++) { buf.set(wx + dx, 1, P.MON_FR); buf.set(wx + dx, wbH, P.MON_FR); }
      for (let d = 0; d < wbH; d++) { buf.set(wx, 1 + d, P.MON_FR); buf.set(wx + wbW - 1, 1 + d, P.MON_FR); }
      // Boxes + arrow
      buf.fill(wx + 2, 3, 4, 3, [220, 220, 220]);
      for (let dx = 0; dx < 4; dx++) buf.set(wx + 2 + dx, 3, P.MON_RD);
      for (let dx = 6; dx < Math.min(wbW - 4, 10); dx++) buf.set(wx + dx, 4, P.WARN_R);
      if (wbW > 12) buf.fill(wx + wbW - 6, 3, 4, 3, P.WARN_R);
    }
    // Agent pointing
    if (w >= 45) {
      const ptr = fi % 2 === 0 ? SP.point : SP.stand;
      buf.sprite(ptr, A1, wx - 4 >= 0 ? wx - 4 : 10, fy - 16);
    }
    // Agent examining
    if (w >= 40) {
      const ex = fi % 2 === 0 ? SP.examine : SP.stand;
      buf.sprite(ex, A2, 5, dy - 20 + 1);
      const mx = 7, my = dy - 8;
      for (let r = 0; r < 4; r++)
        for (let c = 0; c < Math.min(6, dw - 4); c++)
          if ((c + fi) % 4 === 0) buf.set(mx + c, my + r, P.MON_RD);
          else if ((c + r + fi) % 6 === 0) buf.set(mx + c, my + r, P.WARN_Y);
    }
    // Warning triangle
    if (w >= 50 && fi % 3 !== 2) buf.sprite(warnArt, warnMap, w / 2 | 0, 0);
    // Server LEDs red
    if (w >= 50) {
      const rx = w - 10, rh = Math.min(12, ph - fy - 2), ry = fy - rh + 2;
      for (let r = 1; r < rh - 1; r += 2) {
        const led = (fi + r) % 2 === 0 ? P.LED_R : P.LED_O;
        buf.set(rx + 1, ry + r, led); buf.set(rx + 4, ry + r, led);
      }
    }
    // Selective red tint
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
    const { buf, wallH, fy, dy, dw } = buildOffice(w, ph, fi);
    // Control panel
    const pw = Math.min(16, w / 4 | 0), pHeight = Math.min(8, wallH - 3), px = w / 3 | 0;
    if (pw >= 8 && pHeight >= 5) {
      buf.fill(px, 1, pw, pHeight, P.IRON_D);
      buf.fill(px + 1, 2, pw - 2, pHeight - 2, P.IRON);
      for (let dx = 1; dx < pw - 1; dx++) buf.set(px + dx, 2, [220, 220, 225]);
      for (let bx = 2; bx < pw - 2; bx += 3)
        for (let by = 2; by < Math.min(pHeight - 1, 6); by++) {
          const s = (fi + bx + by * pw) % 5;
          const colors = [P.LED_G, P.LED_A, P.LED_G, P.LED_G, P.LED_O];
          buf.set(px + bx, 1 + by, colors[s]);
          buf.set(px + bx + 1, 1 + by, P.IRON_D);
        }
    }
    // Agent pushing
    const pushes = [SP.push1, SP.push2, SP.stand];
    buf.sprite(pushes[fi % pushes.length], A1, px - 4 >= 0 ? px - 4 : 10, fy - 16);
    // Gear
    if (w >= 55) {
      const gx = (w >> 1) + 10, gy = fy - 8;
      buf.sprite(gears[fi % gears.length], gMap, gx, gy);
    }
    // Progress bar
    if (w >= 40) {
      const bw = Math.min(24, w / 3 | 0), bx = 4, by = ph - 5;
      buf.fill(bx - 1, by - 1, bw + 2, 4, P.PROG_FR);
      buf.fill(bx, by, bw, 2, P.PROG_BG);
      const fill = ((fi + 1) * bw / n) | 0;
      for (let dx = 0; dx < fill; dx++) {
        const c = dx === fill - 1 ? [100, 255, 100] : dx === fill - 2 ? [70, 240, 70] : P.PROG_G;
        buf.set(bx + dx, by, c); buf.set(bx + dx, by + 1, c);
      }
    }
    // Log on monitor
    if (w >= 40) {
      const mx = 7, my = dy - 8;
      for (let r = 0; r < 4; r++) {
        const len = ((r + fi) * 3) % Math.max(1, dw - 4) + 1;
        for (let c = 0; c < Math.min(len, 6); c++)
          buf.set(mx + c, my + r, (r + fi) % 3 !== 0 ? P.MON_GR : P.MON_WH);
      }
    }
    return buf;
  });
}

function genBuilding(w, h, n = 8) {
  const ph = h * 2;
  const bColors = [P.GOLD, P.LAPIS, P.RED, P.EMERALD, P.DIAMOND];
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy } = buildOffice(w, ph, fi);
    const cw = Math.min(w - 14, (w * 2 / 3) | 0), cx = 4, cy = fy + 5;
    // Conveyor
    if (cw >= 12) {
      for (let dx = 0; dx < cw; dx++) {
        const m = (dx + fi) % 4;
        buf.set(cx + dx, cy, m === 0 ? P.CONV_D : m === 1 ? P.CONV_L : P.CONV);
        buf.set(cx + dx, cy + 1, m === 0 ? P.CONV_D : P.CONV);
      }
      for (let dx = 0; dx < cw; dx++) { buf.set(cx + dx, cy - 1, P.STONE_D); buf.set(cx + dx, cy + 2, P.STONE_D); }
      for (let dx = 0; dx < cw; dx += 8)
        for (let dy = 3; dy < 6; dy++) { buf.set(cx + dx, cy + dy, P.STONE_D); buf.set(cx + dx + 1, cy + dy, P.STONE_D); }
    }
    // Carrier
    if (cw >= 12) {
      const ax = cx + ((fi * 5) % Math.max(1, cw - 16));
      buf.sprite(CARRY1, CARRY_MAP, ax, cy - 21);
    }
    // Second agent
    if (w >= 55 && cw >= 12) {
      const wx2 = cx + cw - ((fi * 4) % Math.max(1, cw - 16)) - 16;
      buf.sprite(fi % 2 === 0 ? SP.walk1 : SP.walk2, A1, Math.max(cx, wx2), cy - 21);
    }
    // Blocks on belt
    if (cw >= 24) {
      for (let i = 0; i < 3; i++) {
        const bx = cx + 6 + ((fi * 5 + i * 10) % Math.max(1, cw - 10));
        const bc = bColors[(fi + i) % bColors.length];
        const shade = [Math.max(0, bc[0] - 40), Math.max(0, bc[1] - 40), Math.max(0, bc[2] - 40)];
        const light = [Math.min(255, bc[0] + 30), Math.min(255, bc[1] + 30), Math.min(255, bc[2] + 30)];
        buf.fill(bx, cy - 5, 5, 5, bc);
        for (let dx = 0; dx < 5; dx++) buf.set(bx + dx, cy - 5, light);
        for (let dy = 0; dy < 5; dy++) buf.set(bx, cy - 5 + dy, light);
        for (let dx = 0; dx < 5; dx++) buf.set(bx + dx, cy - 1, shade);
        for (let dy = 0; dy < 5; dy++) buf.set(bx + 4, cy - 5 + dy, shade);
      }
    }
    // Stack
    if (w >= 50) {
      const sx = w - 14, sy = fy + 4, cnt = Math.min(fi + 1, 4);
      for (let i = 0; i < cnt; i++) {
        const bc = bColors[i % bColors.length];
        const shade = [Math.max(0, bc[0] - 40), Math.max(0, bc[1] - 40), Math.max(0, bc[2] - 40)];
        const light = [Math.min(255, bc[0] + 30), Math.min(255, bc[1] + 30), Math.min(255, bc[2] + 30)];
        buf.fill(sx, sy - i * 5, 5, 5, bc);
        for (let dx = 0; dx < 5; dx++) buf.set(sx + dx, sy - i * 5, light);
        for (let dy = 0; dy < 5; dy++) buf.set(sx + 4, sy - i * 5 + dy, shade);
      }
    }
    // Progress
    if (w >= 40) {
      const bw = Math.min(20, w / 3 | 0), bx = 4, by = ph - 5;
      buf.fill(bx - 1, by - 1, bw + 2, 4, P.PROG_FR);
      buf.fill(bx, by, bw, 2, P.PROG_BG);
      const fill = ((fi + 1) * bw / n) | 0;
      for (let dx = 0; dx < fill; dx++) { buf.set(bx + dx, by, P.PROG_G); buf.set(bx + dx, by + 1, P.PROG_G); }
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
    const { buf, fy, dy } = buildOffice(w, ph, fi);
    const ay = dy - 20 + 1;
    // Agent drinking
    if (w >= 40) {
      const drinks = [SP.drink1, SP.drink2, SP.drink1];
      buf.sprite(drinks[fi % drinks.length], DRINK_MAP, 5, ay);
      // Steam
      const parts = [[0, 0], [1, -1], [-1, -2], [0, -3], [1, -4], [-1, -5]];
      for (let i = 0; i < parts.length; i++) {
        const [dx, ddy] = parts[i];
        const py = ay - 2 + ddy - (fi % 4), ppx = 18 + dx + ((fi + i) % 3 - 1);
        if (py >= 0 && ppx >= 0 && ppx < buf.w) {
          const fade = Math.abs(ddy) + fi % 4;
          buf.set(ppx, py, fade < 3 ? P.STEAM : P.STEAM_F);
          if (ppx + 1 < buf.w) buf.set(ppx + 1, py, fade < 2 ? P.STEAM : P.STEAM_F);
        }
      }
    }
    // Agent leaning
    if (w >= 60) {
      const d2 = (w / 3 | 0) + 4;
      buf.sprite(fi % 4 < 2 ? SP.lean : SP.sit, A2, d2 + 3, ay);
    }
    // Chat bubbles
    if (w >= 55) {
      if (fi % 4 < 2) {
        const by = Math.max(0, ay - 7);
        buf.sprite(chatA, chatMapA, 20, by);
      } else if (fi % 4 === 2) {
        const d2 = (w / 3 | 0) + 4;
        const by = Math.max(0, ay - 7);
        buf.sprite(chatB, chatMapB, d2 + 16, by);
      }
    }
    // Steam from coffee machine
    if (w >= 55) {
      const cmx = (w >> 1) + 8, cmy = fy;
      for (let i = 0; i < 3; i++) {
        const py = cmy - (fi % 3) - i;
        if (py >= 0) {
          buf.set(cmx + ((fi + i) % 2), py, i < 2 ? P.STEAM : P.STEAM_F);
        }
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
