// measure_flagship.mjs -- the flagship package's marks (LD2; branch design/marks-flagship; a PIN surface, so this
// measures a package that lands only in a declared pin move). Design lane, 2026-09-26. Serve the package's site/
// with /combined mapped to combined.html, then:
//   PLAYWRIGHT=<.../node_modules/playwright/index.mjs> BASE=http://127.0.0.1:8784 node design/glyph_architecture/measure_flagship.mjs > out.json
// Asserts: no horizontal overflow; the ladder beside the title; exactly one tier mark in every tier badge and on
// every tier filter, each lit in its own tier's colour from the page's TIERS; the title's one-shot only where the
// house gate is open (read from the layer's own classes on that run, since the flagship's high-contrast axis is
// the one that turns the ground light); a shared link to one objection plays that badge's mark once and no other.
const { chromium, firefox } = await import(process.env.PLAYWRIGHT || 'playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8784';
const MODES = ['standard', 'legible', 'high-contrast', 'both'];
const WIDTHS = [360, 390, 430, 768, 1024, 1440];
const init = ([mode, tier]) => { try {
  const g = Storage.prototype.getItem;
  Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
  sessionStorage.setItem('wz-hint-seen', '1'); localStorage.setItem('arglib-mode', mode);
  if (tier !== '') localStorage.setItem('wz-tier', tier); } catch (e) {} };
const PROBE = () => {
  const hex = c => '#' + c.match(/\d+/g).slice(0, 3).map(v => (+v).toString(16).padStart(2, '0')).join('');
  const badges = [...document.querySelectorAll('#results .objection-header .tier-badge')];
  const filters = [...document.querySelectorAll('#tierFilters .filter-btn[data-tier]')];
  const litWrong = [...badges, ...filters].filter(b => { const t = +b.getAttribute('data-tier'), l = b.querySelector('.sg-lit');
    return !l || hex(getComputedStyle(l).fill) !== TIERS[t].color.toLowerCase(); }).length;
  return { overflow: document.documentElement.scrollWidth - innerWidth,
    titleMark: document.querySelectorAll('.header h1 .lib-mark').length,
    badges: badges.length, badgesMarked: badges.filter(b => b.querySelectorAll('.mk-tile').length === 1).length,
    filters: filters.length, filtersMarked: filters.filter(b => b.querySelectorAll('.mk-tile').length === 1).length,
    litWrong, gateOpen: document.documentElement.classList.contains('wz-vfx') && !document.documentElement.classList.contains('wz-lightbg') };
};
async function open(b, url, { w = 1440, h = 900, mode = 'standard', tier = '', reduced = 'no-preference' } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: reduced });
  await ctx.addInitScript(init, [mode, tier]); const p = await ctx.newPage(), errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', c => { if (c.type() === 'error') errs.push(c.text()); });
  await p.goto(BASE + url, { waitUntil: 'load' }); await p.waitForFunction(() => document.querySelectorAll('#results .objection-header').length > 0);
  return { ctx, p, errs };
}
const running = (p, sel) => p.evaluate(s => [...document.querySelectorAll(s)]
  .reduce((n, e) => n + e.getAnimations().filter(a => a.playState === 'running').length, 0), sel);
const rec = { base: BASE, engines: {}, layout: { runs: 0, overflowRuns: 0, errors: 0, marksWrong: 0, litWrong: 0 }, motion: [], arrival: [] };
for (const [en, eng] of [['chromium', chromium], ['firefox', firefox]]) {
  const b = await eng.launch(); rec.engines[en] = b.version();
  for (const mode of MODES) for (const w of WIDTHS) {
    const { ctx, p, errs } = await open(b, '/combined', { w, h: w <= 600 ? 844 : 900, mode, tier: '1' });
    await p.waitForTimeout(250); const r = await p.evaluate(PROBE); await ctx.close();
    const L = rec.layout; L.runs++; L.overflowRuns += r.overflow > 0; L.errors += errs.length; L.litWrong += r.litWrong;
    const wrong = r.titleMark !== 1 || r.badges !== 82 || r.badgesMarked !== 82 || r.filters !== 5 || r.filtersMarked !== 5;
    if (wrong || r.overflow > 0 || errs.length) (L.detail ||= []).push({ engine: en, mode, w, ...r, errs: errs.slice(0, 2) });
    L.marksWrong += wrong;
  }
  for (const [name, o] of [['vfx, standard', {}], ['vfx, legible', { mode: 'legible' }], ['vfx, high-contrast', { mode: 'high-contrast' }],
      ['vfx, both', { mode: 'both' }], ['reduced motion', { reduced: 'reduce' }], ['display: cosmetic', { tier: '1' }], ['display: off', { tier: '0' }]]) {
    const { ctx, p } = await open(b, '/combined', o);
    const gate = await p.evaluate(() => document.documentElement.classList.contains('wz-vfx') && !document.documentElement.classList.contains('wz-lightbg'))
      && !o.reduced;
    const early = await running(p, '.header h1 .lib-mark rect');
    await p.waitForTimeout(2000); const after = await running(p, '.header h1 .lib-mark rect');
    await ctx.close();
    rec.motion.push({ engine: en, case: name, gateOpen: gate, early, after, ok: (gate ? early > 0 : early === 0) && after === 0 });
  }
  for (const [name, o] of [['vfx, standard', {}], ['reduced motion', { reduced: 'reduce' }]]) {
    const id = 'obj-just-depressed';
    const { ctx, p } = await open(b, '/combined#' + id, o);
    await p.waitForTimeout(250);
    const focused = await p.evaluate(i => { const e = document.getElementById(i); return !!e && e.classList.contains('focused'); }, id);
    const target = await running(p, `#${id} .tier-badge .sg-m`);
    const others = await p.evaluate(i => [...document.querySelectorAll('#results .objection-header')].filter(e => e.id !== i)
      .reduce((n, e) => n + [...e.querySelectorAll('.sg-m')].reduce((m, x) => m + x.getAnimations().filter(a => a.playState === 'running').length, 0), 0), id);
    await p.waitForTimeout(1500); const after = await running(p, `#${id} .tier-badge .sg-m`);
    await ctx.close();
    rec.arrival.push({ engine: en, case: name, focused, target, others, after,
                       ok: focused && (o.reduced ? target === 0 : target > 0) && others === 0 && after === 0 });
  }
  await b.close();
}
const L = rec.layout;
rec.summary = { layoutOk: L.overflowRuns === 0 && L.errors === 0 && L.marksWrong === 0 && L.litWrong === 0,
  layout: `${L.runs} runs: overflow ${L.overflowRuns}, errors ${L.errors}, marks wrong ${L.marksWrong}, lit not its tier colour ${L.litWrong}`,
  motion: rec.motion.filter(m => m.ok).length + ' of ' + rec.motion.length,
  arrival: rec.arrival.filter(m => m.ok).length + ' of ' + rec.arrival.length };
console.log(JSON.stringify(rec, null, 1));
