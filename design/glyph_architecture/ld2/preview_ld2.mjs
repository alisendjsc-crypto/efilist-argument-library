// preview_ld2.mjs -- screenshots of the BUILT pages (branch design/marks) and the flagship package (branch
// design/marks-flagship) for Josiah's look before the merge, plus frames of the front door's marks speaking.
// Design lane (seat l), 2026-09-26. Serve each branch's site/ (mapping /<page>/combined to its .html), then:
//   PLAYWRIGHT=<.../playwright/index.mjs> BASE=http://127.0.0.1:8783 FLAG=http://127.0.0.1:8784 OUT=<dir> node preview_ld2.mjs
// The layer's first-visit tours and hint are stubbed; the display tier stays at its default (vfx).
const { chromium } = await import(process.env.PLAYWRIGHT || 'playwright');
import { mkdirSync, copyFileSync } from 'node:fs';
const BASE = process.env.BASE, FLAG = process.env.FLAG, OUT = process.env.OUT || 'preview';
mkdirSync(OUT + '/frames', { recursive: true });
const init = ([mode]) => { try {
  const g = Storage.prototype.getItem;
  Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
  sessionStorage.setItem('wz-hint-seen', '1'); localStorage.setItem('wuld:libmode', mode); localStorage.setItem('arglib-mode', mode);
} catch (e) {} };
const b = await chromium.launch(), errors = [];
async function page(url, { w = 1440, h = 900, mode = 'standard', dpr = 1 } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
  await ctx.addInitScript(init, [mode]); const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(url + ' ' + e)); p.on('console', c => { if (c.type() === 'error') errors.push(url + ' ' + c.text()); });
  await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(1800); return { ctx, p };
}
async function shot(name, url, o = {}, act = null, sel = null) {
  const { ctx, p } = await page(url, o); if (act) await act(p);
  if (sel) await p.locator(sel).first().screenshot({ path: `${OUT}/${name}.png` }); else await p.screenshot({ path: `${OUT}/${name}.png` });
  await ctx.close();
}
const D = BASE + '/libraries/', R = BASE + '/right-to-die/combined';
await shot('door_dark', D); await shot('door_light', D, { mode: 'legible' }); await shot('door_phone', D, { w: 390, h: 844, dpr: 2 });
await shot('rtd_dark', R); await shot('rtd_light', R, { mode: 'legible' });
await shot('rtd_phone_dark', R, { w: 390, h: 844, dpr: 2 }); await shot('rtd_phone_light', R, { w: 390, h: 844, dpr: 2, mode: 'legible' });
await shot('rtd_spine', R, {}, async p => { await p.evaluate(() => { const c = document.querySelectorAll('#list .obj')[9];
  scrollTo(0, c.getBoundingClientRect().top + scrollY - 120); }); await p.waitForTimeout(300); });
for (const w of ['right-to-die', 'abortion', 'transgenderism', 'anthropocentrism', 'veganism']) {
  await shot('title_' + w, `${BASE}/${w}/combined`, {}, null, 'header.site h1');
  await shot('plate_' + w, `${BASE}/${w}/combined`, {}, async p => { await p.click('#tab-about'); await p.waitForTimeout(200); }, '.mk-plate');
}
await shot('flag_head', FLAG + '/combined', {}, null, '.header');
await shot('flag_badges', FLAG + '/combined', {}, async p => { await p.evaluate(() => { const f = document.getElementById('tierFilters');
  scrollTo(0, f.getBoundingClientRect().top + scrollY - 150); }); await p.waitForTimeout(300); });
// frames: the front door's title and first cards saying their sentences, seeked (exact whatever the speed)
{
  const { ctx, p } = await page(D);
  const end = await p.evaluate(() => {
    const els = [document.querySelector('header.site h1'), ...document.querySelectorAll('.lib-card')].filter(e => e && e.querySelector('.lib-mark'));
    els.forEach(e => e.classList.remove('play')); void document.body.offsetWidth; els.forEach(e => e.classList.add('play'));
    const as = document.getAnimations().filter(a => a.effect && a.effect.target && a.effect.target.closest && a.effect.target.closest('.lib-mark'));
    as.forEach(a => a.pause()); window.__as = as;
    return Math.max(...as.map(a => { const t = a.effect.getComputedTiming(); return t.delay + t.activeDuration; }));
  });
  const clip = { x: 0, y: 0, width: 1100, height: 900 };
  let n = 0; const f = () => `${OUT}/frames/f${String(n).padStart(3, '0')}.png`;
  await p.evaluate(() => window.__as.forEach(a => { a.currentTime = 0; })); await p.screenshot({ path: f(), clip }); const first = f(); n++;
  for (let i = 1; i < 10; i++) { copyFileSync(first, f()); n++; }
  let last = first;
  for (let t = 40; t <= end + 40; t += 40) { await p.evaluate(t => window.__as.forEach(a => { a.currentTime = t; }), Math.min(t, end));
    await p.screenshot({ path: f(), clip }); last = f(); n++; }
  for (let i = 0; i < 55; i++) { copyFileSync(last, f()); n++; }
  console.log(JSON.stringify({ frames: n, animations: await p.evaluate(() => window.__as.length), end_ms: end }));
  await ctx.close();
}
await b.close();
console.log(JSON.stringify({ errors }));
