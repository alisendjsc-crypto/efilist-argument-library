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
    // WHOLE PIXELS (K410). Chrome composites the stage at whatever offset it is given, and at a
    // fractional one it resamples the layer: every glyph on the page went soft wherever the pointer
    // happened to rest. Measured on a wing at 1440: edge energy -13.2% at -1.5px, -7.2% at -1.2px,
    // nothing at 0 or -3px; the flagship -10.0% at -1.5px; Firefox unaffected. The transition still
    // eases between steps, so the move is as smooth as before -- only the resting place snaps.
    H.style.setProperty('--wz-px', Math.round(px - dx * base) + 'px');
    H.style.setProperty('--wz-py', Math.round(py - dy * base * 0.6) + 'px');
    // Blur the end the camera is NOT at.
    H.style.setProperty('--wz-sl', Math.max(0,  dx).toFixed(3));
    H.style.setProperty('--wz-sr', Math.max(0, -dx).toFixed(3));
  }
  /* THE FOCUS RIDES THE TICK THAT ALREADY EXISTS. One rAF, already coalesced, already gated on the
     tier and on reduced motion -- adding a second listener for the same pointer would double the
     work to say the same thing twice. Two custom properties and one class; the box's transform and
     the vignette's mask both read them, so the DOM writes are 2 per frame, not 2 per consumer. */
  var focusOn = false, focusIdle = 0;
  /* A TOUCH IS NOT A GAZE (K410). A tap synthesises one mousemove at the tap point, so on a phone every
     tap swung the camera -- measured at 390px: 5.88px against a 2px lip -- and lit the far-side strip
     over the reading column. Unzoomed, the camera now answers only a real pointer, the same gate the
     clearing has always had in the stylesheet. Under the magnifier the pointer IS the camera (K317)
     and that path is left exactly as it was. */
  var FINE = matchMedia('(hover: hover) and (pointer: fine)');
  function onMove(e) {
    if (i !== 2 || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (zoom <= 1.0001 && (!FINE.matches || (e.sourceCapabilities && e.sourceCapabilities.firesTouchEvents))) return;
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
