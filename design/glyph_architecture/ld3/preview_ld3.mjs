// preview_ld3.mjs -- the flagship package, merged with v4.1.3, for Josiah's look before the pin move (LD3, seat l,
// 2026-09-26). Serve the package's site/ (mapping /combined to combined.html), then:
//   PLAYWRIGHT=<.../playwright/index.mjs> FLAG=http://127.0.0.1:8784 OUT=<dir> node preview_ld3.mjs
// Dark = the standard mode; light = high-contrast (the flagship's axis that turns the ground light). Tours stubbed.
const { chromium } = await import(process.env.PLAYWRIGHT || 'playwright');
import { mkdirSync } from 'node:fs';
const FLAG = process.env.FLAG, OUT = process.env.OUT || 'preview'; mkdirSync(OUT, { recursive: true });
const init = ([mode]) => { try {
  const g = Storage.prototype.getItem;
  Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
  sessionStorage.setItem('wz-hint-seen', '1'); localStorage.setItem('arglib-mode', mode);
} catch (e) {} };
const b = await chromium.launch(), errors = [], light = {};
async function shot(name, { w = 1440, h = 900, mode = 'standard', dpr = 1, at = null, sel = null } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
  await ctx.addInitScript(init, [mode]); const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(name + ' ' + e)); p.on('console', c => { if (c.type() === 'error') errors.push(name + ' ' + c.text()); });
  await p.goto(FLAG + '/combined', { waitUntil: 'networkidle' }); await p.waitForTimeout(1800);
  light[name] = await p.evaluate(() => document.documentElement.classList.contains('wz-lightbg') || getComputedStyle(document.body).backgroundColor);
  if (at) { await p.evaluate(s => { const e = document.querySelector(s); scrollTo(0, e.getBoundingClientRect().top + scrollY - 20); }, at); await p.waitForTimeout(300); }
  if (sel) await p.locator(sel).first().screenshot({ path: `${OUT}/${name}.png` }); else await p.screenshot({ path: `${OUT}/${name}.png` });
  await ctx.close();
}
for (const [tag, mode] of [['dark', 'standard'], ['light', 'high-contrast']]) {
  await shot(`desktop_${tag}_top`, { mode });
  await shot(`desktop_${tag}_filters`, { mode, at: '#tierFilters' });
  await shot(`phone_${tag}_top`, { mode, w: 390, h: 844, dpr: 2 });
  await shot(`phone_${tag}_cards`, { mode, w: 390, h: 844, dpr: 2, at: '#tierFilters' });
}
await shot('closeup_title', { sel: '.header h1', dpr: 3 });
await shot('closeup_filters', { sel: '#tierFilters', dpr: 3 });
await b.close();
console.log(JSON.stringify({ errors, light }, null, 1));
