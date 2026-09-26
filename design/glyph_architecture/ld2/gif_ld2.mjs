// gif_ld2.mjs -- frames of proposal A (the seven library marks saying their sentences) from the design sheet,
// for a GIF. Design lane (seat l), 2026-09-26. Every CSS animation in the sheet's #a grid is paused and SEEKED to
// each frame's time, so the frames are exact whatever the machine's speed. Then assemble, e.g.:
//   ffmpeg -framerate 25 -i f%03d.png -vf "split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=none" -loop 0 a.gif
// Usage: PLAYWRIGHT=<.../playwright/index.mjs> URL=<sheet url> OUT=<frames dir> node gif_ld2.mjs
const { chromium } = await import(process.env.PLAYWRIGHT || 'playwright');
import { mkdirSync, copyFileSync } from 'node:fs';
const OUT = process.env.OUT || 'frames', STEP = 40, LEAD = 10, HOLD = 55;   // ms per frame; frames held at each end
mkdirSync(OUT, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.goto(process.env.URL, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
const end = await p.evaluate(() => {
  const g = document.getElementById('a'); g.classList.remove('play'); void g.offsetWidth; g.classList.add('play');
  const as = document.getAnimations().filter(a => g.contains(a.effect.target));
  as.forEach(a => a.pause());
  window.__as = as;
  return Math.max(...as.map(a => { const t = a.effect.getComputedTiming(); return t.delay + t.activeDuration; }));
});
const grid = p.locator('#a');
let n = 0;
const frame = async t => {
  await p.evaluate(t => window.__as.forEach(a => { a.currentTime = t; }), t);
  const f = `${OUT}/f${String(n).padStart(3, '0')}.png`; await grid.screenshot({ path: f }); n++; return f;
};
const first = await frame(0);
for (let i = 1; i < LEAD; i++) copyFileSync(first, `${OUT}/f${String(n++).padStart(3, '0')}.png`);
let last = first;
for (let t = STEP; t <= end + STEP; t += STEP) last = await frame(Math.min(t, end));
for (let i = 0; i < HOLD; i++) copyFileSync(last, `${OUT}/f${String(n++).padStart(3, '0')}.png`);
console.log(JSON.stringify({ frames: n, animations: await p.evaluate(() => window.__as.length), end_ms: end }));
await b.close();
