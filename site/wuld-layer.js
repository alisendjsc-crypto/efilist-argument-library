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

  /* ---- THE CAMERA ----------------------------------------------------------------------------
     Unzoomed, the pan is --wz-pan (6px) toward the pointer and no more: the pointer at an edge slides
     the picture that far, and the bezel's lip is wider than that, so the gap it opens is under the
     frame. Zoomed, 6px is nothing against a line three viewports wide, and there is no wheel for the
     rest of it: Shift+wheel is the zoom, and once the magnifier is armed the plain wheel is too. So
     under the magnifier THE POINTER IS THE CAMERA (K317). Its place across the viewport maps onto
     what the scaled stage hides past that edge: at the centre nothing moves, at the right edge the
     whole of what lies past the right edge has come in, at the left edge the whole of what lies past
     the left. The sweep is exactly the overflow, no number chosen -- which is what "enough to finish
     the paragraph, never off the page" comes to when written down: the bound is the geometry.
     Vertically the same map, capped at (zoom-1) x half the viewport per side, because the wheel still
     scrolls that axis and a page is tall. The 6px rides on top at every zoom so the feel is
     continuous through 1.0. The camera's translation is composed OUTSIDE the scale (see the
     stylesheet), so all of this is in screen pixels. */
  var cam = { px: 0, py: 0 };                        // the applied camera, the zoomed part only
  var ptr = { x: innerWidth / 2, y: innerHeight / 2 };
  function stage(){ return document.querySelector('.wz-stage'); }
  function cw(){ return document.documentElement.clientWidth  || innerWidth; }
  function ch(){ return document.documentElement.clientHeight || innerHeight; }
  function geom() {
    var s = stage();
    return s ? { l: s.offsetLeft, t: s.offsetTop, w: s.offsetWidth, h: s.offsetHeight }
             : { l: 0, t: 0, w: cw(), h: ch() };
  }
  /* What the scaled stage hides past each viewport edge with the camera at rest, in screen px, from
     LAYOUT geometry: the stage's rect is mid-transition half the time and would read the easing. The
     origin is 0 0, so the stage's left and top stay put and only its far edges grow. */
  function hidden(g, k) {
    return { l: Math.max(0, scrollX - g.l), r: Math.max(0, g.l + g.w * k - scrollX - cw()),
             t: Math.max(0, scrollY - g.t), b: Math.max(0, g.t + g.h * k - scrollY - ch()) };
  }
  function vcap(k){ return (k - 1) * ch() / 2; }
  // the camera the model puts at a pointer position, at the current scroll and zoom
  function model(x, y) {
    var dx = (x / innerWidth - 0.5) * 2, dy = (y / innerHeight - 0.5) * 2;   // -1 .. 1
    if (zoom <= 1.0001) return { px: 0, py: 0, dx: dx, dy: dy };
    var hd = hidden(geom(), zoom), v = vcap(zoom);
    return { dx: dx, dy: dy,
             px: dx < 0 ? -dx * hd.l : -dx * hd.r,
             py: dy < 0 ? -dy * Math.min(hd.t, v) : -dy * Math.min(hd.b, v) };
  }
  function applyCam(px, py, dx, dy) {
    var base = num(getComputedStyle(H).getPropertyValue('--wz-pan'), 6);   // read, never restated: cccxvii
    cam.px = px; cam.py = py;
    // The camera moves TOWARD the cursor, so the picture slides the other way and you see further
    // to that side.
    H.style.setProperty('--wz-px', (px - dx * base).toFixed(2) + 'px');
    H.style.setProperty('--wz-py', (py - dy * base * 0.6).toFixed(2) + 'px');
    // Blur the end the camera is NOT at.
    H.style.setProperty('--wz-sl', Math.max(0,  dx).toFixed(3));
    H.style.setProperty('--wz-sr', Math.max(0, -dx).toFixed(3));
  }
  /* THE FOCUS RIDES THE TICK THAT ALREADY EXISTS. One rAF, already coalesced, already gated on the
     tier and on reduced motion -- adding a second listener for the same pointer would double the
     work to say the same thing twice. Two custom properties and one class; the box's transform and
     the vignette's mask both read them, so the DOM writes are 2 per frame, not 2 per consumer. */
  var focusOn = false, focusIdle = 0;
  function onMove(e) {
    if (i !== 2 || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    ptr.x = e.clientX; ptr.y = e.clientY;
    if (raf) return;
    raf = requestAnimationFrame(function () {
      raf = null;
      var m = model(ptr.x, ptr.y);
      applyCam(m.px, m.py, m.dx, m.dy);
      H.style.setProperty('--wz-fx', ptr.x + 'px');
      H.style.setProperty('--wz-fy', ptr.y + 'px');
      if (!focusOn) { focusOn = true; H.classList.add('wz-focusing'); }
      clearTimeout(focusIdle);
      /* A pointer that has not moved for a while is a reader who has stopped using it -- a keyboard
         reader, or a hand off the mouse. The clearing fades rather than sitting where it was left. */
      focusIdle = setTimeout(function () { focusOn = false; H.classList.remove('wz-focusing'); }, 2600);
    });
  }
  addEventListener('pointerleave', function () {
    clearTimeout(focusIdle); focusOn = false; H.classList.remove('wz-focusing');
  }, { passive: true });
  /* NOT WHILE SCROLLING, and the reason is both cost and intent. Cost: measured on these bytes at
     1440x1000, scrolling AND moving the pointer at once, focus display:none vs on --
       median 16.70 -> 16.70   p75 16.80 -> 33.30   p90 33.40 -> 50.00   frames over 33ms 24.5% -> 26.0%
     so the scroll owns most of it and the clearing owns the p75. Intent: a reader who is scrolling is
     not reading the word under the cursor. It comes back on the next pointer move, which is the
     gesture that means they have stopped and started looking. */
  var scrollHold = 0;
  addEventListener('scroll', function () {
    if (focusOn) { focusOn = false; H.classList.remove('wz-focusing'); }
    clearTimeout(scrollHold);
  }, { passive: true });
  /* A wheel scroll with the pointer still moves the bounds, not the camera: clamp to the new bounds
     and never re-place, so nothing moves that the reader did not move. Our own scrollTo lands here
     too, asynchronously, and finds a camera already inside its bounds. */
  function onScroll() {
    if (zoom <= 1.0001) return;
    var hd = hidden(geom(), zoom), px = clamp(cam.px, -hd.r, hd.l), py = clamp(cam.py, -hd.b, hd.t);
    if (px !== cam.px || py !== cam.py) { var m = model(ptr.x, ptr.y); applyCam(px, py, m.dx, m.dy); }
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

  /* The camera has two parts the reader cannot tell apart, the scroll and the pan, and after a zoom
     step they have to be split so that the pan is what the model would give at that scroll -- then
     the next pointer move changes nothing. The map scroll -> (scroll - pan) is monotone, so a
     bisection finds the split; where the model cannot express the camera (the pointer at an edge
     pins it to that end whatever the scroll) the remainder stays in the pan and the next move eases
     it out. What is never traded away is the anchor: the point under the cursor stays under it. */
  function split(u, hi, f) {
    var a = 0, b = Math.max(0, hi);
    if (b <= a) return a;
    if (a - f(a) >= u) return a;
    if (b - f(b) <= u) return b;
    for (var n = 0; n < 24; n++) { var m = (a + b) / 2; if (m - f(m) < u) a = m; else b = m; }
    return (a + b) / 2;
  }

  function setZoom(next, cx, cy) {
    if (i !== 2) return;                       // zoom belongs to the vfx tier and nowhere else
    next = clamp(next, 1, zmax());
    if (Math.abs(next - zoom) < 0.0005) return;
    var k0 = zoom, k1 = next, g = geom(),
        base = num(getComputedStyle(H).getPropertyValue('--wz-pan'), 6),
        dx = (cx / innerWidth - 0.5) * 2, dy = (cy / innerHeight - 0.5) * 2,
        bx = dx * base, by = dy * base * 0.6;
    // The document point under the cursor, in the stage's own unscaled coordinates. The camera's
    // translation sits outside the scale, so it comes off before the division: with a K317 camera
    // at 600px, dividing the raw scroll would slide the anchor 72px on every step.
    var docX = (scrollX + cx - cam.px + bx - g.l) / k0, docY = (scrollY + cy - cam.py + by - g.t) / k0;
    H.classList.add('wz-zooming');
    H.style.setProperty('--wz-zoom', k1.toFixed(4));
    // opacity ramps from nothing at 1x, so the grille cannot show up uninvited
    var gmax = num(getComputedStyle(H).getPropertyValue('--wz-grille-max'), 0.42);
    H.style.setProperty('--wz-grille-a',
      (clamp((k1 - 1) / Math.max(0.001, zmax() - 1), 0, 1) * gmax).toFixed(3));
    zoom = k1;
    // The camera position that keeps the anchor (the viewport's corner on the scaled stage, base
    // pan aside), clamped to where the stage still fills the viewport; then the split.
    var rx = g.l + g.w * k1 - cw(), ry = g.t + g.h * k1 - ch(),
        ux = clamp(g.l + docX * k1 - cx - bx, g.l, Math.max(g.l, rx)),
        uy = clamp(g.t + docY * k1 - cy - by, g.t, Math.max(g.t, ry)),
        v  = vcap(k1);
    var fx = function (sx) { return dx < 0 ? -dx * Math.max(0, sx - g.l) : -dx * Math.max(0, rx - sx); };
    var fy = function (sy) { return dy < 0 ? -dy * Math.min(Math.max(0, sy - g.t), v)
                                           : -dy * Math.min(Math.max(0, ry - sy), v); };
    if (k1 <= 1.0001) {                        // back to 1x: no camera, the scroll alone holds the anchor
      applyCam(0, 0, dx, dy);
      scrollTo(Math.round(g.l + docX - cx - bx), Math.round(g.t + docY - cy - by));
    } else {
      var sx = split(ux, rx, fx), sy = split(uy, ry, fy);
      applyCam(sx - ux, sy - uy, dx, dy);
      scrollTo(Math.round(sx), Math.round(sy));
      // the browser rounds and clamps the scroll; the pan absorbs the difference so the anchor holds
      if (Math.abs(scrollX - sx) > 0.01 || Math.abs(scrollY - sy) > 0.01) applyCam(scrollX - ux, scrollY - uy, dx, dy);
    }
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
    var g = geom(), docX = (scrollX - cam.px - g.l) / zoom, docY = (scrollY - cam.py - g.t) / zoom;
    zoom = 1; cam.px = 0; cam.py = 0;
    H.style.setProperty('--wz-zoom', '1');
    H.style.setProperty('--wz-grille-a', '0');
    H.style.setProperty('--wz-px', '0px'); H.style.setProperty('--wz-py', '0px');
    H.classList.remove('wz-zoomed', 'wz-mag-on');
    scrollTo(Math.round(g.l + docX), Math.round(g.t + docY));
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

  /* ---- THE STAGE BREAKS `body >` SELECTORS, SO MIRROR THEM ------------------------------------
     The stage wrapper is what carries the camera transform, and it has to be a real element between
     <body> and the content -- which silently stops every `body > #x` rule in the page's own
     stylesheet from matching. On the wings nothing uses that shape. On the FLAGSHIP the three
     top-level sections are switched with exactly that shape:

         body > #combined-library, body > #combined-rwe, body > #combined-coda { display: none; }
         body[data-active-view="rwe"] > #combined-rwe { display: block; }

     so wrapping turned the whole top-level navigation off: every section rendered at once, the
     library tour fired against a page showing five views simultaneously, and the page's own script
     threw setting textContent on an element it no longer expected to find. Measured before and
     after the wrap on the same page, which is the only way to tell this from a page behaviour.

     The fix is mechanical rather than hand-written: walk the page's own rules, and for any selector
     with a `body ... >` combinator, inject a copy with `.wz-stage` spliced in. Every mirrored rule
     gains exactly one class of specificity, so their order relative to each other is preserved, and
     the originals no longer match anything at all. Rules are mirrored, never edited. */
  function mirrorBodyChildRules() {
    if (!document.querySelector('.wz-stage')) return 0;
    if (document.getElementById('wz-stage-shim')) return 0;
    var RE = /\bbody((?:[.#\[:][^\s>,]*)*)\s*>/g, out = [], n = 0;
    function walk(rules) {
      for (var i = 0; i < rules.length; i++) {
        var r = rules[i];
        if (r.cssRules && r.conditionText !== undefined) {          // @media / @supports
          var inner = [];
          for (var j = 0; j < r.cssRules.length; j++) {
            var t = one(r.cssRules[j]); if (t) inner.push(t);
          }
          /* Re-emit under the rule's OWN at-keyword. '@media ' + conditionText was wrong for
             @supports, which also has conditionText -- it would have produced an @media rule with a
             supports condition, which parses as a media query that never matches. */
          var at = r.cssText.slice(0, r.cssText.indexOf('{')).trim();
          if (inner.length) out.push(at + '{' + inner.join('') + '}');
          continue;
        }
        var t2 = one(r); if (t2) out.push(t2);
      }
    }
    function one(r) {
      if (!r.selectorText || !r.style) return null;
      RE.lastIndex = 0;
      if (!RE.test(r.selectorText)) return null;
      RE.lastIndex = 0;
      n++;
      return r.selectorText.replace(RE, 'body$1 .wz-stage >') + '{' + r.style.cssText + '}';
    }
    for (var s = 0; s < document.styleSheets.length; s++) {
      var rules; try { rules = document.styleSheets[s].cssRules; } catch (e) { continue; }
      if (rules) walk(rules);
    }
    if (!out.length) return 0;
    var el = document.createElement('style');
    el.id = 'wz-stage-shim';
    el.textContent = '/* mirrored from the page\'s own `body >` rules, which the stage wrapper\n'
                   + '   would otherwise stop matching. ' + n + ' rule(s). */\n' + out.join('\n');
    document.head.appendChild(el);
    return n;
  }
  window.wzStageShim = mirrorBodyChildRules;

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
    ['wz-vig','wz-grille','wz-soft-l','wz-soft-r','wz-focus'].forEach(function (c) {
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
    addEventListener('scroll', onScroll, { passive: true });
    // Rest at a slight angle rather than snapping flat: the POV reading is what makes it stop
    // looking like a plain page, and it should not depend on the cursor still moving.
    rest = function () {
      H.style.setProperty('--wz-sl','0');   H.style.setProperty('--wz-sr','0');
      // Zoomed, the pointer leaving the window keeps the camera where it was: a reader who overshoots
      // the window's edge while finishing a line must not have the line pulled away (K317).
      if (zoom > 1.0001) return;
      cam.px = 0; cam.py = 0;
      H.style.setProperty('--wz-px','0px'); H.style.setProperty('--wz-py','0px');
    };
    addEventListener('mouseleave', rest);
    window.wzRest = rest;
    i = recall();
    mirrorBodyChildRules();
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
  /* K322: the cue files are served `public, max-age=14400` (the sound files were deliberately left
     on the default when the layer took its `private` rule), so a reader who has already loaded them
     keeps the old set for up to four hours after a change -- the same shape as the K315 layer-cache
     defect, one file type over. A `private` header on /sfx/* would fix it and cost seven conditional
     requests on every page load, for assets that change about twice a year. The version query is the
     cheaper half of the trade: the sounds stay long-cached, and the bump busts them exactly when they
     move. wuld-layer.js itself is `private, max-age=0`, so this line reaches every reader at once. */
  var SRC = '/sfx/';
  var SFXV = '?v=K322';
  /* gain per sound. Hover is the quietest by a wide margin because it is the one that fires most --
     82 objection cards on the flagship -- and an event that common has to sit under the reading
     rather than on top of it. */
  /* Softened 2026-09-12 after the first evening on the flagship ("less chirpy"): hover -9 dB and
     fired at most every 250 ms instead of 120 (on 82 rows it was the loudest thing on the page),
     click/expand/collapse -6 dB; the magnifier, the tier step and the room tone are as they were,
     because they answer a deliberate press, not a passing pointer. */
  var BANK = {
    hover:        { f: 'wz-hover.ogg',        g: 0.064 },
    click:        { f: 'wz-click.ogg',        g: 0.21 },
    expand:       { f: 'wz-expand.ogg',       g: 0.19 },
    collapse:     { f: 'wz-collapse.ogg',     g: 0.17 },
    magnifier_in: { f: 'wz-magnifier_in.ogg', g: 0.40 },
    tier_step:    { f: 'wz-tier_step.ogg',    g: 0.46 },
    /* WI-K321b: the video seat's four VIEW cues (HANDOFF_view_cues_sfx.md, 2026-09-13). One open-
       fifth chord, four gestures -- at rest / converging / descending / branching -- with every
       amplitude read out of the corpus at generation time (tier counts, out-degree, strong-vs-weak
       edge split), so the sound tracks the data and re-runs with it.
       THE GAINS ARE THEIRS, UNCHANGED, and that is a measured decision rather than deference.
       Checked against this bank two ways. Whole-file A-weighted RMS put the family 5.2 dB under the
       cue bank and said "lift them" -- but that metric averages a 7.5-second settle's tail against a
       0.2-second click, which is not a scale either is heard on. On the loudest-400ms A-weighted
       level, which is what a listener judges a transient by, the family mean is -35.5 dB against the
       bank's -34.9: 0.6 dB under, i.e. already level. Their own instruction was to level the four
       against each other rather than individually, and the 3.7 dB spread inside the family is the
       information the cues carry (flow_fan brightest, library_index quietest). Left alone. */
    library_index:{ f: 'wz-library_index.ogg', g: 0.22 },
    settle_swarm: { f: 'wz-settle_swarm.ogg',  g: 0.34 },
    dep_cascade:  { f: 'wz-dep_cascade.ogg',   g: 0.30 },
    flow_fan:     { f: 'wz-flow_fan.ogg',      g: 0.38 },
    /* WI-K322 2026-09-13: the NODE-SELECT cues. Josiah: "I wanted SFX for when you click on what the
       cursor is hovering over -- unique to those sections."  One per graph view, built from the SAME
       open-fifth stack as the four view cues -- measured off their own shipped bytes rather than
       taken from prose, since the generators the handoff names are not in the folder it names:
       FFT peaks under 600 Hz across the four are 55.0 / 82.5 / 110.0 / 123.6 / 164.8 / 220.0 / 247.2,
       i.e. A1 E2 A2 E3 A3 with B2/B3 as the ninth.
       VOICED AN OCTAVE UP, deliberately, and it is not a departure. The view cues sit at centroid
       114-148 Hz with essentially nothing above 250, and the video seat states that cost themselves:
       "on a phone all four will be quiet ... do not make any of these the only feedback for a view
       change." A pick IS the only sound for a selection, so it has to survive a laptop speaker. These
       land at centroid 208-268 Hz -- beside wz-magnifier_in (251) and wz-tier_step (181), the bank's
       own instrument cues -- with 9-70% of their energy in 250-800. Master low-pass still 1.8 kHz,
       no partial above A4.
       LEVELS: 2 dB under the cue bank's -34.9 dB short-term reference. Bank parity would be
       0.365 / 0.279 / 0.336; a pick is longer than a click (0.28-0.34s against 0.20) and fires on
       every node, so it sits just under. Generator: gen_pick_cues.py, seed 2010, deterministic. */
    pick_web:     { f: 'wz-pick_web.ogg',      g: 0.290 },
    pick_dep:     { f: 'wz-pick_dep.ogg',      g: 0.222 },
    pick_flow:    { f: 'wz-pick_flow.ogg',     g: 0.267 }
  };
  var AMB = { f: 'wz-ambience_loop.ogg', g: 0.30 };
  /* MASTER GAIN IS A CSS NUMBER. `--wz-sfx-gain` on <html> (default 1) scales every cue and the
     room tone, read at the moment each sound starts, so the next adjustment is a value that can be
     tried live in the console -- document.documentElement.style.setProperty('--wz-sfx-gain','0.5')
     -- and then written into wuld-vfx.css's :root, not a rebuild of this file. Clamped to 0..2. */
  function master() {
    try {
      var v = parseFloat(getComputedStyle(H).getPropertyValue('--wz-sfx-gain'));
      return isNaN(v) ? 1 : Math.max(0, Math.min(2, v));
    } catch (e) { return 1; }
  }

  /* Variation depth, same contract as the master gain: a CSS number on <html>, read per play,
     clamped 0..2. 0 is today's behaviour byte for byte -- one identical waveform per cue. */
  function vary() {
    try {
      var v = parseFloat(getComputedStyle(H).getPropertyValue('--wz-sfx-vary'));
      return isNaN(v) ? 1 : Math.max(0, Math.min(2, v));
    } catch (e) { return 1; }
  }

  var ctx = null, buf = {}, raw = {}, dec = {}, ambNode = null, ambGain = null, unlocked = false;
  var HOVER_MS = 250, lastHover = 0;
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
      fetch(SRC + p[1] + SFXV).then(function (r) { return r.ok ? r.arrayBuffer() : null; })
        .then(function (b) { if (b) { raw[p[0]] = b; decodeOne(p[0]); } })
        .catch(function () {});         // a missing sound is silence, never an error the reader sees
    });
  }

  /* WI-K321b 2026-09-13: SOUND ACROSS PAGES. Reported as "sfx disabling and reenabling randomly
     when going across pages", and it was neither random nor a bug in the cues. An AudioContext is
     unlocked PER DOCUMENT: the click that follows a link is a gesture on the page being LEFT, so
     every arrival starts locked, and the listeners were pointerdown/keydown only -- neither hover
     nor scroll nor a wheel is an activation. So a page where the reader clicked something early
     had sound and a page where they only read and hovered had none, which from the outside is a
     site that turns its own sound off at random. Three changes, in order of how much they buy:

     (1) EAGER CONTEXT. The context is now created and resumed at boot instead of waiting. Under a
         cold autoplay policy the resume is refused and we fall back to the gesture exactly as
         before; once the browser's media-engagement score for this origin is earned -- which is
         what repeated visits WITH playback earn -- the resume succeeds and sound is live from the
         first hover of every later page. The old comment traded this away to avoid a console
         warning. A warning nobody reads is not worth a reader hearing nothing.
     (2) THE LISTENER RE-ARMS. It was {once:true}: the first pointerdown consumed it whether or not
         the resume actually succeeded, so one refused attempt meant silence for the rest of that
         page. It now stays armed until ctx.state is genuinely 'running'.
     (3) CAPTURE PHASE, WIDER SET. pointerdown/pointerup/touchend/keydown/click, all captured at the
         window, so no handler between the target and us can swallow the one gesture the reader
         makes -- the feedback control stops propagation by design, and the tour and panels do too.

     What this cannot do, and no page can: make the very FIRST hover on a first-ever visit audible.
     That gesture requirement is the browser's, not ours. */
  function armGesture(on) {
    ['pointerdown', 'pointerup', 'touchend', 'keydown', 'click'].forEach(function (t) {
      try { removeEventListener(t, unlock, true); } catch (e) {}
      if (on) addEventListener(t, unlock, { passive: true, capture: true });
    });
  }
  function settleUnlock() {
    if (ctx && ctx.state === 'running') { unlocked = true; armGesture(false); ambMaybeStart(); }
    else armGesture(true);
  }
  /* A keyboard reader never hovers; a touch reader's first tap is the gesture.  Either is presence. */
  function gesturePresent() { markPresent(); }
  function unlock() {
    if (unlocked) return;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) { unlocked = true; return; }
    if (!ctx) { try { ctx = new AC(); } catch (e) { return; } }
    Object.keys(raw).forEach(decodeOne);
    if (ctx.state === 'suspended') {
      var pr;
      try { pr = ctx.resume(); } catch (e) { pr = null; }
      if (pr && pr.then) pr.then(settleUnlock, function () { armGesture(true); });
      else setTimeout(settleUnlock, 0);
      return;
    }
    settleUnlock();
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
    /* An eagerly created context can sit 'suspended'.  Sources started on it QUEUE, so a page's
       worth of dropped hovers would all arrive at once the moment it resumes.  Drop instead. */
    if (ctx && ctx.state !== 'running') return;
    if (!ctx || !buf[name]) {
      if (ctx && raw[name]) { pending = name; pendingAt = performance.now(); decodeOne(name); }
      return;
    }
    try {
      var s = ctx.createBufferSource(), g = ctx.createGain();
      s.buffer = buf[name];
      var gv = (BANK[name] || { g: 0.3 }).g * master();
      /* PER-PLAY VARIATION. The room tone is excluded: it is a continuous bed, and detuning a
         loop on every start would audibly step. Cues only, and only while --wz-sfx-vary > 0. */
      var vy = vary();
      if (vy > 0 && name !== '_amb') {
        s.playbackRate.value = 1 + (Math.random() * 2 - 1) * 0.025 * vy;
        gv *= Math.pow(10, ((Math.random() * 2 - 1) * 1.0 * vy) / 20);
      }
      g.gain.value = gv;
      s.connect(g); g.connect(ctx.destination);
      s.start(0);
    } catch (e) {}
  }

  /* WI-K321b: PRESENCE GATES THE BED, NOT THE CUES.  With the context now resumed at boot, the
     cues are right to be eager -- every one of them answers the reader's own pointer, so a cue
     that fires proves someone is there.  The bed does not: it would start in a tab opened in the
     background and never looked at, which is the case the autoplay rule exists for and is a worse
     manner than the defect being fixed.  So the bed waits for presence -- any gesture, or one
     hover, whichever comes first -- and the cues do not. */
  var present = false;
  function markPresent() { if (present) return; present = true; ambMaybeStart(); }
  /* A VIEW CUE MUST CANCEL THE LAST ONE. play() fires and forgets, which is right for a 180ms
     click and wrong for a 2.9-7.5s cue: four tabs pressed in two seconds would stack four
     overlapping settles and the result is mud. The video seat flagged this as the part that would
     bite after ship, so it is built in before ship. Keeping the node is the whole mechanism. */
  var viewSrc = null;
  function playView(name) {
    if (!live()) return;
    if (ctx && ctx.state !== 'running') return;
    if (!ctx || !buf[name]) {
      if (ctx && raw[name]) { pending = name; pendingAt = performance.now(); decodeOne(name); }
      return;
    }
    try { if (viewSrc) { viewSrc.stop(); } } catch (e) {}
    viewSrc = null;
    try {
      var s = ctx.createBufferSource(), g = ctx.createGain();
      s.buffer = buf[name];
      g.gain.value = (BANK[name] || { g: 0.3 }).g * master();
      s.connect(g); g.connect(ctx.destination);
      s.onended = function () { if (viewSrc === s) viewSrc = null; };
      s.start(0); viewSrc = s;
    } catch (e) {}
  }

  function ambMaybeStart() {
    if (!ctx || !buf._amb) return;
    if (!live() || !present) { ambStop(); return; }
    if (ctx.state !== 'running') return;   /* a bed built on a suspended clock is a node, not a sound */
    if (ambNode) return;
    try {
      ambNode = ctx.createBufferSource(); ambGain = ctx.createGain();
      ambNode.buffer = buf._amb; ambNode.loop = true;
      ambGain.gain.value = 0;
      ambNode.connect(ambGain); ambGain.connect(ctx.destination);
      ambNode.start(0);
      ambGain.gain.linearRampToValueAtTime(AMB.g * master(), ctx.currentTime + 1.6);   // no sudden arrival
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
  /* .objection-header is the flagship's card row (pin move, 2026-09-12): it is the expander itself, a
     div with its own click handler rather than a <summary>, so it is named here or the flagship's 82
     rows would hover and open in silence while every button around them clicked. */
  function hoverable(t) { return t && t.closest && t.closest('.obj, .card, .lib-card, .objection-header, button, summary, a'); }
  function onOver(e) {
    if (!live()) return;
    var el = hoverable(e.target); if (!el) return;
    if (e.relatedTarget && el.contains(e.relatedTarget)) return;   // moving WITHIN a card is not a new hover
    var now = performance.now();
    if (now - lastHover < HOVER_MS) return;                        // drop, never queue
    lastHover = now;
    markPresent();
    play('hover');
  }
  var VIEW_CUE = { 'vbtn-library': 'library_index', 'vbtn-map':  'settle_swarm',
                   'vbtn-dep':     'dep_cascade',   'vbtn-map1': 'flow_fan' };
  var VIEW_PICK = { 'map-view': 'pick_web', 'dep-view': 'pick_dep', 'map1-view': 'pick_flow' };
  function onClick(e) {
    unlock(); markPresent();
    if (!live()) return;
    /* Ahead of the generic button branch: a tab press is a view change, not a click. */
    var vb = e.target.closest && e.target.closest('[id^="vbtn-"]');
    if (vb && VIEW_CUE[vb.id]) { playView(VIEW_CUE[vb.id]); return; }
    /* Then a NODE SELECT, which is a click on the thing the cursor is over rather than on the
       furniture around it. Keyed on the VIEW, not on the node's markup: the three graphs are drawn
       by d3 and their node classes are the graph's business, not the layer's. What makes it a node
       is measured -- a click on a node hit-tests to a <circle> or a <rect> INSIDE the svg and never
       to the <svg> root, which is what an empty-canvas click hits. So: a drawn element inside the
       svg, or a row in the flow map's source list, and not the toolbar or the legend. */
    var gv = e.target.closest && e.target.closest('#map-view, #dep-view, #map1-view');
    if (gv && VIEW_PICK[gv.id]) {
      var t = e.target, tag = (t.tagName || '').toLowerCase();
      var drawn = t.closest && t.closest('svg') && tag !== 'svg';
      var row   = t.closest && t.closest('.m1-source-item, .m1-succ, [class*="succ-card"], [class*="-chip"]');
      var furn  = t.closest && t.closest('button, [class*="methodology"], [class*="legend"], [class*="controls"], input, select, a');
      if ((drawn || row) && !furn) { play(VIEW_PICK[gv.id]); return; }
    }
    var d = e.target.closest && e.target.closest('details');
    if (e.target.closest && e.target.closest('summary') && d) { play(d.open ? 'collapse' : 'expand'); return; }
    /* This listener is capture-phase, so it runs before the flagship row's own handler re-renders
       the list: .open here is the row's state BEFORE the click, which is the state to sound. A link
       or button inside the row (the feedback control) is a click, not an open. */
    var h = e.target.closest && e.target.closest('.objection-header');
    if (h && !(e.target.closest('a, button'))) { play(h.classList.contains('open') ? 'collapse' : 'expand'); return; }
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
    armGesture(true);
    ['pointerdown', 'touchend', 'keydown'].forEach(function (t) {
      addEventListener(t, gesturePresent, { passive: true, capture: true });
    });
    unlock();                      /* eager: succeeds where the origin is trusted, else re-arms */
    addEventListener('pointerover', onOver, { passive: true });
    addEventListener('click', onClick, true);
    /* The tier can change under us -- the power button, or the ground flipping with a mode toggle.
       gradeBg's observer already watches for that; this one keeps the ambience honest about it. */
    /* The observer fires on EVERY class change of <html>, and the magnifier toggles wz-zooming on
       every wheel event (added on the event, removed 90ms later) -- so a fast wheel gesture was
       running paint()'s five DOM writes per tick for a state that had not changed. paint() now
       runs only when the answer it paints has actually moved. */
    if (window.MutationObserver) {
      var lastLive = live(), lastOff = muted() || reduced();
      new MutationObserver(function () {
        var l = live(), off = muted() || reduced();
        var liveChanged = (l !== lastLive), offChanged = (off !== lastOff);
        lastLive = l; lastOff = off;
        if (liveChanged) { if (l) ambMaybeStart(); else ambStop(); }
        if (liveChanged || offChanged) paint();
      }).observe(H, { attributes: true, attributeFilter: ['class', 'data-mode'] });
    }
  };
})();


/* ==============================================================================================
   wuld-fb.js
   ============================================================================================== */

/* wuld-fb.js -- per-card feedback. One control per objection, carrying the card's own id.
 *
 * WHY PER-CARD AND NOT A CORNER BUTTON. A corner button produces "something's broken somewhere";
 * a per-card one arrives with the objection id already attached, which is the difference between a
 * report you can act on and one you have to chase. Site-wide comments already have a route --
 * wuld.ink/contact -- so a fourth chin button would add a channel without adding information, and
 * at 320px the chin row is already as wide as it can be.
 *
 * A FORM, SINCE 2026-09-12, WITH THE MAIL DRAFT KEPT AS THE SECOND DOOR. The first version was a
 * mailto: only -- no backend, no storage, no consent banner. In use it opened the reader's mail
 * client, which on a desktop is a chooser dialog and on a phone is a second app, and it required an
 * address before anything could be said. The form posts to the same hosted relay wuld.ink/contact
 * already uses (Formspree, form xpqnzqlr): a message, an optional address so a reply can find its
 * way back, and the card's own context added by the page. The relay accepts JSON from this origin
 * (probed: CORS preflight and a honeypot-filled post both answered 200 from library.wuld.ink), so
 * the panel never leaves the page. The mail draft stays as a link inside the panel -- the alias is
 * still a way in, and it is the fallback the panel offers when the relay refuses.
 *
 * THE PANEL LIVES ON <body>, NOT IN THE CARD. The flagship's toggleObjection() re-renders the whole
 * #results list on every click and every filter, so anything inside a row is destroyed the moment
 * the reader opens a second row. A fixed-position panel anchored to the control's rect survives
 * that; if its card is re-rendered it finds the new control by the card's id and follows it.
 *
 * INJECTED, NOT DELEGATED, AND OBSERVED. The wings build their card list from JSON after load --
 * measured: 0 of 5 wings have a single `class="obj"` in their static HTML -- and re-render it when
 * a filter changes. A one-shot pass at boot would find nothing at all. */
(function () {
  var TO = 'contact@wuld.ink';
  var RELAY = 'https://formspree.io/f/xpqnzqlr';
  /* TWO CARD SHAPES. The wings render <article class="obj"> with an .obj-meta strip and .kw chips. The
     flagship (library.wuld.ink/combined, pin move 2026-09-12) renders a <div class="objection-header">
     row into #results -- the row IS the expander, its heading is the .trigger-text line, the tier and
     register live in the row's own badge strip, and the colloquial names sit in the sibling
     .detail-panel as .keyword chips. Same draft, read from whichever shape the card has. */
  var SEL = 'article.obj[id^="obj-"]:not([data-wz-fb]), div.objection-header[id^="obj-"]:not([data-wz-fb])';
  function isHeader(card) { return card.classList.contains('objection-header'); }

  function heading(card) {
    var h = card.querySelector(isHeader(card) ? '.trigger-text' : 'h2, h3, h4');
    return h ? h.textContent.replace(/\s+/g, ' ').trim() : '';
  }
  /* THE CARD DESCRIBES ITSELF. A report that says only "this one is wrong" costs whoever reads it
     a hunt through five libraries to work out which card it was. So the report arrives carrying the
     card's own context -- the library, the headline, the colloquial names on its chips, and its
     classification strip -- pulled from the card at the moment of the click, which means it cannot
     drift out of date the way a hand-written note would.
     The strip is read child by child rather than with textContent, because the control is itself a
     DOM child of that strip and would otherwise append the word "feedback" to its own report. */
  function strip(card) {
    var m = card.querySelector(isHeader(card) ? ':scope > div > div' : '.obj-meta');
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
    var k, kids;
    if (isHeader(card)) {
      var d = card.nextElementSibling;
      k = d && d.classList.contains('detail-panel') ? d : null;
      kids = k ? k.querySelectorAll('.keyword') : [];
    } else {
      k = card.querySelector('.kw');
      kids = k ? k.children : [];
    }
    if (!k) return [];
    var out = [];
    for (var i = 0; i < kids.length && out.length < 8; i++) {
      var t = kids[i].textContent.replace(/\s+/g, ' ').trim();
      if (t && t.length <= 40) out.push(t);
    }
    return out;
  }
  function clip(s, n) { return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '\u2026' : s; }

  function context(card) {
    return {
      id: card.id,
      link: location.href.split('#')[0] + '#' + card.id,
      library: (document.title.split('\u2014')[0] || '').trim(),
      objection: clip(heading(card), 240),
      classification: strip(card),
      also: chips(card)
    };
  }

  /* The writing space goes FIRST. Mail clients drop the cursor at the top of the body, so anything
     above the prompt is something the reader has to scroll past before they can type. Everything
     the machine contributed sits below the rule, out of the way but travelling with the message.
     MAILTO LENGTH IS A REAL LIMIT -- Windows passes the whole URL through a shell, and clients
     start truncating well before 2000 characters. So the body is built longest-first and the
     optional parts are dropped, in order, until the encoded URL fits under the budget. */
  var MAX_URL = 1800;
  function href(card) {
    var c = context(card);
    var lead = "(what's wrong, or what's missing?)\n\n\n"
             + "-- added automatically, so you needn't describe which card --\n";
    function build(withKw, headLen) {
      var b = lead;
      if (c.library)   b += 'library:        ' + c.library + '\n';
      if (c.objection) b += 'objection:      "' + clip(c.objection, headLen) + '"\n';
      if (withKw && c.also.length) b += 'also called:    ' + c.also.join(' \u00b7 ') + '\n';
      if (c.classification) b += 'classification: ' + c.classification + '\n';
      return b + 'id:             ' + c.id + '\nlink:           ' + c.link + '\n';
    }
    var subj = 'library feedback \u2014 ' + c.id;
    var tries = [[true, 240], [true, 140], [false, 140], [false, 80]];
    var out;
    for (var i = 0; i < tries.length; i++) {
      out = 'mailto:' + TO + '?subject=' + encodeURIComponent(subj)
          + '&body=' + encodeURIComponent(build(tries[i][0], tries[i][1]));
      if (out.length <= MAX_URL) break;
    }
    return out;
  }

  /* ---- THE PANEL ------------------------------------------------------------------------------- */
  var panel = null, form, ta, email, hp, status, sendBtn, mailLink, titleEl;
  var openId = null, opener = null, sending = false, raf = null, doneTimer = null;
  /* A stray click outside the panel closes it -- popover behaviour -- but not at the cost of what
     was typed: an unsent draft is kept for its card and restored when that card's control is opened
     again. One draft, the last one; a different card starts empty. */
  var draft = null;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function build() {
    panel = el('div', 'wz-fb-panel');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Feedback on this objection');
    panel.hidden = true;
    var head = el('div', 'wz-fb-head');
    titleEl = el('span', 'wz-fb-title', 'Feedback');
    var x = el('button', 'wz-fb-close', '\u00d7');
    x.type = 'button'; x.setAttribute('aria-label', 'Close');
    x.addEventListener('click', function () { close(true); });
    head.appendChild(titleEl); head.appendChild(x);
    form = el('form', 'wz-fb-form');
    form.setAttribute('novalidate', '');
    ta = el('textarea', 'wz-fb-text');
    ta.name = 'message'; ta.rows = 4; ta.required = true;
    ta.placeholder = "What's wrong, or what's missing?";
    ta.setAttribute('aria-label', "What's wrong, or what's missing?");
    email = el('input', 'wz-fb-email');
    email.type = 'email'; email.name = 'email'; email.autocomplete = 'email';
    email.placeholder = 'your email \u2014 optional, only so a reply can find you';
    email.setAttribute('aria-label', 'Your email, optional, only so a reply can find you');
    /* Honeypot: bots fill every field; the relay discards a post that has this one. */
    var trap = el('div', 'wz-fb-trap'); trap.setAttribute('aria-hidden', 'true');
    hp = el('input'); hp.type = 'text'; hp.name = '_gotcha'; hp.tabIndex = -1; hp.autocomplete = 'off';
    trap.appendChild(hp);
    var row = el('div', 'wz-fb-row');
    sendBtn = el('button', 'wz-fb-send', 'Send'); sendBtn.type = 'submit';
    mailLink = el('a', 'wz-fb-mail', 'or write an email');
    mailLink.rel = 'nofollow';
    mailLink.title = 'Open a mail draft to ' + TO + ' that already names this card';
    status = el('span', 'wz-fb-status'); status.setAttribute('aria-live', 'polite');
    row.appendChild(sendBtn); row.appendChild(mailLink); row.appendChild(status);
    var note = el('p', 'wz-fb-note', 'Sent through the same relay as wuld.ink/contact; nothing is stored on this site.');
    form.appendChild(ta); form.appendChild(email); form.appendChild(trap); form.appendChild(row); form.appendChild(note);
    form.addEventListener('submit', onSubmit);
    panel.appendChild(head); panel.appendChild(form);
    /* Clicks inside the panel are the panel's: the sound layer's delegated listener may still hear
       them (it listens in the capture phase), the page's own handlers must not. */
    panel.addEventListener('click', function (e) { e.stopPropagation(); });
    panel.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); close(true); }
    });
    document.body.appendChild(panel);
    addEventListener('scroll', schedule, true);
    addEventListener('resize', schedule);
    /* The camera pan moves the whole stage under the pointer by up to --wz-pan; the panel is outside
       the stage, so it follows the control on pointer moves too (one rect read per frame at most). */
    addEventListener('pointermove', schedule, true);
    addEventListener('transitionend', function (e) { if (e.propertyName === 'transform') schedule(); }, true);
    document.addEventListener('pointerdown', function (e) {
      if (!openId || panel.hidden) return;
      if (panel.contains(e.target)) return;
      var c = e.target.closest && e.target.closest('.wz-fb');
      if (c && c === opener) return;                 // the control itself toggles, in onClick
      close(false);
    }, true);
  }

  function control(id) {
    var card = document.getElementById(id);
    return card ? card.querySelector('.wz-fb') : null;
  }
  function schedule() { if (openId && !raf) raf = requestAnimationFrame(function () { raf = null; place(); }); }
  function place() {
    if (!openId || panel.hidden) return;
    var c = control(openId);
    if (c) opener = c;                               // the card may have been re-rendered; follow it
    if (!opener) return;
    var r = opener.getBoundingClientRect();
    if (!r.width && !r.height) return;               // control off-DOM mid-render: keep the last place
    var w = Math.min(380, innerWidth - 24);
    panel.style.width = w + 'px';
    var h = panel.offsetHeight || 200;
    var below = r.bottom + 8;
    var top = (below + h < innerHeight - 12) ? below : Math.max(12, r.top - 8 - h);
    panel.style.top = Math.min(top, Math.max(12, innerHeight - h - 12)) + 'px';
    panel.style.left = Math.max(12, Math.min(r.right - w, innerWidth - w - 12)) + 'px';
  }

  function setState(s, msg) {
    panel.setAttribute('data-state', s);
    status.textContent = msg || '';
    sendBtn.disabled = (s === 'sending' || s === 'sent');
  }
  function openFor(card, ctrl) {
    if (!panel) build();
    if (doneTimer) { clearTimeout(doneTimer); doneTimer = null; }
    var c = context(card);
    openId = c.id; opener = ctrl;
    titleEl.textContent = 'Feedback \u2014 ' + c.id;
    mailLink.href = ctrl.href;
    var keep = draft && draft.id === c.id;
    ta.value = keep ? draft.msg : ''; email.value = keep ? draft.email : ''; hp.value = '';
    setState('idle', '');
    panel.hidden = false;
    ctrl.setAttribute('aria-expanded', 'true');
    place();
    try { ta.focus({ preventScroll: true }); } catch (e) { ta.focus(); }
  }
  function close(restoreFocus) {
    if (!panel || panel.hidden) return;
    if (panel.getAttribute('data-state') !== 'sent' && (ta.value.trim() || email.value.trim())) draft = { id: openId, msg: ta.value, email: email.value };
    else if (draft && draft.id === openId) draft = null;
    panel.hidden = true;
    var c = control(openId);
    if (c) c.setAttribute('aria-expanded', 'false');
    if (restoreFocus && c) { try { c.focus({ preventScroll: true }); } catch (e) {} }
    openId = null; opener = null; sending = false;
  }
  window.wzFbClose = function () { close(false); };

  function onSubmit(e) {
    e.preventDefault(); e.stopPropagation();
    if (sending || !openId) return;
    var msg = ta.value.trim();
    if (!msg) { setState('idle', 'Write something first.'); ta.focus(); return; }
    var card = document.getElementById(openId);
    var c = card ? context(card) : { id: openId, link: location.href, library: '', objection: '', classification: '', also: [] };
    var body = {
      _subject: 'library feedback \u2014 ' + c.id,
      message: msg,
      library: c.library, objection: c.objection, also_called: c.also.join(' \u00b7 '),
      classification: c.classification, id: c.id, link: c.link
    };
    var em = email.value.trim();
    if (em) body.email = em;
    if (hp.value) { setState('sent', 'Sent \u2014 thank you.'); doneTimer = setTimeout(function () { close(true); }, 1800); return; }
    sending = true;
    setState('sending', 'Sending\u2026');
    var failed = function (why) {
      sending = false;
      setState('error', why || 'Could not send \u2014 try again, or use the email link.');
    };
    try {
      fetch(RELAY, { method: 'POST', mode: 'cors', headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) {
          return r.json().then(function (j) { return { ok: r.ok && !(j && j.ok === false), j: j }; },
                               function () { return { ok: r.ok, j: null }; });
        })
        .then(function (res) {
          if (!res.ok) {
            var why = res.j && res.j.errors && res.j.errors.length && res.j.errors[0].message;
            failed(why ? 'The relay refused it: ' + why + ' \u2014 use the email link.' : null); return;
          }
          sending = false;
          setState('sent', 'Sent \u2014 thank you.');
          doneTimer = setTimeout(function () { close(true); }, 1800);
        })
        .catch(function () { failed(null); });
    } catch (err) { failed(null); }
  }

  function onClick(e) {
    e.preventDefault();            // the href stays a mail draft for the no-script reader and the copy menu
    e.stopPropagation();           // the flagship's row is itself the expander
    var a = e.currentTarget, card = a.closest('article.obj, .objection-header');
    if (!card) return;
    if (openId === card.id && panel && !panel.hidden) { close(true); return; }
    openFor(card, a);
  }

  function pass() {
    var cards = document.querySelectorAll(SEL), n = 0;
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i], hdr = isHeader(c), m = hdr ? c : c.querySelector('.obj-meta');
      c.setAttribute('data-wz-fb', '1');            // set even when there is no meta strip, so a
      if (!m) continue;                             // card without one is not re-examined forever
      var a = document.createElement('a');
      a.className = 'wz-fb';
      a.href = href(c);
      a.rel = 'nofollow';
      a.textContent = 'feedback';   // uppercased by CSS, like every other micro-label on the card
      a.title = 'Report a correction or comment about this objection';
      a.setAttribute('aria-label', 'Report a correction or comment about this objection: ' + (heading(c) || c.id));
      a.setAttribute('aria-haspopup', 'dialog');
      a.setAttribute('aria-expanded', openId === c.id ? 'true' : 'false');
      a.addEventListener('click', onClick);
      /* Appended, not prepended. While the control was floated it had to precede the meta text to
         sit beside it; anchored, its position is set by CSS and DOM order is free to match reading
         order instead -- so a keyboard lands on the meta text first and the utility after it. */
      m.appendChild(a);
      n++;
    }
    if (openId) schedule();                          // a re-render moved the anchor; follow it
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
