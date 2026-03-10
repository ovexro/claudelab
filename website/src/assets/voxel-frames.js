// Voxel-style frames for ClaudeLab website — Minecraft half-block rendering
// Mirrors the Python PixelBuffer but renders to HTML <span> elements

// ─── Palette ────────────────────────────────────────────────────────

const P = {
  // Block materials
  STONE: [128, 128, 128], STONE_DARK: [80, 80, 80], STONE_LIGHT: [160, 160, 160],
  OAK_PLANK: [170, 130, 80], OAK_PLANK_DARK: [140, 105, 65], OAK_LOG: [85, 65, 40],
  IRON_BLOCK: [200, 200, 200], IRON_DARK: [150, 150, 155],
  BIRCH_PLANK: [200, 190, 160],
  // Agent
  HAIR: [75, 50, 30], SKIN: [200, 160, 120], SKIN_S: [160, 120, 80],
  EYE_W: [255, 255, 255], EYE_P: [30, 30, 60],
  SHIRT1: [50, 160, 200], SHIRT1D: [35, 120, 160],
  SHIRT2: [200, 50, 50], SHIRT2D: [150, 35, 35],
  PANTS: [40, 50, 140], PANTS_S: [28, 35, 100], SHOE: [80, 80, 80],
  // Sky
  SKY_DAY: [120, 180, 255], SKY_NIGHT: [15, 15, 45], SKY_DAWN: [255, 180, 120],
  SUN: [255, 230, 80], MOON: [230, 230, 210], STAR: [255, 255, 200], CLOUD: [240, 240, 255],
  // Tech
  MON_BG: [25, 30, 50], MON_FRAME: [55, 55, 70],
  MON_GREEN: [80, 255, 80], MON_WHITE: [210, 210, 210],
  MON_YELLOW: [255, 220, 80], MON_RED: [255, 80, 80], MON_CYAN: [80, 220, 255],
  LED_GREEN: [50, 255, 50], LED_RED: [255, 50, 50], LED_AMBER: [255, 180, 0], LED_OFF: [50, 50, 55],
  // Objects
  LEAF: [50, 150, 50], LEAF_D: [30, 110, 30], POT: [180, 100, 60],
  COFFEE: [110, 65, 30], STEAM: [210, 210, 230], STEAM_F: [150, 150, 170],
  CHAIR: [60, 50, 40],
  // Effects
  THOUGHT: [220, 220, 240], THOUGHT_D: [180, 180, 200],
  WARN_R: [220, 40, 40], WARN_Y: [255, 210, 50],
  GEAR: [160, 80, 200], GEAR_D: [120, 55, 155],
  CONV: [150, 150, 160], CONV_D: [110, 110, 120],
  PROG_G: [50, 220, 50], PROG_BG: [50, 50, 55],
  GOLD: [240, 200, 50], LAPIS: [50, 70, 180], REDSTONE: [180, 40, 40],
  EMERALD: [50, 200, 80], DIAMOND: [80, 210, 230], GLOWSTONE: [210, 190, 120],
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
}

// ─── Office builder ─────────────────────────────────────────────────

function drawWall(buf, wallH) {
  for (let y = 0; y < wallH; y++)
    for (let x = 0; x < buf.w; x++) {
      const bx = (x + ((y >> 1) % 2 ? 2 : 0)) % 4;
      const by = y % 2;
      buf.set(x, y, bx === 0 || by === 0 ? P.STONE_DARK : ((x + y) % 5 === 0 ? P.STONE_LIGHT : P.STONE));
    }
}

function drawFloor(buf, fy) {
  for (let y = fy; y < buf.h; y++)
    for (let x = 0; x < buf.w; x++)
      buf.set(x, y, y % 3 === 0 ? P.OAK_PLANK_DARK : P.OAK_PLANK);
}

function drawWindow(buf, x, y, w, h, fi) {
  const sky = P.SKY_DAY;
  // Frame
  for (let dx = 0; dx < w; dx++) { buf.set(x + dx, y, P.OAK_LOG); buf.set(x + dx, y + h - 1, P.OAK_LOG); }
  for (let dy = 0; dy < h; dy++) { buf.set(x, y + dy, P.OAK_LOG); buf.set(x + w - 1, y + dy, P.OAK_LOG); }
  const mx = x + (w >> 1), my = y + (h >> 1);
  for (let dy = 1; dy < h - 1; dy++) buf.set(mx, y + dy, P.OAK_LOG);
  for (let dx = 1; dx < w - 1; dx++) buf.set(x + dx, my, P.OAK_LOG);
  // Sky
  for (let dy = 1; dy < h - 1; dy++)
    for (let dx = 1; dx < w - 1; dx++)
      if (dx !== mx - x && dy !== my - y) buf.set(x + dx, y + dy, sky);
  // Sun
  buf.set(x + 2, y + 2, P.SUN); buf.set(x + 3, y + 2, P.SUN);
  buf.set(x + 2, y + 3, P.SUN); buf.set(x + 3, y + 3, P.SUN);
  if (w > 8) { for (let dx = 0; dx < 3; dx++) buf.set(x + w - 4 + dx, y + 2, P.CLOUD); for (let dx = 0; dx < 4; dx++) buf.set(x + w - 5 + dx, y + 3, P.CLOUD); }
}

function drawDesk(buf, x, y, w) {
  buf.fill(x, y, w, 2, P.OAK_PLANK);
  for (let dy = 2; dy < 6; dy++) { buf.set(x + 1, y + dy, P.OAK_LOG); buf.set(x + w - 2, y + dy, P.OAK_LOG); }
}

function drawChair(buf, x, y) {
  buf.fill(x, y, 4, 1, P.CHAIR);
  buf.fill(x, y - 3, 1, 3, P.CHAIR);
  buf.set(x, y + 1, P.CHAIR); buf.set(x + 3, y + 1, P.CHAIR);
}

function drawMonitor(buf, x, y, w = 8, h = 6) {
  buf.fill(x, y, w, h, P.MON_FRAME);
  buf.fill(x + 1, y + 1, w - 2, h - 2, P.MON_BG);
  buf.fill(x + (w >> 1) - 1, y + h, 2, 1, P.IRON_DARK);
  buf.fill(x + (w >> 1) - 2, y + h + 1, 4, 1, P.IRON_DARK);
}

function drawServerRack(buf, x, y, h, fi) {
  buf.fill(x, y, 4, h, P.IRON_DARK);
  for (let r = 1; r < h - 1; r += 2) {
    buf.fill(x + 1, y + r, 2, 1, P.IRON_BLOCK);
    const led = (fi + r) % 4 === 0 ? P.LED_GREEN : (fi + r) % 4 === 1 ? P.LED_AMBER : (fi + r) % 4 === 2 ? P.LED_GREEN : P.LED_OFF;
    buf.set(x + 2, y + r, led);
  }
}

function drawPlant(buf, x, y, fi) {
  buf.fill(x, y + 4, 4, 2, P.POT);
  buf.set(x + 2, y + 3, P.LEAF_D); buf.set(x + 2, y + 2, P.LEAF_D);
  const s = fi % 8 < 4 ? 1 : 0;
  buf.set(x + 1 + s, y, P.LEAF); buf.set(x + 2 + s, y, P.LEAF);
  buf.set(x + 3, y + 1, P.LEAF); buf.set(x + s, y + 1, P.LEAF_D);
  buf.set(x + 1, y + 2, P.LEAF); buf.set(x + 3, y + 2, P.LEAF);
}

function drawCoffee(buf, x, y) {
  buf.fill(x, y, 3, 4, P.IRON_BLOCK);
  buf.set(x + 1, y + 1, P.COFFEE); buf.set(x + 1, y + 2, P.COFFEE);
  buf.fill(x, y + 4, 3, 1, P.IRON_DARK);
}

function buildOffice(w, ph, fi) {
  const buf = new PixelBuffer(w, ph);
  const wallH = Math.max(4, Math.round(ph * 0.4));
  const fy = wallH;
  drawWall(buf, wallH); drawFloor(buf, fy);
  const ww = Math.min(12, w / 5 | 0), wh = Math.min(8, wallH - 2);
  if (ww >= 6 && wh >= 4) drawWindow(buf, w - ww - 3, 1, ww, wh, fi);
  const dw = Math.min(10, w / 6 | 0), dy = fy + 2;
  if (w >= 40) { drawDesk(buf, 3, dy, dw); drawMonitor(buf, 4, dy - 7, Math.min(8, dw - 2), 6); drawChair(buf, 4, dy + 5); }
  if (w >= 60) { const d2 = (w / 3 | 0) + 2; drawDesk(buf, d2, dy, dw); drawMonitor(buf, d2 + 1, dy - 7, Math.min(8, dw - 2), 6); drawChair(buf, d2 + 1, dy + 5); }
  if (w >= 50) { const rh = Math.min(10, ph - fy - 2); if (rh >= 6) drawServerRack(buf, w - 8, fy - rh + 2, rh, fi); }
  if (ph - fy > 8) drawPlant(buf, 1, fy + 1, fi);
  if (w >= 55) drawCoffee(buf, (w >> 1) + 4, fy + 2);
  return { buf, wallH, fy, dy, dw };
}

// ─── Agent sprites ──────────────────────────────────────────────────

const A1 = { H: P.HAIR, S: P.SKIN, s: P.SKIN_S, W: P.EYE_W, E: P.EYE_P, C: P.SHIRT1, c: P.SHIRT1D, P: P.PANTS, p: P.PANTS_S, G: P.SHOE, '.': null };
const A2 = { ...A1, C: P.SHIRT2, c: P.SHIRT2D };

const SP = {
  sit: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCC.','.CCCCCC.','..CCCC..','........','..PPPP..','..PPPP..','..PPPP..','..GGGG..'],
  sitL: ['..HHHH..','..HHHH..','.SWESWE.','..sSss..','.CCCCCC.','.CCCCCC.','cCC..CC.','c.......','..PPPP..','..PPPP..','..PPPP..','..GGGG..'],
  sitR: ['..HHHH..','..HHHH..','.SWESWE.','..sSss..','.CCCCCC.','.CCCCCC.','.CC..CCc','.......c','..PPPP..','..PPPP..','..PPPP..','..GGGG..'],
  stand: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCC.','.CCCCCC.','.CC..CC.','.CC..CC.','..PPPP..','..PPPP..','..PP.PP.','..GG.GG.'],
  point: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCCc','.CCCCCCc','.CC....c','........','..PPPP..','..PPPP..','..PP.PP.','..GG.GG.'],
  walk1: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCC.','.CCCCCC.','.CC..CC.','.CC..CC.','..PPPP..','..PPPP..','.PP...PP','.GG...GG'],
  walk2: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCC.','.CCCCCC.','.CC..CC.','.CC..CC.','..PPPP..','..PPPP..','..PP.PP.','..GG.GG.'],
  drink1: ['..HHHH..','..HHHH..','.SWESWE.','..SSSSK.k','.CCCCCC.','.CCCCCC.','..CCCC..','........','..PPPP..','..PPPP..','..PPPP..','..GGGG..'],
  drink2: ['..HHHH..','..HHHHK.k','.SWESWE.','..SSSS..','.CCCCCC.','.CCCCCC.','..CCCC..','........','..PPPP..','..PPPP..','..PPPP..','..GGGG..'],
  lean: ['...HHHH.','...HHHH.','..SWESWs','...SSSS.','..CCCCCC','..CCCCCC','...CCCC.','........','..PPPP..','..PPPP..','..PPPP..','..GGGG..'],
  push1: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCCc','.CCCCCCc','.CC.....','........','..PPPP..','..PPPP..','..PP.PP.','..GG.GG.'],
  push2: ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','cCCCCCC.','cCCCCCC.','.....CC.','........','..PPPP..','..PPPP..','..PP.PP.','..GG.GG.'],
};

const DRINK_MAP = { ...A1, K: P.COFFEE, k: [220, 195, 150] };

// Carry block maps
const CARRY_MAP = { ...A1, B: P.GOLD, b: P.LAPIS };
const CARRY1 = ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCCBB','.CCCCCCBB','.CC..CC..', '.CC..CC..','..PPPP...','..PPPP...','.PP...PP.','.GG...GG.'];
const CARRY2 = ['..HHHH..','..HHHH..','.SWESWE.','..SSSS..','.CCCCCCbb','.CCCCCCbb','.CC..CC..', '.CC..CC..','..PPPP...','..PPPP..','..PP.PP..','..GG.GG..'];

// ─── Scene generators ───────────────────────────────────────────────

function genThinking(w, h, n = 8) {
  const ph = h * 2;
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy, dy } = buildOffice(w, ph, fi);
    const ay = dy - 12 + 1;
    if (w >= 40) {
      buf.sprite(SP.sit, A1, 5, ay);
      // Thought bubble
      const tb = [
        '...CCC..','..CCCCC.','.CDDCDC.','..CCCCC.','...CCC..','....C...','.....c..'
      ];
      const tbMap = { C: P.THOUGHT, D: fi % 3 === 0 ? P.WARN_Y : P.THOUGHT_D, c: P.THOUGHT_D, '.': null };
      buf.sprite(tb, tbMap, 3, ay - 8);
    }
    if (w >= 60) {
      const d2 = (w / 3 | 0) + 2;
      buf.sprite(SP.sit, A2, d2 + 2, ay);
      buf.set(d2 + 2, dy - 5, fi % 2 === 0 ? P.MON_GREEN : P.MON_BG);
    }
    return buf.toHtml();
  });
}

function genCoding(w, h, n = 8) {
  const ph = h * 2;
  const rng = (s) => ((s * 1103515245 + 12345) & 0x7fffffff) % 256;
  const codeColors = [P.MON_GREEN, P.MON_YELLOW, P.MON_WHITE, P.MON_CYAN];
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy, dy, dw } = buildOffice(w, ph, fi);
    const ay = dy - 12 + 1;
    const types = [SP.sitL, SP.sitR, SP.sit, SP.sitL];
    if (w >= 40) {
      buf.sprite(types[fi % types.length], A1, 5, ay);
      // Code on monitor 1
      const mx = 5, my = dy - 6;
      for (let r = 0; r < 4; r++)
        for (let c = 0; c < Math.min(6, dw - 3); c++) {
          const seed = rng(fi * 100 + r * 10 + c);
          if (seed > 80) buf.set(mx + c, my + r, codeColors[seed % codeColors.length]);
        }
    }
    if (w >= 60) {
      const d2 = (w / 3 | 0) + 2;
      buf.sprite(types[(fi + 2) % types.length], A2, d2 + 2, ay);
      const mx = d2 + 2, my = dy - 6;
      for (let r = 0; r < 4; r++)
        for (let c = 0; c < Math.min(6, dw - 3); c++) {
          const seed = rng((fi + 3) * 100 + r * 10 + c);
          if (seed > 60) buf.set(mx + c, my + r, codeColors[seed % codeColors.length]);
        }
    }
    return buf.toHtml();
  });
}

function genDebugging(w, h, n = 8) {
  const ph = h * 2;
  return Array.from({ length: n }, (_, fi) => {
    const { buf, wallH, fy, dy, dw } = buildOffice(w, ph, fi);
    const ay = fy - 8;
    // Whiteboard
    const wbW = Math.min(12, w / 5 | 0), wbH = Math.min(8, wallH - 2);
    if (wbW >= 6 && wbH >= 4 && w >= 45) {
      const wx = w / 3 | 0;
      buf.fill(wx, 1, wbW, wbH, P.BIRCH_PLANK);
      for (let dx = 0; dx < wbW; dx++) { buf.set(wx + dx, 1, P.MON_FRAME); buf.set(wx + dx, wbH, P.MON_FRAME); }
      for (let dy2 = 0; dy2 < wbH; dy2++) { buf.set(wx, 1 + dy2, P.MON_FRAME); buf.set(wx + wbW - 1, 1 + dy2, P.MON_FRAME); }
      for (let dx = 1; dx < wbW - 2; dx++) if ((dx + fi) % 3 !== 0) buf.set(wx + dx, 3, P.MON_RED);
      buf.sprite(SP.point, A1, wx - 2, ay);
    }
    if (w >= 40) {
      buf.sprite(SP.stand, A2, 5, dy - 12 + 1);
      const mx = 5, my = dy - 6;
      for (let r = 0; r < 4; r++)
        for (let c = 0; c < Math.min(6, dw - 3); c++)
          if ((c + fi) % 4 === 0) buf.set(mx + c, my + r, P.MON_RED);
          else if ((c + r + fi) % 6 === 0) buf.set(mx + c, my + r, P.WARN_Y);
    }
    // Warning triangle blink
    if (w >= 50 && fi % 3 !== 2) {
      const tw = [['...Y...'],['..YYY..'], ['.YYRYY.'],['YYYYYYY']];
      const tMap = { Y: P.WARN_Y, R: P.WARN_R, '.': null };
      tw.forEach((row, i) => buf.sprite(row, tMap, w / 2 | 0, 1 + i));
    }
    // Red tint
    for (let y = 0; y < buf.h; y++)
      for (let x = 0; x < buf.w; x++) {
        const [r, g, b] = buf.px[y][x];
        buf.px[y][x] = [Math.min(255, r + 25), Math.max(0, g - 10), Math.max(0, b - 10)];
      }
    return buf.toHtml();
  });
}

function genRunning(w, h, n = 8) {
  const ph = h * 2;
  return Array.from({ length: n }, (_, fi) => {
    const { buf, wallH, fy, dy, dw } = buildOffice(w, ph, fi);
    // Control panel
    const pw = Math.min(14, w / 4 | 0), pHeight = Math.min(6, wallH - 2);
    const px = w / 3 | 0;
    if (pw >= 6 && pHeight >= 4) {
      buf.fill(px, 1, pw, pHeight, P.IRON_DARK);
      buf.fill(px + 1, 2, pw - 2, pHeight - 2, P.IRON_BLOCK);
      for (let bx = 2; bx < pw - 2; bx += 2)
        for (let by = 1; by < Math.min(pHeight - 1, 4); by++) {
          const s = (fi + bx + by * pw) % 4;
          buf.set(px + bx, 1 + by, s === 0 ? P.LED_GREEN : s === 1 ? P.LED_AMBER : s === 2 ? P.LED_GREEN : P.LED_OFF);
        }
    }
    const pushes = [SP.push1, SP.push2, SP.stand];
    buf.sprite(pushes[fi % pushes.length], A1, px - 2, fy - 8);
    // Gear
    if (w >= 55) {
      const gx = (w >> 1) + 8, gy = fy - 6;
      const gArt = [['..GG..', '.GGGG.', 'GGggGG', 'GGggGG', '.GGGG.', '..GG..'],
                     ['.G..G.', 'GGGGG.', '.GggGG', 'GGggG.', '.GGGGG', '.G..G.']];
      const gMap = { G: P.GEAR, g: P.GEAR_D, '.': null };
      buf.sprite(gArt[fi % gArt.length], gMap, gx, gy);
    }
    // Progress bar
    if (w >= 40) {
      const bw = Math.min(20, w / 3 | 0), bx = 3, by = ph - 4;
      const fill = ((fi + 1) * bw / n) | 0;
      for (let dx = 0; dx < bw; dx++) { const c = dx < fill ? P.PROG_G : P.PROG_BG; buf.set(bx + dx, by, c); buf.set(bx + dx, by + 1, c); }
    }
    // Log on monitor
    if (w >= 40) {
      const mx = 5, my = dy - 6;
      for (let r = 0; r < 4; r++) {
        const len = ((r + fi) * 3) % 5 + 1;
        for (let c = 0; c < len; c++) buf.set(mx + c, my + r, (r + fi) % 3 !== 0 ? P.MON_GREEN : P.MON_WHITE);
      }
    }
    return buf.toHtml();
  });
}

function genBuilding(w, h, n = 8) {
  const ph = h * 2;
  const bColors = [P.GOLD, P.LAPIS, P.REDSTONE, P.EMERALD, P.DIAMOND];
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy } = buildOffice(w, ph, fi);
    const cw = Math.min(w - 10, (w * 2 / 3) | 0), cx = 3, cy = fy + 4;
    // Conveyor
    if (cw >= 10) {
      for (let dx = 0; dx < cw; dx++) {
        const c = (dx + fi) % 4 === 0 ? P.CONV_D : P.CONV;
        buf.set(cx + dx, cy, c); buf.set(cx + dx, cy + 1, c);
      }
      buf.set(cx, cy + 2, P.STONE_DARK); buf.set(cx + cw - 1, cy + 2, P.STONE_DARK);
    }
    // Carrier
    if (cw >= 10) {
      const ax = cx + ((fi * 4) % Math.max(1, cw - 10));
      buf.sprite(CARRY1, CARRY_MAP, ax, cy - 12);
    }
    // Blocks on belt
    if (cw >= 20) {
      for (let i = 0; i < 3; i++) {
        const bx = cx + 5 + ((fi * 4 + i * 8) % Math.max(1, cw - 8));
        const bc = bColors[(fi + i) % bColors.length];
        buf.fill(bx, cy - 3, 3, 3, bc);
      }
    }
    // Stack
    if (w >= 50) {
      const sx = w - 12, sy = fy + 3, cnt = Math.min(fi + 1, 4);
      for (let i = 0; i < cnt; i++) buf.fill(sx, sy - i * 3, 3, 3, bColors[i % bColors.length]);
    }
    // Progress
    if (w >= 40) {
      const bw = Math.min(16, w / 4 | 0), bx = 3, by = ph - 4;
      const fill = ((fi + 1) * bw / n) | 0;
      for (let dx = 0; dx < bw; dx++) { const c = dx < fill ? P.PROG_G : P.PROG_BG; buf.set(bx + dx, by, c); buf.set(bx + dx, by + 1, c); }
    }
    return buf.toHtml();
  });
}

function genIdle(w, h, n = 8) {
  const ph = h * 2;
  return Array.from({ length: n }, (_, fi) => {
    const { buf, fy, dy } = buildOffice(w, ph, fi);
    const ay = dy - 12 + 1;
    // Agent drinking
    if (w >= 40) {
      const drinks = [SP.drink1, SP.drink2, SP.drink1];
      buf.sprite(drinks[fi % drinks.length], DRINK_MAP, 5, ay);
      // Steam
      const particles = [[0, 0], [1, -1], [-1, -2], [0, -3], [1, -4]];
      for (let i = 0; i < particles.length; i++) {
        const [dx, ddy] = particles[i];
        const py = ay - 2 + ddy - (fi % 4), ppx = 12 + dx + ((fi + i) % 3 - 1);
        if (py >= 0 && ppx >= 0 && ppx < buf.w) buf.set(ppx, py, (Math.abs(ddy) + fi % 4) < 3 ? P.STEAM : P.STEAM_F);
      }
    }
    // Agent leaning
    if (w >= 60) {
      const d2 = (w / 3 | 0) + 2;
      buf.sprite(fi % 4 < 2 ? SP.lean : SP.sit, A2, d2 + 2, ay);
      // Chat bubble
      if (fi % 4 < 2) {
        const cb = ['..CCCCC.','CCTTTCC','CCTTTCC','..CCCCC.','CC......'];
        buf.sprite(cb, { C: P.THOUGHT, T: P.MON_WHITE, '.': null }, 14, ay - 6);
      }
    }
    // Steam from coffee machine
    if (w >= 55) {
      const cmx = (w >> 1) + 5, cmy = fy;
      for (let i = 0; i < 3; i++) {
        const py = cmy - (fi % 3) - i;
        if (py >= 0) buf.set(cmx + ((fi + i) % 2), py, i < 2 ? P.STEAM : P.STEAM_F);
      }
    }
    return buf.toHtml();
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
    description: 'Claude is analyzing the problem, reading code, and planning the approach.',
    trigger: 'Triggered when Claude reads files or formulates a plan',
    generateFrames: genThinking,
  },
  coding: {
    name: 'Coding', icon: '>>_',
    description: 'Active code generation. Engineers typing simultaneously at their workstations.',
    trigger: 'Triggered when Claude writes or edits code files',
    generateFrames: genCoding,
  },
  debugging: {
    name: 'Debugging', icon: '/!\\',
    description: 'Engineers at the whiteboard tracking bugs, examining error traces.',
    trigger: 'Triggered when Claude investigates errors or test failures',
    generateFrames: genDebugging,
  },
  running: {
    name: 'Running', icon: '[>>]',
    description: 'Control panel activated, server rack blinking, progress bar advancing.',
    trigger: 'Triggered when Claude runs shell commands or tests',
    generateFrames: genRunning,
  },
  building: {
    name: 'Building', icon: '▐█▌',
    description: 'Engineers carry code blocks along conveyor belt to the assembly platform.',
    trigger: 'Triggered when Claude runs build or compilation commands',
    generateFrames: genBuilding,
  },
  idle: {
    name: 'Idle', icon: '~☕~',
    description: 'Coffee break. Engineers chat, relax, and sip coffee while waiting.',
    trigger: 'Shown when Claude Code is idle or between tasks',
    generateFrames: genIdle,
  },
};

export function getPreviewFrame(sceneKey, width = 40, height = 14) {
  const scene = SCENES[sceneKey];
  if (!scene) return [];
  return scene.generateFrames(width, height, 1)[0] || [];
}

export function getHeroFrames(width = 68, height = 20) {
  const all = [];
  for (const key of ['thinking', 'coding', 'debugging', 'running', 'building', 'idle']) {
    const scene = SCENES[key];
    const frames = scene.generateFrames(width, height, 4);
    for (const frame of frames) all.push({ lines: frame, scene: key, label: scene.name });
  }
  return all;
}
