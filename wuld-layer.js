/* wuld-layer.js -- library.wuld.ink cosmetic + sound layer. */
/* wuld-vfx.js -- power-button cycling and the clamped pivot. Pairs with wuld-vfx.css. */
(function () {
  /* THE LADDER DESCENDS. vfx -> cosmetic -> off -> vfx. The operator's call, and it is the better
     mental model independently of what the default is: a power button that DIMS reads correctly,
     one that builds up reads like a feature you have to discover. The tier persists per reader, so
     stepping down is not re-imposed on the next page; localStorage can throw (private windows,
     blocked site data) so every touch of it is wrapped and the layer works fine without it.
     To reset while testing:  localStorage.removeItem('wz-tier')  */
  var H = document.documentElement, TIERS = ['off', 'cosmetic', 'vfx'], START = 2, i = START;
  function remember(v) { try { localStorage.setItem('wz-tier', v); } catch (e) {} }
  function recall() {
    try { var v = localStorage.getItem('wz-tier');
          if (v !== null && +v >= 0 && +v <= 2) return +v; } catch (e) {}
    return START;
  }

  /* ADOPT, don't build. When the page ships <div class="wz-stage"> in its own markup the wrapper
     already exists at first paint and there is no reparent, no reflow and no flash -- which is the
     whole reason the wrapper moved into the markup. Building one is the fallback for the console
     snippet and for any page that has not been integrated yet. */
  function wrapStage() {
    if (document.querySelector('.wz-stage')) return;
    var s = document.createElement('div'); s.className = 'wz-stage';
    var keep = ['wz-frame', 'wz-chin'];
    [].slice.call(document.body.children).forEach(function (el) {
      if (keep.indexOf(el.className) === -1 && el.tagName !== 'SCRIPT') s.appendChild(el);
    });
    document.body.insertBefore(s, document.body.firstChild);
  }


  /* THE GATE IS MEASURED, NOT NAMED -- see the long note in wuld-vfx.css. The mode name does not
     predict the background: the flagship is dark in legible and cream in high-contrast, the
     libraries umbrella is the other way round. So read the ground and grade it. */
  function bgLuma() {
    var els = [document.body, document.documentElement], i, c, m;
    for (i = 0; i < els.length; i++) {
      if (!els[i]) continue;
      c = getComputedStyle(els[i]).backgroundColor;
      m = c && c.match(/[\d.]+/g);
      if (!m || m.length < 3) continue;
      if (m.length > 3 && parseFloat(m[3]) < 0.5) continue;      // see-through: keep looking
      return 0.2126 * +m[0] + 0.7152 * +m[1] + 0.0722 * +m[2];
    }
    return 255;                       // unreadable ground -> treat as light -> stay silent
  }
  function gradeBg() {
    var want = bgLuma() > num(getComputedStyle(H).getPropertyValue('--wz-dark-max'), 90);
    if (H.classList.contains('wz-lightbg') !== want) H.classList.toggle('wz-lightbg', want);
  }

  function apply() {
    H.classList.toggle('wz-on',  i >= 1);
    H.classList.toggle('wz-vfx', i === 2);
    var b = document.querySelector('.wz-power');
    if (b) { b.setAttribute('title', 'Display: ' + TIERS[i] + ' — click to cycle');
             b.setAttribute('aria-label', 'Display mode: ' + TIERS[i] + '. Click to cycle.'); }
    document.querySelectorAll('.wz-led').forEach(function (l, n) {   // the LEDs REPORT the tier
      l.style.opacity = i === 0 ? .18 : i === 1 ? .55 : (n < 2 ? .55 : .95);
    });
    if (i !== 2) { rest(); clearZoom(); }
  }

  var rest = function () {};
  var raf = null;
  function num(v, d){ var n = parseFloat(v); return isNaN(n) ? d : n; }

  function onMove(e) {
    if (i !== 2 || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (raf) return;
    raf = requestAnimationFrame(function () {
      raf = null;
      var cs  = getComputedStyle(H),
          pan = num(cs.getPropertyValue('--wz-pan'), 6),   // read, never restated: cccxvii
          dx  = (e.clientX / innerWidth  - 0.5) * 2,       // -1 .. 1
          dy  = (e.clientY / innerHeight - 0.5) * 2;
      // The camera moves TOWARD the cursor, so the picture slides the other way and you see a little
      // further to that side. Bounded by --wz-pan, which is bounded by the lip, so the gap that opens
      // at the trailing edge is always underneath the frame.
      H.style.setProperty('--wz-px', (-dx * pan).toFixed(2) + 'px');
      H.style.setProperty('--wz-py', (-dy * pan * 0.6).toFixed(2) + 'px');
      // Blur the end the camera is NOT at.
      H.style.setProperty('--wz-sl', Math.max(0,  dx).toFixed(3));
      H.style.setProperty('--wz-sr', Math.max(0, -dx).toFixed(3));
    });
  }

  /* Shown once per BROWSER SESSION, not once ever: a reader who closes the tab and comes back
     tomorrow has plausibly forgotten. sessionStorage can throw (private windows, blocked site
     data) and every touch is wrapped -- a hint that fails to record itself is shown again, which
     is the harmless direction. Never shown if the reader is not actually at the vfx tier, because
     then there is nothing to offer to turn down. */
  function hint() {
    if (i !== 2) return;
    var KEY = 'wz-hint-seen';
    try { if (sessionStorage.getItem(KEY)) return; } catch (e) {}
    try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
    var d = document.createElement('div');
    d.className = 'wz-hint';
    // role=status + aria-live=polite: announced in turn, never stealing focus, and appended last
    // so it is not the first thing a screen reader meets on the page.
    d.setAttribute('role', 'status');
    d.setAttribute('aria-live', 'polite');
    var span = document.createElement('span');
    span.innerHTML = 'Screen effects are on. The <b>\u23FB</b> button in the frame dims them.';
    var x = document.createElement('button');
    x.type = 'button'; x.textContent = '\u00D7';
    x.setAttribute('aria-label', 'Dismiss');
    var gone = false;
    function close() {
      if (gone) return; gone = true;
      d.classList.remove('wz-in');
      setTimeout(function () { if (d.parentNode) d.parentNode.removeChild(d); }, 400);
    }
    x.addEventListener('click', close);
    d.appendChild(span); d.appendChild(x);
    document.body.appendChild(d);
    requestAnimationFrame(function () { d.classList.add('wz-in'); });
    setTimeout(close, 9000);
    // Using the button is the best possible dismissal: they found what the hint was for.
    var b = document.querySelector('.wz-power');
    if (b) b.addEventListener('click', close, { once: true });
  }

  /* ---- THE MAGNIFIER --------------------------------------------------------------------------
     Two ways in, one state: Shift+wheel always zooms, and the chin's magnifier button arms a mode
     in which a plain wheel zooms. NOT Ctrl+wheel -- that is the browser's own zoom, and trackpad
     pinch arrives as ctrl+wheel too, so binding it would take real accessible zoom AND pinch away
     in exchange for an aesthetic one. Shift+wheel is free here: measured, it fires a cancelable
     wheel event and its native job (horizontal scroll) is a no-op on a page with no horizontal
     overflow. Once zoomed there IS horizontal overflow, so the mode releases it again below 1.02.

     Zoom is anchored to the POINTER, not to the viewport centre: the document point under the
     cursor stays under the cursor. Measured drift on the equivalent centre-anchored version: 0px. */
  var zoom = 1;
  function clamp(v, lo, hi){ return v < lo ? lo : (v > hi ? hi : v); }
  function zmax(){ return num(getComputedStyle(H).getPropertyValue('--wz-zoom-max'), 4); }

  function setZoom(next, cx, cy) {
    if (i !== 2) return;                       // zoom belongs to the vfx tier and nowhere else
    next = clamp(next, 1, zmax());
    if (Math.abs(next - zoom) < 0.0005) return;
    var k0 = zoom, k1 = next;
    // the document point under the cursor, in unscaled coordinates
    var docX = (scrollX + cx) / k0, docY = (scrollY + cy) / k0;
    H.classList.add('wz-zooming');
    H.style.setProperty('--wz-zoom', k1.toFixed(4));
    // opacity ramps from nothing at 1x, so the grille cannot show up uninvited
    var gmax = num(getComputedStyle(H).getPropertyValue('--wz-grille-max'), 0.42);
    H.style.setProperty('--wz-grille-a',
      (clamp((k1 - 1) / Math.max(0.001, zmax() - 1), 0, 1) * gmax).toFixed(3));
    zoom = k1;
    scrollTo(Math.round(docX * k1 - cx), Math.round(docY * k1 - cy));
    H.classList.toggle('wz-zoomed', k1 > 1.0001);
    if (k1 <= 1.0001) H.classList.remove('wz-mag-on');
    clearTimeout(setZoom._t);
    setZoom._t = setTimeout(function(){ H.classList.remove('wz-zooming'); }, 90);
    var b = document.querySelector('.wz-mag');
    if (b) b.setAttribute('aria-label', 'Magnifier, ' + k1.toFixed(1) + 'x. Shift and scroll to zoom.');
  }
  function resetZoom(){ setZoom(1, innerWidth / 2, innerHeight / 2); }
  /* Stepping the power button DOWN has to drop the zoom with the tier, and it cannot go through
     setZoom() to do it: apply() has already moved `i` off 2 by the time it runs, and setZoom's
     first line is a guard on exactly that. Routing a teardown through a function gated on the state
     you just left is a bug that reads as correct -- it left the page stuck at 1.35x with no visible
     control, because the magnifier button is also gated on the vfx tier. Unconditional, and it
     restores the scroll position the zoom was anchored from. */
  function clearZoom(){
    if (zoom <= 1.0001) return;
    var docX = scrollX / zoom, docY = scrollY / zoom;
    zoom = 1;
    H.style.setProperty('--wz-zoom', '1');
    H.style.setProperty('--wz-grille-a', '0');
    H.classList.remove('wz-zoomed', 'wz-mag-on');
    scrollTo(Math.round(docX), Math.round(docY));
  }

  function onWheel(e) {
    if (i !== 2) return;
    var armed = e.shiftKey || H.classList.contains('wz-mag-on');
    if (!armed) return;
    if (e.ctrlKey) return;                     // leave browser zoom and trackpad pinch alone
    e.preventDefault();
    // wheel deltas differ wildly between mice, trackpads and OSes; use only the sign
    var step = e.deltaY < 0 ? 1.12 : 1 / 1.12;
    setZoom(zoom * step, e.clientX, e.clientY);
  }

  window.wzInit = function () {
    wrapStage();
    gradeBg();
    // The toggles change a class on <body> or an attribute on <html>; either way the ground may
    // flip, so re-grade on any of it. gradeBg only writes when the verdict changes, so the
    // observer cannot feed itself.
    if (window.MutationObserver) {
      var mo = new MutationObserver(gradeBg);
      mo.observe(H, { attributes: true, attributeFilter: ['class', 'data-mode', 'style'] });
      mo.observe(document.body, { attributes: true, attributeFilter: ['class', 'data-mode', 'style'] });
    }
    addEventListener('click', function () { setTimeout(gradeBg, 0); }, true);
    ['wz-vig','wz-grille','wz-soft-l','wz-soft-r'].forEach(function (c) {
      if (document.querySelector('.' + c)) return;
      var d = document.createElement('div'); d.className = c; d.setAttribute('aria-hidden', 'true');
      document.body.appendChild(d);
    });
    var b = document.querySelector('.wz-power');
    if (b) b.addEventListener('click', function () { i = (i + 2) % 3; remember(i); apply(); });

    var mg = document.querySelector('.wz-mag');
    if (mg) mg.addEventListener('click', function () {
      if (i !== 2) return;
      if (H.classList.contains('wz-mag-on') || zoom > 1.0001) { H.classList.remove('wz-mag-on'); resetZoom(); }
      else { H.classList.add('wz-mag-on'); setZoom(1.35, innerWidth / 2, innerHeight / 2); }
    });
    addEventListener('wheel', onWheel, { passive: false });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && zoom > 1.0001) { H.classList.remove('wz-mag-on'); resetZoom(); }
    });
    addEventListener('mousemove', onMove, { passive: true });
    // Rest at a slight angle rather than snapping flat: the POV reading is what makes it stop
    // looking like a plain page, and it should not depend on the cursor still moving.
    rest = function () {
      H.style.setProperty('--wz-px','0px'); H.style.setProperty('--wz-py','0px');
      H.style.setProperty('--wz-sl','0');   H.style.setProperty('--wz-sr','0');
    };
    addEventListener('mouseleave', rest);
    window.wzRest = rest;
    i = recall();
    apply(); rest(); hint();
  };
})();


/* ==============================================================================================
   wuld-sfx.js
   ============================================================================================== */

/* wuld-sfx.js -- the sound layer for library.wuld.ink. Pairs with wuld-vfx.js and shares its tier.
 *
 * THE SOUNDS ARE SYNTHESIZED, NOT SAMPLED. See P5_SFX_SPEC.md: the reference recording was segmented
 * into 100 events and measured, the operator's "no high-pitched" instruction turned out to be a clean
 * filter (centroid <1200 Hz, <5% of energy above 3 kHz) keeping 76 of them, and these seven were
 * generated from the surviving profile. Nothing here is cut from anyone's recording.
 *
 * THE DESIGN RULE, inherited from that profile: the longer the sound, the lower it sits. Hover near
 * 900 Hz, mode changes near 175 Hz. That inverse relation is most of why the set coheres, so if a
 * sound is ever added, place it on that line rather than beside it. */
(function () {
  var H = document.documentElement;
  var SRC = '/sfx/';
  /* gain per sound. Hover is the quietest by a wide margin because it is the one that fires most --
     82 objection cards on the flagship -- and an event that common has to sit under the reading
     rather than on top of it. */
  var BANK = {
    hover:        { f: 'wz-hover.ogg',        g: 0.18 },
    click:        { f: 'wz-click.ogg',        g: 0.42 },
    expand:       { f: 'wz-expand.ogg',       g: 0.38 },
    collapse:     { f: 'wz-collapse.ogg',     g: 0.34 },
    magnifier_in: { f: 'wz-magnifier_in.ogg', g: 0.40 },
    tier_step:    { f: 'wz-tier_step.ogg',    g: 0.46 }
  };
  var AMB = { f: 'wz-ambience_loop.ogg', g: 0.30 };

  var ctx = null, buf = {}, raw = {}, dec = {}, ambNode = null, ambGain = null, unlocked = false;
  var HOVER_MS = 120, lastHover = 0;
  /* A sound asked for before its buffer existed, and when. PENDING_MS is how long a late arrival
     still reads as a response to the click that asked for it rather than as a stray noise. */
  var pending = null, pendingAt = 0, PENDING_MS = 400;

  function reduced() { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
  function muted() { try { return localStorage.getItem('wz-muted') === '1'; } catch (e) { return false; } }
  function setMuted(v) { try { localStorage.setItem('wz-muted', v ? '1' : '0'); } catch (e) {} paint(); }

  /* Audible only at the vfx tier, on a dark ground, with motion allowed and sound not muted.
     Same gate shape as the glow, deliberately: one power button should mean one thing. */
  function live() {
    return H.classList.contains('wz-vfx') && !H.classList.contains('wz-lightbg')
           && !reduced() && !muted();
  }

  /* NETWORK EARLY, CONTEXT LATE. The ArrayBuffers are fetched on idle -- plain fetch needs no
     AudioContext and no gesture -- while decodeAudioData and resume() wait for the first real
     gesture, which is what the autoplay policy actually requires. Creating a context before a
     gesture is legal but starts it suspended and earns a console warning; doing the network first
     means the first click is audible instead of silently arming. */
  function prefetch() {
    var all = Object.keys(BANK).map(function (k) { return [k, BANK[k].f]; });
    all.push(['_amb', AMB.f]);
    all.forEach(function (p) {
      fetch(SRC + p[1]).then(function (r) { return r.ok ? r.arrayBuffer() : null; })
        .then(function (b) { if (b) { raw[p[0]] = b; decodeOne(p[0]); } })
        .catch(function () {});         // a missing sound is silence, never an error the reader sees
    });
  }

  function unlock() {
    if (unlocked) return;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) { unlocked = true; return; }
    unlocked = true;
    try { ctx = new AC(); } catch (e) { return; }
    if (ctx.state === 'suspended') ctx.resume();
    Object.keys(raw).forEach(decodeOne);
  }

  /* DECODE IS ARRIVAL-DRIVEN, NOT GESTURE-DRIVEN. It used to be a single pass over raw{} inside
     unlock(), which meant any sound whose download had not landed by the first gesture was never
     decoded at all -- silent for the rest of the session, not just for that click. Measured: with
     the sound files arriving 3s late, a click at 1.2s left every later click silent too. So both
     sides call this, it is idempotent, and whichever of the two happens second does the decoding. */
  function decodeOne(k) {
    if (!ctx || buf[k] || !raw[k] || dec[k]) return;
    dec[k] = 1;
    try {
      ctx.decodeAudioData(raw[k].slice(0),
        function (d) { buf[k] = d; onDecoded(k); },
        function () { dec[k] = 0; });
    } catch (e) { dec[k] = 0; }
  }

  /* The first gesture creates the context and schedules the decodes in the same tick, so the click
     that unlocks audio asks for a buffer that is ~45ms from existing (measured) and used to get
     silence -- the one click most likely to be a reader testing whether sound works. play() leaves
     the name here; this fires it once, if the tier still allows it. */
  function onDecoded(k) {
    if (k === '_amb') { ambMaybeStart(); return; }
    if (pending === k && performance.now() - pendingAt < PENDING_MS) { pending = null; play(k); }
  }

  /* ONE DECODED BUFFER PER SAMPLE, a fresh source node per play. BufferSourceNodes are single-use by
     spec -- reusing one throws -- so the pooling that matters is of the decoded PCM, which is the
     expensive part, not of the node, which is nearly free. */
  function play(name) {
    if (!live()) return;
    if (!ctx || !buf[name]) {
      if (ctx && raw[name]) { pending = name; pendingAt = performance.now(); decodeOne(name); }
      return;
    }
    try {
      var s = ctx.createBufferSource(), g = ctx.createGain();
      s.buffer = buf[name];
      g.gain.value = (BANK[name] || { g: 0.3 }).g;
      s.connect(g); g.connect(ctx.destination);
      s.start(0);
    } catch (e) {}
  }

  function ambMaybeStart() {
    if (!ctx || !buf._amb) return;
    if (!live()) { ambStop(); return; }
    if (ambNode) return;
    try {
      ambNode = ctx.createBufferSource(); ambGain = ctx.createGain();
      ambNode.buffer = buf._amb; ambNode.loop = true;
      ambGain.gain.value = 0;
      ambNode.connect(ambGain); ambGain.connect(ctx.destination);
      ambNode.start(0);
      ambGain.gain.linearRampToValueAtTime(AMB.g, ctx.currentTime + 1.6);   // no sudden arrival
    } catch (e) { ambNode = null; }
  }
  function ambStop() {
    if (!ambNode) return;
    var n = ambNode, g = ambGain; ambNode = null; ambGain = null;
    try {
      g.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.5);
      setTimeout(function () { try { n.stop(); } catch (e) {} }, 700);
    } catch (e) { try { n.stop(); } catch (e2) {} }
  }

  /* DELEGATION, not 82 listeners. The wings build their objection list from JSON after load, so
     anything bound at init would miss every card on the page. One listener on the document survives
     that, and survives the list being re-rendered by a filter. */
  function hoverable(t) { return t && t.closest && t.closest('.obj, .card, .lib-card, button, summary, a'); }
  function onOver(e) {
    if (!live()) return;
    var el = hoverable(e.target); if (!el) return;
    if (e.relatedTarget && el.contains(e.relatedTarget)) return;   // moving WITHIN a card is not a new hover
    var now = performance.now();
    if (now - lastHover < HOVER_MS) return;                        // drop, never queue
    lastHover = now;
    play('hover');
  }
  function onClick(e) {
    unlock();
    if (!live()) return;
    var d = e.target.closest && e.target.closest('details');
    if (e.target.closest && e.target.closest('summary') && d) { play(d.open ? 'collapse' : 'expand'); return; }
    if (e.target.closest && e.target.closest('.wz-power')) { play('tier_step'); return; }
    if (e.target.closest && e.target.closest('.wz-mag'))   { play('magnifier_in'); return; }
    if (e.target.closest && e.target.closest('button, a, summary')) play('click');
  }

  function paint() {
    var b = document.querySelector('.wz-mute');
    if (!b) return;
    var off = muted() || reduced();
    b.textContent = off ? '✕' : '●';
    b.setAttribute('aria-pressed', off ? 'true' : 'false');
    b.setAttribute('aria-label', off ? 'Sound off. Turn on.' : 'Sound on. Turn off.');
    b.setAttribute('title', off ? 'Sound off' : 'Sound on');
    H.classList.toggle('wz-muted', off);
    if (off) ambStop(); else ambMaybeStart();
  }

  window.wzSfxInit = function () {
    var chin = document.querySelector('.wz-chin');
    if (chin && !document.querySelector('.wz-mute')) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'wz-mute';
      chin.appendChild(b);
      b.addEventListener('click', function (e) { e.stopPropagation(); unlock(); setMuted(!muted()); });
    }
    paint();
    if ('requestIdleCallback' in window) requestIdleCallback(prefetch, { timeout: 3000 });
    else setTimeout(prefetch, 1200);
    ['pointerdown', 'keydown'].forEach(function (t) {
      addEventListener(t, unlock, { once: true, passive: true });
    });
    addEventListener('pointerover', onOver, { passive: true });
    addEventListener('click', onClick, true);
    /* The tier can change under us -- the power button, or the ground flipping with a mode toggle.
       gradeBg's observer already watches for that; this one keeps the ambience honest about it. */
    if (window.MutationObserver) {
      new MutationObserver(function () { if (live()) ambMaybeStart(); else ambStop(); paint(); })
        .observe(H, { attributes: true, attributeFilter: ['class', 'data-mode'] });
    }
  };
})();

(function(){
  var FURNITURE = "<!-- append as the last children of <body>; add class wz-on to <html> -->\n<div class=\"wz-frame\" aria-hidden=\"true\"></div>\n<div class=\"wz-chin\" aria-hidden=\"true\">\n  <span class=\"wz-perf\"></span>\n  <span class=\"wz-mark\">W<i class=\"wz-led\"></i>U<i class=\"wz-led\"></i>L<i class=\"wz-led\"></i>D<i class=\"wz-led\"></i></span>\n  <span class=\"wz-perf\"></span>\n  <button class=\"wz-mag\" title=\"Magnifier\" aria-label=\"Magnifier. Shift and scroll to zoom.\">&#x2315;</button>\n  <button class=\"wz-power\" title=\"Cosmetics\" aria-label=\"Toggle cosmetics\">&#x23FB;</button>\n</div>\n";
  function boot(){
    if (!document.querySelector('.wz-frame')) document.body.insertAdjacentHTML('beforeend', FURNITURE);
    window.wzInit();
    if (window.wzSfxInit) window.wzSfxInit();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
