// measure_front_door.mjs -- the front-door key ("Reading the marks"), measured in a real browser, both engines.
// Design lane, 2026-09-25. Serve site/ first, then run:
//   (cd site && python3 -m http.server 8765 --bind 127.0.0.1) &
//   PLAYWRIGHT=<.../node_modules/playwright/index.mjs> node design/glyph_architecture/measure_front_door.mjs > out.json
// Optional: BASELINE_URL=<the same page before the change> adds the vfx-tier overflow comparison (the house
// layer's tour pan, a finding in ARCHITECTURE_library_v0_1.md §9). Prints one JSON record, no timestamps.
// On 2026-09-25 PLAYWRIGHT was ~/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs (1.63.0), the
// build that matches the installed chromium-1243 and firefox-1543. npx cache paths move; find one that runs.
const { chromium, firefox } = await import(process.env.PLAYWRIGHT || 'playwright');
const URL = process.env.URL || 'http://127.0.0.1:8765/libraries/', BASE = process.env.BASELINE_URL || '';
const MODES = ['standard', 'legible', 'high-contrast', 'both'];
const WIDTHS = [360, 390, 430, 600, 768, 1024, 1152, 1280, 1440, 1920];
const init = ([mode, tier]) => { try { localStorage.setItem('wuld:libmode', mode);
  localStorage.setItem('wz-tour:library:index', '1'); sessionStorage.setItem('wz-hint-seen', '1');
  if (tier !== '') localStorage.setItem('wz-tier', tier); } catch (e) {} };

// overflow, AA contrast of every text item in the key and the rail cell, where the key sits
const PROBE = () => {
  const lum = (r, g, b) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; };
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const rgb = s => s.match(/[\d.]+/g).map(Number);
  const bg = el => { for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor);
    if (c.length < 4 || c[3] > .5) return c; } return [255, 255, 255]; };
  const ratio = (a, b) => { const x = lum(...a.slice(0, 3)), y = lum(...b.slice(0, 3)); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const k = document.getElementById('marks'), m = document.querySelector('main');
  const items = [...k.querySelectorAll('h2,h3,p,figcaption,.mk-name,.mk-says,.mk-name b,a'), ...document.querySelectorAll('.rail-tiers b,.rail-tiers>span')]
    .filter(e => e.textContent.trim()).map(e => ratio(rgb(getComputedStyle(e).color), bg(e)));
  for (const t of document.querySelectorAll('.mk-plate-svg text')) items.push(ratio(rgb(getComputedStyle(t).fill), bg(t.closest('.pl'))));
  return { overflow: document.documentElement.scrollWidth - innerWidth, aaMin: Math.min(...items), aaN: items.length,
           aaBelow: items.filter(r => r < 4.5).length, beside: k.getBoundingClientRect().left > m.getBoundingClientRect().right - 1,
           keyHeight: k.offsetHeight, namedMarks: document.querySelectorAll('.lib-card h2 .lib-mark, header.site h1 .lib-mark').length };
};
const anims = p => p.evaluate(() => [...document.querySelectorAll('.sg-m')].reduce((n, e) => n + e.getAnimations().length, 0));
async function open(b, url, { w, h, mode = 'standard', tier = '', reduced = 'no-preference' }) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: reduced });
  await ctx.addInitScript(init, [mode, tier]); const p = await ctx.newPage(), errs = [];
  p.on('pageerror', e => errs.push(String(e))); p.on('console', c => { if (c.type() === 'error') errs.push(c.text()); });
  await p.goto(url, { waitUntil: 'networkidle' }); return { ctx, p, errs };
}
const rec = { url: URL, engines: {}, layout: { runs: 0, overflowRuns: 0, aaMin: 99, aaBelow: 0, errors: 0, besideFromPx: null, namedMarksMin: 99 },
              motion: [], sticky: [], layerPan: null };
for (const [en, eng] of [['chromium', chromium], ['firefox', firefox]]) {
  const b = await eng.launch(); rec.engines[en] = b.version();
  // 1. layout and AA at the cosmetic display tier (the vfx tier pans the stage; that is the layer's, see 4.)
  for (const mode of MODES) for (const w of WIDTHS) {
    const { ctx, p, errs } = await open(b, URL, { w, h: w <= 600 ? 844 : 900, mode, tier: '1' });
    await p.waitForTimeout(300); const r = await p.evaluate(PROBE); await ctx.close();
    const L = rec.layout; L.runs++; L.overflowRuns += r.overflow > 0; L.aaMin = Math.min(L.aaMin, +r.aaMin.toFixed(2));
    L.aaBelow += r.aaBelow; L.errors += errs.length; L.aaItems = r.aaN; L.namedMarksMin = Math.min(L.namedMarksMin, r.namedMarks);
    if (r.beside && (L.besideFromPx === null || w < L.besideFromPx)) L.besideFromPx = w;
  }
  // 2. the motion gate: [case, options, animations wanted while playing]
  for (const [name, o, want] of [['vfx, dark, motion allowed', { w: 1440, h: 900 }, 12], ['reduced motion', { w: 1440, h: 900, reduced: 'reduce' }, 0],
      ['legible (light ground)', { w: 1440, h: 900, mode: 'legible' }, 0], ['display: cosmetic', { w: 1440, h: 900, tier: '1' }, 0],
      ['display: off', { w: 1440, h: 900, tier: '0' }, 0], ['phone, key below the fold', { w: 390, h: 844 }, 'scroll']]) {
    // every case scrolls the tier rows into view: they play the first time they are seen, wherever they sit
    const { ctx, p } = await open(b, URL, o); await p.waitForTimeout(600); const early = await anims(p);
    await p.locator('#mk-rows').scrollIntoViewIfNeeded();
    await p.waitForTimeout(350); const during = await anims(p); await p.waitForTimeout(2800); const after = await anims(p);
    let hover = null; if (want === 12) { await p.locator('.mk-row.t4').hover(); await p.waitForTimeout(150); hover = await anims(p); }
    await ctx.close();
    const ok = want === 'scroll' ? early === 0 && during === 12 && after === 0
             : want === 12 ? during === 12 && after === 0 && hover === 1
             : early === 0 && during === 0 && after === 0;
    rec.motion.push({ engine: en, case: name, during, after, hover, beforeScroll: early, ok });
  }
  // 3. sticky only while the key fits the window
  for (const [w, h] of [[1440, 1100], [1440, 900], [1920, 1080]]) {
    const { ctx, p } = await open(b, URL, { w, h }); await p.waitForTimeout(600);
    const r = await p.evaluate(async () => { const k = document.getElementById('marks'); scrollTo(0, 700);
      await new Promise(f => setTimeout(f, 300)); return { stick: k.classList.contains('stick'), top: Math.round(k.getBoundingClientRect().top), h: k.offsetHeight }; });
    await ctx.close(); rec.sticky.push({ engine: en, viewport: w + 'x' + h, ...r });
  }
  // 4. the house layer's own overflow at the vfx tier during its first-visit tour: this page vs the baseline
  if (BASE) {
    const n = { page: 0, baseline: 0, runs: 0 };
    for (const mode of MODES) for (const w of [360, 390, 430, 600, 768, 1024]) for (const [k, url] of [['page', URL], ['baseline', BASE]]) {
      const ctx = await b.newContext({ viewport: { width: w, height: 844 } });
      await ctx.addInitScript(m => { try { localStorage.setItem('wuld:libmode', m); } catch (e) {} }, mode);
      const p = await ctx.newPage(); await p.goto(url, { waitUntil: 'networkidle' }); await p.waitForTimeout(400);
      n[k] += await p.evaluate(() => document.documentElement.scrollWidth > innerWidth); n.runs += k === 'page';
      await ctx.close();
    }
    (rec.layerPan ||= {})[en] = n;
  }
  await b.close();
}
rec.summary = { layoutOk: rec.layout.overflowRuns === 0 && rec.layout.aaBelow === 0 && rec.layout.errors === 0 && rec.layout.namedMarksMin === 7,
                motionOk: rec.motion.filter(m => m.ok).length + ' of ' + rec.motion.length };
console.log(JSON.stringify(rec, null, 1));
