// measure_depth.mjs -- the house layer's depth, measured on the live library pages. WI-K410 (R0160), 2026-09-26.
//
//   PLAYWRIGHT=<.../node_modules/playwright/index.mjs> node layer/measure_depth.mjs [depth] [frames] [fb] > out.json
//   LAYER=<dir>   serve wuld-layer.css and .js from <dir> (a candidate's site/) by route interception, so a
//                 candidate is measured on the live pages without deploying anything. Unset: the live layer.
//   BASE=<url>    default https://library.wuld.ink
//   GPU=intel|nvidia|none   Chromium's compositor for `frames` (default intel: the modest machine).
//   SHOTS=<dir>   also write the depth section's screenshots there.
//   PAGES=<p,p>   fb only: these paths instead of every page that links the layer.
//
// depth  -- flagship and one wing, dark ground, vfx tier, 1440x900: the camera's travel and any gap it opens
//           inside the lip; the far-side blur by the layer's own section-11 test (render with the treatment
//           and without, diff: amplitude, area, and the sharpness kept on the treated side, where the
//           untreated side must read exactly 0); the vignette's corner darkening. A phone tap at the right
//           edge, because the camera listens to mousemove and a touch screen synthesises one per tap. The
//           vertical far side the same way, pointer at the bottom, where the layer has top/bottom strips.
// frames -- rAF intervals over a scripted scroll with the pointer at the right edge (the left strip lit),
//           the strips as configured against the strips hidden, three runs each.
// fb     -- every page that links the layer, seven widths, both grounds, two engines: card text lying under
//           the per-card feedback link. Line boxes, not element boxes: a block's box spans the card whether
//           or not its words reach the link.
// tilt   -- the chin's tilt toggle (K410): it leans and is not inert, the far edge foreshortens, it rests flat
//           and as sharp as with the toggle off, scroll and zoom flatten it, phone / reduced motion / narrow never
//           show it, the chin row is exposed and does not overlap, and frames while it leans. Not in the default run.
import { createRequire } from 'module';
import { writeFileSync } from 'fs';
const PW = process.env.PLAYWRIGHT || 'playwright';
const { chromium, firefox } = await import(PW);
const { PNG } = createRequire(import.meta.url)(PW.replace(/playwright\/index\.mjs$/, 'playwright-core/lib/utilsBundle.js'));
const BASE = process.env.BASE || 'https://library.wuld.ink';
const LAYER = process.env.LAYER || '';
const SHOTS = process.env.SHOTS || '';
const GPU = process.env.GPU || 'intel';
const ARGS = { intel: ['--enable-gpu', '--ignore-gpu-blocklist'],
               nvidia: ['--enable-gpu', '--ignore-gpu-blocklist', '--use-angle=vulkan', '--enable-features=Vulkan'],
               none: [] };
const SECTIONS = process.argv.slice(2).length ? process.argv.slice(2) : ['depth', 'frames', 'fb'];
const PAGES = process.env.PAGES ? process.env.PAGES.split(',') :
              ['/combined', '/right-to-die/combined', '/anthropocentrism/combined', '/transgenderism/combined',
               '/abortion/combined', '/veganism/combined', '/libraries/', '/adversarial/', '/troubleshooting/'];
const DEPTH_PAGES = ['/combined', '/right-to-die/combined'];
const MODES = ['standard', 'legible', 'high-contrast', 'both'];
const WIDTHS = [320, 360, 390, 430, 768, 1024, 1440];

const init = tier => { try {
  const g = Storage.prototype.getItem;       // no walkthroughs, no first-visit hint: they darken the page
  Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
  sessionStorage.setItem('wz-hint-seen', '1');
  if (tier !== '') localStorage.setItem('wz-tier', tier); } catch (e) {} };

async function open(b, url, { w = 1440, h = 900, tier = '2', reduced = 'no-preference', touch = false, mode = '' } = {}) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: reduced,
    hasTouch: touch, ...(touch && b.browserType().name() === 'chromium' ? { isMobile: true } : {}) });
  if (LAYER) for (const f of ['wuld-layer.css', 'wuld-layer.js'])
    await ctx.route(u => u.pathname === '/' + f, r => r.fulfill({ path: LAYER + '/' + f, headers: { 'cache-control': 'no-store' },
      contentType: f.endsWith('.css') ? 'text/css; charset=utf-8' : 'application/javascript; charset=utf-8' }));
  await ctx.addInitScript(init, tier);
  const p = await ctx.newPage(), errs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 160)));
  p.on('console', c => { if (c.type() === 'error') errs.push(c.text().slice(0, 160)); });
  await p.goto(BASE + url, { waitUntil: 'load' });
  await p.waitForFunction(() => document.querySelector('.wz-frame') && document.querySelector('.wz-stage'), null, { timeout: 20000 });
  await p.waitForFunction(() => document.querySelector('[data-wz-fb]') || !document.querySelector('article.obj, .objection-header'),
    null, { timeout: 10000 }).catch(() => errs.push('no card took a feedback link within 10s'));
  if (mode) await setMode(p, mode);
  await p.waitForTimeout(700);
  return { ctx, p, errs };
}
// A page's own mode switch when it has one (the flagship: #mode-standard/-legible/-hc/-both, which run its
// setMode), else the data-mode attribute the wings and the umbrella pages style from.
const setMode = (p, m) => p.evaluate(m => { const b = document.getElementById('mode-' + (m === 'high-contrast' ? 'hc' : m));
  if (b) b.click(); else (document.querySelector('[data-mode]') || document.documentElement).setAttribute('data-mode', m); }, m);
const state = p => p.evaluate(() => { const c = document.documentElement.classList;
  return { vfx: c.contains('wz-vfx'), light: c.contains('wz-lightbg'), zoomed: c.contains('wz-zoomed') }; });
const addStyle = (p, css) => p.evaluate(css => { const s = document.createElement('style'); s.className = 'k410-probe';
  s.textContent = css; document.head.appendChild(s); }, css);
const dropStyles = p => p.evaluate(() => document.querySelectorAll('style.k410-probe').forEach(s => s.remove()));
const shot = async p => PNG.sync.read(await p.screenshot({ animations: 'disabled' }));

async function camAt(p, x, y, tap = false) {
  if (tap) await p.touchscreen.tap(x, y); else await p.mouse.move(x, y, { steps: 5 });
  await p.waitForTimeout(650);                             // the pan eases over --wz-pan-ease (260ms)
  return p.evaluate(() => {
    const H = document.documentElement, st = document.querySelector('.wz-stage'), fr = document.querySelector('.wz-frame');
    const sl = document.querySelector('.wz-soft-l'), sr = document.querySelector('.wz-soft-r');
    const stp = document.querySelector('.wz-soft-t'), sbt = document.querySelector('.wz-soft-b');
    const m = new DOMMatrix(getComputedStyle(st).transform === 'none' ? undefined : getComputedStyle(st).transform);
    const f = getComputedStyle(fr), r = st.getBoundingClientRect(), W = H.clientWidth;
    const lipX = parseFloat(f.borderLeftWidth), lipY = parseFloat(f.borderTopWidth);
    return { tx: +m.e.toFixed(2), ty: +m.f.toFixed(2), lipX: +lipX.toFixed(2), lipY: +lipY.toFixed(2),
      pan: getComputedStyle(H).getPropertyValue('--wz-pan').trim(),
      // what neither the stage nor the lip covers: the stage's edge pulled inside the lip's inner edge
      gapL: +Math.max(0, r.left - lipX).toFixed(2), gapR: +Math.max(0, (W - lipX) - r.right).toFixed(2),
      sl: sl ? +(+getComputedStyle(sl).opacity).toFixed(3) : null, sr: sr ? +(+getComputedStyle(sr).opacity).toFixed(3) : null,
      st: stp ? +(+getComputedStyle(stp).opacity).toFixed(3) : null, sb: sbt ? +(+getComputedStyle(sbt).opacity).toFixed(3) : null,
      softW: sl ? Math.round(sl.getBoundingClientRect().width) : null,
      blur: sl ? getComputedStyle(sl).backdropFilter : null };
  });
}

// ---- pixels --------------------------------------------------------------------------------------------
const luma = (d, i) => 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2];
function region(img, x0, y0, x1, y1) { return { x0: Math.max(0, x0 | 0), y0: Math.max(0, y0 | 0),
  x1: Math.min(img.width, x1 | 0), y1: Math.min(img.height, y1 | 0) }; }
function diff(a, b, R) {                              // section 11: amplitude AND area, never one alone
  let amp = 0, moved = 0, vis = 0, n = 0;
  for (let y = R.y0; y < R.y1; y++) for (let x = R.x0; x < R.x1; x++) {
    const i = (y * a.width + x) * 4;
    const d = Math.max(Math.abs(a.data[i] - b.data[i]), Math.abs(a.data[i + 1] - b.data[i + 1]), Math.abs(a.data[i + 2] - b.data[i + 2]));
    n++; if (d > amp) amp = d; if (d > 0) moved++; if (d > 8) vis++;
  }
  return { amp, moved: +(100 * moved / n).toFixed(2), visible: +(100 * vis / n).toFixed(2) };
}
function sharp(img, R) {                              // mean |grad L|: what a blur removes, whatever the mean does
  let s = 0, n = 0;
  for (let y = R.y0; y < R.y1 - 1; y++) for (let x = R.x0; x < R.x1 - 1; x++) {
    const i = (y * img.width + x) * 4, L = luma(img.data, i);
    s += Math.abs(luma(img.data, i + 4) - L) + Math.abs(luma(img.data, i + img.width * 4) - L); n++;
  }
  return s / n;
}
function meanL(img, R) { let s = 0, n = 0;
  for (let y = R.y0; y < R.y1; y++) for (let x = R.x0; x < R.x1; x++) { s += luma(img.data, (y * img.width + x) * 4); n++; }
  return s / n; }
function save(img, name) { if (SHOTS) writeFileSync(`${SHOTS}/${name}.png`, PNG.sync.write(img)); }

// ---- depth ---------------------------------------------------------------------------------------------
async function depth(rec) {
  const b = await chromium.launch({ channel: 'chromium', args: ARGS[GPU] });
  rec.depth = { engine: b.version(), gpu: GPU, pages: {} };
  for (const url of DEPTH_PAGES) {
    const { ctx, p, errs } = await open(b, url);
    const out = { state: await state(p) };
    await addStyle(p, '.wz-focus{display:none!important}');   // the clearing follows the pointer; hold it out of every diff
    const W = 1440, H = 900;
    out.camLeft = await camAt(p, 1, H / 2);
    out.camRight = await camAt(p, W - 2, H / 2);
    out.travel = +(out.camLeft.tx - out.camRight.tx).toFixed(2);
    // the far-side blur, pointer at the right edge so the LEFT strip is the treated side
    const A = await shot(p);
    await addStyle(p, '.wz-soft-l,.wz-soft-r{visibility:hidden!important}');
    const B = await shot(p);
    const sw = out.camRight.softW || Math.round(W * 0.34);
    const L = region(A, 0, 0, sw, H), Rr = region(A, W - sw, 0, W, H);
    out.blur = { computed: out.camRight.blur, treated: diff(A, B, L), untreated: diff(A, B, Rr),
      keptTreated: +(100 * sharp(A, L) / sharp(B, L)).toFixed(1), keptUntreated: +(100 * sharp(A, Rr) / sharp(B, Rr)).toFixed(1),
      // the blur's reach into the reading column: sharpness kept in 60px bands from the edge inward
      bands: [0, 60, 120, 180, 240, 300, 360, 420].filter(x => x < sw).map(x => { const G = region(A, x, 0, x + 60, H);
        return [x, +(100 * sharp(A, G) / sharp(B, G)).toFixed(1)]; }) };
    save(A, `${url.replace(/\W+/g, '_')}_blur_on`); save(B, `${url.replace(/\W+/g, '_')}_blur_off`);
    await dropStyles(p);
    // the vertical far side (K410): pointer at the bottom, centred, so the TOP strip is the treated side
    await addStyle(p, '.wz-focus{display:none!important}');
    out.camBottom = await camAt(p, W / 2, H - 2);
    const hasT = await p.evaluate(() => !!document.querySelector('.wz-soft-t'));
    if (hasT) {
      const VA = await shot(p);
      await addStyle(p, '.wz-soft-l,.wz-soft-r,.wz-soft-t,.wz-soft-b{visibility:hidden!important}');
      const VB = await shot(p);
      const sh = await p.evaluate(() => Math.round(document.querySelector('.wz-soft-t').getBoundingClientRect().height));
      const T = region(VA, 0, 0, W, sh), Bm = region(VA, 0, H - sh, W, H);
      out.blurV = { strip: sh, st: await p.evaluate(() => +getComputedStyle(document.querySelector('.wz-soft-t')).opacity),
        treated: diff(VA, VB, T), untreated: diff(VA, VB, Bm),
        bands: [0, 50, 100, 150, 200, 250].filter(y => y < sh).map(y => { const G = region(VA, 0, y, W, y + 50);
          return [y, +(100 * sharp(VA, G) / sharp(VB, G)).toFixed(1)]; }) };
      save(VA, `${url.replace(/\W+/g, '_')}_blurV_on`); save(VB, `${url.replace(/\W+/g, '_')}_blurV_off`);
    } else out.blurV = 'no vertical strips in this layer';
    await dropStyles(p);
    await addStyle(p, '.wz-focus{display:none!important}');
    // the vignette, camera at rest
    out.camRest = await camAt(p, W / 2, H * 0.45);
    await addStyle(p, '.wz-soft-l,.wz-soft-r{visibility:hidden!important}');
    const V1 = await shot(p);
    await addStyle(p, '.wz-vig{visibility:hidden!important}');
    const V0 = await shot(p);
    const lx = out.camRest.lipX, ly = out.camRest.lipY, band = await p.evaluate(() => parseFloat(getComputedStyle(document.querySelector('.wz-frame')).borderBottomWidth));
    const C = region(V1, W / 2 - 100, H * 0.45 - 100, W / 2 + 100, H * 0.45 + 100);
    const corners = [region(V1, lx + 8, ly + 8, lx + 168, ly + 168), region(V1, W - lx - 168, ly + 8, W - lx - 8, ly + 168),
                     region(V1, lx + 8, H - band - 168, lx + 168, H - band - 8), region(V1, W - lx - 168, H - band - 168, W - lx - 8, H - band - 8)];
    const cm = img => corners.reduce((s, R) => s + meanL(img, R), 0) / corners.length;
    out.vignette = { centreOn: +meanL(V1, C).toFixed(2), centreOff: +meanL(V0, C).toFixed(2), cornerOn: +cm(V1).toFixed(2), cornerOff: +cm(V0).toFixed(2) };
    out.vignette.cornerStops = +Math.abs(Math.log2(out.vignette.cornerOn / out.vignette.cornerOff)).toFixed(3);
    out.vignette.ratioOn = +(out.vignette.centreOn / out.vignette.cornerOn).toFixed(3);
    out.vignette.ratioOff = +(out.vignette.centreOff / out.vignette.cornerOff).toFixed(3);
    out.errors = errs;
    rec.depth.pages[url] = out;
    await ctx.close();
  }
  // a phone: no hover, but a tap synthesises one mousemove at the tap point, and the camera listens to that
  for (const url of DEPTH_PAGES) {
    const { ctx, p } = await open(b, url, { w: 390, h: 844, touch: true });
    const s = await state(p);
    rec.depth.pages[url].phoneTapRight = { state: s, ...(await camAt(p, 386, 300, true)) };
    await ctx.close();
  }
  // reduced motion stops the camera and the strips
  { const { ctx, p } = await open(b, '/right-to-die/combined', { reduced: 'reduce' });
    rec.depth.reducedMotion = await camAt(p, 1438, 450); await ctx.close(); }
  await b.close();
}

// ---- frames --------------------------------------------------------------------------------------------
async function frames(rec) {
  const b = await chromium.launch({ channel: 'chromium', args: ARGS[GPU] });
  rec.frames = { engine: b.version(), gpu: GPU, pages: {} };
  const run = p => p.evaluate(async () => {
    scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
    const t = [];
    await new Promise(res => { let k = 0; const f = ts => { t.push(ts); scrollBy(0, 12); if (++k < 181) requestAnimationFrame(f); else res(); };
      requestAnimationFrame(f); });
    const d = t.slice(1).map((v, i) => v - t[i]).sort((a, b) => a - b), q = x => d[Math.min(d.length - 1, Math.floor(x * d.length))];
    return { med: +q(.5).toFixed(2), p95: +q(.95).toFixed(2), max: +d[d.length - 1].toFixed(2),
             over20: d.filter(v => v > 20).length, over34: d.filter(v => v > 34).length, n: d.length };
  });
  for (const url of DEPTH_PAGES) {
    const { ctx, p } = await open(b, url);
    const out = { state: await state(p), cam: await camAt(p, 1438, 450), lit: [], corner: [], hidden: [] };
    for (let k = 0; k < 3; k++) out.lit.push(await run(p));
    out.camCorner = await camAt(p, 1438, 895);          // bottom-right: the left AND the top strip lit
    for (let k = 0; k < 3; k++) out.corner.push(await run(p));
    await addStyle(p, '.wz-soft-l,.wz-soft-r,.wz-soft-t,.wz-soft-b{visibility:hidden!important}');
    for (let k = 0; k < 3; k++) out.hidden.push(await run(p));
    rec.frames.pages[url] = out;
    await ctx.close();
  }
  await b.close();
}

// ---- fb ------------------------------------------------------------------------------------------------
const FB = () => {
  const cards = [...document.querySelectorAll('article.obj[data-wz-fb], .objection-header[data-wz-fb]')], hits = [];
  for (const c of cards) {
    const fb = c.querySelector('.wz-fb'); if (!fb) continue;
    const r = fb.getBoundingClientRect(); if (!r.width) continue;
    const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT); let n, hit = null;
    while (!hit && (n = w.nextNode())) {
      if (!n.textContent.trim() || fb.contains(n)) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const q of rg.getClientRects()) if (q.width > 0.5 && q.left < r.right - 0.5 && q.right > r.left + 0.5 &&
        q.top < r.bottom - 0.5 && q.bottom > r.top + 0.5) { hit = { card: c.id, in: n.parentElement.className ? String(n.parentElement.className).slice(0, 30) : n.parentElement.tagName, text: n.textContent.trim().slice(0, 36) }; break; }
    }
    if (hit) hits.push(hit);
  }
  // overflow = can the reader actually scroll sideways; scrollWidth also counts the camera's own offset,
  // which overflow-x:clip hides, so it is the wrong reading
  const se = document.scrollingElement; se.scrollLeft = 1e6; const overflow = se.scrollLeft; se.scrollLeft = 0;
  return { cards: cards.length, links: document.querySelectorAll('.wz-fb').length, hit: hits.length, sample: hits.slice(0, 2), overflow };
};
// THE CONTROL THAT MUST FAIL: take away the lane the layer reserves and put the link over the headline. A probe
// that still reads 0 here is not measuring overlap, and every 0 above it means nothing.
const FB_BREAK = '.obj[data-wz-fb] > .obj-meta{padding-right:0!important}' +
                 '.objection-header[data-wz-fb] > .wz-fb{top:auto!important;bottom:.2rem!important;right:auto!important;left:1rem!important}';
async function fb(rec) {
  // One load per page per engine, then every mode and width in place: the link is placed by CSS, so a resize
  // re-lays it out exactly as a fresh load would. The 390px standard run is repeated as a fresh load to prove it.
  rec.fb = { engines: {}, pages: {} };
  for (const [en, eng] of [['chromium', chromium], ['firefox', firefox]]) {
    const b = await eng.launch(); rec.fb.engines[en] = b.version();
    for (const url of PAGES) {
      const P = rec.fb.pages[url] ||= { runs: 0, hitRuns: 0, overflowRuns: 0, grounds: {}, detail: [] };
      const { ctx, p, errs } = await open(b, url);
      for (const mode of MODES) {
        await setMode(p, mode);
        for (const w of WIDTHS) {
          await p.setViewportSize({ width: w, height: w <= 600 ? 844 : 900 });
          await p.mouse.move(w / 2, 300); await p.waitForTimeout(400);   // camera at rest before any reading
          const s = await state(p), r = await p.evaluate(FB);
          P.runs++; P.hitRuns += r.hit > 0; P.overflowRuns += r.overflow > 0; P.grounds[mode] = s.light ? 'light' : 'dark';
          P.cards = Math.max(P.cards || 0, r.cards); P.links = Math.max(P.links || 0, r.links);
          if (r.hit || r.overflow > 0) P.detail.push({ en, mode, w, ...r });
          if (mode === 'standard' && w === 390) P[`inPlace390_${en}`] = r.hit;
        }
      }
      P.errors = [...new Set(errs)].slice(0, 3);
      await ctx.close();
      const f = await open(b, url, { w: 390, h: 844 }); P[`fresh390_${en}`] = (await f.p.evaluate(FB)).hit;
      if (P.cards) { await addStyle(f.p, FB_BREAK); await f.p.waitForTimeout(150);
        const c = (await f.p.evaluate(FB)).hit; P[`control390_${en}`] = c; if (!c) rec.fb.controlFailed = true; }
      await f.ctx.close();
    }
    await b.close();
  }
  for (const P of Object.values(rec.fb.pages)) P.detail = P.detail.slice(0, 12);
}

// ---- tilt (K410) -----------------------------------------------------------------------------------------
// The chin's tilt toggle, where the layer has one: the lean happens and is not inert (section 11), the far
// edge foreshortens, it settles flat at rest with text exactly as sharp as with the toggle off, scroll and
// the magnifier flatten it, a phone and reduced motion never get it, the chin row does not overlap and is
// exposed to assistive technology, and what a lean costs per frame.
async function tilt(rec) {
  const b = await chromium.launch({ channel: 'chromium', args: ARGS[GPU] });
  rec.tilt = { engine: b.version(), gpu: GPU, pages: {} };
  const flatCSS = 'html.wz-tilting .wz-stage{transform:translate3d(var(--wz-px,0px),var(--wz-py,0px),0) scale(var(--wz-zoom,1))!important}';
  const mx = p => p.evaluate(() => { const s = document.querySelector('.wz-stage'), t = getComputedStyle(s).transform;
    return { is2D: t === 'none' || new DOMMatrix(t).is2D, tilting: document.documentElement.classList.contains('wz-tilting'),
             blur: getComputedStyle(document.querySelector('.wz-soft-l')).backdropFilter }; });
  for (const url of DEPTH_PAGES) {
    const { ctx, p, errs } = await open(b, url);
    const out = {};
    out.hasToggle = await p.evaluate(() => !!document.querySelector('.wz-tilt'));
    if (!out.hasToggle) { rec.tilt.pages[url] = { hasToggle: false }; await ctx.close(); continue; }
    await addStyle(p, '.wz-focus{display:none!important}');
    out.off = { pressed: await p.getAttribute('.wz-tilt', 'aria-pressed'), ...(await mx(p)) };
    await p.mouse.move(1400, 450, { steps: 6 }); await p.waitForTimeout(3300);
    const offImg = await shot(p);                                   // toggle off, pointer right, settled
    await p.click('.wz-tilt'); await p.waitForTimeout(300);
    out.on = { pressed: await p.getAttribute('.wz-tilt', 'aria-pressed'), stored: await p.evaluate(() => localStorage.getItem('wz-tilt')), ...(await mx(p)) };
    // lean: move to the right edge, measure inside the idle window
    await p.mouse.move(1100, 450, { steps: 4 }); await p.mouse.move(1400, 450, { steps: 6 }); await p.waitForTimeout(650);
    out.leaning = await mx(p);
    out.foreshortening = await p.evaluate(() => { const s = document.querySelector('.wz-stage'), M = new DOMMatrix(getComputedStyle(s).transform);
      const W = document.documentElement.clientWidth, oy = scrollY + innerHeight / 2 - s.offsetTop, P = (x, y) => { const q = M.transformPoint(new DOMPoint(x, y, 0, 1)); return [q.x / q.w, q.y / q.w]; };
      const hl = P(0, oy + 400)[1] - P(0, oy - 400)[1], hr = P(W, oy + 400)[1] - P(W, oy - 400)[1];
      return { leftEdge: +(hl / 800).toFixed(4), rightEdge: +(hr / 800).toFixed(4) }; });
    const lean = await shot(p);
    await addStyle(p, flatCSS); const flatSame = await shot(p);   // same moment, lean suppressed
    await dropStyles(p); await addStyle(p, '.wz-focus{display:none!important}');
    out.leanDiff = diff(lean, flatSame, region(lean, 0, 0, lean.width, lean.height));
    save(lean, `${url.replace(/\W+/g, '_')}_tilt_lean`);
    // settle: no move for longer than the idle interval
    await p.waitForTimeout(3300);
    out.settled = await mx(p);
    const onImg = await shot(p);
    const C = region(onImg, 560, 250, 880, 650);
    out.restSharpness = +(100 * sharp(onImg, C) / sharp(offImg, C)).toFixed(2);   // toggle on at rest vs toggle off
    // scroll flattens at once
    await p.mouse.move(1380, 450, { steps: 3 }); await p.waitForTimeout(150);
    const before = await mx(p);
    await p.mouse.wheel(0, 300); await p.waitForTimeout(120);
    out.scroll = { leaningBefore: before.tilting, leaningAfter: (await mx(p)).tilting };
    // the magnifier: no lean while zoomed
    await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(200);
    await p.click('.wz-mag'); await p.waitForTimeout(400);
    await p.mouse.move(1200, 450, { steps: 4 }); await p.waitForTimeout(300);
    out.zoomed = await mx(p);
    await p.keyboard.press('Escape'); await p.waitForTimeout(300);
    // persistence across a reload
    await p.reload({ waitUntil: 'load' }); await p.waitForTimeout(900);
    out.afterReload = { pressed: await p.getAttribute('.wz-tilt', 'aria-pressed'), on: await p.evaluate(() => document.documentElement.classList.contains('wz-tilt-on')) };
    // the chin: exposed, and no two controls sharing a point
    out.chin = await p.evaluate(() => { const c = document.querySelector('.wz-chin'), bs = [...c.querySelectorAll('button')].filter(x => getComputedStyle(x).display !== 'none');
      const rs = bs.map(x => x.getBoundingClientRect()), hit = bs.map((x, k) => document.elementFromPoint(rs[k].left + rs[k].width / 2, rs[k].top + rs[k].height / 2) === x);
      let overlap = 0; for (let a = 0; a < rs.length; a++) for (let z = a + 1; z < rs.length; z++) if (rs[a].left < rs[z].right && rs[z].left < rs[a].right && rs[a].top < rs[z].bottom && rs[z].top < rs[a].bottom) overlap++;
      const mk = c.querySelector('.wz-mark'), mr = mk && getComputedStyle(mk).display !== 'none' ? mk.getBoundingClientRect() : null, tr = c.querySelector('.wz-tilt').getBoundingClientRect();
      return { chinHidden: c.getAttribute('aria-hidden'), exposed: bs.filter(x => !x.closest('[aria-hidden="true"]')).map(x => x.className), hitOwnCentre: hit.every(Boolean),
               overlaps: overlap, markHidden: mk && mk.getAttribute('aria-hidden'), markClear: !mr || mr.right <= tr.left }; });
    out.errors = errs;
    rec.tilt.pages[url] = out;
    await ctx.close();
  }
  // where the toggle must not appear: a phone, reduced motion, a narrow window; and where it must (just above)
  const vis = async (o, w, h) => { const { ctx, p } = await open(b, '/right-to-die/combined', { w, h, ...o });
    const r = await p.evaluate(() => { const t = document.querySelector('.wz-tilt'); return t ? getComputedStyle(t).display : 'absent'; }); await ctx.close(); return r; };
  rec.tilt.visibility = { phone390: await vis({ touch: true }, 390, 844), reducedMotion: await vis({ reduced: 'reduce' }, 1440, 900),
    narrow760: await vis({}, 760, 900), wide800: await vis({}, 800, 900), desktop1440: await vis({}, 1440, 900) };
  // the wordmark against the row, every 20px from 780 to 1000 (the mark is centred and scales with vw)
  { const { ctx, p } = await open(b, '/right-to-die/combined'); const clash = [];
    for (let w = 780; w <= 1000; w += 20) { await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(120);
      const r = await p.evaluate(() => { const mk = document.querySelector('.wz-chin .wz-mark'), t = document.querySelector('.wz-tilt');
        if (!mk || getComputedStyle(t).display === 'none') return null; const a = mk.getBoundingClientRect(), z = t.getBoundingClientRect(); return +(z.left - a.right).toFixed(1); });
      clash.push([w, r]); }
    rec.tilt.markToToggleGap = clash; await ctx.close(); }
  // frames while leaning: a continuous pointer sweep with the recorder running, toggle off against on
  const sweep = p => p.evaluate(() => new Promise(res => { const t = []; let k = 0;
    const f = ts => { t.push(ts); if (++k < 121) requestAnimationFrame(f); else { const d = t.slice(1).map((v, i) => v - t[i]).sort((a, b) => a - b), q = x => d[Math.floor(x * d.length)];
      res({ med: +q(.5).toFixed(2), p95: +q(.95).toFixed(2), max: +d[d.length - 1].toFixed(2), over20: d.filter(v => v > 20).length }); } };
    requestAnimationFrame(f); }));
  rec.tilt.frames = {};
  for (const [label, on] of [['toggleOff', false], ['toggleOn', true]]) {
    const { ctx, p } = await open(b, '/combined');
    if (on) await p.click('.wz-tilt');
    const runs = [];
    for (let k = 0; k < 3; k++) {
      await p.mouse.move(200, 300);
      const [r] = await Promise.all([sweep(p), p.mouse.move(1400, 700, { steps: 120 })]);
      runs.push(r);
    }
    rec.tilt.frames[label] = runs; await ctx.close();
  }
  await b.close();
}

const rec = { base: BASE, layer: LAYER || 'live', when: new Date().toISOString() };
for (const s of SECTIONS) await ({ depth, frames, fb, tilt })[s](rec);
console.log(JSON.stringify(rec, null, 1));
