// measure_wings.mjs -- the wings' marks (LD2), measured in a real browser, both engines.
// Design lane, 2026-09-26. Serve site/ first with /<wing>/combined mapped to its .html, then:
//   PLAYWRIGHT=<.../node_modules/playwright/index.mjs> BASE=http://127.0.0.1:8783 node design/glyph_architecture/measure_wings.mjs > out.json
// Prints one JSON record, no timestamps. What it asserts, per wing, engine, width and reading mode:
//   no horizontal overflow on either tab; the title's mark; a tier mark on every card's tier line and every tier
//   filter (never more than one); the plate on About; WCAG AA for the text LD2 adds (the plate's part names, its
//   caption) and the tier line the marks sit beside. Then the motion gate (the title says its sentence once at
//   vfx + dark + motion allowed, and nowhere else), anchor arrival (a link to one card plays that card's tier mark
//   and no other), and Right to Die's reading spine (one node per shown card, the lit node follows the reader,
//   hidden on About and where there is no margin, page ink on a light ground).
const { chromium, firefox } = await import(process.env.PLAYWRIGHT || 'playwright');
const BASE = process.env.BASE || 'http://127.0.0.1:8783';
const WINGS = ['right-to-die', 'abortion', 'transgenderism', 'anthropocentrism', 'veganism'];
const MODES = ['standard', 'legible', 'high-contrast', 'both'];
const WIDTHS = [360, 390, 430, 768, 1024, 1440];
const init = ([mode, tier]) => { try {
  const g = Storage.prototype.getItem;
  Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
  sessionStorage.setItem('wz-hint-seen', '1'); localStorage.setItem('wuld:libmode', mode);
  if (tier !== '') localStorage.setItem('wz-tier', tier); } catch (e) {} };
const PROBE = () => {
  const lum = (r, g, b) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; };
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const rgb = s => s.match(/[\d.]+/g).map(Number);
  const bg = el => { for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor);
    if (c.length < 4 || c[3] > .5) return c; } return [255, 255, 255]; };
  const ratio = (a, b) => { const x = lum(...a.slice(0, 3)), y = lum(...b.slice(0, 3)); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const items = [];
  for (const t of document.querySelectorAll('.mk-plate .pl-name')) items.push(ratio(rgb(getComputedStyle(t).fill), bg(t.closest('figure'))));
  for (const t of document.querySelectorAll('.mk-plate figcaption, #list .obj-meta')) items.push(ratio(rgb(getComputedStyle(t).color), bg(t)));
  const cards = document.querySelectorAll('#list .obj'), metas = document.querySelectorAll('#list .obj-meta');
  const chips = [...document.querySelectorAll('#tier-chips .chip[data-tier]')].filter(c => c.getAttribute('data-tier') !== '');
  return { overflow: document.documentElement.scrollWidth - innerWidth,
    aaMin: items.length ? Math.min(...items) : 99, aaN: items.length, aaBelow: items.filter(r => r < 4.5).length,
    titleMark: document.querySelectorAll('header.site h1 .lib-mark').length,
    cards: cards.length, metasMarked: [...metas].filter(m => m.querySelectorAll('.mk-tile').length === 1).length, metas: metas.length,
    chips: chips.length, chipsMarked: chips.filter(c => c.querySelectorAll('.mk-tile').length === 1).length,
    plate: document.querySelectorAll('#panel-about .mk-plate svg[role="img"]').length };
};
async function open(b, url, { w = 1440, h = 900, mode = 'standard', tier = '', reduced = 'no-preference' } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: reduced });
  await ctx.addInitScript(init, [mode, tier]); const p = await ctx.newPage(), errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', c => { if (c.type() === 'error') errs.push(c.text()); });
  await p.goto(BASE + url, { waitUntil: 'networkidle' }); return { ctx, p, errs };
}
// RUNNING animations: a finished one-shot whose fill holds its last frame (the card keeps its .flash) has stopped
const anims = (p, sel) => p.evaluate(s => [...document.querySelectorAll(s)]
  .reduce((n, e) => n + e.getAnimations().filter(a => a.playState === 'running').length, 0), sel);
const rec = { base: BASE, engines: {}, layout: { runs: 0, overflowRuns: 0, aboutOverflowRuns: 0, aaMin: 99, aaBelow: 0, errors: 0, marksWrong: 0 },
              motion: [], arrival: [], spine: [] };
for (const [en, eng] of [['chromium', chromium], ['firefox', firefox]]) {
  const b = await eng.launch(); rec.engines[en] = b.version();
  // 1. layout, marks and AA at the cosmetic tier (the vfx tier's camera pans the stage; that is the layer's own)
  for (const wing of (process.env.ONLY ? [] : WINGS)) for (const mode of MODES) for (const w of WIDTHS) {
    const { ctx, p, errs } = await open(b, `/${wing}/combined`, { w, h: w <= 600 ? 844 : 900, mode, tier: '1' });
    await p.waitForTimeout(250); const r = await p.evaluate(PROBE);
    await p.click('#tab-about'); await p.waitForTimeout(120);
    const about = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    await ctx.close();
    const L = rec.layout; L.runs++; L.overflowRuns += r.overflow > 0; L.aboutOverflowRuns += about > 0;
    L.aaMin = Math.min(L.aaMin, +r.aaMin.toFixed(2)); L.aaBelow += r.aaBelow; L.errors += errs.length; L.aaItems = r.aaN;
    const wrong = r.titleMark !== 1 || r.metasMarked !== r.metas || r.metas !== r.cards || r.cards === 0 || r.chipsMarked !== r.chips || r.plate !== 1;
    if (wrong) (L.wrong ||= []).push({ engine: en, wing, mode, w, ...r });
    L.marksWrong += wrong;
  }
  // 2. the motion gate: the title's mark on arrival. [case, options, animations wanted early]
  for (const wing of ['right-to-die', 'veganism']) for (const [name, o, want] of [
      ['vfx, dark, motion allowed', {}, 'some'], ['reduced motion', { reduced: 'reduce' }, 0], ['legible (light ground)', { mode: 'legible' }, 0],
      ['display: cosmetic', { tier: '1' }, 0], ['display: off', { tier: '0' }, 0]]) {
    const { ctx, p } = await open(b, `/${wing}/combined`, o);
    const early = await anims(p, 'header.site h1 .lib-mark rect');
    await p.waitForTimeout(2200); const after = await anims(p, 'header.site h1 .lib-mark rect');
    await ctx.close();
    rec.motion.push({ engine: en, wing, case: name, early, after, ok: (want === 'some' ? early > 0 : early === 0) && after === 0 });
  }
  // 3. anchor arrival: a link straight to the sixth card plays that card's tier mark, once, and no other card's
  for (const [name, o, want] of [['vfx, dark, motion allowed', {}, 'some'], ['reduced motion', { reduced: 'reduce' }, 0], ['legible', { mode: 'legible' }, 0]]) {
    const first = await open(b, '/right-to-die/combined', o);
    const id = await first.p.evaluate(() => document.querySelectorAll('#list .obj')[5].id); await first.ctx.close();
    const { ctx, p } = await open(b, `/right-to-die/combined#${id}`, o);
    await p.waitForTimeout(150);
    const target = await anims(p, `#${id} .obj-meta .sg-m`);
    const others = await p.evaluate(i => [...document.querySelectorAll('#list .obj')].filter(c => c.id !== i)
      .reduce((n, c) => n + [...c.querySelectorAll('.sg-m')].reduce((m, e) => m + e.getAnimations().filter(a => a.playState === 'running').length, 0), 0), id);
    await p.waitForTimeout(1500); const after = await anims(p, `#${id} .obj-meta .sg-m`);
    await ctx.close();
    rec.arrival.push({ engine: en, case: name, target, others, after,
                       ok: (want === 'some' ? target > 0 : target === 0) && others === 0 && after === 0 });
  }
  // 4. the reading spine (Right to Die only)
  {
    const { ctx, p } = await open(b, '/right-to-die/combined', { tier: '1' });
    const s = {};
    const lit = () => p.evaluate(() => [...document.querySelectorAll('.mk-spine .sp-n')].findIndex(n => n.classList.contains('lit')));
    const shown = () => p.evaluate(() => { const e = document.querySelector('.mk-spine'); return !!e && getComputedStyle(e).display !== 'none' && !e.hidden; });
    s.nodes = await p.evaluate(() => document.querySelectorAll('.mk-spine .sp-n').length);
    s.cards = await p.evaluate(() => document.querySelectorAll('#list .obj').length);
    s.shownAt1440 = await shown(); s.litAtTop = await lit();
    await p.evaluate(() => { const c = document.querySelectorAll('#list .obj')[5]; scrollTo(0, c.getBoundingClientRect().top + scrollY - 120); });
    await p.waitForTimeout(250); s.litAtSixth = await lit();
    await p.evaluate(() => scrollTo(0, document.documentElement.scrollHeight)); await p.waitForTimeout(250); s.litAtEnd = await lit();
    await p.evaluate(() => scrollTo(0, 0)); await p.fill('#kw-input', 'coercion'); await p.waitForTimeout(250);
    s.filteredNodes = await p.evaluate(() => document.querySelectorAll('.mk-spine .sp-n').length);
    s.filteredCards = await p.evaluate(() => document.querySelectorAll('#list .obj').length);
    await p.fill('#kw-input', ''); await p.click('#tab-about'); await p.waitForTimeout(150); s.shownOnAbout = await shown();
    await p.click('#tab-library'); await p.waitForTimeout(150); s.shownBack = await shown();
    await p.setViewportSize({ width: 390, height: 844 }); await p.waitForTimeout(200); s.shownAt390 = await shown();
    await p.setViewportSize({ width: 1440, height: 900 }); await p.evaluate(() => setMode('legible')); await p.waitForTimeout(150);
    s.lightGround = await p.evaluate(() => getComputedStyle(document.querySelector('.mk-spine')).backgroundColor);
    s.lightLit = await p.evaluate(() => { const n = document.querySelector('.mk-spine .sp-n.lit'); return n && getComputedStyle(n).backgroundColor; });
    await ctx.close();
    s.ok = s.nodes === s.cards && s.cards === 17 && s.shownAt1440 && s.litAtTop === 0 && s.litAtSixth === 5 && s.litAtEnd === 16
      && s.filteredNodes === s.filteredCards && s.filteredCards > 0 && s.filteredCards < 17 && !s.shownOnAbout && s.shownBack
      && !s.shownAt390 && s.lightGround === 'rgba(0, 0, 0, 0)';
    rec.spine.push({ engine: en, ...s });
  }
  await b.close();
}
const L = rec.layout;
rec.summary = { layoutOk: L.overflowRuns === 0 && L.aboutOverflowRuns === 0 && L.aaBelow === 0 && L.errors === 0 && L.marksWrong === 0,
  layout: `${L.runs} runs: overflow ${L.overflowRuns} (About ${L.aboutOverflowRuns}), AA min ${L.aaMin}, below AA ${L.aaBelow}, errors ${L.errors}, marks wrong ${L.marksWrong}`,
  motion: rec.motion.filter(m => m.ok).length + ' of ' + rec.motion.length,
  arrival: rec.arrival.filter(m => m.ok).length + ' of ' + rec.arrival.length,
  spine: rec.spine.filter(m => m.ok).length + ' of ' + rec.spine.length };
console.log(JSON.stringify(rec, null, 1));
