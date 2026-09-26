// shoot_ld2.mjs -- screenshots of LD2's prototypes (build_ld2.py proto) for the design sheet.
// Design lane (seat l), 2026-09-26. Serve <out>/site first (any static server that maps /combined and
// /<wing>/combined to their .html), then:
//   PLAYWRIGHT=<.../node_modules/playwright/index.mjs> BASE=http://127.0.0.1:8781 OUT=<out>/shots node shoot_ld2.mjs
// The layer's first-visit tours and hint are stubbed so nothing covers a page; the display tier is left at
// its default (vfx), which is what a first-time reader gets.
const { chromium } = await import(process.env.PLAYWRIGHT || 'playwright');
import { mkdirSync } from 'node:fs';
const BASE = process.env.BASE || 'http://127.0.0.1:8781', OUT = process.env.OUT || 'shots';
mkdirSync(OUT, { recursive: true });
const init = ([mode]) => {
  try {
    const g = Storage.prototype.getItem;
    Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
    sessionStorage.setItem('wz-hint-seen', '1');
    localStorage.setItem('wuld:libmode', mode); localStorage.setItem('arglib-mode', mode === 'legible' ? 'legible' : 'standard');
  } catch (e) {}
};
const b = await chromium.launch();
const errors = [];
async function page(url, { w = 1440, h = 900, mode = 'standard', dpr = 1 } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
  await ctx.addInitScript(init, [mode]);
  const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(url + ' ' + e)); p.on('console', c => { if (c.type() === 'error') errors.push(url + ' ' + c.text()); });
  await p.goto(BASE + url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
  return { ctx, p };
}
const shots = [];
async function shot(name, url, o = {}, act = null, clip = null) {
  const { ctx, p } = await page(url, o);
  if (act) await act(p);
  const file = `${OUT}/${name}.png`;
  if (typeof clip === 'string') await p.locator(clip).first().screenshot({ path: file });   // an element, exactly
  else await p.screenshot({ path: file, clip: clip || undefined });
  shots.push(name); await ctx.close();
}
const W = '/right-to-die/combined';
// B + C + D on a wing, desktop: the title's mark, the tier marks on chips and cards, the spine in the margin
await shot('wing_desktop_dark', W, { w: 1440, h: 900 });
await shot('wing_desktop_light', W, { w: 1440, h: 900, mode: 'legible' });
// C: scrolled to the sixth objection, the spine's lit node has moved with the reader
await shot('wing_spine_scrolled', W, { w: 1440, h: 900 }, async p => {
  await p.evaluate(() => { const c = document.querySelectorAll('#list .obj')[5]; scrollTo(0, c.getBoundingClientRect().top + scrollY - 120); });
  await p.waitForTimeout(400);
});
// phones: no margin, so no spine; the title's mark and the tier marks
await shot('wing_phone_dark', W, { w: 390, h: 844, dpr: 2 });
await shot('wing_phone_light', W, { w: 390, h: 844, dpr: 2, mode: 'legible' });
// B: the About tab's plate
await shot('wing_about_plate', W, { w: 1440, h: 900 }, async p => {
  await p.click('#tab-about'); await p.waitForTimeout(300);
  await p.evaluate(() => { const f = document.querySelector('.mk-plate'); scrollTo(0, f.getBoundingClientRect().top + scrollY - 200); });
  await p.waitForTimeout(300);
});
for (const wing of ['abortion', 'transgenderism', 'anthropocentrism', 'veganism'])
  await shot(`head_${wing}`, `/${wing}/combined`, { w: 1440, h: 900 }, null, 'header.site h1');
// B's flagship half, in the package: the ladder beside the flagship's title
await shot('flag_head', '/combined?c=tier', { w: 1440, h: 900 }, null, '.header');
// D on the flagship (a PIN surface; scratch copy only): tier colour, then crimson
for (const c of ['tier', 'crimson']) {
  await shot(`flag_${c}`, `/combined?c=${c}`, { w: 1440, h: 900 }, async p => {
    await p.evaluate(() => { const f = document.getElementById('tierFilters'); scrollTo(0, f.getBoundingClientRect().top + scrollY - 190); });
    await p.waitForTimeout(400);
  });
}
await b.close();
console.log(JSON.stringify({ shots, errors }, null, 1));
