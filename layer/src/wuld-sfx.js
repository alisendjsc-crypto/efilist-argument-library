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
