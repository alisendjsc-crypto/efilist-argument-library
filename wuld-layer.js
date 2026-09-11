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


/* ==============================================================================================
   wuld-fb.js
   ============================================================================================== */

/* wuld-fb.js -- per-card feedback. One mailto per objection, carrying the card's own id.
 *
 * WHY PER-CARD AND NOT A CORNER BUTTON. A corner button produces "something's broken somewhere";
 * a per-card one arrives with the objection id already attached, which is the difference between a
 * report you can act on and one you have to chase. Site-wide comments already have a route --
 * wuld.ink/contact -- so a fourth chin button would add a channel without adding information, and
 * at 320px the chin row is already as wide as it can be.
 *
 * NO BACKEND. A mailto: costs nothing, needs no form, no storage and no consent banner. A form
 * needs all four, and that is a bigger decision than it looks.
 *
 * INJECTED, NOT DELEGATED, AND OBSERVED. The wings build their card list from JSON after load --
 * measured: 0 of 5 wings have a single `class="obj"` in their static HTML -- and re-render it when
 * a filter changes. A one-shot pass at boot would find nothing at all. */
(function () {
  var TO = 'contact@wuld.ink';
  var SEL = 'article.obj[id^="obj-"]:not([data-wz-fb])';

  function heading(card) {
    var h = card.querySelector('h2, h3, h4');
    return h ? h.textContent.replace(/\s+/g, ' ').trim() : '';
  }
  /* THE CARD DESCRIBES ITSELF. A report that says only "this one is wrong" costs whoever reads it
     a hunt through five libraries to work out which card it was. So the draft arrives carrying the
     card's own context -- the library, the headline, the colloquial names on its chips, and its
     classification strip -- pulled from the card at the moment of the click, which means it cannot
     drift out of date the way a hand-written note would.
     The strip is read child by child rather than with textContent, because the control is itself a
     DOM child of that strip and would otherwise append the word "feedback" to its own report. */
  function strip(card) {
    var m = card.querySelector('.obj-meta');
    if (!m) return '';
    var out = '';
    for (var i = 0; i < m.childNodes.length; i++) {
      var n = m.childNodes[i];
      if (n.nodeType === 1 && String(n.className || '').indexOf('wz-fb') > -1) continue;
      out += n.textContent || '';
    }
    return out.replace(/\s+/g, ' ').trim();
  }
  function chips(card) {
    var k = card.querySelector('.kw');
    if (!k) return [];
    var out = [];
    for (var i = 0; i < k.children.length && out.length < 8; i++) {
      var t = k.children[i].textContent.replace(/\s+/g, ' ').trim();
      if (t && t.length <= 40) out.push(t);
    }
    return out;
  }
  function clip(s, n) { return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '\u2026' : s; }

  /* The writing space goes FIRST. Mail clients drop the cursor at the top of the body, so anything
     above the prompt is something the reader has to scroll past before they can type. Everything
     the machine contributed sits below the rule, out of the way but travelling with the message.
     MAILTO LENGTH IS A REAL LIMIT -- Windows passes the whole URL through a shell, and clients
     start truncating well before 2000 characters. So the body is built longest-first and the
     optional parts are dropped, in order, until the encoded URL fits under the budget. */
  var MAX_URL = 1800;
  function href(card) {
    var id   = card.id;
    var url  = location.href.split('#')[0] + '#' + id;
    var lib  = (document.title.split('\u2014')[0] || '').trim();
    var head = clip(heading(card), 240);
    var cls  = strip(card);
    var kw   = chips(card);
    var lead = "(what's wrong, or what's missing?)\n\n\n"
             + "-- added automatically, so you needn't describe which card --\n";
    function build(withKw, headLen) {
      var b = lead;
      if (lib)  b += 'library:        ' + lib + '\n';
      if (head) b += 'objection:      "' + clip(head, headLen) + '"\n';
      if (withKw && kw.length) b += 'also called:    ' + kw.join(' \u00b7 ') + '\n';
      if (cls)  b += 'classification: ' + cls + '\n';
      return b + 'id:             ' + id + '\nlink:           ' + url + '\n';
    }
    var subj = 'library feedback \u2014 ' + id;
    var tries = [[true, 240], [true, 140], [false, 140], [false, 80]];
    var out;
    for (var i = 0; i < tries.length; i++) {
      out = 'mailto:' + TO + '?subject=' + encodeURIComponent(subj)
          + '&body=' + encodeURIComponent(build(tries[i][0], tries[i][1]));
      if (out.length <= MAX_URL) break;
    }
    return out;
  }

  function pass() {
    var cards = document.querySelectorAll(SEL), n = 0;
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i], m = c.querySelector('.obj-meta');
      c.setAttribute('data-wz-fb', '1');            // set even when there is no meta strip, so a
      if (!m) continue;                             // card without one is not re-examined forever
      var a = document.createElement('a');
      a.className = 'wz-fb';
      a.href = href(c);
      a.rel = 'nofollow';
      a.textContent = 'feedback';   // uppercased by CSS, like every other micro-label on the card
      a.title = 'Email a correction or comment about this objection';
      a.setAttribute('aria-label', 'Email a correction or comment about this objection: ' + (heading(c) || c.id));
      /* Appended, not prepended. While the control was floated it had to precede the meta text to
         sit beside it; anchored, its position is set by CSS and DOM order is free to match reading
         order instead -- so a keyboard lands on the meta text first and the utility after it. */
      m.appendChild(a);
      n++;
    }
    return n;
  }

  window.wzFbInit = function () {
    var n = pass();
    if (window.MutationObserver) {
      var queued = false;
      new MutationObserver(function () {
        if (queued) return;                          // a filter re-render is hundreds of mutations;
        queued = true;                               // coalesce them into one pass on the next frame
        requestAnimationFrame(function () { queued = false; pass(); });
      }).observe(document.body, { childList: true, subtree: true });
    }
    return n;
  };
})();


/* ==============================================================================================
   wuld-tour.js
   ============================================================================================== */

/* wuld-tour.js -- the first-visit walkthrough. One feature at a time, everything else darkened.
 *
 * IT OWNS THE FIRST VISIT, AND THAT IS WHY IT RUNS AT PARSE TIME. The one-line hint in wuld-vfx.js
 * says the same thing as step 1 of this tour, and a first-time reader who gets both is being told
 * twice. wzInit() fires hint() during boot, before any init function here could run, so the decision
 * has to be made earlier than boot: the block at the bottom of this file marks the hint as seen the
 * moment the script parses, if and only if the tour is actually going to run. On every later visit
 * the tour stays away and the hint resumes its normal once-per-session job.
 *
 * ONCE EVER, NOT ONCE PER SESSION -- unlike the hint. A walkthrough is worth sitting through once;
 * meeting it again next week is an insult. localStorage can throw (private windows, blocked site
 * data) and every touch is wrapped; a tour that cannot record itself simply never runs, which is
 * the harmless direction here, the opposite of the hint's.
 *
 * THE COPY BELOW IS A DRAFT. Edit STEPS[].text freely; nothing else reads it. */
(function () {
  var DONE = 'wz-tour-done';
  var H = document.documentElement;

  var STEPS = [
    { sel: '.wz-power',
      text: 'Screen effects. This steps the whole layer down — full effects, then colour and type only, then nothing at all. It remembers what you chose.' },
    { sel: '.wz-mag',
      text: 'Magnifier. Hold Shift and scroll to zoom anywhere on the page, or press this and zoom with a plain wheel. Escape returns to 1×.' },
    { sel: '.wz-mute',
      text: 'Sound. A quiet mechanical room tone and small cues, only while effects are on. This switches it off and keeps it off.' },
    { sel: '#mode-standard,#mode-legible,#mode-hc,#mode-both|union',
      text: 'Reading modes. Legible lightens the page, High contrast strengthens it, Both does both. Your choice is remembered.' },
    { sel: 'article.obj',
      text: 'Every objection is a card: the claim as people actually put it, the words they use for it, a diagnosis of where it goes wrong, and the full response behind [+].' },
    { sel: '.wz-fb',
      text: 'Something wrong, or missing? Feedback opens a mail draft that already names the card — so you never have to describe which one you meant.' }
  ];

  var live = [], idx = 0, mask = [], ring, card, body, dots, prevFocus, open = false;

  function reduced() { try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
  function seen() { try { return localStorage.getItem(DONE) === '1'; } catch (e) { return true; } }
  function mark() { try { localStorage.setItem(DONE, '1'); } catch (e) {} }

  /* A step whose target is not on this page is not a step. /libraries/ has no objection cards and
     /troubleshooting/ has no chin furniture worth pointing at, so the set is resolved per page
     rather than assumed -- an empty spotlight pointing at nothing is worse than a shorter tour. */
  function resolve() {
    var out = [];
    for (var i = 0; i < STEPS.length; i++) {
      /* "a,b,c|union" spotlights the box that contains all of them. The mode row has no class of
         its own; its container is full-width, so ringing the container drew a box running far past
         the last button into empty space. Matching the buttons by LABEL TEXT -- the first thing I
         reached for -- would have tied the tour to editorial copy that is free to change; the ids
         do not change, and the union of four of them is exactly the row. */
      var sel = STEPS[i].sel, uni = false;
      if (sel.slice(-6) === '|union') { sel = sel.slice(0, -6); uni = true; }
      var els = uni ? [].slice.call(document.querySelectorAll(sel))
                    : [document.querySelector(sel)];
      els = els.filter(function (e) { return e && e.getClientRects().length; });
      if (els.length) out.push({ els: els, text: STEPS[i].text });
    }
    return out;
  }

  function build() {
    /* FOUR PANELS AROUND THE TARGET, not one overlay with a hole. The single-element version used
       a huge box-shadow spread and then had to raise the spotlit element above it -- which, for a
       chin button, meant raising the whole chin, leaving the entire row undarkened and the ring
       stranded behind it. Panels cover everything EXCEPT the target, so nothing on the page is ever
       covered and no z-index of anyone else's has to be touched. */
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
    card.setAttribute('aria-label', 'A quick tour of this page');

    body = document.createElement('p'); body.className = 'wz-tour-text';
    dots = document.createElement('span'); dots.className = 'wz-tour-dots';

    var nav = document.createElement('div'); nav.className = 'wz-tour-nav';
    var skip = mkbtn('Skip', 'Skip the tour', function () { finish(); });
    skip.className = 'wz-tour-skip';
    var prev = mkbtn('←', 'Previous', function () { go(idx - 1); });
    var next = mkbtn('→', 'Next', function () { go(idx + 1); });
    nav.appendChild(skip); nav.appendChild(dots); nav.appendChild(prev); nav.appendChild(next);
    card.appendChild(body); card.appendChild(nav);
    card._prev = prev; card._next = next; card._skip = skip;

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
    for (var q = 1; q < els.length; q++) {
      var z = els[q].getBoundingClientRect();
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
    set(mask[0], 0, 0, W, y);                    // above
    set(mask[1], 0, y + h, W, Hh - (y + h));     // below
    set(mask[2], 0, y, x, h);                    // left
    set(mask[3], x + w, y, W - (x + w), h);      // right
    set(ring, x, y, w, h);
    return [Math.round(r.top), Math.round(r.left), Math.round(r.width), Math.round(r.height)];
  }

  function place(els) {
    /* A TALL TARGET IS NOT CENTRED. An objection card can be taller than the viewport, and
       block:'center' then puts its middle in the middle -- both ring edges off-screen, so the
       spotlight has no visible boundary at all. Showing the top of it is what a reader needs. */
    var tall = unionRect(els).height > innerHeight * 0.7;
    els[0].scrollIntoView({ block: tall ? 'start' : 'center', behavior: reduced() ? 'auto' : 'smooth' });

    /* WAIT FOR THE SCROLL TO SETTLE. Smooth scrolling runs for a few hundred milliseconds, so a
       rect read two frames later is a rect mid-flight -- which is exactly what it drew: a box
       spanning the bottom of one card and the top of the next, matching no element on the page.
       This re-reads until the rect stops moving, or gives up after 800ms and draws where it is. */
    var stable = 0, last = null, t0 = performance.now();
    (function tick() {
      if (!open) return;
      var now = paint(els);
      if (last && now[0] === last[0] && now[1] === last[1] && now[2] === last[2] && now[3] === last[3]) stable++;
      else stable = 0;
      last = now;
      if (stable < 2 && performance.now() - t0 < 800) { requestAnimationFrame(tick); return; }

      var r = unionRect(els), cw = Math.min(340, innerWidth - 24);
      card.style.width = cw + 'px';
      var ch = card.offsetHeight || 120;
      var below = r.bottom + 6 + 12;
      var top = (below + ch < innerHeight - 12) ? below : Math.max(12, r.top - 18 - ch);
      var left = r.left + r.width / 2 - cw / 2;
      card.style.top = Math.min(top, Math.max(12, innerHeight - ch - 12)) + 'px';
      card.style.left = Math.max(12, Math.min(left, innerWidth - cw - 12)) + 'px';
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
    if (e.key === 'Escape')     { e.preventDefault(); finish(); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1); }
    else if (e.key === 'ArrowLeft')  { e.preventDefault(); go(idx - 1); }
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
  function onDown(e) { if (open && !card.contains(e.target)) finish(); }   // clicking off ends it

  function finish() {
    if (!open) return;
    open = false; mark();
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

  function start() {
    if (open) return 0;
    live = resolve();
    if (live.length < 2) return 0;          // one lonely spotlight is not a walkthrough
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

  /* Console entry point, and the only way back in once it has been seen. A permanent "?" button
     would be a seventh piece of chrome earning its keep two minutes a lifetime. */
  window.wzTour = function () { return start(); };

  window.wzTourInit = function () {
    if (seen() || reduced()) return 0;      // reduced motion: a moving spotlight is the whole idea
    /* ONLY ON A LIBRARY SURFACE. The chin exists on every page the layer touches, so a page with
       nothing else on it still resolves three steps and passed the "enough steps" test -- which is
       how /troubleshooting/ came to run a tour. That page is where a reader lands when the site is
       BROKEN; a walkthrough of screen effects is the last thing they want, and it would spend the
       once-ever flag so the real tour never runs on a wing. The tour therefore requires an
       objection card or a library card, not merely a chin.
       The cards are rendered from JSON after load, so this waits for one rather than assuming. If
       none ever arrives the tour does NOT fall back to a shorter one -- it stays away, and the
       once-ever flag is left unspent. */
    /* IS THIS A LIBRARY SURFACE AT ALL? The mode buttons carry stable ids and are present in the
       STATIC html of every wing and of the index, and absent from /troubleshooting/ -- so the
       question is answerable at parse time, before any card has been fetched. */
    if (!document.querySelector('#mode-standard, #mode-legible')) return 0;
    if (document.querySelector('.lib-card')) { setTimeout(start, 250); return 1; }
    var started = false, t = null, obs = null;
    function once() {
      if (started) return; started = true;
      obs && obs.disconnect(); clearTimeout(t);
      if (document.querySelector('article.obj')) start();
    }
    t = setTimeout(once, 2500);
    if (window.MutationObserver) {
      obs = new MutationObserver(function () { if (document.querySelector('article.obj')) setTimeout(once, 250); });
      obs.observe(document.body, { childList: true, subtree: true });
    }
    return 1;
  };

  /* PARSE TIME, not init time -- see the header. Claiming the hint's key here is what stops the
     reader being told about the power button twice. */
  if (!seen() && !reduced() && document.querySelector('#mode-standard, #mode-legible')) {
    try { sessionStorage.setItem('wz-hint-seen', '1'); } catch (e) {}
  }
})();

(function(){
  var FURNITURE = "<!-- append as the last children of <body>; add class wz-on to <html> -->\n<div class=\"wz-frame\" aria-hidden=\"true\"></div>\n<div class=\"wz-chin\" aria-hidden=\"true\">\n  <span class=\"wz-perf\"></span>\n  <span class=\"wz-mark\">W<i class=\"wz-led\"></i>U<i class=\"wz-led\"></i>L<i class=\"wz-led\"></i>D<i class=\"wz-led\"></i></span>\n  <span class=\"wz-perf\"></span>\n  <button class=\"wz-mag\" title=\"Magnifier\" aria-label=\"Magnifier. Shift and scroll to zoom.\">&#x2315;</button>\n  <button class=\"wz-power\" title=\"Cosmetics\" aria-label=\"Toggle cosmetics\">&#x23FB;</button>\n</div>\n";
  function boot(){
    if (!document.querySelector('.wz-frame')) document.body.insertAdjacentHTML('beforeend', FURNITURE);
    window.wzInit();
    if (window.wzSfxInit) window.wzSfxInit();
    if (window.wzFbInit)  window.wzFbInit();
    if (window.wzTourInit) window.wzTourInit();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
