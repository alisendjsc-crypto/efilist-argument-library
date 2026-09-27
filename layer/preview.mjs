// preview.mjs -- try a candidate layer on the live library pages, in a real Chrome window, deploying nothing.
//
//   PLAYWRIGHT=<.../node_modules/playwright/index.mjs> LAYER=<candidate site/ dir> node layer/preview.mjs [path ...]
//
// Opens two windows per path (default /combined and /right-to-die/combined): one with the live layer, titled
// "LIVE ·", and one with wuld-layer.css/.js served from LAYER, titled "CANDIDATE ·". Both load the live page;
// only the two layer files differ. A fresh profile, so the display tier starts at vfx; the walkthroughs and
// the first-visit hint are held back so the page is what shows. Close the windows, or Ctrl-C, to end.
const { chromium } = await import(process.env.PLAYWRIGHT || 'playwright');
const LAYER = process.env.LAYER;
if (!LAYER) { console.error('LAYER=<dir holding wuld-layer.css and wuld-layer.js> is required'); process.exit(2); }
const BASE = process.env.BASE || 'https://library.wuld.ink';
const PATHS = process.argv.slice(2).length ? process.argv.slice(2) : ['/combined', '/right-to-die/combined'];
const SMOKE = !!process.env.SMOKE;           // SMOKE=1: headless; print each window's title and which layer it got; exit
const b = await chromium.launch({ channel: 'chromium', headless: SMOKE, args: ['--window-size=1440,960'] });
const pages = [];
for (const [label, swap] of [['LIVE', false], ['CANDIDATE', true]]) {
  const ctx = await b.newContext({ viewport: null });
  if (swap) for (const f of ['wuld-layer.css', 'wuld-layer.js'])
    await ctx.route(u => u.pathname === '/' + f, r => r.fulfill({ path: LAYER + '/' + f, headers: { 'cache-control': 'no-store' },
      contentType: f.endsWith('.css') ? 'text/css; charset=utf-8' : 'application/javascript; charset=utf-8' }));
  await ctx.addInitScript(label => { try {
    const g = Storage.prototype.getItem;
    Storage.prototype.getItem = function (k) { return (typeof k === 'string' && k.indexOf('wz-tour:') === 0) ? '1' : g.call(this, k); };
    sessionStorage.setItem('wz-hint-seen', '1'); } catch (e) {}
    addEventListener('load', () => { document.title = label + ' · ' + document.title; }); }, label);
  for (const path of PATHS) { const p = await ctx.newPage(); await p.goto(BASE + path); pages.push(p); }
}
if (SMOKE) {
  for (const p of pages) { await p.waitForLoadState('load'); await p.waitForTimeout(500);
    console.log(await p.title(), '|', await p.evaluate(async () => { const t = await (await fetch('/wuld-layer.css', { cache: 'no-store' })).text();
      return t.length + ' B css, blur token ' + (t.includes('--wz-soft-blur:') ? 'declared' : 'absent'); })); }
  await b.close(); process.exit(0);
}
console.log('open: %d windows. Close them all, or Ctrl-C, to end.', pages.length);
await Promise.all(pages.map(p => p.waitForEvent('close', { timeout: 0 }).catch(() => {})));
await b.close();
