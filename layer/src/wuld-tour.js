/* wuld-tour.js -- per-view walkthroughs. One feature at a time, everything else darkened.
 *
 * ONE TOUR PER VIEW, NOT ONE PER PAGE. The flagship is five surfaces behind one URL -- the library,
 * the mechanism web, the dependency graph, the argument flow map and the real-world examples -- and
 * a reader who opens the dependency graph for the first time three weeks after their first visit
 * has had no introduction to it at all. Each view therefore carries its own short tour and its own
 * once-ever flag, fired when that view is ACTIVATED rather than when the page loads.
 *
 * THREE STEPS EACH, except the library's six. A tour is a tax on the reader's attention and the
 * only honest justification for it is that the thing genuinely is not self-evident. The last step
 * of every view tour is its METHODOLOGY button, because that is the affordance readers most often
 * never find and the one that most changes how the view should be read.
 *
 * ALWAYS SKIPPABLE: Skip, Escape, and clicking anywhere off the card, at every step. Never runs
 * under prefers-reduced-motion. The chin's ? button re-opens the tour for whatever view you are
 * looking at, seen or not.
 *
 * THE COPY BELOW IS A DRAFT. Edit the `text` strings freely; nothing else reads them. */
(function () {
  var H = document.documentElement;
  var PREFIX = 'wz-tour:';

  function vis(e) { return !!(e && e.getClientRects().length); }
  function q(s) { return document.querySelector(s); }

  /* Views are resolved most-specific first: `library` is the fallback, so it must be last or it
     would answer for every page that has a card on it -- including the graph views, which sit
     inside the same library section. */
  var TOURS = [
    /* THE GRAPH-VIEW COPY BELOW IS SOURCE-GATED, LIKE THE PRECIS. It describes the operator's own
       apparatus, and the first draft got three things wrong that no test noticed: it said to click
       an EDGE on the mechanism web (nodes are what is clickable -- 117 with pointer cursors, 142
       lines with none), described that web's edges as relations between mechanisms (they join an
       objection to a mechanism), and called the dependency graph's weak edges "low-confidence"
       (weak means the response would survive the premise's removal; confidence is what the REVIEW
       and PROVISIONAL badges mark). tourcopy_gate.py now holds a source sentence for every claim
       in these steps and fails on any it cannot find verbatim in the panel. */
    { key: 'map', name: 'the mechanism web',
      when: function () { return vis(q('#map-view')); },
      steps: [
        { sel: '#map-graph',
          text: 'The mechanism web. Two kinds of node \u2014 objections, and the psychological mechanisms that generate them \u2014 with an edge wherever an objection runs on a mechanism. It answers why an interlocutor says a thing, not what they said. Click a node to see everything it connects to.' },
        { sel: '#map-view .map-toolbar button:not(.map-methodology-btn)|union',
          text: 'Legend explains the node types; Reset puts the layout back where it started, which is worth knowing before you drag anything. Bigger mechanism nodes are more common patterns.' },
        { sel: '.map-methodology-btn',
          text: 'Methodology. Why this map exists, the five mechanism types and what each one wants as a response, and how the assignments were derived.' }
      ] },
    { key: 'dep', name: 'the dependency graph',
      when: function () { return vis(q('#dep-view')); },
      steps: [
        { sel: '#dep-graph',
          text: 'The dependency graph. An edge joins a premise to an objection whose response invokes it. Solid means load-bearing \u2014 remove the premise and the response collapses; dashed means the response would survive without it.' },
        { sel: '#dep-view .map-toolbar button:not(.dep-methodology-btn)|union',
          text: 'Toggle weak hides the dashed edges, which is the fastest way to see the structure that is actually carrying the argument.' },
        { sel: '.dep-methodology-btn',
          text: 'Methodology. Which premises are foundational and which are diagnostic, the test that decides strong from weak, and where the graph is still marked provisional.' }
      ] },
    { key: 'map1', name: 'the argument flow map',
      when: function () { return vis(q('#map1-view')); },
      steps: [
        { sel: '#m1-graph',
          text: 'The argument flow map. Given the objection just made and your response to it, which objection is most likely to come next \u2014 the library as a move tree rather than a dictionary.' },
        { sel: '#m1btn-blended,#m1btn-sophisticate,#m1btn-defender,#m1btn-drifter|union',
          text: 'Three interlocutor models and a blend. The sophisticate attacks the premise your response invoked, the defender retreats within the same mechanism, the drifter moves one tier at a time. Most edges appear in only one of them \u2014 the disagreement is the signal.' },
        { sel: '.m1-methodology-btn',
          text: 'Methodology. How the three matrices are generated, what the weights are and are not, and which edges were applied without independent validation.' }
      ] },
    { key: 'examples', name: 'the examples view',
      when: function () { return vis(q('#combined-rwe')) && !vis(q('#map-view')) && !vis(q('#dep-view')) && !vis(q('#map1-view')); },
      steps: [
        { sel: '#view-tabs',
          text: 'Real-world examples \u2014 things people actually said \u2014 grouped three ways: by the objection they instantiate, by who said it, or by the archetype they fit.' },
        { sel: '.filter-bar',
          text: 'Filters narrow by polarity, archetype and speaker type. Reset clears them all at once.' },
        { sel: '#sidebar',
          text: 'The left column narrows the instances shown on the right; every instance arrives with its source.' }
      ] },
    { key: 'library', name: 'this page',
      /* The wings and the flagship are different markup for the same idea: the wings render
         `article.obj` cards, the flagship renders `.objection-header` rows into #results. Steps
         below are written for both and resolve() drops whichever set is not on this page, so the
         wings land on six and the flagship on seven without either being a special case. Visibility
         matters here, not mere presence: on the flagship the cards stay in the DOM while a graph
         view is showing, and this is the fallback tour checked last. */
      when: function () { return vis(q('article.obj, .lib-card, .objection-header[id^="obj-"]')); },
      steps: [
        { sel: '.wz-power',
          text: 'Screen effects. This steps the whole layer down — full effects, then colour and type only, then nothing at all. It remembers what you chose.' },
        { sel: '.wz-mag',
          text: 'Magnifier. Hold Shift and scroll to zoom anywhere on the page, or press this and zoom with a plain wheel. Zoomed in, the pointer is the camera: move it toward an edge and what lies past that edge comes in. Escape returns to 1×.' },
        { sel: '.wz-mute',
          text: 'Sound. A quiet mechanical room tone and small cues, only while effects are on. This switches it off and keeps it off.' },
        { sel: '#mode-standard,#mode-legible,#mode-hc,#mode-both|union',
          text: 'Reading modes. Legible changes the type for longer reading, High contrast changes the ground, and the two combine. Your choice is remembered.' },
        { sel: '.view-switcher',
          text: 'Four views of the same corpus \u2014 the library, the mechanism web, the dependency graph and the argument flow map. Each has its own short tour the first time you open it.' },
        { sel: 'article.obj',
          text: 'Every objection is a card: the claim as people actually put it, the words they use for it, a diagnosis of where it goes wrong, and the full response behind [+].' },
        { sel: '.objection-header',
          text: 'Every objection is a row: its tier, the register it belongs to, and the claim as people actually put it. Click one to open the response underneath it.' },
        { sel: '.rsi-methodology-btn',
          text: 'RSI methodology. How every response here was graded, what the five inputs are, and what a grade is not claiming.' },
        { sel: '.wz-fb',
          text: 'Something wrong, or missing? Feedback opens a short form that already names the card — a message, an address only if you want a reply, or a mail draft if you would rather write.' }
      ] }
  ];

  var live = [], idx = 0, mask = [], ring, card, body, dots, prevFocus, open = false, current = null, placeGen = 0;

  function reduced() { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
  function seen(k) { try { return localStorage.getItem(PREFIX + k) === '1'; } catch (e) { return true; } }
  function mark(k) { try { localStorage.setItem(PREFIX + k, '1'); } catch (e) {} }

  /* ONE FLAG PER TOUR, NOT PER TOUR NAME. The library tour is one entry above but three tours in
     practice: the flagship's rows (seven steps), a wing's cards (six) and the index's list (four).
     Until 2026-09-12 all three spent the same flag, so a reader who had seen a wing's tour was
     never shown the flagship's -- the once-ever key was per origin, and the origin has eleven
     surfaces. The surface is read from markup that is in the static HTML, so the answer is the
     same at parse time and after the cards render: .view-switcher exists only on /combined,
     .lib-card only on the index. The wings keep the old name; nobody who has seen a wing's tour is
     shown it again by this change. */
  function surface() {
    if (q('.view-switcher')) return 'flagship';
    if (q('.lib-card')) return 'index';
    return 'wing';
  }
  function keyOf(tour) {
    if (!tour) return '';
    if (tour.key !== 'library') return tour.key;
    var s = surface();
    return s === 'wing' ? 'library' : 'library:' + s;
  }

  function activeTour() {
    for (var i = 0; i < TOURS.length; i++) { if (TOURS[i].when()) return TOURS[i]; }
    return null;
  }

  /* "a,b,c|union" spotlights the box containing all matches; a plain selector spotlights one. A step
     whose target is not on this page is not a step -- resolving per view rather than assuming keeps
     an empty spotlight pointing at nothing from ever being drawn. */
  function resolve(tour) {
    var out = [];
    for (var i = 0; i < tour.steps.length; i++) {
      var sel = tour.steps[i].sel, uni = false;
      if (sel.slice(-6) === '|union') { sel = sel.slice(0, -6); uni = true; }
      var els = uni ? [].slice.call(document.querySelectorAll(sel)) : [q(sel)];
      els = els.filter(vis);
      if (els.length) out.push({ els: els, text: tour.steps[i].text });
    }
    return out;
  }

  function build() {
    /* FOUR PANELS AROUND THE TARGET, not one overlay with a hole. The single-element version used a
       huge box-shadow spread and then had to raise the spotlit element above it -- which, for a chin
       button, meant raising the whole chin, leaving the row undarkened and the ring stranded behind
       it. Panels cover everything EXCEPT the target, so nothing is covered and no z-index of anyone
       else's has to be touched. */
    for (var m = 0; m < 4; m++) {
      var d = document.createElement('div');
      d.className = 'wz-tour-mask'; d.setAttribute('aria-hidden', 'true');
      document.body.appendChild(d); mask.push(d);
    }
    ring = document.createElement('div');
    ring.className = 'wz-tour-ring'; ring.setAttribute('aria-hidden', 'true');
    document.body.appendChild(ring);

    card = document.createElement('div');
    card.className = 'wz-tour-card';
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-modal', 'true');
    body = document.createElement('p'); body.className = 'wz-tour-text';
    dots = document.createElement('span'); dots.className = 'wz-tour-dots';
    var nav = document.createElement('div'); nav.className = 'wz-tour-nav';
    var skip = mkbtn('Skip', 'Skip the tour', function () { finish(); }); skip.className = 'wz-tour-skip';
    var prev = mkbtn('←', 'Previous', function () { go(idx - 1); });
    var next = mkbtn('→', 'Next', function () { go(idx + 1); });
    nav.appendChild(skip); nav.appendChild(dots); nav.appendChild(prev); nav.appendChild(next);
    card.appendChild(body); card.appendChild(nav);
    card._prev = prev; card._next = next;
    document.body.appendChild(card);
  }
  function mkbtn(label, aria, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.setAttribute('aria-label', aria);
    b.addEventListener('click', function (e) { e.stopPropagation(); fn(); });
    return b;
  }

  function unionRect(els) {
    var r = els[0].getBoundingClientRect();
    if (els.length === 1) return r;
    var t = r.top, l = r.left, bo = r.bottom, g = r.right;
    for (var i = 1; i < els.length; i++) {
      var z = els[i].getBoundingClientRect();
      t = Math.min(t, z.top); l = Math.min(l, z.left);
      bo = Math.max(bo, z.bottom); g = Math.max(g, z.right);
    }
    return { top: t, left: l, bottom: bo, right: g, width: g - l, height: bo - t };
  }

  function paint(els) {
    var r = unionRect(els), pad = 6;
    var x = r.left - pad, y = r.top - pad, w = r.width + pad * 2, h = r.height + pad * 2;
    var W = innerWidth, Hh = innerHeight;
    function set(e, a, b, c, d) {
      e.style.left = Math.max(0, a) + 'px'; e.style.top = Math.max(0, b) + 'px';
      e.style.width = Math.max(0, c) + 'px'; e.style.height = Math.max(0, d) + 'px';
    }
    set(mask[0], 0, 0, W, y);
    set(mask[1], 0, y + h, W, Hh - (y + h));
    set(mask[2], 0, y, x, h);
    set(mask[3], x + w, y, W - (x + w), h);
    set(ring, x, y, w, h);
    return [Math.round(r.top), Math.round(r.left), Math.round(r.width), Math.round(r.height)];
  }

  function place(els) {
    /* A TALL TARGET IS NOT CENTRED. A card or a graph can exceed the viewport, and block:'center'
       then puts its middle in the middle -- both ring edges off-screen, so the spotlight has no
       visible boundary at all. Showing the top of it is what a reader needs. */
    var tall = unionRect(els).height > innerHeight * 0.7;
    /* INSTANT SCROLL, DELIBERATELY. Smooth scrolling produced two different bugs in this function.
       First a rect read two frames after the call was a rect in flight, drawing a box that spanned
       two cards. The settle loop below fixed that -- and then smooth scroll's STARTUP latency
       (about two frames before anything moves) satisfied "stable for two frames" before the scroll
       had begun, so on the flagship the loop exited with the toolbar still at its pre-scroll
       position and the ring eased, via its own CSS transition, onto the view switcher 130px above.
       Frame-by-frame: loop out at 39ms, page still scrolling until 221ms. The wings passed by
       timing luck. A reader in a tour is watching the ring, not the page scroll; the ring's own
       0.2s transition carries the continuity, and an instant scroll has no latency to be fooled by. */
    els[0].scrollIntoView({ block: tall ? 'start' : 'center', behavior: 'auto' });

    /* STILL WAIT FOR LAYOUT TO SETTLE -- pages adjust themselves after a scroll (sticky headers,
       the flagship's own scroll handlers), so the rect is re-read until it stops moving. The
       MINIMUM time is the part that matters: no stability observed inside the first 150ms counts,
       because that is exactly the window in which a not-yet-started motion looks like rest. */
    /* ONE LOOP AT A TIME. Two quick arrow presses used to start two settle loops, each closing over
       its own target; both painted every frame and whichever happened to run last won -- so a fast
       reader could end a step with the ring on the previous step's target. Each call now takes a
       generation number and a loop that is no longer current stops painting. */
    var gen = ++placeGen;
    var stable = 0, last = null, t0 = performance.now();
    (function tick() {
      if (!open || gen !== placeGen) return;
      var now = paint(els);
      if (last && now[0] === last[0] && now[1] === last[1] && now[2] === last[2] && now[3] === last[3]) stable++;
      else stable = 0;
      last = now;
      var age = performance.now() - t0;
      if ((stable < 2 || age < 150) && age < 900) { requestAnimationFrame(tick); return; }
      var r = unionRect(els), cw = Math.min(340, innerWidth - 24);
      card.style.width = cw + 'px';
      var ch = card.offsetHeight || 120;
      var below = r.bottom + 18;
      var top = (below + ch < innerHeight - 12) ? below : Math.max(12, r.top - 18 - ch);
      card.style.top = Math.min(top, Math.max(12, innerHeight - ch - 12)) + 'px';
      card.style.left = Math.max(12, Math.min(r.left + r.width / 2 - cw / 2, innerWidth - cw - 12)) + 'px';
    })();
  }

  function go(n) {
    if (n < 0) return;
    if (n >= live.length) { finish(); return; }
    idx = n;
    body.textContent = live[idx].text;
    dots.textContent = (idx + 1) + ' / ' + live.length;
    card._prev.disabled = (idx === 0);
    card._next.textContent = (idx === live.length - 1) ? 'Done' : '→';
    card._next.setAttribute('aria-label', (idx === live.length - 1) ? 'Finish' : 'Next');
    place(live[idx].els);
  }

  function onKey(e) {
    if (!open) return;
    /* The tour is modal while it is open, so the keys it answers do not also reach the page --
       the flagship has its own Escape and arrow handling for the graphs, and a reader closing the
       tour should not also close a legend or nudge a graph. Capture-phase listener, so this runs
       before any page handler; stopPropagation is what keeps it from getting there. */
    if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); finish(); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); e.stopPropagation(); go(idx + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); e.stopPropagation(); go(idx - 1); }
    else if (e.key === 'Tab') {
      /* Focus stays inside the dialog. Without this a keyboard reader tabs straight out into a page
         that is visually blacked out, which is the worst of both. */
      var f = card.querySelectorAll('button:not([disabled])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  }
  function onDown(e) { if (open && !card.contains(e.target)) finish(); }

  function finish() {
    if (!open) return;
    open = false;
    if (current) mark(keyOf(current));
    current = null;
    H.classList.remove('wz-touring');
    removeEventListener('keydown', onKey, true);
    removeEventListener('pointerdown', onDown, true);
    removeEventListener('resize', onResize);
    mask.forEach(function (d) { if (d.parentNode) d.parentNode.removeChild(d); });
    mask = [];
    if (ring && ring.parentNode) ring.parentNode.removeChild(ring);
    if (card && card.parentNode) card.parentNode.removeChild(card);
    try { if (prevFocus && prevFocus.focus) prevFocus.focus(); } catch (e) {}
  }
  function onResize() { if (open && live[idx]) place(live[idx].els); }

  function start(tour) {
    if (open || !tour) return 0;
    live = resolve(tour);
    if (live.length < 2) return 0;          // one lonely spotlight is not a walkthrough
    current = tour;
    prevFocus = document.activeElement;
    build(); open = true;
    H.classList.add('wz-touring');
    addEventListener('keydown', onKey, true);
    addEventListener('pointerdown', onDown, true);
    addEventListener('resize', onResize);
    go(0);
    card._next.focus();
    return live.length;
  }

  /* A VIEW CHANGES ONLY WHEN SOMETHING IS CLICKED, so the check rides on clicks rather than on a
     standing observer over the whole document. The delay lets the view actually swap first. */
  var pending = null;
  function maybe() {
    if (open) return;
    var t = activeTour();
    if (t && !seen(keyOf(t))) start(t);
  }
  function onClickCheck() { clearTimeout(pending); pending = setTimeout(maybe, 420); }

  window.wzTour = function () { return start(activeTour()); };   // console entry point

  window.wzTourInit = function () {
    /* The ? button is not gated on anything: it is the way back in after a tour has been seen, and
       it runs the tour for whatever view is in front of you rather than offering a menu of five. */
    /* NO BUTTON WHERE THERE IS NOTHING TO SHOW. The chin exists on every page the layer touches,
       so /troubleshooting/ was getting a ? that returned 0 and opened nothing -- a control whose
       only behaviour is to do nothing when pressed, which is worse than its absence. The same test
       that gates the auto-run gates the button: a library surface, detected by the mode buttons'
       stable ids, which are in the static HTML of every wing and the index and absent there. */
    var chin = q('.wz-chin');
    if (chin && !q('.wz-help') && q('#mode-standard, #mode-legible')) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'wz-help'; b.textContent = '?';
      b.setAttribute('title', 'Tutorial for this view');
      b.setAttribute('aria-label', 'Show the tutorial for this view');
      b.addEventListener('click', function (e) { e.stopPropagation(); start(activeTour()); });
      chin.appendChild(b);
    }
    if (reduced()) return 0;                 // a moving spotlight is the whole idea
    addEventListener('click', onClickCheck, true);
    /* Cards and graphs are built after load, so the first check waits for one rather than assuming.
       If none ever arrives, no tour runs and no flag is spent -- /troubleshooting/ has a chin but no
       library surface, and a walkthrough of screen effects is the last thing wanted by someone who
       landed there because the site would not load. */
    if (q('article.obj, .lib-card, #map-view')) { setTimeout(maybe, 300); return 1; }
    if (window.MutationObserver) {
      var obs = new MutationObserver(function () {
        if (q('article.obj, .lib-card')) { obs.disconnect(); setTimeout(maybe, 300); }
      });
      obs.observe(document.body, { childList: true, subtree: true });
      setTimeout(function () { obs.disconnect(); }, 6000);
    }
    return 1;
  };

  /* PARSE TIME, not init time. The one-line hint in wuld-vfx.js says the same thing as the library
     tour's first step, and wzInit() fires hint() during boot -- before any init function here could
     run. Claiming the hint's key here is what stops a first-time reader being told twice, and it is
     claimed only on a page that can actually run that tour. */
  if (!reduced() && !seen(keyOf({ key: 'library' })) && q('#mode-standard, #mode-legible')) {
    try { sessionStorage.setItem('wz-hint-seen', '1'); } catch (e) {}
  }
})();
